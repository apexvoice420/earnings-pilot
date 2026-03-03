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

# CIK mapping for major tickers
TICKER_TO_CIK = {
    "AAPL": "0000320193",
    "MSFT": "0000789019",
    "GOOGL": "0001652044",
    "GOOG": "0001652044",
    "AMZN": "0001018724",
    "META": "0001326801",
    "NVDA": "0001045810",
    "TSLA": "0001318605",
    "JPM": "0000019617",
    "V": "0001403161",
    "JNJ": "0000200406",
    "WMT": "0000104169",
    "PG": "0000080424",
    "MA": "0001141391",
    "UNH": "0000731766",
    "HD": "0000354950",
    "DIS": "0001744489",
    "PYPL": "0001633917",
    "NFLX": "0001065280",
    "INTC": "0000050863",
    "AMD": "0000002488",
    "CRM": "0001108524",
    "ADBE": "0000796343",
    "ORCL": "0001341439",
    "CSCO": "0000858877",
}


def get_cik(ticker):
    """Get CIK number for ticker."""
    return TICKER_TO_CIK.get(ticker.upper())


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


def get_10k_text(cik):
    """Fetch the actual 10-K document text."""
    filings = get_filings_list(cik)
    if not filings:
        return None
    
    recent = filings.get("filings", {}).get("recent", {})
    forms = recent.get("form", [])
    accession_numbers = recent.get("accessionNumber", [])
    primary_docs = recent.get("primaryDocument", [])
    
    # Find most recent 10-K
    for i, form in enumerate(forms):
        if form == "10-K":
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
                }
            except Exception as e:
                print(f"Error fetching 10-K document: {e}")
                continue
    
    return None


def extract_sections_from_html(html_text):
    """Extract key sections from 10-K HTML."""
    
    # Remove HTML tags for text extraction
    clean_text = re.sub(r'<[^>]+>', ' ', html_text)
    clean_text = re.sub(r'\s+', ' ', clean_text)
    
    sections = {}
    
    # Define section patterns for 10-K
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
    
    for section_name, pattern in section_patterns.items():
        match = re.search(pattern, clean_text, re.IGNORECASE | re.DOTALL)
        if match:
            content = match.group(1).strip()
            # Limit to first 10000 chars per section for token management
            sections[section_name] = content[:10000]
    
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


def fetch_and_process_10k(ticker):
    """Main function to fetch and process 10-K data."""
    
    cik = get_cik(ticker)
    if not cik:
        return {"error": f"Ticker {ticker} not found in CIK map"}
    
    # Get financial metrics from XBRL
    print(f"Fetching financial metrics for {ticker}...")
    metrics = extract_financial_metrics(cik)
    
    # Get 10-K document
    print("Fetching 10-K document...")
    doc_data = get_10k_text(cik)
    
    # Extract sections
    sections = {}
    if doc_data and doc_data.get("text"):
        sections = extract_sections_from_html(doc_data["text"])
    
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
        "chunks": chunk_sections(sections),
    }


def chunk_sections(sections, chunk_size=1000):
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
                        "source": "10-K",
                    })
    
    return chunks
