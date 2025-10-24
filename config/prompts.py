"""
LLM Prompts for various analysis tasks
"""

PROMPTS = {
    'document_analysis': """You are an expert investment analyst conducting due diligence.

Analyze the following document and provide:
1. Key highlights and important findings
2. Financial metrics and data points
3. Risk factors and red flags
4. Opportunities and strengths
5. Recommendations for further investigation

Document content:
{document_content}

Provide a structured analysis in markdown format.""",

    'financial_summary': """Analyze the following financial data and provide a comprehensive summary.

Financial Data:
{financial_data}

Include:
- Revenue trends and growth rates
- Profitability metrics (gross margin, EBITDA, net income)
- Key ratios (P/E, ROE, ROA, debt-to-equity)
- Cash flow analysis
- Notable items or concerns

Format your response as a professional financial summary.""",

    'market_analysis': """Conduct a market analysis based on the following information:

Company: {company_name}
Industry: {industry}
Market Data: {market_data}

Provide:
1. Market size and growth trends
2. Competitive landscape overview
3. Market positioning and differentiation
4. Industry dynamics and trends
5. Opportunities and threats

Structure your analysis professionally.""",

    'risk_assessment': """Evaluate investment risks for the following opportunity:

Company Information:
{company_info}

Financial Data:
{financial_data}

Market Context:
{market_context}

Identify and assess:
1. Business risks (operational, strategic, execution)
2. Financial risks (liquidity, leverage, profitability)
3. Market risks (competition, demand, regulation)
4. Overall risk rating (Low/Medium/High)
5. Risk mitigation strategies

Provide a detailed risk assessment report.""",

    'investment_memo': """Generate a professional investment memo based on the following analysis:

Company: {company_name}
Investment Size: {investment_size}
Valuation: {valuation}

Analysis Summary:
{analysis_summary}

Financial Data:
{financial_data}

Market Analysis:
{market_analysis}

Risk Assessment:
{risk_assessment}

Create a comprehensive investment memo with the following sections:
1. Executive Summary
2. Investment Thesis
3. Company Overview
4. Market Opportunity
5. Financial Analysis
6. Competitive Position
7. Risk Factors
8. Valuation Analysis
9. Investment Recommendation

Use professional language and formatting.""",

    'deal_qualification': """Evaluate if this startup meets investment criteria:

Startup Information:
{startup_info}

Investment Criteria:
- Stage: {target_stage}
- Sector: {target_sector}
- Revenue Range: {revenue_range}
- Geography: {geography}

Provide:
1. Qualification status (Qualified/Not Qualified/Needs Review)
2. Matching criteria
3. Missing information
4. Red flags or concerns
5. Recommendation for next steps""",

    'competitive_analysis': """Analyze the competitive landscape for:

Company: {company_name}
Competitors: {competitors}
Market Data: {market_data}

Provide:
1. Competitive positioning matrix
2. Strengths vs competitors
3. Weaknesses vs competitors
4. Differentiation factors
5. Competitive threats
6. Strategic recommendations""",

    'scenario_planning': """Generate financial scenarios based on:

Base Case Assumptions:
{base_assumptions}

Variables to Test:
{variables}

Create three scenarios (Bull/Base/Bear) and provide:
1. Revenue projections (5 years)
2. Margin assumptions
3. Cash flow forecasts
4. Key value drivers
5. Probability-weighted outcomes
6. Sensitivity analysis"""
}

# Prompt templates for specific document types
DOCUMENT_TYPE_PROMPTS = {
    'financial_statement': """Extract and analyze key metrics from this financial statement:
    
{content}

Extract:
- Revenue and revenue growth
- Cost structure and margins
- Operating expenses
- EBITDA and net income
- Cash flow components
- Balance sheet highlights
- Key ratios""",

    'legal_document': """Review this legal document for investment due diligence:
    
{content}

Identify:
- Key terms and conditions
- Rights and obligations
- Risk factors and liabilities
- Unusual or concerning clauses
- Material provisions
- Red flags or deal breakers""",

    'market_report': """Summarize insights from this market report:
    
{content}

Extract:
- Market size and growth
- Key trends and drivers
- Competitive dynamics
- Opportunities and threats
- Relevant data points and statistics"""
}
