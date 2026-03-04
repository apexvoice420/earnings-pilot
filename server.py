"""
Earnings Copilot - FastAPI Backend
Real SEC data + GLM-5 analysis
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os

app = FastAPI(title="Earnings Copilot API")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state for current analysis
current_data = {}


@app.get("/")
async def root():
    return {"message": "Earnings Copilot API", "status": "running"}


@app.get("/api/status")
async def get_status():
    """Health check endpoint for Railway."""
    return {
        "status": "healthy",
        "version": "2.0.0",
        "name": "Earnings Copilot",
        "features": ["SEC EDGAR", "GLM-5 Analysis", "Real Financial Data"]
    }


@app.get("/health")
async def health():
    """Simple health check."""
    return {"status": "ok"}


@app.get("/api/fetch/{ticker}")
async def fetch_data(ticker: str):
    """Fetch real 10-K and earnings transcript data for a ticker."""
    global current_data
    
    try:
        from src.sec_fetcher import fetch_and_process_10k
        from src.transcript_fetcher import fetch_and_analyze_transcript
        
        ticker = ticker.upper()
        
        # Fetch 10-K data with real financial metrics
        print(f"Fetching SEC data for {ticker}...")
        sec_data = fetch_and_process_10k(ticker)
        
        if "error" in sec_data:
            raise HTTPException(status_code=404, detail=sec_data["error"])
        
        # Fetch earnings transcript
        print(f"Fetching transcript for {ticker}...")
        transcript_data = fetch_and_analyze_transcript(ticker)
        
        # Combine into current_data for report generation
        current_data[ticker] = {
            "ticker": ticker,
            "company_name": sec_data.get("company_name", ticker),
            "metrics": sec_data.get("metrics", {}),
            "sections": sec_data.get("sections", {}),
            "filing_date": sec_data.get("filing_date"),
            "transcript": transcript_data.get("full_content"),
            "transcript_date": transcript_data.get("date"),
            "qa_content": transcript_data.get("qa_content"),
            "sentiment": transcript_data.get("sentiment", {}),
            "management_statements": transcript_data.get("management_statements", []),
        }
        
        # Also store in vector DB for semantic search
        try:
            from src.vector_store import get_store
            store = get_store()
            store.clear_all()
            
            # Add 10-K chunks
            chunks = sec_data.get("chunks", [])
            for chunk in chunks[:50]:  # Limit
                store.add_documents(
                    [chunk["content"]],
                    [{"source": "10-K", "section": chunk["section"]}]
                )
            
            # Add transcript
            if transcript_data.get("full_content"):
                transcript_chunks = [
                    transcript_data["full_content"][i:i+1000]
                    for i in range(0, min(len(transcript_data["full_content"]), 10000), 1000)
                ]
                for chunk in transcript_chunks:
                    store.add_documents([chunk], [{"source": "Transcript"}])
                    
        except Exception as e:
            print(f"Warning: Vector store error: {e}")
        
        return {
            "ticker": ticker,
            "company_name": sec_data.get("company_name", ticker),
            "filing_date": sec_data.get("filing_date"),
            "metrics_available": list(sec_data.get("metrics", {}).keys()),
            "sections_loaded": list(sec_data.get("sections", {}).keys()),
            "transcript_date": transcript_data.get("date"),
            "sentiment": transcript_data.get("sentiment", {}),
            "status": "success"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/generate/{ticker}")
async def generate_report(ticker: str):
    """Generate earnings prep report using GLM-5."""
    global current_data
    
    try:
        ticker = ticker.upper()
        
        # Check if we have data for this ticker
        if ticker not in current_data:
            raise HTTPException(
                status_code=400, 
                detail=f"No data found for {ticker}. Please fetch filings first using /api/fetch/{ticker}"
            )
        
        from src.report_generator import ReportGenerator
        
        gen = ReportGenerator()
        gen.set_data(current_data[ticker])
        
        print(f"Generating report for {ticker}...")
        report = gen.generate_full_report()
        
        return report
        
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/metrics/{ticker}")
async def get_metrics(ticker: str):
    """Get just the financial metrics for a ticker."""
    try:
        from src.sec_fetcher import extract_financial_metrics, get_cik
        
        ticker = ticker.upper()
        cik = get_cik(ticker)
        
        if not cik:
            raise HTTPException(status_code=404, detail=f"Ticker {ticker} not found")
        
        metrics = extract_financial_metrics(cik)
        
        return {
            "ticker": ticker,
            "cik": cik,
            "metrics": metrics
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/audit/{ticker}")
async def run_sec_audit(ticker: str):
    """Run SEC Specialist Agent audit on a ticker's 10-K filing."""
    global current_data
    
    try:
        ticker = ticker.upper()
        
        # Ensure we have data first
        if ticker not in current_data:
            # Auto-fetch if not already loaded
            from src.sec_fetcher import fetch_and_process_10k
            from src.transcript_fetcher import fetch_and_analyze_transcript
            
            print(f"Auto-fetching data for {ticker}...")
            sec_data = fetch_and_process_10k(ticker)
            
            if "error" in sec_data:
                raise HTTPException(status_code=404, detail=sec_data["error"])
            
            transcript_data = fetch_and_analyze_transcript(ticker)
            
            current_data[ticker] = {
                "ticker": ticker,
                "company_name": sec_data.get("company_name", ticker),
                "metrics": sec_data.get("metrics", {}),
                "sections": sec_data.get("sections", {}),
                "filing_date": sec_data.get("filing_date"),
                "transcript": transcript_data.get("full_content"),
                "transcript_date": transcript_data.get("date"),
                "qa_content": transcript_data.get("qa_content"),
                "sentiment": transcript_data.get("sentiment", {}),
            }
        
        # Run the SEC Specialist Agent
        from src.sec_agent import run_sec_audit as audit
        print(f"Running SEC Specialist Audit for {ticker}...")
        
        results = audit(ticker)
        
        if "error" in results:
            raise HTTPException(status_code=400, detail=results["error"])
        
        return results
        
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/audit/{ticker}")
async def run_audit(ticker: str):
    """Run SEC Specialist Agent compliance audit for a ticker."""
    try:
        from src.sec_agent import SECSpecialistAgent
        
        ticker = ticker.upper()
        
        print(f"Running SEC audit for {ticker}...")
        agent = SECSpecialistAgent()
        results = agent.run_audit(ticker)
        
        if "error" in results:
            raise HTTPException(status_code=404, detail=results["error"])
        
        return results
        
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting Earnings Copilot API on port {port}...")
    print(f"MODAL_API_KEY configured: {'Yes' if os.environ.get('MODAL_API_KEY') else 'No'}")
    uvicorn.run(app, host="0.0.0.0", port=port)
