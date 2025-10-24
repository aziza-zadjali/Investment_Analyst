"""
LLM interaction handler using LangChain and OpenAI
"""

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.schema import HumanMessage, SystemMessage
from typing import Dict, List, Any, Optional
import streamlit as st
from config.prompts import PROMPTS
from config.constants import DEFAULT_MODEL, TEMPERATURE, MAX_TOKENS

class LLMHandler:
    """Handle all LLM interactions"""
    
    def __init__(self):
        """Initialize LLM with API key from secrets"""
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
            st.error(f"Failed to initialize LLM: {str(e)}")
            self.llm = None
            self.embeddings = None
    
    def analyze_document(self, document_content: str, document_type: str = "general") -> str:
        """Analyze document using appropriate prompt"""
        if not self.llm:
            return "LLM not initialized. Please check API key."
        
        try:
            prompt = PROMPTS.get('document_analysis', '').format(
                document_content=document_content
            )
            
            messages = [
                SystemMessage(content="You are an expert investment analyst."),
                HumanMessage(content=prompt)
            ]
            
            response = self.llm.invoke(messages)
            return response.content
            
        except Exception as e:
            st.error(f"Error analyzing document: {str(e)}")
            return f"Analysis failed: {str(e)}"
    
    def generate_financial_summary(self, financial_data: Dict[str, Any]) -> str:
        """Generate financial summary from data"""
        if not self.llm:
            return "LLM not initialized."
        
        try:
            prompt = PROMPTS.get('financial_summary', '').format(
                financial_data=str(financial_data)
            )
            
            messages = [
                SystemMessage(content="You are a financial analyst expert."),
                HumanMessage(content=prompt)
            ]
            
            response = self.llm.invoke(messages)
            return response.content
            
        except Exception as e:
            return f"Summary generation failed: {str(e)}"
    
    def conduct_market_analysis(self, company_name: str, industry: str, market_data: str) -> str:
        """Conduct market analysis"""
        if not self.llm:
            return "LLM not initialized."
        
        try:
            prompt = PROMPTS.get('market_analysis', '').format(
                company_name=company_name,
                industry=industry,
                market_data=market_data
            )
            
            messages = [
                SystemMessage(content="You are a market research analyst."),
                HumanMessage(content=prompt)
            ]
            
            response = self.llm.invoke(messages)
            return response.content
            
        except Exception as e:
            return f"Market analysis failed: {str(e)}"
    
    def assess_risks(self, company_info: Dict, financial_data: Dict, market_context: str) -> str:
        """Assess investment risks"""
        if not self.llm:
            return "LLM not initialized."
        
        try:
            prompt = PROMPTS.get('risk_assessment', '').format(
                company_info=str(company_info),
                financial_data=str(financial_data),
                market_context=market_context
            )
            
            messages = [
                SystemMessage(content="You are a risk assessment expert."),
                HumanMessage(content=prompt)
            ]
            
            response = self.llm.invoke(messages)
            return response.content
            
        except Exception as e:
            return f"Risk assessment failed: {str(e)}"
    
    def generate_investment_memo(self, **kwargs) -> str:
        """Generate complete investment memo"""
        if not self.llm:
            return "LLM not initialized."
        
        try:
            prompt = PROMPTS.get('investment_memo', '').format(**kwargs)
            
            messages = [
                SystemMessage(content="You are a senior investment professional drafting a memo."),
                HumanMessage(content=prompt)
            ]
            
            response = self.llm.invoke(messages)
            return response.content
            
        except Exception as e:
            return f"Memo generation failed: {str(e)}"
    
    def qualify_deal(self, startup_info: Dict, criteria: Dict) -> str:
        """Qualify deal against investment criteria"""
        if not self.llm:
            return "LLM not initialized."
        
        try:
            prompt = PROMPTS.get('deal_qualification', '').format(
                startup_info=str(startup_info),
                **criteria
            )
            
            messages = [
                SystemMessage(content="You are a deal sourcing analyst."),
                HumanMessage(content=prompt)
            ]
            
            response = self.llm.invoke(messages)
            return response.content
            
        except Exception as e:
            return f"Deal qualification failed: {str(e)}"
    
    def embed_text(self, text: str) -> List[float]:
        """Generate embeddings for text"""
        if not self.embeddings:
            return []
        
        try:
            return self.embeddings.embed_query(text)
        except Exception as e:
            st.error(f"Embedding generation failed: {str(e)}")
            return []
    
    def chat_completion(self, messages: List[Dict[str, str]]) -> str:
        """General chat completion"""
        if not self.llm:
            return "LLM not initialized."
        
        try:
            formatted_messages = [
                SystemMessage(content=msg['content']) if msg['role'] == 'system' 
                else HumanMessage(content=msg['content'])
                for msg in messages
            ]
            
            response = self.llm.invoke(formatted_messages)
            return response.content
            
        except Exception as e:
            return f"Chat completion failed: {str(e)}"
