"""
LLM interaction handler using LangChain and OpenAI
"""

from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# ✅ Cross-version compatible imports
try:
    # Legacy (≤ 0.0.331)
    from langchain.prompts import PromptTemplate
    from langchain.chains import LLMChain
    from langchain.schema import HumanMessage, SystemMessage
except ImportError:
    try:
        # Mid-era (~ 0.1 – 0.2)
        from langchain_core.prompts import PromptTemplate
        from langchain_core.messages import HumanMessage, SystemMessage
        from langchain.chains import LLMChain
    except ImportError:
        # Latest (≥ 0.3.x)
        from langchain_core.prompts import PromptTemplate
        from langchain_core.messages import HumanMessage, SystemMessage

        # Define fallback dummy LLMChain to avoid ImportError
        class LLMChain:
            def __init__(self, *args, **kwargs):
                pass
            def run(self, *args, **kwargs):
                return None

from typing import Dict, List, Any, Optional
import streamlit as st
from config.prompts import PROMPTS
from config.constants import DEFAULT_MODEL, TEMPERATURE, MAX_TOKENS


class LLMHandler:
    """Handle all LLM interactions"""

    def __init__(self):
        """Initialize LLM with API key from Streamlit secrets"""
        try:
            self.api_key = st.secrets["OPENAI_API_KEY"]
            self.llm = ChatOpenAI(
                model=DEFAULT_MODEL,
                temperature=TEMPERATURE,
                max_tokens=MAX_TOKENS,
                api_key=self.api_key,
            )
            self.embeddings = OpenAIEmbeddings(api_key=self.api_key)
        except Exception as e:
            st.error(f"Failed to initialize LLM: {str(e)}")
            self.llm = None
            self.embeddings = None

    def analyze_document(self, document_content: str, document_type: str = "general") -> str:
        """Analyze document using an analyst prompt"""
        if not self.llm:
            return "LLM not initialized. Please check API key."

        try:
            prompt = PROMPTS.get("document_analysis", "").format(
                document_content=document_content
            )
            messages = [
                SystemMessage(content="You are an expert investment analyst."),
                HumanMessage(content=prompt),
            ]
            response = self.llm.invoke(messages)
            return response.content
        except Exception as e:
            st.error(f"Error analyzing document: {str(e)}")
            return f"Analysis failed: {str(e)}"

    def generate_financial_summary(self, financial_data: Dict[str, Any]) -> str:
        """Generate financial summary from structured data"""
        if not self.llm:
            return "LLM not initialized."

        try:
            prompt = PROMPTS.get("financial_summary", "").format(
                financial_data=str(financial_data)
            )
            messages = [
                SystemMessage(content="You are a financial analyst expert."),
                HumanMessage(content=prompt),
            ]
            response = self.llm.invoke(messages)
            return response.content
        except Exception as e:
            return f"Summary generation failed: {str(e)}"

    def conduct_market_analysis(self, company_name: str, industry: str, market_data: str) -> str:
        """Conduct a detailed market analysis"""
        if not self.llm:
            return "LLM not initialized."

        try:
            prompt = PROMPTS.get("market_analysis", "").format(
                company_name=company_name,
                industry=industry,
                market_data=market_data,
            )
            messages = [
                SystemMessage(content="You are a market research analyst."),
                HumanMessage(content=prompt),
            ]
            response = self.llm.invoke(messages)
            return response.content
        except Exception as e:
            return f"Market analysis failed: {str(e)}"

    def assess_risks(self, company_info: Dict, financial_data: Dict, market_context: str) -> str:
        """Perform comprehensive risk assessment"""
        if not self.llm:
            return "LLM not initialized."

        try:
            prompt = PROMPTS.get("risk_assessment", "").format(
                company_info=str(company_info),
                financial_data=str(financial_data),
                market_context=market_context,
            )
            messages = [
                SystemMessage(content="You are a risk assessment expert."),
                HumanMessage(content=prompt),
            ]
            response = self.llm.invoke(messages)
            return response.content
        except Exception as e:
            return f"Risk assessment failed: {str(e)}"

    def generate_investment_memo(self, **kwargs) -> str:
        """Generate a structured investment memo"""
        if not self.llm:
            return "LLM not initialized."

        try:
            prompt = PROMPTS.get("investment_memo", "").format(**kwargs)
            messages = [
                SystemMessage(
                    content="You are a senior investment professional drafting a detailed investment memo."
                ),
                HumanMessage(content=prompt),
            ]
            response = self.llm.invoke(messages)
            return response.content
        except Exception as e:
            return f"Memo generation failed: {str(e)}"

    def embed_text(self, text: str) -> List[float]:
        """Generate vector embeddings for text"""
        if not self.embeddings:
            return []
        try:
            return self.embeddings.embed_query(text)
        except Exception as e:
            st.error(f"Embedding generation failed: {str(e)}")
            return []

    def chat_completion(self, messages: List[Dict[str, str]]) -> str:
        """Perform a general chat completion task"""
        if not self.llm:
            return "LLM not initialized."

        try:
            formatted_messages = [
                SystemMessage(content=m["content"])
                if m["role"] == "system"
                else HumanMessage(content=m["content"])
                for m in messages
            ]
            response = self.llm.invoke(formatted_messages)
            return response.content
        except Exception as e:
            return f"Chat completion failed: {str(e)}"
