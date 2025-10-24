"""
LLM interaction handler using LangChain and OpenAI — optimized for 2025 releases
and backward-compatible with legacy LangChain versions.
"""

from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# --- Fail-safe imports to cover all LangChain versions ---
try:
    # Legacy (≤ 0.0.331)
    from langchain.prompts import PromptTemplate
    from langchain.chains import LLMChain
    from langchain.schema import HumanMessage, SystemMessage
except ImportError:
    try:
        # Mid-range (0.1.x to <0.3)
        from langchain_core.prompts import PromptTemplate
        from langchain_core.messages import HumanMessage, SystemMessage
        from langchain.chains import LLMChain
    except ImportError:
        # ≥ 0.3.0 — LLMChain deprecated/moved
        from langchain_core.prompts import PromptTemplate
        from langchain_core.messages import HumanMessage, SystemMessage

        class LLMChain:
            """Fallback placeholder class if missing in this LangChain version"""
            def __init__(self, *args, **kwargs):
                pass
            def run(self, *args, **kwargs):
                return None

from typing import Dict, List, Any, Optional
import streamlit as st
from config.prompts import PROMPTS
from config.constants import DEFAULT_MODEL, TEMPERATURE, MAX_TOKENS


class LLMHandler:
    """Central manager for all LLM-based interactions across the platform"""

    def __init__(self):
        """Initialize model and embedding engine"""
        try:
            self.api_key = st.secrets["OPENAI_API_KEY"]
            self.llm = ChatOpenAI(
                model=DEFAULT_MODEL,
                temperature=TEMPERATURE,
                max_tokens=MAX_TOKENS,
                api_key=self.api_key
            )
            self.embeddings = OpenAIEmbeddings(api_key=self.api_key)
        except Exception as e:
            st.error(f"LLM initialization failed: {str(e)}")
            self.llm = None
            self.embeddings = None

    # -------------------------------------------------------------------------
    # Document & Investment Analysis Functions
    # -------------------------------------------------------------------------
    def analyze_document(self, document_content: str, document_type: str = "general") -> str:
        """Run a due diligence or content analysis on uploaded documents"""
        if not self.llm:
            return "LLM not initialized."
        try:
            prompt = PROMPTS.get("document_analysis", "").format(document_content=document_content)
            messages = [
                SystemMessage(content="You are an expert investment analyst."),
                HumanMessage(content=prompt)
            ]
            response = self.llm.invoke(messages)
            return response.content
        except Exception as e:
            st.error(f"Document analysis failed: {str(e)}")
            return f"Error: {str(e)}"

    def generate_financial_summary(self, financial_data: Dict[str, Any]) -> str:
        """Summarize financial datasets"""
        if not self.llm:
            return "LLM not initialized."
        try:
            prompt = PROMPTS.get("financial_summary", "").format(financial_data=str(financial_data))
            messages = [
                SystemMessage(content="You are a financial analyst expert."),
                HumanMessage(content=prompt)
            ]
            response = self.llm.invoke(messages)
            return response.content
        except Exception as e:
            return f"Summary generation failed: {str(e)}"

    def conduct_market_analysis(self, company_name: str, industry: str, market_data: str) -> str:
        """Analyze market, competitors, and positioning"""
        if not self.llm:
            return "LLM not initialized."
        try:
            prompt = PROMPTS.get("market_analysis", "").format(
                company_name=company_name, industry=industry, market_data=market_data
            )
            messages = [
                SystemMessage(content="You are an expert market research consultant."),
                HumanMessage(content=prompt)
            ]
            response = self.llm.invoke(messages)
            return response.content
        except Exception as e:
            return f"Market analysis failed: {str(e)}"

    def assess_risks(self, company_info: Dict, financial_data: Dict, market_context: str) -> str:
        """Perform investment risk assessment"""
        if not self.llm:
            return "LLM not initialized."
        try:
            prompt = PROMPTS.get("risk_assessment", "").format(
                company_info=str(company_info),
                financial_data=str(financial_data),
                market_context=market_context,
            )
            messages = [
                SystemMessage(content="You are an investment risk analyst."),
                HumanMessage(content=prompt)
            ]
            response = self.llm.invoke(messages)
            return response.content
        except Exception as e:
            return f"Risk assessment failed: {str(e)}"

    def generate_investment_memo(self, **kwargs) -> str:
        """AI-generated investment memo (professional format)"""
        if not self.llm:
            return "LLM not initialized."
        try:
            prompt = PROMPTS.get("investment_memo", "").format(**kwargs)
            messages = [
                SystemMessage(content="You are a senior venture partner writing an investment memo."),
                HumanMessage(content=prompt)
            ]
            response = self.llm.invoke(messages)
            return response.content
        except Exception as e:
            return f"Memo generation failed: {str(e)}"

    # -------------------------------------------------------------------------
    # Deal Sourcing & Qualification
    # -------------------------------------------------------------------------
    def qualify_deal(self, deal: Dict[str, Any], criteria: Dict[str, Any]) -> str:
        """Evaluate if a startup meets investment filters (sector, stage, geography)"""
        if not self.llm:
            return "LLM not initialized."
        try:
            prompt = PROMPTS.get("deal_qualification", "").format(
                startup_info=str(deal),
                target_stage=criteria.get("stage_range", "Seed to Series B"),
                target_sector=", ".join(criteria.get("sectors", ["Various"])),
                revenue_range=criteria.get("revenue_range", "$500K–$10M"),
                geography=", ".join(criteria.get("geography", ["Global"]))
            )
            messages = [
                SystemMessage(content="You are a venture analyst assessing startup fit."),
                HumanMessage(content=prompt)
            ]
            response = self.llm.invoke(messages)
            return response.content
        except Exception as e:
            return f"Deal qualification failed: {str(e)}"

    # -------------------------------------------------------------------------
    # Supporting Utility Functions
    # -------------------------------------------------------------------------
    def embed_text(self, text: str) -> List[float]:
        """Generate text embeddings for semantic search or clustering"""
        if not self.embeddings:
            return []
        try:
            return self.embeddings.embed_query(text)
        except Exception as e:
            st.error(f"Embedding generation failed: {str(e)}")
            return []

    def chat_completion(self, messages: List[Dict[str, str]]) -> str:
        """Run general-purpose chat completions"""
        if not self.llm:
            return "LLM not initialized."
        try:
            formatted_messages = [
                SystemMessage(content=m["content"]) if m["role"] == "system"
                else HumanMessage(content=m["content"]) for m in messages
            ]
            response = self.llm.invoke(formatted_messages)
            return response.content
        except Exception as e:
            return f"Chat completion failed: {str(e)}"
