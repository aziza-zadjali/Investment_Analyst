"""
LLM Handler – Regulus AI / QDB Analyst Platform
Unified OpenAI v1.x text generation client.
"""

import os
from openai import OpenAI


class LLMHandler:
    """
    Unified LLM interface for Regulus Analyst app pages
    (Deal Sourcing, Due Diligence, Market Analysis, Financial Modeling, Investment Memo)
    """

    def __init__(
        self,
        model_name: str = "gpt-4o-mini",
        temperature: float = 0.4,
        system_prompt: str = (
            "You are Regulus AI, a specialized financial analyst for Qatar Development Bank. "
            "Your responses must be concise, well‑structured, and insight‑oriented."
        ),
    ):
        """Initialize the OpenAI client and model settings."""
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model_name
        self.temperature = temperature
        self.system_prompt = system_prompt

    # =============================================================
    # CORE METHOD
    # =============================================================
    def generate_text(self, user_input: str, max_tokens: int = 800) -> str:
        """
        Generate structured text output based on a prompt.
        Works with OpenAI Python SDK v1+ responses API.
        """
        try:
            response = self.client.responses.create(
                model=self.model,
                input=[
                    {
                        "role": "system",
                        "content": self.system_prompt,
                    },
                    {
                        "role": "user",
                        "content": user_input,
                    },
                ],
                temperature=self.temperature,
                max_output_tokens=max_tokens,
            )
            # the new API provides output_text instead of choices→text
            return response.output_text.strip()
        except Exception as e:
            return f"⚠️ LLM execution failed: {e}"

    # =============================================================
    # AUXILIARY UTILITIES
    # =============================================================
    def summarize_deals(self, deals: list) -> str:
        """Summarize list of deals in executive paragraph form."""
        if not deals:
            return "No deals available for summary."
        listings = "\n".join(
            [
                f"{d.get('Company','N/A')} – {d.get('Industry','N/A')} "
                f"({d.get('Stage','N/A')}, {d.get('Region','N/A')})"
                for d in deals
            ]
        )
        prompt = (
            f"Summarize the following {len(deals)} startup opportunities. "
            "Highlight sector patterns, regional trends, and investment risks:\n\n"
            f"{listings}"
        )
        return self.generate_text(prompt, max_tokens=700)

    def generate_due_diligence_checklist(self, sector: str) -> str:
        """Generate a custom due‑diligence checklist by sector."""
        prompt = (
            f"Prepare a QDB‑style Due Diligence Checklist for the {sector} sector. "
            "Organize under Legal, Financial, Operational, and Market sections."
        )
        return self.generate_text(prompt, max_tokens=600)

    def generate_investment_summary(self, company: str, highlights: str) -> str:
        """Compose a brief investment summary for a given company."""
        prompt = (
            f"Create an investment summary for {company}. "
            f"Use these highlights:\n{highlights}\n\n"
            "Include key investment thesis, risks, and recommendations."
        )
        return self.generate_text(prompt, max_tokens=700)
