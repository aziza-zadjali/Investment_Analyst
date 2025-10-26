"""
Regulus AI – LLM Handler
Unified intelligent interface for all LLM-assisted modules (Deal Sourcing, Due Diligence, Market Analysis, etc.)
"""

import os
import openai
from datetime import datetime


class LLMHandler:
    """
    Core LLM Handler for the QDB × Regulus Analyst Platform.
    Provides standardized text generation & summarization utilities.
    """

    def __init__(self, 
                 model_name: str = "gpt-4-turbo",
                 temperature: float = 0.4,
                 system_prompt: str = (
                     "You are Regulus AI, an expert financial analyst working "
                     "for Qatar Development Bank. Your style is concise, "
                     "structured, and analytical."
                 )):
        """
        Initialize the model and environment.
        Reads `OPENAI_API_KEY` from environment variables securely.
        """
        self.model_name = model_name
        self.temperature = temperature
        self.system_prompt = system_prompt

        if "OPENAI_API_KEY" not in os.environ:
            raise EnvironmentError("⚠️ OPENAI_API_KEY is not set in your environment variables.")
        openai.api_key = os.getenv("OPENAI_API_KEY")

    # ----------------------------------------------------------------------
    # PUBLIC METHODS
    # ----------------------------------------------------------------------

    def generate_text(self, user_input: str, max_tokens: int = 800) -> str:
        """
        Generate human‑readable analytical text output for any task.
        Usage example:
            handler = LLMHandler()
            result = handler.generate_text("Summarize Qatar’s SME growth opportunities.")
        """
        try:
            response = openai.ChatCompletion.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_input},
                ],
                temperature=self.temperature,
                max_tokens=max_tokens,
            )
            message = response["choices"][0]["message"]["content"].strip()
            return message

        except Exception as e:
            return f"⚠️ LLM generation error: {str(e)}"

    # ----------------------------------------------------------------------

    def summarize_deals(self, deals: list) -> str:
        """
        Summarize a list of discovered deals into an executive overview.
        Expected deal format:
            [{"Company": ..., "Industry": ..., "Stage": ..., "Region": ...}, ...]
        """
        try:
            if not deals:
                return "No deals available to summarize."

            text_block = "\n".join(
                [f"{d.get('Company','N/A')} – {d.get('Industry','N/A')} "
                 f"({d.get('Stage','N/A')} • {d.get('Region','N/A')})"
                 for d in deals]
            )
            prompt = (
                f"Provide a one‑page executive analysis of the following investment opportunities:\n\n{text_block}\n\n"
                "Highlight potential standouts, macro trends, and risks in a professional tone."
            )
            return self.generate_text(prompt, max_tokens=700)

        except Exception as e:
            return f"⚠️ Summary failed: {e}"

    # ----------------------------------------------------------------------

    def generate_due_diligence_checklist(self, industry: str) -> str:
        """
        Produce a QDB‑standard Due Diligence checklist for a given industry.
        """
        checklist_prompt = (
            f"Generate a concise Due Diligence checklist for investments in the {industry} sector. "
            "Structure under Legal, Financial, Operational, and Market aspects."
        )
        return self.generate_text(checklist_prompt, max_tokens=600)

    # ----------------------------------------------------------------------

    def generate_investment_summary(self, company: str, highlights: str) -> str:
        """
        Create a short investment memo summary for a given company and highlights.
        """
        memo_prompt = (
            f"Prepare an investment summary for {company}. "
            f"Use this information:\n\n{highlights}\n\n"
            "Include key selling points and potential risks in executive tone."
        )
        return self.generate_text(memo_prompt, max_tokens=700)
