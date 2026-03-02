"""
Earnings Copilot - FastAPI Backend
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn

from src.sec_fetcher import fetch_and_process_10k
from src.transcript_fetcher import fetch_and_analyze_transcript
from src.vector_store import get_store
from src.report_generator import ReportGenerator

app = FastAPI(title="Earnings Copilot API")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

store = get_store()
report_gen = ReportGenerator()

# Store sentiment in memory for demo
current_sentiment = {}

class ReportResponse(BaseModel):
    summary: str
    questions: str
    contradictions: str

class SentimentResponse(BaseModel):
    sentiment: str
    positive_count: int
    negative_count: int


@app.get("/")
async def root():
    return {"message": "Earnings Copilot API", "status": "running"}


@app.get("/api/fetch/{ticker}")
async def fetch_data(ticker: str):
    """Fetch 10-K and transcripts for a ticker"""
    global current_sentiment
    
    try:
        # Fetch 10-K
        sections = fetch_and_process_10k(ticker.upper())
        
        # Fetch transcript
        transcript_data = fetch_and_analyze_transcript(ticker.upper())
        
        # Store in vector DB
        store.clear_all()
        
        for section_name, chunks in sections.items():
            metadatas = [{"source": "10-K", "section": section_name}] * len(chunks)
            store.add_documents(chunks, metadatas)
        
        transcript_chunks = [transcript_data['full_content'][i:i+1000] 
                            for i in range(0, len(transcript_data['full_content']), 1000)]
        store.add_documents(transcript_chunks, [{"source": "Transcript"}] * len(transcript_chunks))
        
        current_sentiment = transcript_data['sentiment']
        
        return {
            "ticker": ticker.upper(),
            "sentiment": transcript_data['sentiment'],
            "sections_loaded": list(sections.keys()),
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/generate/{ticker}")
async def generate_report(ticker: str):
    """Generate earnings prep report"""
    try:
        report = report_gen.generate_report()
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/status")
async def get_status():
    """API status check"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "name": "Earnings Copilot"
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
