# Earnings Pilot 🚀

AI-powered earnings call prep platform. Analyzes 10-Ks and earnings transcripts to generate comprehensive prep reports for CFOs and IR teams.

## Quick Start

### 1. Setup Backend

```bash
cd earnings-pilot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy env file and add your API keys
cp .env.example .env
```

### 2. Add API Keys to `.env`

```
SEC_USER_AGENT=EarningsPilot your@email.com
FMP_API_KEY=your_fmp_key_here
ANTHROPIC_API_KEY=sk-ant-your_key_here
OPENAI_API_KEY=sk-your_key_here
```

- **SEC_USER_AGENT**: Required by SEC EDGAR (free)
- **FMP_API_KEY**: Get from [financialmodelingprep.com](https://financialmodelingprep.com/) ($49/mo)
- **ANTHROPIC_API_KEY**: Get from [console.anthropic.com](https://console.anthropic.com/)
- **OPENAI_API_KEY**: Get from [platform.openai.com](https://platform.openai.com/)

### 3. Run Backend

```bash
# Option A: FastAPI server (recommended for frontend)
python server.py

# Option B: Streamlit only (no frontend needed)
streamlit run app.py
```

Backend runs at: http://localhost:8000

### 4. Run Frontend (Optional)

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at: http://localhost:3000

## Features

- **SEC EDGAR Integration**: Fetches 10-K/10-Q filings by ticker
- **Earnings Transcripts**: Pulls from Financial Modeling Prep API
- **Vector Storage**: ChromaDB for semantic search
- **AI Analysis**: Claude 3.5 Sonnet generates reports
- **Sentiment Analysis**: Tracks management tone

## Generated Report Sections

1. **Executive Summary** - Key highlights and risks
2. **Analyst Questions** - 10 tough questions with suggested responses
3. **Risk Factors** - Top risks from 10-K
4. **Contradictions** - Gaps between 10-K and transcript statements

## Supported Tickers

- AAPL (Apple)
- TSLA (Tesla)
- NVDA (NVIDIA)
- MSFT (Microsoft)
- GOOGL (Alphabet)
- AMZN (Amazon)
- META (Meta Platforms)

## Project Structure

```
earnings-pilot/
├── app.py              # Streamlit UI (alternative)
├── server.py           # FastAPI backend
├── requirements.txt
├── .env.example
├── src/
│   ├── sec_fetcher.py      # SEC EDGAR API
│   ├── transcript_fetcher.py
│   ├── embeddings.py       # OpenAI embeddings
│   ├── vector_store.py     # ChromaDB
│   ├── prompts.py          # LLM prompts
│   └── report_generator.py
└── frontend/            # React + Vite UI
    ├── src/
    │   └── App.jsx
    └── package.json
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/fetch` | POST | Fetch 10-K and transcripts |
| `/api/generate` | POST | Generate earnings report |
| `/api/health` | GET | Health check |

## Tech Stack

- **Backend**: Python, FastAPI, LangChain
- **Frontend**: React, Vite, Tailwind CSS
- **AI**: Claude 3.5 Sonnet (Anthropic)
- **Embeddings**: OpenAI text-embedding-3-small
- **Vector DB**: ChromaDB
- **Data**: SEC EDGAR (free), Financial Modeling Prep (paid)
