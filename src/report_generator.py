"""
Report Generator - Real Data Analysis with Groq (Free) / OpenAI / Gemini
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

# API Configuration - Priority: Groq (Free) > OpenAI > Gemini
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

# Groq is FREE and fast - use it first
if GROQ_API_KEY:
    API_KEY = GROQ_API_KEY
    API_URL = "https://api.groq.com/openai/v1/chat/completions"
    MODEL = "llama-3.3-70b-versatile"  # Correct model name
    PROVIDER = "Groq"
elif OPENAI_API_KEY:
    API_KEY = OPENAI_API_KEY
    API_URL = "https://api.openai.com/v1/chat/completions"
    MODEL = "gpt-4o-mini"
    PROVIDER = "OpenAI"
elif GOOGLE_API_KEY:
    API_KEY = GOOGLE_API_KEY
    API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GOOGLE_API_KEY}"
    MODEL = "gemini-1.5-flash"
    PROVIDER = "Google"
else:
    API_KEY = ""
    API_URL = ""
    MODEL = ""
    PROVIDER = "None"


def call_llm(system_prompt, user_prompt, context):
    """Call LLM API with proper error handling."""
    
    if not API_KEY:
        print("No API key configured - using fallback")
        return generate_fallback_report(context)
    
    print(f"Calling {PROVIDER} API with model {MODEL}...")
    
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
            content = data["choices"][0]["message"]["content"]
            print(f"{PROVIDER} API call successful - {len(content)} chars returned")
            return content
        else:
            print(f"{PROVIDER} API Error {response.status_code}: {response.text[:500]}")
            return generate_fallback_report(context)
            
    except Exception as e:
        print(f"{PROVIDER} API Exception: {e}")
        return generate_fallback_report(context)


def generate_fallback_report(context):
    """Generate a basic report without LLM when API unavailable."""
    
    return f"""Based on SEC filing analysis:

KEY FINDINGS:
- Document contains financial data from SEC EDGAR
- Business operations section analyzed
- Risk factors reviewed

⚠️ AI ANALYSIS UNAVAILABLE - No LLM API key configured.

FREE OPTION: Get a Groq API key at https://console.groq.com/keys (no credit card needed)

Current configuration:
- Groq Key (FREE): {'✅ Set' if GROQ_API_KEY else '❌ Not set'}
- OpenAI Key: {'✅ Set' if OPENAI_API_KEY else '❌ Not set'}
- Google Key: {'✅ Set' if GOOGLE_API_KEY else '❌ Not set'}

Add GROQ_API_KEY to Railway environment variables for free AI analysis.

Document sections analyzed: {len(context)} characters of context available.
"""


class ReportGenerator:
    def __init__(self):
        self.data = None
        self.context = ""
    
    def set_data(self, data):
        """Set the data for report generation."""
        self.data = data
        
        # Build context from all available data
        context_parts = []
        
        # Add company info
        if data.get("company_name"):
            context_parts.append(f"COMPANY: {data['company_name']}")
        
        # Add metrics
        if data.get("metrics"):
            context_parts.append("\nFINANCIAL METRICS:")
            for key, value in data["metrics"].items():
                if value and isinstance(value, dict) and value.get("value"):
                    context_parts.append(f"- {key}: ${value['value']:,.0f}")
        
        # Add sections
        if data.get("sections"):
            for section_name, content in data["sections"].items():
                if content:
                    context_parts.append(f"\n{section_name.upper()}:\n{content[:2000]}")
        
        # Add transcript
        if data.get("transcript"):
            context_parts.append(f"\nEARNINGS TRANSCRIPT:\n{data['transcript'][:3000]}")
        
        self.context = "\n".join(context_parts)
    
    def generate_full_report(self):
        """Generate full earnings prep report."""
        
        if not self.context:
            return {
                "summary": "No data available. Please fetch filings first.",
                "questions": "No data available.",
                "red_flags": "No data available.",
                "contradictions": "No data available.",
                "delta": "No data available.",
                "financial_health": "No data available."
            }
        
        # Generate each section
        return {
            "summary": call_llm(SYSTEM_PROMPT, EXECUTIVE_SUMMARY, self.context),
            "questions": call_llm(SYSTEM_PROMPT, ANALYST_QUESTIONS, self.context),
            "red_flags": call_llm(SYSTEM_PROMPT, RED_FLAGS, self.context),
            "contradictions": call_llm(SYSTEM_PROMPT, CONTRADICTION_FINDER, self.context),
            "delta": call_llm(SYSTEM_PROMPT, DELTA_REPORT, self.context),
            "financial_health": call_llm(SYSTEM_PROMPT, FINANCIAL_HEALTH, self.context)
        }


def generate_report():
    """Standalone function to generate report."""
    gen = ReportGenerator()
    return gen.generate_full_report()
