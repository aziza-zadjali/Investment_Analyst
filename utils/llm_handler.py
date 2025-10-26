"""
QDB | Regulus AI – LLM Handler
Unified large‑language‑model utility that powers all analytical pages
(Deal Sourcing, Due Diligence, Market Analysis, Financial Modeling, Investment Memo).
"""

import os
from datetime import datetime
import openai


class LLMHandler:
    """Central AI text generator for the Regulus Analyst Platform."""

    def __init__(self, model_name: str = "gpt-4-turbo", temperature: float = 0.5):
        """
        Initialize the Regulus AI LLM handler.
        Auto‑reads API key, and sets default model for financial analysis tasks.
        """
        self.model_name = model_name
        self.temperature = temperature

        if "OPENAI_API_KEY" not in os.environ:
            raise EnvironmentError(
                "⚠️ Environment variable OPENAI_API_KEY not set. Please configure your OpenAI key."
            )
        openai.api_key = os.getenv("OPENAI_API_KEY")

    # ------------------------------------------------------------------
    # CORE FUNCTION ----------------------------------------------------
    # ------------------------------------------------------------------

    def generate_text(self, prompt: str, max_tokens: int = 900) -> str:
        """
        Generate structured, contextual text for any workflow module.
        Example:
            llm = LLMHandler()
            output = llm.generate_text("Summarize today’s MENA fintech funding activity.")
        """
        try:
            completion = openai.ChatCompletion.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are Regulus AI – a professional investment analyst at Qatar Development Bank (QDB). "
                            "Write clear, concise, structured financial analysis, following institutional tone and report style."
                        ),
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=self.temperature,
                max_tokens=max_tokens,
            )
            return completion.choices[0].message.content.strip()

        except Exception as e:
            return f"⚠️ LLM Error – {str(e)}"

    # ------------------------------------------------------------------
    # SPECIALIZED HELPERS ----------------------------------------------
    # ------------------------------------------------------------------

    def summarize_deals(self, deals: list) -> str:
        """
        Summarize a list of deal dictionaries into AI‑curated highlights.
        Each deal requires: Company, Industry, Stage, Region, and Ticket Size fields.
        """
        if not deals:
            return "No deals available for summary."

        lines = []
        for d in deals:
            company = d.get("Company", "N/A")
            sector = d.get("Industry", "N/A")
            region = d.get("Region", "N/A")
            stage = d.get("Stage", "N/A")
            amount = d.get("Ticket Size (USD M)", "N/A")
            lines.append(f"{company} – {sector} | {region} | Stage: {stage} | Ticket ≈ ${amount} M")
        formatted = "\n".join(lines)

        summary_prompt = (
            f"Below is a list of recent investment opportunities curated by Regulus AI:\n\n{formatted}\n\n"
            "Please summarize in executive form – highlighting key sectors, regional trends, and AI‑based insights."
        )
        return self.generate_text(summary_prompt, max_tokens=800)

    def generate_due_diligence_checklist(self, sector: str) -> str:
        """
        Build a custom due diligence checklist for a specific sector or industry.
        """
        prompt = (
            f"Create a QDB‑style Due Diligence Checklist for the {sector} sector. "
            "Organize sections: Legal, Financial, Operational, Market, and ESG Considerations."
        )
        return self.generate_text(prompt, max_tokens=700)

    def generate_investment_memo(self, company: str, context: str) -> str:
        """
        Generate a compact investment memo for a given company profile.
        """
        memo_prompt = (
            f"Prepare a summary investment memo for {company}. Include:\n\n{context}\n\n"
            "Summarize thesis, risks, and recommendations using Regulus AI’s analytical framework."
        )
        return self.generate_text(memo_prompt, max_tokens=700)
