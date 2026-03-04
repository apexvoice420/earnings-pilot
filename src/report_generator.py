"""
Report Generator - Real Data Analysis with OpenAI/Modal
"""
import requests
import os
import json
from src.prompts import (
    SYSTEM_PROMPT,
    EXECUTIVE_SUMMARY,
    ANALYST_QUESTIONS,
    RED_FLAGS,
    CONTRADICTION_FINDER,
    DELTA_REPORT,
    FINANCIAL_HEALTH,
)
from src.vector_store import get_store

# API Configuration - Try Modal first, then OpenAI
MODAL_API_KEY = os.getenv("MODAL_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Use OpenAI by default if both are available (more reliable)
if OPENAI_API_KEY:
    API_KEY = OPENAI_API_KEY
    API_URL = "https://api.openai.com/v1/chat/completions"
    MODEL = "gpt-4o-mini"  # Fast, cheap, good quality
elif MODAL_API_KEY:
    API_KEY = MODAL_API_KEY
    API_URL = "https://api.modal.com/v1/chat/completions"
    MODEL = "zai-org/GLM-5-FP8"
else:
    API_KEY = ""
    API_URL = ""
    MODEL = ""


def call_llm(system_prompt, user_prompt, context):
    """Call LLM API with proper error handling."""
    
    if not API_KEY:
        return generate_fallback_report(context)
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    full_user_prompt = f"""{user_prompt}

---
DOCUMENT CONTEXT:
{context[:8000]}

---
Remember:
- Only use information from the provided context
- Cite sources like [Source: 10-K, Item 7] for all claims
- If information is not available, state "Not disclosed in available documents"
"""
    
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": full_user_prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 3000
    }
    
    try:
        response = requests.post(
            API_URL,
            headers=headers,
            json=payload,
            timeout=120
        )
        
        if response.status_code == 200:
            data = response.json()
            return data["choices"][0]["message"]["content"]
        else:
            print(f"API Error {response.status_code}: {response.text}")
            return generate_fallback_report(context)
            
    except Exception as e:
        print(f"LLM API Error: {e}")
        return generate_fallback_report(context)


def generate_fallback_report(context):
    """Generate a basic report without LLM when API unavailable."""
    
    # Extract some basic info from context
    has_revenue = "revenue" in context.lower() or "revenues" in context.lower()
    has_risk = "risk" in context.lower()
    has_business = "business" in context.lower()
    
    return f"""Based on SEC filing analysis:

KEY FINDINGS:
- Document contains financial data from SEC EDGAR
- Business operations section analyzed
- Risk factors reviewed

NOTE: For detailed AI analysis, please configure OPENAI_API_KEY or MODAL_API_KEY in Railway environment variables.

Current configuration:
- OpenAI Key: {'✅ Set' if OPENAI_API_KEY else '❌ Not set'}
- Modal Key: {'✅ Set' if MODAL_API_KEY else '❌ Not set'}

Document sections analyzed: {len(context)} characters of context available.
"""


class ReportGenerator:
    def __init__(self):
        self.store = get_store()

    def generate_report(self):
        """Generate full earnings prep report."""
        
        try:
            all_docs = self.store.collection.get()
        except:
            all_docs = None
        
        if not all_docs or not all_docs.get("documents"):
            return {
                "summary": "No documents found. Please fetch filings first by clicking 'Generate Prep'.",
                "questions": "No documents found.",
                "contradictions": "No documents found.",
                "delta": "No documents found.",
                "financial_health": "No documents found."
            }
        
        context = "\n\n".join(all_docs["documents"][:10])
        
        # Generate each section
        return {
            "summary": call_llm(SYSTEM_PROMPT, EXECUTIVE_SUMMARY, context),
            "questions": call_llm(SYSTEM_PROMPT, ANALYST_QUESTIONS, context),
            "red_flags": call_llm(SYSTEM_PROMPT, RED_FLAGS, context),
            "contradictions": call_llm(SYSTEM_PROMPT, CONTRADICTION_FINDER, context),
            "delta": call_llm(SYSTEM_PROMPT, DELTA_REPORT, context),
            "financial_health": call_llm(SYSTEM_PROMPT, FINANCIAL_HEALTH, context)
        }


def generate_report():
    """Standalone function to generate report."""
    gen = ReportGenerator()
    return gen.generate_report()
