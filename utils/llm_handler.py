"""
LLM Handler for Investment Analyst AI
Manages OpenAI API calls with error handling and fallbacks
"""
from openai import OpenAI
import os

class LLMHandler:
    """Handles LLM interactions with error recovery"""
    
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key) if self.api_key else None
        self.model = "gpt-4"
        self.fallback_model = "gpt-3.5-turbo"
    
    def generate(self, prompt: str, model: str = None) -> str:
        """
        Generate text using OpenAI API with fallback
        """
        try:
            if not self.client:
                return self._fallback_response(prompt)
            
            selected_model = model or self.model
            
            response = self.client.chat.completions.create(
                model=selected_model,
                messages=[
                    {"role": "system", "content": "You are an expert investment analyst."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.7
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            print(f"LLM Error: {str(e)}")
            return self._fallback_response(prompt)
    
    def _fallback_response(self, prompt: str) -> str:
        """
        Provide fallback response when API fails
        """
        if "financial" in prompt.lower():
            return "Financial analysis pending - API temporarily unavailable. Recommend manual review of revenue trends, profitability margins, and cash position from uploaded documents."
        
        elif "legal" in prompt.lower():
            return "Legal assessment pending - Please review corporate structure, compliance status, and any litigation from provided documentation."
        
        elif "operational" in prompt.lower():
            return "Operational review pending - Analyze business model efficiency, team structure, and supply chain from uploaded materials."
        
        elif "risk" in prompt.lower():
            return "Risk assessment pending - Identify market, financial, operational, and regulatory risks from available data."
        
        elif "aml" in prompt.lower():
            return "AML screening pending - Conduct sanctions check and PEP screening using external databases."
        
        else:
            return "Analysis pending - Manual review recommended for comprehensive assessment."
