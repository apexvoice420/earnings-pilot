import anthropic
from src.config import ANTHROPIC_API_KEY
from src.vector_store import get_store
from src.prompts import EXECUTIVE_SUMMARY, ANALYST_QUESTIONS, CONTRADICTION_FINDER

class ReportGenerator:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        self.store = get_store()

    def generate_section(self, prompt_template, context_query):
        if not ANTHROPIC_API_KEY:
            return "Anthropic API Key missing. Cannot generate report."

        # Retrieve relevant chunks
        results = self.store.search(context_query, k=8)
        context = "\n".join(results['documents'][0])
        
        full_prompt = f"Context:\n{context}\n\nTask: {prompt_template}"
        
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=2000,
            messages=[
                {"role": "user", "content": full_prompt}
            ]
        )
        
        return response.content[0].text

    def generate_report(self):
        report = {}
        
        print("Generating Executive Summary...")
        report['summary'] = self.generate_section(EXECUTIVE_SUMMARY, "financial highlights and risk tone")
        
        print("Generating Analyst Questions...")
        report['questions'] = self.generate_section(ANALYST_QUESTIONS, "tough analyst questions and risks")
        
        print("Generating Contradictions...")
        report['contradictions'] = self.generate_section(CONTRADICTION_FINDER, "risk factors vs management statements")
        
        return report
