"""
LLM Handler for Investment Analyst AI
Manages OpenAI API calls with error handling and fallbacks
"""
import os
from openai import OpenAI

class LLMHandler:
    """Handles LLM interactions with robust error recovery"""
    
    def __init__(self):
        """Initialize OpenAI client"""
        self.api_key = os.getenv("OPENAI_API_KEY")
        
        if self.api_key:
            try:
                self.client = OpenAI(api_key=self.api_key)
            except Exception as e:
                print(f"OpenAI client initialization error: {e}")
                self.client = None
        else:
            print("Warning: OPENAI_API_KEY not found in environment")
            self.client = None
        
        self.model = "gpt-4"
        self.fallback_model = "gpt-3.5-turbo"
        self.max_tokens = 1500
        self.temperature = 0.7
    
    def generate(self, prompt: str, model: str = None, max_tokens: int = None, temperature: float = None) -> str:
        """
        Generate text using OpenAI API with automatic fallback
        
        Args:
            prompt: The input prompt for the LLM
            model: Optional model override (default: self.model)
            max_tokens: Optional max token override
            temperature: Optional temperature override
        
        Returns:
            Generated text response
        """
        try:
            # Check if client is available
            if not self.client:
                print("LLM client not available, using fallback")
                return self._fallback_response(prompt)
            
            # Use provided parameters or defaults
            selected_model = model or self.model
            tokens = max_tokens or self.max_tokens
            temp = temperature if temperature is not None else self.temperature
            
            # Make API call
            response = self.client.chat.completions.create(
                model=selected_model,
                messages=[
                    {"role": "system", "content": "You are an expert investment analyst with deep knowledge of financial analysis, legal due diligence, operational assessment, and risk management."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=tokens,
                temperature=temp
            )
            
            # Extract and return content
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            print(f"LLM generation error: {str(e)}")
            
            # Try fallback model if primary fails
            if model != self.fallback_model:
                try:
                    print(f"Attempting fallback to {self.fallback_model}")
                    return self.generate(prompt, model=self.fallback_model, max_tokens=max_tokens, temperature=temperature)
                except Exception as fallback_error:
                    print(f"Fallback model also failed: {fallback_error}")
            
            # Return structured fallback response
            return self._fallback_response(prompt)
    
    def _fallback_response(self, prompt: str) -> str:
        """
        Provide intelligent fallback response when API fails
        
        Args:
            prompt: Original prompt to determine response type
        
        Returns:
            Context-appropriate fallback message
        """
        prompt_lower = prompt.lower()
        
        # Financial analysis
        if "financial" in prompt_lower or "revenue" in prompt_lower or "profitability" in prompt_lower:
            return """**Financial Analysis (Manual Review Required)**

Due to API unavailability, please conduct manual analysis focusing on:

1. **Revenue Trends**: Analyze year-over-year growth rates, revenue composition, and sustainability
2. **Profitability Metrics**: Review gross margin, EBITDA, and net profit trends
3. **Cash Flow**: Assess operating cash flow, free cash flow, and cash conversion cycle
4. **Liquidity Position**: Evaluate current ratio, quick ratio, and working capital
5. **Leverage Ratios**: Examine debt-to-equity, interest coverage, and debt service capacity
6. **Red Flags**: Identify negative trends, inconsistencies, or concerning patterns

Recommend engaging financial advisor for detailed assessment."""

        # Legal analysis
        elif "legal" in prompt_lower or "compliance" in prompt_lower or "corporate" in prompt_lower:
            return """**Legal & Compliance Review (Manual Review Required)**

Please review the following areas manually:

1. **Corporate Structure**: Verify legal entity structure, ownership, and governance
2. **Regulatory Compliance**: Check licensing, permits, and regulatory standings
3. **Legal Proceedings**: Identify ongoing or potential litigation, disputes, or claims
4. **Intellectual Property**: Review patents, trademarks, copyrights, and IP ownership
5. **Contractual Obligations**: Assess key contracts, commitments, and liabilities
6. **Compliance Risks**: Evaluate regulatory exposure and compliance gaps

Recommend engaging legal counsel for comprehensive due diligence."""

        # Operational analysis
        elif "operational" in prompt_lower or "operations" in prompt_lower or "business model" in prompt_lower:
            return """**Operational Assessment (Manual Review Required)**

Conduct manual evaluation of:

1. **Business Model**: Analyze value proposition, revenue model, and scalability
2. **Supply Chain**: Review supplier relationships, logistics, and inventory management
3. **Technology & Systems**: Assess IT infrastructure, systems, and digital capabilities
4. **Human Resources**: Evaluate team structure, key personnel, and talent retention
5. **Operational Efficiency**: Review KPIs, productivity metrics, and cost structure
6. **Scalability Potential**: Assess growth capacity and operational constraints

Recommend operational audit for detailed insights."""

        # Risk assessment
        elif "risk" in prompt_lower or "risks" in prompt_lower:
            return """**Risk Assessment (Manual Review Required)**

Key risk categories to evaluate:

1. **Market Risks**: Competition, market dynamics, customer concentration
2. **Financial Risks**: Cash flow volatility, leverage, liquidity constraints
3. **Operational Risks**: Process failures, supply chain disruption, key person dependency
4. **Regulatory Risks**: Compliance exposure, regulatory changes, legal liabilities
5. **Strategic Risks**: Business model viability, technology obsolescence, competitive threats
6. **Overall Risk Rating**: Classify as Low / Medium / High based on aggregate assessment

Recommend comprehensive risk workshop with stakeholders."""

        # AML/KYC screening
        elif "aml" in prompt_lower or "kyc" in prompt_lower or "sanctions" in prompt_lower or "pep" in prompt_lower:
            return """**AML/KYC Screening (External Verification Required)**

Manual screening required for:

1. **Sanctions Lists**: Check OFAC SDN, EU sanctions, UN sanctions lists
2. **PEP (Politically Exposed Persons)**: Screen key individuals and beneficial owners
3. **FATCA Compliance**: Verify entity classification and GIIN status (if applicable)
4. **Adverse Media**: Conduct negative news screening across reputable sources
5. **Enhanced Due Diligence**: Required if high-risk jurisdiction or PEP connections identified
6. **Compliance Status**: Document findings and risk classification

Recommend engaging compliance specialist for thorough screening."""

        # Recommendations
        elif "recommend" in prompt_lower or "recommendation" in prompt_lower:
            return """**Investment Recommendation (Pending Detailed Analysis)**

**Preliminary Assessment:**
- Comprehensive due diligence required before final recommendation
- Key data points need verification through manual review
- Stakeholder consultations recommended

**Next Steps:**
1. Complete financial, legal, and operational due diligence
2. Conduct management interviews and site visits
3. Validate key assumptions and projections
4. Engage external advisors (legal, financial, technical)
5. Present findings to investment committee

**Final Recommendation:** Pending completion of above steps."""

        # Generic fallback
        else:
            return """**Analysis Pending (API Temporarily Unavailable)**

The AI analysis service is currently unavailable. Please proceed with manual review of uploaded documents and conduct traditional due diligence processes.

**Recommended Actions:**
- Review all uploaded documentation thoroughly
- Engage subject matter experts (financial, legal, operational)
- Conduct stakeholder interviews
- Verify all claims and assumptions independently
- Document findings in standard due diligence format

For urgent analysis needs, please contact your AI support team or proceed with manual workflows."""
    
    def analyze_financial(self, text: str, company_name: str) -> str:
        """Specialized method for financial analysis"""
        prompt = f"""Analyze the financial health and performance of {company_name} based on the following data:

{text[:8000]}

Provide a comprehensive financial analysis covering:
1. Revenue trends and growth trajectory
2. Profitability metrics (gross margin, EBITDA, net margin)
3. Cash flow and liquidity position
4. Asset quality and leverage ratios
5. Key financial ratios (ROE, ROA, debt-to-equity)
6. Red flags or concerns
7. Overall financial health assessment

Be specific with numbers, dates, and quantitative metrics where available."""
        
        return self.generate(prompt)
    
    def analyze_legal(self, text: str, company_name: str) -> str:
        """Specialized method for legal analysis"""
        prompt = f"""Review legal and compliance aspects for {company_name}:

{text[:8000]}

Cover the following areas:
1. Corporate structure and governance
2. Regulatory compliance status
3. Legal proceedings, disputes, or litigation
4. Intellectual property portfolio
5. Contractual obligations and commitments
6. Compliance risks and exposure

Provide clear assessment of legal risks and concerns."""
        
        return self.generate(prompt)
    
    def analyze_operations(self, text: str, company_name: str) -> str:
        """Specialized method for operational analysis"""
        prompt = f"""Assess operational capabilities of {company_name}:

{text[:8000]}

Analyze:
1. Business model and revenue operations
2. Supply chain and distribution channels
3. Technology infrastructure and systems
4. Human resources and management team
5. Operational efficiency and KPIs
6. Scalability potential and constraints

Provide actionable insights on operational strengths and weaknesses."""
        
        return self.generate(prompt)
    
    def assess_risks(self, text: str, company_name: str) -> str:
        """Specialized method for risk assessment"""
        prompt = f"""Conduct comprehensive risk assessment for {company_name}:

{text[:8000]}

Identify and evaluate:
1. Market and competitive risks
2. Financial and liquidity risks
3. Operational and execution risks
4. Regulatory and legal risks
5. Strategic and business model risks
6. Overall risk rating (Low/Medium/High)

Prioritize risks by severity and likelihood."""
        
        return self.generate(prompt)
    
    def screen_aml(self, text: str, company_name: str) -> str:
        """Specialized method for AML/KYC screening"""
        prompt = f"""Perform AML/KYC screening for {company_name}:

{text[:4000]}

Check for:
- OFAC SDN list concerns
- EU/UN sanctions exposure
- High-risk jurisdiction connections
- PEP (Politically Exposed Persons) indicators
- FATCA compliance status
- Adverse media or negative press

Provide compliance screening status and risk classification."""
        
        return self.generate(prompt, max_tokens=1000)
