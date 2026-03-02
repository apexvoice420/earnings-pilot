"""
FastAPI backend for Earnings Pilot
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn

from src.sec_fetcher import fetch_and_process_10k
from src.transcript_fetcher import fetch_and_analyze_transcript
from src.vector_store import get_store
from src.report_generator import ReportGenerator

app = FastAPI(title="Earnings Pilot API")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store and generator instances
store = get_store()
report_gen = ReportGenerator()

# In-memory state (use proper DB in production)
current_ticker = None
current_sentiment = None


class FetchRequest(BaseModel):
    ticker: str


class GenerateRequest(BaseModel):
    ticker: str


@app.post("/api/fetch")
async def fetch_data(request: FetchRequest):
    """Fetch 10-K and transcripts for a ticker"""
    global current_ticker, current_sentiment

    ticker = request.ticker.upper()

    try:
        # Fetch 10-K
        sections = fetch_and_process_10k(ticker)

        # Fetch transcript
        transcript_data = fetch_and_analyze_transcript(ticker)

        # Store in ChromaDB
        store.clear_all()

        for section_name, chunks in sections.items():
            metadatas = [{"source": "10-K", "section": section_name}] * len(chunks)
            store.add_documents(chunks, metadatas)

        # Chunk and store transcript
        transcript_chunks = [
            transcript_data['full_content'][i:i+1000]
            for i in range(0, len(transcript_data['full_content']), 1000)
        ]
        store.add_documents(
            transcript_chunks,
            [{"source": "Transcript"}] * len(transcript_chunks)
        )

        current_ticker = ticker
        current_sentiment = transcript_data['sentiment']

        return {
            "success": True,
            "ticker": ticker,
            "sentiment": current_sentiment,
            "sections_loaded": list(sections.keys())
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/generate")
async def generate_report(request: GenerateRequest):
    """Generate earnings prep report"""
    global current_sentiment

    try:
        report = report_gen.generate_report()

        return {
            "success": True,
            "ticker": request.ticker,
            "report": report,
            "sentiment": current_sentiment
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/health")
async def health():
    return {"status": "ok"}


# Serve frontend in production
# app.mount("/", StaticFiles(directory="frontend/dist", html=True), name="static")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
