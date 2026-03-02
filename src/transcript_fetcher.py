import requests
import re
from src.config import FMP_API_KEY

class TranscriptFetcher:
    def __init__(self):
        self.api_key = FMP_API_KEY
        self.base_url = "https://financialmodelingprep.com/api/v3/earning_call_transcript/{ticker}?year={year}&quarter={quarter}&apikey={key}"
        # Alternative simple endpoint if quarter/year not specified
        self.simple_url = "https://financialmodelingprep.com/api/v3/earning_call_transcript/{ticker}?apikey={key}"

    def fetch_transcript(self, ticker):
        if not self.api_key:
            return self.get_sample_transcript(ticker)
        
        url = self.simple_url.format(ticker=ticker, key=self.api_key)
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                # Return the most recent one
                return data[0].get("content", "")
        
        return self.get_sample_transcript(ticker)

    def extract_qa_section(self, text):
        # Transcripts often have a "Question and Answer" or "Q&A" header
        # Pattern: look for "Question and Answer Session" or similar
        pattern = r"(Question and Answer Session|Q&A Session|Operator:.*?questions)(.*)"
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            return match.group(2).strip()
        return "Q&A section not explicitly found."

    def calculate_sentiment(self, text):
        pos_words = ["strong", "growth", "record", "confident"]
        neg_words = ["challenging", "decline", "weak", "pressure"]
        
        text_lower = text.lower()
        pos_count = sum(len(re.findall(f"\\b{word}\\b", text_lower)) for word in pos_words)
        neg_count = sum(len(re.findall(f"\\b{word}\\b", text_lower)) for word in neg_words)
        
        sentiment = "Neutral"
        if pos_count > neg_count * 1.5:
            sentiment = "Positive"
        elif neg_count > pos_count * 1.5:
            sentiment = "Negative"
            
        return {
            "positive_count": pos_count,
            "negative_count": neg_count,
            "sentiment": sentiment
        }

    def get_sample_transcript(self, ticker):
        return f"""
        {ticker} Earnings Call Transcript (SAMPLE DATA)
        
        CEO: We had a strong quarter with record growth in our cloud division. We are confident in our long-term strategy despite some macroeconomic pressure.
        
        Question and Answer Session
        
        Analyst: Can you talk about the decline in margins?
        CFO: The margin decline was due to weak demand in certain segments and challenging supply chain issues. However, our strong performance elsewhere offset this pressure.
        """

def fetch_and_analyze_transcript(ticker):
    fetcher = TranscriptFetcher()
    content = fetcher.fetch_transcript(ticker)
    qa_content = fetcher.extract_qa_section(content)
    sentiment = fetcher.calculate_sentiment(content)
    
    return {
        "full_content": content,
        "qa_content": qa_content,
        "sentiment": sentiment
    }
