"""
LLM Handler - Unified interface for all LLM calls
"""
import os
from typing import Optional
import openai

class LLMHandler:
    """Handles all LLM interactions with fallback logic"""
    
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "")
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY", "")
        
        if self.openai_api_key:
            openai.api_key = self.openai_api_key
    
    def generate(self, prompt: str, model: str = "gpt-3.5-turbo", max_tokens: int = 2000, temperature: float = 0.7) -> str:
        """
        Generate text using OpenAI API
        
        Args:
            prompt: The prompt to send to the model
            model: Model to use (gpt-3.5-turbo, gpt-4, etc.)
            max_tokens: Maximum tokens in response
            temperature: Creativity level (0-1)
        
        Returns:
            Generated text
        """
        try:
            if not self.openai_api_key:
                return self._generate_mock_response(prompt)
            
            response = openai.ChatCompletion.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are an expert investment analyst providing detailed market and financial analysis."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=temperature,
                timeout=60
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            print(f"OpenAI Error: {str(e)}")
            return self._generate_mock_response(prompt)
    
    def _generate_mock_response(self, prompt: str) -> str:
        """Generate mock response when API is unavailable"""
        
        if "market size" in prompt.lower():
            return f"""
## Market Size & Growth Analysis

### Total Addressable Market (TAM)
Based on the analysis, the estimated TAM is approximately $2.5-3.2 billion, with expected compound annual growth rate (CAGR) of 18-22% through 2028.

### Market Segments
1. **Premium Segment** (40% market share): High-value customers, $1.2B
2. **Mid-Market Segment** (35% market share): Growing segment, $1.0B  
3. **SME Segment** (25% market share): Emerging opportunities, $0.8B

### Growth Drivers
- Digital transformation initiatives
- Regulatory compliance requirements
- Cloud migration acceleration
- Increased focus on operational efficiency

### Market Maturity
The market is in **Growth Phase** (Years 3-5 of typical 10-year cycle), with:
- High customer acquisition velocity
- Moderate churn rates (8-12%)
- Strong pricing power
- Increasing competitive intensity
"""
        
        elif "competitive" in prompt.lower():
            return f"""
## Competitive Landscape Analysis

### Major Competitors
1. **Market Leader A** - 28% market share, $700M revenue
2. **Market Leader B** - 22% market share, $550M revenue
3. **Emerging Player C** - 12% market share, $300M revenue
4. **Target Company** - Estimated 2-3% market share

### Competitive Positioning
- **Pricing Strategy**: Premium positioning at 15% above market average
- **Product Differentiation**: AI-powered features, superior UX
- **Go-to-Market**: Direct sales + channel partnerships
- **Customer Concentration**: Top 10 customers = 35% of revenue

### Market Threats
- Price compression from new entrants
- Technology disruption risks
- Talent acquisition challenges
- Regulatory changes
"""
        
        elif "swot" in prompt.lower():
            return f"""
## SWOT Analysis

### Strengths
- Strong founding team with industry experience
- Proprietary technology and IP
- Excellent customer retention (92%)
- Sustainable unit economics

### Weaknesses
- Limited brand awareness in some markets
- High customer acquisition costs
- Smaller scale vs. competitors
- Limited geographic presence

### Opportunities
- Expansion into adjacent markets
- International expansion (APAC, Europe)
- Strategic partnerships
- M&A consolidation play

### Threats
- Aggressive competition from well-funded players
- Economic downturn impact
- Talent market competition
- Regulatory changes
"""
        
        elif "trend" in prompt.lower():
            return f"""
## Market Trends & Drivers

### Key Industry Trends
1. **Digital-First Adoption** - 72% of enterprises prioritizing digital transformation
2. **AI Integration** - 65% of companies planning AI investments
3. **Cloud Migration** - Continued shift to cloud infrastructure (40% CAGR)
4. **Sustainability Focus** - Growing importance of ESG criteria in purchasing

### Market Drivers
- Rising operational costs driving efficiency focus
- Talent shortage accelerating automation
- Regulatory compliance requirements
- Customer demand for innovation
- Post-pandemic digital acceleration

### Forecast
- Market expected to reach $4.2B by 2028
- Continued consolidation among players
- Rise of specialized solution providers
- Increased focus on vertical markets
"""
        
        elif "porter" in prompt.lower():
            return f"""
## Porter's Five Forces Analysis

### 1. Threat of New Entrants: MEDIUM
- Moderate barriers to entry
- Capital requirements: $5-10M to achieve scale
- Technology barriers mitigating factor
- Incumbent advantages in customer relationships

### 2. Bargaining Power of Buyers: MEDIUM
- Buyers have moderate switching costs
- Multiple vendors available
- Price sensitivity varies by segment
- Long-term contracts lock in customers

### 3. Threat of Substitutes: MEDIUM
- Alternative solutions exist
- Substitution rate: 8-12% annually
- Service differentiation reduces threat
- Integration benefits create stickiness

### 4. Bargaining Power of Suppliers: LOW
- Diverse technology suppliers
- Low supplier concentration
- High competition among vendors
- Ability to vertically integrate

### 5. Industry Rivalry: HIGH
- Increasing competitive intensity
- Differentiation critical for survival
- Price-based competition emerging
- M&A consolidation underway

**Overall Industry Attractiveness: MODERATE** - Good margins but increasing competition
"""
        
        elif "customer" in prompt.lower():
            return f"""
## Customer Segmentation Analysis

### Segment 1: Enterprise Customers (35% of revenue)
- Avg. Deal Size: $500K-2M
- Implementation Timeline: 6-9 months
- Churn Rate: 3-5%
- Key Decision Makers: C-suite, IT/Ops heads
- Pain Points: Compliance, scalability

### Segment 2: Mid-Market (45% of revenue)
- Avg. Deal Size: $50K-300K
- Implementation Timeline: 2-4 months
- Churn Rate: 8-12%
- Key Decision Makers: Department heads, project managers
- Pain Points: Cost efficiency, ease of use

### Segment 3: SMB (20% of revenue)
- Avg. Deal Size: $5K-50K
- Implementation Timeline: 1-2 weeks
- Churn Rate: 15-20%
- Key Decision Makers: Founders, operations
- Pain Points: Affordability, simplicity

### Recommendations
- Expand enterprise segment (higher LTV)
- Develop self-serve model for SMB
- Create vertical-specific solutions
"""
        
        elif "regulatory" in prompt.lower():
            return f"""
## Regulatory Environment Assessment

### Primary Regulatory Frameworks
1. **Data Protection & Privacy**
   - GDPR compliance required for EU customers
   - CCPA compliance for US West Coast
   - Local data residency requirements

2. **Financial Services** (if applicable)
   - SOC 2 Type II certification
   - Financial crime compliance
   - Risk management frameworks

3. **Industry-Specific**
   - Healthcare: HIPAA compliance
   - Financial: PCI-DSS standards
   - Government: FedRAMP certification

### Compliance Status
- Current certifications: SOC 2 Type II, ISO 27001
- Audit frequency: Annual
- Compliance costs: $200-300K annually
- Timeline to new regulation: 6-12 months

### Risk Assessment: LOW-MEDIUM
- Regulatory environment stable in key markets
- Compliance investments create competitive moat
- Potential for tighter regulations in future
"""
        
        else:
            return f"""
## Analysis Report

Based on comprehensive review of the provided information:

### Executive Summary
This analysis examines key aspects of market positioning, competitive dynamics, and growth opportunities.

### Key Findings
1. Strong market fundamentals with 18-22% annual growth
2. Competitive differentiation through innovation and service quality
3. Multiple expansion opportunities in adjacent markets
4. Risk mitigation through diversified customer base

### Recommendations
1. **Strategic**: Prioritize high-margin segments for growth
2. **Operational**: Invest in AI/automation capabilities
3. **Commercial**: Expand through strategic partnerships
4. **Financial**: Optimize unit economics and CAC payback

### Next Steps
- Conduct detailed competitive analysis
- Develop market expansion roadmap
- Establish KPI tracking framework
- Build 3-year growth projection model
"""
    
    def generate_structured(self, prompt: str, output_format: dict) -> dict:
        """Generate structured output (JSON)"""
        try:
            response_text = self.generate(prompt, max_tokens=3000)
            return {"status": "success", "data": response_text}
        except Exception as e:
            return {"status": "error", "data": str(e)}
