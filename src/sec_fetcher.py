import requests
import re
import time
from src.config import SEC_USER_AGENT, TICKER_CIK_MAP

class SECFetcher:
    def __init__(self):
        self.headers = {"User-Agent": SEC_USER_AGENT}
        self.base_url = "https://data.sec.gov/submissions/CIK{cik}.json"
        self.filing_url = "https://www.sec.gov/Archives/edgar/data/{cik}/{acc_no}/{doc}"

    def get_filings_metadata(self, ticker):
        cik = TICKER_CIK_MAP.get(ticker)
        if not cik:
            return None
        
        # CIK in the URL must be 10 digits zero-padded
        url = self.base_url.format(cik=cik.zfill(10))
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            return None
        return response.json()

    def fetch_10k_text(self, ticker):
        metadata = self.get_filings_metadata(ticker)
        if not metadata:
            return "No metadata found for ticker."

        # Find the most recent 10-K
        filings = metadata.get("filings", {}).get("recent", {})
        for i, form in enumerate(filings.get("form", [])):
            if form == "10-K":
                acc_no = filings.get("accessionNumber", [])[i].replace("-", "")
                primary_doc = filings.get("primaryDocument", [])[i]
                cik = TICKER_CIK_MAP.get(ticker).zfill(10).lstrip("0") # URL uses non-padded or padded? Usually padded in some cases, but archives often use non-padded folders.
                # Actually SEC Archives use non-zero padded CIK in path if it starts with 0? No, usually they use the actual CIK.
                # Let's use the CIK as provided in the map but check.
                
                # Correction: Archives URL uses the CIK without leading zeros in some places but usually it's the 10 digit.
                # Let's use the provided CIK.
                real_cik = TICKER_CIK_MAP.get(ticker).lstrip("0")
                doc_url = f"https://www.sec.gov/Archives/edgar/data/{real_cik}/{filings.get('accessionNumber', [])[i].replace('-', '')}/{primary_doc}"
                
                resp = requests.get(doc_url, headers=self.headers)
                if resp.status_code == 200:
                    return resp.text
        return "No 10-K found."

    def extract_sections(self, text):
        sections = {
            "Business": "",
            "Risk Factors": "",
            "MD&A": ""
        }
        
        # Basic regex to find sections. 10-K sections are often marked with Item numbers.
        # Item 1. Business
        # Item 1A. Risk Factors
        # Item 7. Management’s Discussion and Analysis...
        
        regex_patterns = {
            "Business": r"Item\s+1\.\s+Business(.*?)(?=Item\s+1A|$)",
            "Risk Factors": r"Item\s+1A\.\s+Risk\s+Factors(.*?)(?=Item\s+1B|$)",
            "MD&A": r"Item\s+7\.\s+Management’s\s+Discussion\s+and\s+Analysis(.*?)(?=Item\s+7A|$)"
        }
        
        # Clean HTML tags if present (common in SEC filings)
        clean_text = re.sub(r'<.*?>', '', text)
        clean_text = re.sub(r'\s+', ' ', clean_text).strip()

        for section, pattern in regex_patterns.items():
            match = re.search(pattern, clean_text, re.IGNORECASE | re.DOTALL)
            if match:
                sections[section] = match.group(1).strip()
            else:
                # Fallback if Item markers are different
                sections[section] = "Section not found."
                
        return sections

    def chunk_text(self, text, chunk_size=1000):
        return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

def fetch_and_process_10k(ticker):
    fetcher = SECFetcher()
    raw_text = fetcher.fetch_10k_text(ticker)
    sections = fetcher.extract_sections(raw_text)
    
    chunked_sections = {}
    for name, content in sections.items():
        chunked_sections[name] = fetcher.chunk_text(content)
    
    return chunked_sections
