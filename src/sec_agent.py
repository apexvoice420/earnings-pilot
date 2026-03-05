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
    SEC Specialist Agent - Runs comprehensive 10-K/Q/8 audits and drafts.
    """
    
    def __init__(self):
        self.system_prompt = SEC_SPECIALIST_PROMPT

    def run_audit(self, ticker, form_type="10-K"):
        """Runs the full Comprehensive Audit workflow for a filing."""
        print(f"Starting SEC Specialist Audit for {ticker} ({form_type})...")
        
        ticker = ticker.upper()
        
        # 1. Fetch Data
        from src.sec_fetcher import fetch_and_process_filing
        print(f"Fetching {form_type} filings...")
        filing_data = fetch_and_process_filing(ticker, form_type)
        
        if "error" in filing_data:
            return {"error": filing_data["error"]}
        
        print("Fetching transcript...")
        transcript_data = fetch_and_analyze_transcript(ticker)
        
        # Build context
        context = self._build_context(filing_data, transcript_data)
        
        # 2. Execute Audit Steps
        results = {}
        
        print("Step 1: Analyzing YoY/Period Changes...")
        delta_prompt = f"""Compare the current {form_type} with the previous year's filing. 
        Focus on stagnant text and new risks that should be disclosed."""
        results['yoy_analysis'] = call_llm(self.system_prompt, delta_prompt, context)
        
        print("Step 2: Checking Transcript Alignment...")
        transcript_prompt = f"Cross-reference the {form_type} with the earnings call transcript. Does documentation match management narrative?"
        results['transcript_alignment'] = call_llm(self.system_prompt, transcript_prompt, context)
        
        print("Step 3: Redline & Puffery Check...")
        redline_prompt = "Review the filing (especially MD&A) for puffery, clarity, and driver analysis."
        results['sec_redline'] = call_llm(self.system_prompt, redline_prompt, context)
        
        # Add metadata
        results['ticker'] = ticker
        results['form_type'] = form_type
        results['company_name'] = filing_data.get("company_name", ticker)
        results['filing_date'] = filing_data.get("filing_date")
        results['transcript_date'] = transcript_data.get("date")
        
        return results

    def run_drafting(self, ticker, section="mda", form_type="10-K"):
        """Drafts a specific filing section based on current data and transcripts."""
        print(f"Drafting {section.upper()} for {ticker} ({form_type})...")
        
        ticker = ticker.upper()
        from src.sec_fetcher import fetch_and_process_filing
        filing_data = fetch_and_process_filing(ticker, form_type)
        transcript_data = fetch_and_analyze_transcript(ticker)
        
        context = self._build_context(filing_data, transcript_data)
        
        prompts = {
            "mda": f"""Draft a professional MD&A section for a {form_type} filing.
            Use the financial data provided and the 'drivers' identified in the earnings transcript.
            Ensure you explain the 'Why' behind the numbers. Tone: Wall Street Objective.""",
            "risk_factors": f"Draft an updated Risk Factors (Item 1A) for a {form_type} based on the transcript discussion and current macro environment.",
            "business": "Draft a 'Business Description' update focusing on new product lines or strategic shifts mentioned in recent transcripts."
        }
        
        draft_prompt = prompts.get(section, f"Draft the {section} section for a {form_type} filing.")
        draft = call_llm(self.system_prompt, draft_prompt, context)
        
        return {
            "ticker": ticker,
            "section": section,
            "form_type": form_type,
            "draft": draft,
            "company_name": filing_data.get("company_name", ticker)
        }

    def _build_context(self, filing_data, transcript_data):
        """Builds a structured context string for the LLM."""
        context_parts = []
        if filing_data.get("company_name"):
            context_parts.append(f"COMPANY: {filing_data['company_name']}")
        
        if filing_data.get("sections"):
            for section_name, content in filing_data["sections"].items():
                if content:
                    context_parts.append(f"\n{section_name.upper()}:\n{content[:2000]}")
        
        if transcript_data.get("full_content"):
            context_parts.append(f"\nEARNINGS TRANSCRIPT:\n{transcript_data['full_content'][:3000]}")
            
        return "\n".join(context_parts)

    def format_report(self, ticker, results):
        """Formats the audit results into a professional markdown report."""
        if "error" in results:
            return f"# Error\n\n{results['error']}"
        
        if "draft" in results:
            return f"""# Draft {results['section'].upper()} Section: {results['company_name']} ({results['ticker']})
**Form Type:** {results['form_type']}
**Source:** Earnings Pilot Drafting Assistant

---

{results['draft']}

---
*⚠️ Professional Disclaimer: This draft is generated by an AI assistant and must be reviewed by legal and financial counsel before official filing.*"""

        report = f"""# SEC {results.get('form_type', '10-K')} Compliance Audit: {results.get('company_name', ticker)}

**Filing Date:** {results.get('filing_date', 'N/A')}  
**Transcript Date:** {results.get('transcript_date', 'N/A')}

---

## 1. YoY/Period Delta Analysis
{results.get('yoy_analysis', 'No data.')}

---

## 2. Strategic Alignment
{results.get('transcript_alignment', 'No data.')}

---

## 3. Redline & Puffery Check
{results.get('sec_redline', 'No data.')}

---

*⚠️ Professional Disclaimer: This report is generated by an AI agent for informational purposes only. It does not constitute legal, tax, or financial advice. Consult qualified professionals for official guidance.*"""
        return report


def run_sec_audit(ticker, form_type="10-K"):
    """Convenience function to run audit and return results."""
    agent = SECSpecialistAgent()
    return agent.run_audit(ticker)
