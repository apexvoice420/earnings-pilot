import argparse
from src.sec_agent import SECSpecialistAgent

def main():
    parser = argparse.ArgumentParser(description="Test SEC Agent Drafting and Multi-Filing Audit.")
    parser.add_argument("--ticker", required=True, help="Ticker (e.g., TSLA)")
    parser.add_argument("--mode", choices=["audit", "draft"], default="draft")
    parser.add_argument("--form", default="10-K")
    parser.add_argument("--section", default="mda")
    
    args = parser.parse_args()
    agent = SECSpecialistAgent()
    
    if args.mode == "draft":
        print(f"Testing Drafting for {args.ticker}...")
        results = agent.run_drafting(args.ticker, section=args.section, form_type=args.form)
    else:
        print(f"Testing Audit for {args.ticker} ({args.form})...")
        results = agent.run_audit(args.ticker, form_type=args.form)
        
    report = agent.format_report(args.ticker, results)
    
    filename = f"test_{args.mode}_{args.ticker}_{args.form}.md"
    with open(filename, "w") as f:
        f.write(report)
        
    print(f"✅ Test complete. Report saved to: {filename}")

if __name__ == "__main__":
    main()
