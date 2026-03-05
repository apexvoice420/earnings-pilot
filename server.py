"""
Earnings Copilot - FastAPI Backend
Real SEC data + AI analysis
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
        "version": "3.0.0",
        "name": "Earnings Copilot",
        "features": ["SEC EDGAR", "AI Analysis", "Multi-Filing Support", "Drafting Assistant"]
    }


@app.get("/health")
async def health():
    """Simple health check."""
    return {"status": "ok"}


@app.get("/api/fetch/{ticker}")
async def fetch_data(ticker: str, form_type: str = "10-K"):
    """Fetch SEC filing data for a ticker. Supports 10-K, 10-Q, 8-K."""
    global current_data
    
    try:
        from src.sec_fetcher import fetch_and_process_filing
        from src.transcript_fetcher import fetch_and_analyze_transcript
        
        ticker = ticker.upper()
        
        # Fetch filing data
        print(f"Fetching {form_type} data for {ticker}...")
        sec_data = fetch_and_process_filing(ticker, form_type)
        
        if "error" in sec_data:
            raise HTTPException(status_code=404, detail=sec_data["error"])
        
        # Fetch earnings transcript
        print(f"Fetching transcript for {ticker}...")
        transcript_data = fetch_and_analyze_transcript(ticker)
        
        # Store for report generation
        current_data[ticker] = {
            "ticker": ticker,
            "company_name": sec_data.get("company_name", ticker),
            "metrics": sec_data.get("metrics", {}),
            "sections": sec_data.get("sections", {}),
            "filing_date": sec_data.get("filing_date"),
            "form_type": form_type,
            "transcript": transcript_data.get("full_content"),
            "transcript_date": transcript_data.get("date"),
            "qa_content": transcript_data.get("qa_content"),
            "sentiment": transcript_data.get("sentiment", {}),
            "management_statements": transcript_data.get("management_statements", []),
        }
        
        return {
            "ticker": ticker,
            "company_name": sec_data.get("company_name", ticker),
            "filing_date": sec_data.get("filing_date"),
            "form_type": form_type,
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
    """Generate earnings prep report using AI."""
    global current_data
    
    try:
        ticker = ticker.upper()
        
        # Auto-fetch if not already loaded
        if ticker not in current_data:
            from src.sec_fetcher import fetch_and_process_filing
            from src.transcript_fetcher import fetch_and_analyze_transcript
            
            sec_data = fetch_and_process_filing(ticker, "10-K")
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
            }
        
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
    """Get financial metrics for a ticker."""
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
async def run_audit(ticker: str, form_type: str = "10-K"):
    """Run SEC Specialist Agent compliance audit for a ticker."""
    try:
        from src.sec_agent import SECSpecialistAgent
        
        ticker = ticker.upper()
        
        print(f"Running SEC audit for {ticker} ({form_type})...")
        agent = SECSpecialistAgent()
        results = agent.run_audit(ticker, form_type=form_type)
        
        if "error" in results:
            raise HTTPException(status_code=404, detail=results["error"])
        
        return results
        
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/draft/{ticker}")
async def draft_section(ticker: str, section: str = "mda", form_type: str = "10-K"):
    """Draft a filing section using AI based on SEC data and transcripts."""
    try:
        from src.sec_agent import SECSpecialistAgent
        
        ticker = ticker.upper()
        
        print(f"Drafting {section} for {ticker} ({form_type})...")
        agent = SECSpecialistAgent()
        results = agent.run_drafting(ticker, section=section, form_type=form_type)
        
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
    print(f"GROQ_API_KEY configured: {'Yes' if os.environ.get('GROQ_API_KEY') else 'No'}")
    uvicorn.run(app, host="0.0.0.0", port=port)
