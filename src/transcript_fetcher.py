"""
Earnings Transcript Fetcher - Real Data
"""
import requests
import re
import os

# Financial Modeling Prep API (free tier available)
FMP_API_KEY = os.getenv("FMP_API_KEY", "")

# Free alternative: Alpha Vantage (limited)
ALPHA_VANTAGE_KEY = os.getenv("ALPHA_VANTAGE_KEY", "")


def get_transcript_fmp(ticker):
    """Fetch earnings transcript from Financial Modeling Prep API."""
    if not FMP_API_KEY:
        return None
    
    url = f"https://financialmodelingprep.com/api/v3/earning_call_transcript/{ticker}?apikey={FMP_API_KEY}"
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        if data and len(data) > 0:
            # Return most recent transcripts
            return data[:4]  # Last 4 quarters
    except Exception as e:
        print(f"FMP API error: {e}")
    
    return None


def get_transcript SeekingAlpha(ticker):
    """Alternative: Scrape from Seeking Alpha (requires handling)."""
    # Note: Seeking Alpha has terms of service
    # This is a placeholder for alternative data sources
    return None


def analyze_transcript_sentiment(text):
    """Analyze management tone in transcript."""
    
    if not text:
        return {"sentiment": "Unknown", "positive_count": 0, "negative_count": 0, "cautious_count": 0}
    
    text_lower = text.lower()
    
    # Sentiment word banks
    positive_words = [
        "strong", "growth", "record", "confident", "excited", "optimistic",
        "outperform", "beat", "exceeded", "momentum", "opportunity", "robust",
        "solid", "excellent", "pleased", "delighted", "encouraging"
    ]
    
    negative_words = [
        "challenging", "decline", "weak", "pressure", "difficult", "headwind",
        "uncertain", "disappointed", "concern", "below", "miss", "slowdown",
        "contraction", "lower", "reduced", "impacted", "adverse"
    ]
    
    cautious_words = [
        "cautious", "monitoring", "uncertainty", "depending", "subject to",
        "may", "could", "potential", "risk", "volatility", "fluctuate"
    ]
    
    positive_count = sum(len(re.findall(rf"\b{word}\b", text_lower)) for word in positive_words)
    negative_count = sum(len(re.findall(rf"\b{word}\b", text_lower)) for word in negative_words)
    cautious_count = sum(len(re.findall(rf"\b{word}\b", text_lower)) for word in cautious_words)
    
    total = positive_count + negative_count + cautious_count
    if total == 0:
        total = 1
    
    # Determine overall sentiment
    if positive_count > negative_count * 1.5:
        sentiment = "Bullish"
    elif negative_count > positive_count * 1.5:
        sentiment = "Bearish"
    elif cautious_count > max(positive_count, negative_count):
        sentiment = "Cautious"
    else:
        sentiment = "Neutral"
    
    return {
        "sentiment": sentiment,
        "positive_count": positive_count,
        "negative_count": negative_count,
        "cautious_count": cautious_count,
        "positive_ratio": round(positive_count / total, 2),
        "negative_ratio": round(negative_count / total, 2),
        "cautious_ratio": round(cautious_count / total, 2),
    }


def extract_qa_section(transcript_text):
    """Extract the Q&A portion of the earnings call."""
    
    if not transcript_text:
        return ""
    
    # Common patterns for Q&A start
    qa_patterns = [
        r"Question(?:ing)?\s*(?:and|&)\s*Answer.*?(.*)",
        r"Q\s*&\s*A.*?(.*)",
        r"We'll now open.*?questions.*?(.*)",
        r"Operator:.*?questions.*?(.*)",
        r"The floor is open.*?questions.*?(.*)",
    ]
    
    for pattern in qa_patterns:
        match = re.search(pattern, transcript_text, re.IGNORECASE | re.DOTALL)
        if match:
            return match.group(1).strip()[:5000]  # Limit size
    
    return ""


def extract_management_statements(transcript_text, management_titles=None):
    """Extract statements made by management (not analysts)."""
    
    if not transcript_text:
        return []
    
    if management_titles is None:
        management_titles = ["CEO", "CFO", "COO", "President", "Chairman", "Chief"]
    
    statements = []
    lines = transcript_text.split("\n")
    
    for i, line in enumerate(lines):
        # Check if line contains management title
        for title in management_titles:
            if title in line.upper():
                # Collect the next few lines as their statement
                statement_lines = []
                for j in range(i + 1, min(i + 10, len(lines))):
                    if lines[j].strip() and not any(t in lines[j].upper() for t in management_titles + ["ANALYST", "OPERATOR"]):
                        statement_lines.append(lines[j])
                    else:
                        break
                
                if statement_lines:
                    statements.append({
                        "speaker": line.strip(),
                        "statement": " ".join(statement_lines).strip(),
                    })
    
    return statements[:20]  # Limit to 20 statements


def fetch_and_analyze_transcript(ticker):
    """Main function to fetch and analyze earnings transcripts."""
    
    # Try FMP API first
    transcripts = get_transcript_fmp(ticker)
    
    if transcripts and len(transcripts) > 0:
        # Use the most recent transcript
        latest = transcripts[0]
        transcript_text = latest.get("content", "") or latest.get("transcript", "")
        
        sentiment = analyze_transcript_sentiment(transcript_text)
        qa_section = extract_qa_section(transcript_text)
        management_statements = extract_management_statements(transcript_text)
        
        return {
            "ticker": ticker.upper(),
            "full_content": transcript_text[:20000],  # Limit for processing
            "qa_content": qa_section,
            "management_statements": management_statements,
            "sentiment": sentiment,
            "date": latest.get("date"),
            "quarter": latest.get("quarter"),
            "year": latest.get("year"),
            "source": "FMP API",
        }
    
    # Fallback: Return structured placeholder
    return {
        "ticker": ticker.upper(),
        "full_content": f"No transcript available for {ticker}. Add FMP_API_KEY to environment variables to fetch real earnings call transcripts.",
        "qa_content": "",
        "management_statements": [],
        "sentiment": {"sentiment": "Unknown", "positive_count": 0, "negative_count": 0, "cautious_count": 0},
        "source": "None - API key required",
    }
