"""
SEC EDGAR Fetcher - Real Data Extraction
Fetches actual 10-K, 10-Q filings from SEC EDGAR and extracts structured financial data.
"""
import requests
import re
import json
from datetime import datetime

# SEC requires User-Agent
HEADERS = {
    "User-Agent": "EarningsCopilot contact@earningscopilot.com",
    "Accept": "application/json",
}

# Cache for ticker-to-CIK mapping (loaded once from SEC)
_TICKER_CIK_CACHE = None


def get_cik(ticker):
    """Get CIK number for any ticker using SEC's official mapping."""
    global _TICKER_CIK_CACHE
    
    ticker = ticker.upper()
    
    # Load the full ticker mapping from SEC if not cached
    if _TICKER_CIK_CACHE is None:
        try:
            print("Loading ticker-to-CIK mapping from SEC...")
            url = "https://www.sec.gov/files/company_tickers.json"
            response = requests.get(url, headers=HEADERS, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            # Build lookup dictionary
            _TICKER_CIK_CACHE = {}
            for entry in data.values():
                cik = str(entry.get("cik_str", "")).zfill(10)
                ticker_symbol = entry.get("ticker", "").upper()
                if ticker_symbol and cik:
                    _TICKER_CIK_CACHE[ticker_symbol] = cik
            
            print(f"Loaded {len(_TICKER_CIK_CACHE)} tickers from SEC")
        except Exception as e:
            print(f"Warning: Could not load SEC ticker mapping: {e}")
            _TICKER_CIK_CACHE = {}
    
    return _TICKER_CIK_CACHE.get(ticker)


def get_company_facts(cik):
    """Fetch company facts from SEC EDGAR API - contains all financial data."""
    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik.zfill(10)}.json"
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching company facts: {e}")
        return None


def get_company_concept(cik, concept, taxonomy="us-gaap"):
    """Fetch specific financial concept (Revenue, NetIncome, etc.)."""
    url = f"https://data.sec.gov/api/xbrl/companyconcept/CIK{cik.zfill(10)}/{taxonomy}/{concept}.json"
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching concept {concept}: {e}")
        return None


def get_filings_list(cik):
    """Get list of recent filings for a company."""
    url = f"https://data.sec.gov/submissions/CIK{cik.zfill(10)}.json"
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching filings list: {e}")
        return None


def extract_financial_metrics(cik):
    """Extract key financial metrics from SEC XBRL data."""
    
    facts = get_company_facts(cik)
    if not facts:
        return {}
    
    metrics = {}
    
    # Key financial concepts to extract
    concepts = {
        "Revenues": ["RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues", "SalesRevenueNet", "RevenueFromContractWithCustomerIncludingAssessedTax"],
        "NetIncome": ["NetIncomeLoss", "ProfitLoss"],
        "EBITDA": ["EarningsBeforeInterestAndTaxes", "OperatingIncomeLoss"],
        "Assets": ["Assets"],
        "Liabilities": ["Liabilities"],
        "StockholdersEquity": ["StockholdersEquity", "StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest"],
        "Cash": ["CashAndCashEquivalentsAtCarryingValue", "CashCashEquivalentsAndShortTermInvestments"],
        "Debt": ["LongTermDebt", "LongTermDebtAndCapitalLeaseObligations"],
    }
    
    us_gaap = facts.get("facts", {}).get("us-gaap", {})
    
    for metric_name, concept_list in concepts.items():
        for concept in concept_list:
            if concept in us_gaap:
                units = us_gaap[concept].get("units", {})
                # Get USD values
                if "USD" in units:
                    values = units["USD"]
                    # Get most recent annual and quarterly values
                    annual_values = [v for v in values if v.get("form") == "10-K"]
                    quarterly_values = [v for v in values if v.get("form") == "10-Q"]
                    
                    if annual_values:
                        # Sort by filed date, get most recent
                        annual_values.sort(key=lambda x: x.get("filed", ""), reverse=True)
                        metrics[f"{metric_name}_FY"] = {
                            "value": annual_values[0].get("val"),
                            "date": annual_values[0].get("end"),
                            "filed": annual_values[0].get("filed"),
                        }
                    
                    if quarterly_values:
                        quarterly_values.sort(key=lambda x: x.get("filed", ""), reverse=True)
                        metrics[f"{metric_name}_Q"] = {
                            "value": quarterly_values[0].get("val"),
                            "date": quarterly_values[0].get("end"),
                            "filed": quarterly_values[0].get("filed"),
                        }
                break
    
    return metrics


def get_filing_text(cik, form_type="10-K"):
    """Fetch the actual filing document text for a given form type."""
    filings = get_filings_list(cik)
    if not filings:
        return None
    
    recent = filings.get("filings", {}).get("recent", {})
    forms = recent.get("form", [])
    accession_numbers = recent.get("accessionNumber", [])
    primary_docs = recent.get("primaryDocument", [])
    
    # Find most recent filing of specified type
    for i, form in enumerate(forms):
        if form == form_type:
            acc_num = accession_numbers[i].replace("-", "")
            primary_doc = primary_docs[i]
            
            # Build filing URL
            filing_url = f"https://www.sec.gov/Archives/edgar/data/{cik.lstrip('0')}/{acc_num}/{primary_doc}"
            
            try:
                response = requests.get(filing_url, headers=HEADERS, timeout=60)
                response.raise_for_status()
                return {
                    "text": response.text,
                    "filing_date": recent.get("filingDate", [])[i] if i < len(recent.get("filingDate", [])) else None,
                    "report_date": recent.get("reportDate", [])[i] if i < len(recent.get("reportDate", [])) else None,
                    "accession_number": accession_numbers[i],
                    "form_type": form,
                }
            except Exception as e:
                print(f"Error fetching {form_type} document: {e}")
                continue
    
    return None


def get_10k_text(cik):
    """Fetch the actual 10-K document text (legacy wrapper)."""
    return get_filing_text(cik, "10-K")


def extract_sections_from_html(html_text, form_type="10-K"):
    """Extract key sections from SEC filing HTML based on form type."""
    
    # Remove HTML tags for text extraction
    clean_text = re.sub(r'<[^>]+>', ' ', html_text)
    clean_text = re.sub(r'\s+', ' ', clean_text)
    
    sections = {}
    
    # Define section patterns based on form type
    if form_type == "10-K":
        section_patterns = {
            "business": r"Item\s+1\.\s*Business(.*?)(?=Item\s+1A|$)",
            "risk_factors": r"Item\s+1A\.\s*Risk\s*Factors(.*?)(?=Item\s+1B|Item\s+2|$)",
            "unresolved_staff_comments": r"Item\s+1B\.\s*Unresolved\s*Staff\s*Comments(.*?)(?=Item\s+2|$)",
            "properties": r"Item\s+2\.\s*Properties(.*?)(?=Item\s+3|$)",
            "legal_proceedings": r"Item\s+3\.\s*Legal\s*Proceedings(.*?)(?=Item\s+4|$)",
            "mda": r"Item\s+7\.\s*Management[\'']?s\s*Discussion\s*and\s*Analysis.*?(.*?)(?=Item\s+7A|Item\s+8|$)",
            "quantitative_disclosures": r"Item\s+7A\.\s*Quantitative\s*and\s*Qualitative.*?(.*?)(?=Item\s+8|$)",
            "financial_statements": r"Item\s+8\.\s*Financial\s*Statements(.*?)(?=Item\s+9|$)",
            "controls": r"Item\s+9A\.\s*Controls\s*and\s*Procedures(.*?)(?=Item\s+9B|$)",
        }
    elif form_type == "10-Q":
        section_patterns = {
            "financial_statements": r"Part\s+I\s+Item\s+1\.\s*Financial\s*Statements(.*?)(?=Item\s+2|$)",
            "mda": r"Item\s+2\.\s*Management[\'']?s\s*Discussion\s*and\s*Analysis.*?(.*?)(?=Item\s+3|Item\s+4|$)",
            "quantitative_disclosures": r"Item\s+3\.\s*Quantitative\s*and\s*Qualitative.*?(.*?)(?=Item\s+4|$)",
            "controls": r"Item\s+4\.\s*Controls\s*and\s*Procedures(.*?)(?=Part\s+II|$)",
            "legal_proceedings": r"Part\s+II\s+Item\s+1\.\s*Legal\s*Proceedings(.*?)(?=Item\s+1A|$)",
            "risk_factors": r"Item\s+1A\.\s*Risk\s*Factors(.*?)(?=Item\s+2|$)",
        }
    elif form_type == "8-K":
        section_patterns = {
            "results_of_operations": r"Item\s+2\.02\.\s*Results\s*of\s*Operations(.*?)(?=Item|$)",
            "fd_disclosure": r"Item\s+7\.01\.\s*Regulation\s*FD\s*Disclosure(.*?)(?=Item|$)",
            "other_events": r"Item\s+8\.01\.\s*Other\s*Events(.*?)(?=Item|$)",
            "financial_statements": r"Item\s+9\.01\.\s*Financial\s*Statements(.*?)(?=SIGNATURE|$)",
        }
    else:
        return {}
    
    for section_name, pattern in section_patterns.items():
        match = re.search(pattern, clean_text, re.IGNORECASE | re.DOTALL)
        if match:
            content = match.group(1).strip()
            # Limit for token management
            sections[section_name] = content[:15000]
    
    return sections


def calculate_yoy_qoq(metrics):
    """Calculate Year-over-Year and Quarter-over-Quarter changes."""
    
    changes = {}
    
    for metric_name, data in metrics.items():
        if "_FY" in metric_name or "_Q" in metric_name:
            base_name = metric_name.replace("_FY", "").replace("_Q", "")
            
            if f"{base_name}_FY" in metrics:
                fy_data = metrics[f"{base_name}_FY"]
                changes[f"{base_name}_Latest"] = {
                    "value": fy_data.get("value"),
                    "date": fy_data.get("date"),
                    "formatted": format_currency(fy_data.get("value")),
                }
    
    return changes


def format_currency(value):
    """Format large numbers as currency."""
    if not value:
        return "N/A"
    
    if value >= 1_000_000_000:
        return f"${value / 1_000_000_000:.2f}B"
    elif value >= 1_000_000:
        return f"${value / 1_000_000:.2f}M"
    else:
        return f"${value:,.0f}"


def fetch_and_process_filing(ticker, form_type="10-K"):
    """Main function to fetch and process an SEC filing of any type."""
    
    cik = get_cik(ticker)
    if not cik:
        return {"error": f"Ticker {ticker} not found in CIK map"}
    
    # Get financial metrics from XBRL
    print(f"Fetching financial metrics for {ticker}...")
    metrics = extract_financial_metrics(cik)
    
    # Get document
    print(f"Fetching {form_type} document...")
    doc_data = get_filing_text(cik, form_type)
    
    # Extract sections
    sections = {}
    if doc_data and doc_data.get("text"):
        sections = extract_sections_from_html(doc_data["text"], form_type)
    
    # Get company info
    filings = get_filings_list(cik)
    company_name = filings.get("name", ticker) if filings else ticker
    
    return {
        "ticker": ticker.upper(),
        "cik": cik,
        "company_name": company_name,
        "metrics": metrics,
        "sections": sections,
        "filing_date": doc_data.get("filing_date") if doc_data else None,
        "form_type": form_type,
        "chunks": chunk_sections(sections, source=form_type),
    }


def fetch_and_process_10k(ticker):
    """Main function to fetch and process 10-K data (legacy wrapper)."""
    return fetch_and_process_filing(ticker, "10-K")


def chunk_sections(sections, chunk_size=1000, source="SEC"):
    """Chunk sections for vector storage."""
    chunks = []
    
    for section_name, content in sections.items():
        if content:
            # Split into chunks
            words = content.split()
            for i in range(0, len(words), chunk_size // 5):  # Approximate chunk by words
                chunk = " ".join(words[i:i + chunk_size // 5])
                if chunk:
                    chunks.append({
                        "content": chunk,
                        "section": section_name,
                        "source": source,
                    })
    
    return chunks
