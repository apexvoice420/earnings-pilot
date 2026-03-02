import os
from dotenv import load_dotenv

load_dotenv()

SEC_USER_AGENT = os.getenv("SEC_USER_AGENT", "EarningsCopilot contact@earningscopilot.com")
FMP_API_KEY = os.getenv("FMP_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Database
DATABASE_URL = os.getenv("DATABASE_URL")

TICKER_CIK_MAP = {
    "AAPL": "0000320193",
    "TSLA": "0001318605",
    "NVDA": "0001045810",
    "MSFT": "0000789019",
    "GOOGL": "0001652044",
    "AMZN": "0001018724",
    "META": "0001326801",
}
