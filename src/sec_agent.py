"""
SEC Specialist Agent - Implements the 'sec-10k-compliance-pro' skill logic.
"""
import os
from src.report_generator import call_llm
from src.sec_fetcher import fetch_and_process_10k, get_cik
from src.transcript_fetcher import fetch_and_analyze_transcript


# System prompt from SKILL.md
SEC_SPECIALIST_PROMPT = """You are the Lead Disclosure Counsel. Your goal is to ensure 10-K filings are legally sound, strategically aligned with investor narratives, and compliant with SEC Regulation S-K.

# Instructions
1. **The "Delta" Protocol:** When reviewing a draft, always compare it against the previous year's 10-K. Highlight "boilerplate" text that hasn't changed despite significant business shifts.
2. **Item-Specific Expertise:**
   - **Item 1A (Risk Factors):** Identify new macro/micro risks (e.g., AI, Geopolitical, Supply Chain) not present in the draft.
   - **Item 7 (MD&A):** Ensure financial results are explained by *drivers* (the "Why"), not just *numbers* (the "What").
3. **Puffery Check:** Flag and remove promotional or "marketing" language that could trigger an SEC comment letter.
4. **Consistency Engine:** Cross-reference the 10-K draft with recent Earnings Call transcripts. Ensure the narrative told to analysts matches the formal filing.

# Constraints
- NEVER give definitive legal or tax advice; always include a professional disclaimer.
- Maintain a formal, objective "Wall Street" tone. 
- Use specific citations from the documents when making claims.
"""


class SECSpecialistAgent:
    """
    SEC Specialist Agent - Runs comprehensive 10-K compliance audits.
    """
    
    def __init__(self):
        self.system_prompt = SEC_SPECIALIST_PROMPT

    def run_audit(self, ticker):
        """Runs the full 10-K Comprehensive Audit workflow."""
        print(f"Starting SEC Specialist Audit for {ticker}...")
        
        ticker = ticker.upper()
        
        # 1. Fetch Data
        print("Fetching SEC filings...")
        current_10k = fetch_and_process_10k(ticker)
        
        if "error" in current_10k:
            return {"error": current_10k["error"]}
        
        print("Fetching transcript...")
        transcript_data = fetch_and_analyze_transcript(ticker)
        
        # Build context
        context_parts = []
        
        # Add company info
        if current_10k.get("company_name"):
            context_parts.append(f"COMPANY: {current_10k['company_name']}")
        
        # Add sections from 10-K
        if current_10k.get("sections"):
            for section_name, content in current_10k["sections"].items():
                if content:
                    context_parts.append(f"\n{section_name.upper()}:\n{content[:2000]}")
        
        # Add transcript
        if transcript_data.get("full_content"):
            context_parts.append(f"\nEARNINGS TRANSCRIPT:\n{transcript_data['full_content'][:3000]}")
        
        context = "\n".join(context_parts)
        
        # 2. Execute Audit Steps
        results = {}
        
        print("Step 1: Analyzing YoY Changes...")
        delta_prompt = """Compare the current 10-K with the previous year's filing. 

Focus on:
1. Item 1A (Risk Factors) - Identify stagnant text that hasn't changed despite business shifts
2. New risks that should be disclosed but aren't
3. Changes in language or emphasis

Provide specific citations and recommendations."""
        results['yoy_analysis'] = call_llm(self.system_prompt, delta_prompt, context)
        
        print("Step 2: Checking Transcript Alignment...")
        transcript_prompt = """Cross-reference the 10-K with the earnings call transcript.

Analyze:
1. Does the 10-K narrative match what management told analysts?
2. Any contradictions between the two documents?
3. Topics emphasized on the call but buried or missing in the 10-K?
4. Risks disclosed in 10-K that weren't discussed on the call?

Be specific with citations."""
        results['transcript_alignment'] = call_llm(self.system_prompt, transcript_prompt, context)
        
        print("Step 3: MD&A Redline & Puffery Check...")
        redline_prompt = """Review the MD&A section (Item 7) for:

1. **Puffery Check**: Flag promotional/marketing language that could trigger SEC comments
2. **Clarity Review**: Identify vague statements that lack specificity
3. **Driver Analysis**: Are results explained by *why* not just *what*?

For each issue found, provide:
- The problematic language (quote it)
- Why it's an issue
- Suggested revision

Format as a redline review with [ORIGINAL] and [SUGGESTED] sections."""
        results['sec_redline'] = call_llm(self.system_prompt, redline_prompt, context)
        
        # Add metadata
        results['ticker'] = ticker
        results['company_name'] = current_10k.get("company_name", ticker)
        results['filing_date'] = current_10k.get("filing_date")
        results['transcript_date'] = transcript_data.get("date")
        
        return results

    def format_report(self, ticker, results):
        """Formats the audit results into a professional markdown report."""
        if "error" in results:
            return f"# Error\n\n{results['error']}"
        
        report = f"""# SEC 10-K Compliance Audit: {results.get('company_name', ticker)}

**Filing Date:** {results.get('filing_date', 'N/A')}  
**Transcript Date:** {results.get('transcript_date', 'N/A')}

---

## 1. YoY Delta Analysis (Item 1A Focus)

{results.get('yoy_analysis', 'No data.')}

---

## 2. Strategic Alignment (10-K vs Transcript)

{results.get('transcript_alignment', 'No data.')}

---

## 3. MD&A Redline & Puffery Check

{results.get('sec_redline', 'No data.')}

---

*⚠️ Professional Disclaimer: This report is generated by an AI agent for informational purposes only. It does not constitute legal, tax, or financial advice. Consult qualified professionals for official guidance.*
"""
        return report


def run_sec_audit(ticker):
    """Convenience function to run audit and return results."""
    agent = SECSpecialistAgent()
    return agent.run_audit(ticker)
