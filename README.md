# Earnings Copilot 🚀

AI-powered earnings call preparation platform. Save executives days of work by automating 10-K analysis and transcript review.

## Features

- **SEC EDGAR Integration** — Fetch 10-K/10-Q filings by ticker
- **Earnings Transcripts** — Pull quarterly earnings call transcripts
- **AI Analysis** — Claude 3.5 Sonnet generates executive summaries, analyst questions, and contradiction analysis
- **Vector Search** — ChromaDB-powered semantic search over filings
- **Sentiment Analysis** — Track management tone across quarters

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | React + Vite + Tailwind |
| Backend | FastAPI (Python) |
| AI/LLM | Claude 3.5 Sonnet |
| Embeddings | OpenAI text-embedding-3-small |
| Vector DB | ChromaDB |
| Data Sources | SEC EDGAR, Financial Modeling Prep |

## Quick Start

### 1. Clone and Install

```bash
git clone https://github.com/apexvoice420/earnings-pilot.git
cd earnings-pilot

# Backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

### 2. Configure Environment

```bash
cp .env.example .env
```

Add your API keys:

```
SEC_USER_AGENT=EarningsCopilot your@email.com
FMP_API_KEY=your_fmp_key
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
```

### 3. Run

```bash
# Terminal 1 - Backend
python server.py

# Terminal 2 - Frontend
cd frontend && npm run dev
```

Visit http://localhost:3000

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/fetch/{ticker}` | GET | Fetch 10-K and transcripts |
| `/api/generate/{ticker}` | GET | Generate prep report |
| `/api/status` | GET | API health check |

## Supported Tickers

- AAPL (Apple)
- TSLA (Tesla)
- NVDA (NVIDIA)
- MSFT (Microsoft)
- GOOGL (Google/Alphabet)
- AMZN (Amazon)
- META (Meta/Facebook)

## Deploy

### Railway (Backend)

```bash
railway login
railway init
railway up
```

### Vercel (Frontend)

```bash
cd frontend
vercel --prod
```

## Domain

**earningscopilot.com**

## License

MIT
