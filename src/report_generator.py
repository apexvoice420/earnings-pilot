"""
Report Generator - Real Data Analysis with GLM-5
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

# Modal API for GLM-5
MODAL_API_KEY = os.getenv("MODAL_API_KEY", "")
MODAL_API_URL = os.getenv("MODAL_API_URL", "https://api.modal.com/v1/chat/completions")


def call_glm(system_prompt, user_prompt, context):
    """Call GLM-5 model via Modal API with proper system prompt."""
    
    if not MODAL_API_KEY:
        return "Error: MODAL_API_KEY not configured. Please add your API key to Railway environment variables."
    
    headers = {
        "Authorization": f"Bearer {MODAL_API_KEY}",
        "Content-Type": "application/json"
    }
    
    full_user_prompt = f"""{user_prompt}

---
DOCUMENT CONTEXT:
{context}

---
Remember:
- Only use information from the provided context
- Cite sources like [Source: 10-K, Item 7] for all claims
- If information is not available, state "Not disclosed in available documents"
"""
    
    payload = {
        "model": "zai-org/GLM-5-FP8",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": full_user_prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 3000
    }
    
    try:
        response = requests.post(
            MODAL_API_URL,
            headers=headers,
            json=payload,
            timeout=90
        )
        
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            return f"API Error ({response.status_code}): {response.text[:500]}"
            
    except requests.exceptions.Timeout:
        return "Error: API request timed out. Please try again."
    except Exception as e:
        return f"Error calling GLM-5: {str(e)}"


def format_context_for_llm(data):
    """Format the fetched data into a clean context for the LLM."""
    
    context_parts = []
    
    # Company info
    if data.get("ticker"):
        context_parts.append(f"=== COMPANY: {data.get('company_name', data['ticker'])} ({data['ticker']}) ===")
    
    # Financial metrics
    if data.get("metrics"):
        context_parts.append("\n=== FINANCIAL METRICS (from SEC XBRL) ===")
        for metric, values in data["metrics"].items():
            if isinstance(values, dict) and values.get("value"):
                value = values["value"]
                date = values.get("date", "N/A")
                formatted = format_large_number(value)
                context_parts.append(f"{metric}: {formatted} (as of {date})")
    
    # 10-K sections
    if data.get("sections"):
        context_parts.append("\n=== 10-K SECTIONS ===")
        for section_name, content in data["sections"].items():
            if content:
                context_parts.append(f"\n--- {section_name.upper()} ---")
                context_parts.append(content[:3000])  # Limit per section
    
    # Earnings transcript
    if data.get("transcript"):
        context_parts.append("\n=== EARNINGS CALL TRANSCRIPT ===")
        context_parts.append(f"Date: {data.get('transcript_date', 'N/A')}")
        context_parts.append(f"Management Sentiment: {data.get('sentiment', {}).get('sentiment', 'N/A')}")
        context_parts.append(data["transcript"][:5000])
        
        if data.get("qa_content"):
            context_parts.append("\n--- Q&A SESSION ---")
            context_parts.append(data["qa_content"][:2000])
    
    return "\n".join(context_parts)


def format_large_number(value):
    """Format large numbers for readability."""
    if not value:
        return "N/A"
    
    try:
        value = float(value)
        if abs(value) >= 1_000_000_000:
            return f"${value / 1_000_000_000:.2f}B"
        elif abs(value) >= 1_000_000:
            return f"${value / 1_000_000:.2f}M"
        else:
            return f"${value:,.0f}"
    except:
        return str(value)


class ReportGenerator:
    def __init__(self):
        self.store = get_store()
        self.data = None
    
    def set_data(self, data):
        """Set the data to analyze."""
        self.data = data
    
    def generate_full_report(self):
        """Generate complete earnings prep report."""
        
        if not self.data:
            # Try to get data from vector store
            all_docs = self.store.collection.get()
            if all_docs and all_docs.get("documents"):
                context = "\n\n".join(str(doc) for doc in all_docs["documents"][:15])
            else:
                return {
                    "error": "No data available. Please fetch filings first.",
                    "summary": "",
                    "questions": "",
                    "contradictions": "",
                    "delta": "",
                    "financial_health": "",
                }
        else:
            context = format_context_for_llm(self.data)
        
        # Generate each section
        print("Generating Executive Summary...")
        summary = call_glm(SYSTEM_PROMPT, EXECUTIVE_SUMMARY, context)
        
        print("Generating Analyst Questions...")
        questions = call_glm(SYSTEM_PROMPT, ANALYST_QUESTIONS, context)
        
        print("Generating Red Flags...")
        red_flags = call_glm(SYSTEM_PROMPT, RED_FLAGS, context)
        
        print("Generating Delta Report...")
        delta = call_glm(SYSTEM_PROMPT, DELTA_REPORT, context)
        
        print("Generating Financial Health...")
        financial_health = call_glm(SYSTEM_PROMPT, FINANCIAL_HEALTH, context)
        
        return {
            "summary": summary,
            "questions": questions,
            "contradictions": red_flags,
            "delta": delta,
            "financial_health": financial_health,
        }
    
    def generate_summary_only(self):
        """Generate just the executive summary."""
        if not self.data:
            return "No data available."
        
        context = format_context_for_llm(self.data)
        return call_glm(SYSTEM_PROMPT, EXECUTIVE_SUMMARY, context)


def generate_report():
    """Standalone function to generate report."""
    gen = ReportGenerator()
    return gen.generate_full_report()
