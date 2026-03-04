import argparse
import os
from src.sec_agent import SECSpecialistAgent

def main():
    parser = argparse.ArgumentParser(description="Run an SEC 10-K Audit using the SEC Specialist Agent.")
    parser.add_argument("--ticker", required=True, help="Stock ticker symbol (e.g., TSLA)")
    parser.add_argument("--output", default="audit_report.md", help="Output file path")
    
    args = parser.parse_args()
    
    agent = SECSpecialistAgent()
    
    print(f"🚀 Initializing SEC Specialist Agent for {args.ticker}...")
    try:
        results = agent.run_audit(args.ticker)
        report = agent.format_report(args.ticker, results)
        
        with open(args.output, "w") as f:
            f.write(report)
            
        print(f"✅ Audit complete. Report saved to: {args.output}")
    except Exception as e:
        print(f"❌ Audit failed: {e}")

if __name__ == "__main__":
    main()
