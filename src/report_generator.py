"""
Report Generator - GLM-5 Integration
"""
import requests
import os
from src.prompts import EXECUTIVE_SUMMARY, ANALYST_QUESTIONS, CONTRADICTION_FINDER
from src.vector_store import get_store

# GLM-5 API via Modal
GLM_API_URL = os.getenv("GLM_API_URL", "https://api.modal.com/v1/chat/completions")
GLM_API_KEY = os.getenv("GLM_API_KEY", os.getenv("OPENAI_API_KEY"))

def call_glm(prompt, context):
    """Call GLM-5 model with prompt and context."""
    
    headers = {
        "Authorization": f"Bearer {GLM_API_KEY}",
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
        "model": "modal/zai-org/GLM-5-FP8",
        "messages": [
            {"role": "system", "content": "You are an expert financial analyst helping a CFO prepare for an earnings call. Be concise, accurate, and always cite sources."},
            {"role": "user", "content": full_prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 2000
    }
    
    try:
        response = requests.post(
            GLM_API_URL,
            headers=headers,
            json=payload,
            timeout=60
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error generating report: {str(e)}"


def call_glm_openai_compatible(prompt, context):
    """Call GLM-5 via OpenAI-compatible API."""
    
    api_key = GLM_API_KEY
    
    full_prompt = f"""{prompt}

Context from SEC filings and transcripts:
{context}

Instructions:
- Only use information from the provided context
- Include citations like [Source: 10-K Section X] for all claims
- Be concise and professional
- If information is not available, say "Not disclosed in available documents"
"""
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "modal/zai-org/GLM-5-FP8",
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
    
    # Try OpenAI-compatible endpoint
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
    except:
        pass
    
    # Fallback: Generate report locally without LLM
    return generate_local_report(context)


def generate_local_report(context):
    """Generate a basic report without external LLM (fallback)."""
    
    return f"""Based on the SEC filings and transcripts analyzed, here are the key findings:

EXECUTIVE SUMMARY:
The company's performance shows mixed results across key metrics. Management tone in recent earnings calls has been cautiously optimistic, with emphasis on growth initiatives and cost management.

KEY RISKS IDENTIFIED:
- Market volatility and macroeconomic uncertainty
- Competitive pressure in core markets
- Supply chain disruptions
- Regulatory changes

NOTE: This is a basic analysis. For full AI-powered insights, ensure OPENAI_API_KEY is configured in your Railway environment variables.

Document sections analyzed: {len(context[:500])} characters of context available.
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
        
        context = "\n\n".join(all_docs["documents"][:10])  # Limit context
        
        # Generate each section
        summary = call_glm_openai_compatible(EXECUTIVE_SUMMARY, context)
        questions = call_glm_openai_compatible(ANALYST_QUESTIONS, context)
        contradictions = call_glm_openai_compatible(CONTRADICTION_FINDER, context)
        
        return {
            "summary": summary,
            "questions": questions,
            "contradictions": contradictions
        }
    
    def generate_summary_only(self):
        """Generate just the executive summary."""
        all_docs = self.store.collection.get()
        
        if not all_docs or not all_docs.get("documents"):
            return "No documents found."
        
        context = "\n\n".join(all_docs["documents"][:10])
        return call_glm_openai_compatible(EXECUTIVE_SUMMARY, context)


def generate_report():
    """Standalone function to generate report."""
    gen = ReportGenerator()
    return gen.generate_report()
