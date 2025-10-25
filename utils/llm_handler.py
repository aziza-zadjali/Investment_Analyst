"""
LLM Handler for Investment Analysis
Handles all AI/LLM interactions using LangChain
"""

import os
from typing import Optional
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage


class LLMHandler:
    """Handle LLM interactions for investment analysis"""
    
    def __init__(self, model: str = "gpt-4", temperature: float = 0.7):
        """
        Initialize LLM handler
        
        Args:
            model: OpenAI model to use
            temperature: Temperature for generation (0.0 - 1.0)
        """
        self.model = model
        self.temperature = temperature
        
        # Get API key from environment
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        
        # Initialize ChatOpenAI
        self.llm = ChatOpenAI(
            model=model,
            temperature=temperature,
            api_key=api_key
        )
    
    def generate(self, prompt: str, system_message: Optional[str] = None) -> str:
        """
        Generate text response from LLM
        
        Args:
            prompt: User prompt/question
            system_message: Optional system message to set context
            
        Returns:
            Generated text response
        """
        
        messages = []
        
        # Add system message if provided
        if system_message:
            messages.append(SystemMessage(content=system_message))
        else:
            # Default system message for investment analysis
            messages.append(SystemMessage(content="""You are a professional investment analyst with expertise in due diligence, 
financial analysis, market research, and risk assessment. Provide detailed, accurate, and actionable insights based on the data provided. 
Be specific with numbers, dates, and concrete recommendations. Highlight both opportunities and risks."""))
        
        # Add user prompt
        messages.append(HumanMessage(content=prompt))
        
        try:
            # Generate response
            response = self.llm.invoke(messages)
            return response.content
        
        except Exception as e:
            print(f"Error generating LLM response: {e}")
            return f"Analysis could not be completed due to an error: {str(e)}"
    
    def analyze_document(self, document_text: str, analysis_type: str = "general") -> str:
        """
        Analyze a document with specific focus
        
        Args:
            document_text: Text content of document
            analysis_type: Type of analysis (financial, legal, operational, etc.)
            
        Returns:
            Analysis results
        """
        
        analysis_prompts = {
            "financial": """Analyze the financial aspects of this document:
- Revenue and profitability trends
- Cash flow and liquidity
- Key financial ratios
- Financial risks and concerns
- Overall financial health assessment""",
            
            "legal": """Analyze the legal aspects of this document:
- Corporate structure and governance
- Compliance status
- Legal risks and liabilities
- Contractual obligations
- Regulatory concerns""",
            
            "operational": """Analyze the operational aspects of this document:
- Business model and operations
- Operational efficiency
- Technology and systems
- Human resources
- Scalability assessment""",
            
            "market": """Analyze the market aspects of this document:
- Market size and growth
- Competitive landscape
- Market trends
- Company positioning
- Market opportunities and threats""",
            
            "general": """Provide a comprehensive analysis of this document covering key insights, 
risks, opportunities, and recommendations."""
        }
        
        prompt = f"""{analysis_prompts.get(analysis_type, analysis_prompts['general'])}

Document content:
{document_text[:6000]}

Provide detailed analysis with specific insights."""
        
        return self.generate(prompt)
    
    def compare_documents(self, doc1_text: str, doc2_text: str, comparison_focus: str = "general") -> str:
        """
        Compare two documents
        
        Args:
            doc1_text: First document text
            doc2_text: Second document text
            comparison_focus: What to compare (financials, terms, etc.)
            
        Returns:
            Comparison analysis
        """
        
        prompt = f"""Compare and contrast these two documents focusing on {comparison_focus}:

DOCUMENT 1:
{doc1_text[:3000]}

DOCUMENT 2:
{doc2_text[:3000]}

Provide detailed comparison highlighting:
1. Key similarities
2. Important differences
3. Implications of differences
4. Recommendations"""
        
        return self.generate(prompt)
    
    def summarize(self, text: str, max_length: str = "medium") -> str:
        """
        Summarize text content
        
        Args:
            text: Text to summarize
            max_length: Summary length (short/medium/long)
            
        Returns:
            Summary
        """
        
        length_instructions = {
            "short": "in 3-5 bullet points",
            "medium": "in 1-2 paragraphs with key points",
            "long": "in detailed paragraphs covering all major aspects"
        }
        
        instruction = length_instructions.get(max_length, length_instructions["medium"])
        
        prompt = f"""Summarize the following text {instruction}:

{text[:5000]}

Provide a clear, comprehensive summary."""
        
        return self.generate(prompt)
    
    def extract_key_info(self, text: str, info_type: str) -> str:
        """
        Extract specific information from text
        
        Args:
            text: Source text
            info_type: Type of information to extract
            
        Returns:
            Extracted information
        """
        
        prompt = f"""Extract and list all {info_type} from the following text:

{text[:5000]}

Provide the information in a clear, structured format."""
        
        return self.generate(prompt)
    
    def generate_recommendations(self, analysis_text: str, context: str = "") -> str:
        """
        Generate actionable recommendations based on analysis
        
        Args:
            analysis_text: Analysis results
            context: Additional context
            
        Returns:
            Recommendations
        """
        
        prompt = f"""Based on the following analysis, provide specific, actionable recommendations:

ANALYSIS:
{analysis_text[:4000]}

{f'CONTEXT: {context}' if context else ''}

Provide:
1. Clear recommendation (Proceed/Caution/Decline)
2. Key reasons for recommendation
3. Specific actions to take
4. Risk mitigation strategies
5. Timeline considerations"""
        
        return self.generate(prompt)
