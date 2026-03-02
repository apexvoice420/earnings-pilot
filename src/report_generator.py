"""
Report Generator - GLM-5 via Modal API
"""
import requests
import os
from src.prompts import EXECUTIVE_SUMMARY, ANALYST_QUESTIONS, CONTRADICTION_FINDER
from src.vector_store import get_store

# Modal API for GLM-5
MODAL_API_KEY = os.getenv("MODAL_API_KEY", "")
MODAL_API_URL = os.getenv("MODAL_API_URL", "https://api.modal.com/v1/chat/completions")


def call_glm(prompt, context):
    """Call GLM-5 model via Modal API."""
    
    headers = {
        "Authorization": f"Bearer {MODAL_API_KEY}",
        "Content-Type": "application/json"
    }
    
    full_prompt = f"""{prompt}

Context from SEC filings and transcripts:
{context}

Instructions:
- Only use information from the provided context
- Include citations like [Source: 10-K Section X] for all claims
- Be concise and professional
- If information is not available, say "Not disclosed in available documents"
"""
    
    payload = {
        "model": "zai-org/GLM-5-FP8",
        "messages": [
            {
                "role": "system", 
                "content": "You are an expert financial analyst helping a CFO prepare for an earnings call. Be concise, accurate, and always cite sources."
            },
            {
                "role": "user", 
                "content": full_prompt
            }
        ],
        "temperature": 0.7,
        "max_tokens": 2000
    }
    
    try:
        response = requests.post(
            MODAL_API_URL,
            headers=headers,
            json=payload,
            timeout=60
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"GLM API Error: {e}")
        return generate_local_report(context, str(e))


def generate_local_report(context, error=""):
    """Generate a basic report without LLM (fallback)."""
    
    return f"""Based on the SEC filings and transcripts analyzed:

EXECUTIVE SUMMARY:
The company's performance shows mixed results. Management tone has been cautiously optimistic.

KEY RISKS IDENTIFIED:
- Market volatility
- Competitive pressure
- Supply chain disruptions
- Regulatory changes

[Fallback mode - LLM unavailable: {error}]

Document sections analyzed: {len(context)} characters.
"""


class ReportGenerator:
    def __init__(self):
        self.store = get_store()
    
    def generate_report(self):
        """Generate full earnings prep report."""
        
        # Get context from vector store
        all_docs = self.store.collection.get()
        
        if not all_docs or not all_docs.get("documents"):
            return {
                "summary": "No documents found. Please fetch filings first.",
                "questions": "No documents found. Please fetch filings first.",
                "contradictions": "No documents found. Please fetch filings first."
            }
        
        context = "\n\n".join(all_docs["documents"][:10])
        
        # Generate each section with GLM-5
        summary = call_glm(EXECUTIVE_SUMMARY, context)
        questions = call_glm(ANALYST_QUESTIONS, context)
        contradictions = call_glm(CONTRADICTION_FINDER, context)
        
        return {
            "summary": summary,
            "questions": questions,
            "contradictions": contradictions
        }


def generate_report():
    """Standalone function to generate report."""
    gen = ReportGenerator()
    return gen.generate_report()
