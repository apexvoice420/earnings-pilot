"""
Earnings Copilot - FastAPI Backend
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
import uvicorn

# Initialize app first
app = FastAPI(title="Earnings Copilot API")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Lazy load modules to prevent startup crashes
store = None
report_gen = None
current_sentiment = {}

def get_store():
    global store
    if store is None:
        from src.vector_store import VectorStore
        store = VectorStore()
    return store

def get_report_gen():
    global report_gen
    if report_gen is None:
        from src.report_generator import ReportGenerator
        report_gen = ReportGenerator()
    return report_gen


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


@app.get("/health")
async def health():
    """Health check endpoint for Railway"""
    return {"status": "healthy"}


@app.get("/api/status")
async def get_status():
    """API status check"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "name": "Earnings Copilot"
    }


@app.get("/api/fetch/{ticker}")
async def fetch_data(ticker: str):
    """Fetch 10-K and transcripts for a ticker"""
    global current_sentiment
    
    try:
        from src.sec_fetcher import fetch_and_process_10k
        from src.transcript_fetcher import fetch_and_analyze_transcript
        
        # Fetch 10-K
        sections = fetch_and_process_10k(ticker.upper())
        
        # Fetch transcript
        transcript_data = fetch_and_analyze_transcript(ticker.upper())
        
        # Store in vector DB
        vs = get_store()
        vs.clear_all()
        
        for section_name, chunks in sections.items():
            metadatas = [{"source": "10-K", "section": section_name}] * len(chunks)
            vs.add_documents(chunks, metadatas)
        
        if transcript_data.get('full_content'):
            transcript_chunks = [transcript_data['full_content'][i:i+1000] 
                                for i in range(0, len(transcript_data['full_content']), 1000)]
            vs.add_documents(transcript_chunks, [{"source": "Transcript"}] * len(transcript_chunks))
        
        current_sentiment = transcript_data.get('sentiment', {})
        
        return {
            "ticker": ticker.upper(),
            "sentiment": transcript_data.get('sentiment', {}),
            "sections_loaded": list(sections.keys()),
            "status": "success"
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/generate/{ticker}")
async def generate_report(ticker: str):
    """Generate earnings prep report"""
    try:
        rg = get_report_gen()
        report = rg.generate_report()
        return report
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
