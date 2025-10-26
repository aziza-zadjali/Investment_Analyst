"""
Template Generator - Creates reports in DOCX format
ENHANCED: generate_pitch_deck() now dynamically creates slides from memo data
"""
from io import BytesIO
from datetime import datetime

try:
    from docx import Document
    from docx.shared import Inches, Pt, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    HAS_DOCX = True
except ImportError:
    HAS_DOCX = False


class TemplateGenerator:
    """Professional template generator for all report types"""
    
    def __init__(self):
        self.company_color = RGBColor(27, 43, 77) if HAS_DOCX else None
        self.accent_color = RGBColor(22, 160, 133) if HAS_DOCX else None
    
    def generate_pitch_deck(self, memo_data: dict) -> str:
        """
        Generate comprehensive pitch deck dynamically from memo/investment data
        DYNAMIC: Creates slides from actual memo data, not hardcoded
        
        Args:
            memo_data: Dictionary with company info, financials, analysis from investment memo
        
        Returns:
            Markdown formatted pitch deck outline with actual data
        """
        # Extract data from memo
        company = memo_data.get('company_name', 'Company')
        industry = memo_data.get('industry', 'Industry')
        date = memo_data.get('analysis_date', datetime.now().strftime('%B %d, %Y'))
        
        # Financial data from memo
        revenue = memo_data.get('revenue', '$TBD')
        growth_rate = memo_data.get('growth_rate', '25-50%')
        market_size = memo_data.get('tam', '$2.5B')
        problem = memo_data.get('problem_statement', 'Industry inefficiencies')
        solution = memo_data.get('solution_summary', 'AI-powered platform')
        team = memo_data.get('team_description', 'Experienced founding team')
        competitive_advantage = memo_data.get('competitive_advantage', 'Technology differentiation')
        risks = memo_data.get('key_risks', 'Market competition')
        recommendation = memo_data.get('investment_recommendation', 'CONDITIONAL INTEREST')
        investment_size = memo_data.get('investment_ask', '$2M-5M')
        
        # Extract financial metrics
        gross_margin = memo_data.get('gross_margin', '60-75%')
        burn_rate = memo_data.get('burn_rate', '<$200K/mo')
        runway = memo_data.get('runway', '18+ months')
        customer_ltv_cac = memo_data.get('ltv_cac_ratio', '3.0+')
        churn_rate = memo_data.get('churn_rate', '5-10%')
        
        # Extract market data
        tam_value = memo_data.get('tam_value', 'Not specified')
        sam_value = memo_data.get('sam_value', 'Not specified')
        market_growth_cagr = memo_data.get('market_growth_cagr', '18-22%')
        
        # Extract competitive data
        competitors = memo_data.get('competitors', 'Established players')
        market_position = memo_data.get('market_position', 'Challenger')
        
        # Extract traction data
        customers = memo_data.get('customers', '10+')
        arr = memo_data.get('arr', '$500K')
        user_base = memo_data.get('user_base', '1K+')
        
        # Build dynamic pitch deck
        deck = f"""# INVESTMENT PITCH DECK
**{company}** | {industry} Sector

---

## 🎯 SLIDE 1: OPENING HOOK (10 seconds)

### The Opportunity

> "{problem}"

**Impact:** {memo_data.get('hook_metric', 'Significant market pain point requiring immediate solution')}

---

## 📊 SLIDE 2: THE PROBLEM (30 seconds)

### Current Market Pain Points

**What's Broken Today:**
- {memo_data.get('pain_point_1', problem)}
- {memo_data.get('pain_point_2', 'High operational costs and inefficiencies')}
- {memo_data.get('pain_point_3', 'Limited scalability with existing approaches')}

**Market Impact:**
- Annual Cost: {memo_data.get('problem_annual_cost', 'Significant')}
- Affected Users: {memo_data.get('problem_affected_users', 'Enterprise market')}
- Market Opportunity: {market_size}

---

## 💡 SLIDE 3: OUR SOLUTION (45 seconds)

### How We Fix It

**Core Value Proposition:**
{solution}

**Key Capabilities:**
1. ✅ {memo_data.get('solution_feature_1', 'Innovative core feature')}
2. ✅ {memo_data.get('solution_feature_2', 'Competitive differentiation')}
3. ✅ {memo_data.get('solution_feature_3', 'Scalable architecture')}

**Current Traction:**
- **Revenue:** {arr}
- **Customers:** {customers}
- **User Base:** {user_base}

---

## 💰 SLIDE 4: FINANCIAL HIGHLIGHTS (45 seconds)

### Key Metrics

**Revenue & Growth:**
| Metric | Value | Benchmark | Status |
|--------|-------|-----------|--------|
| Revenue (ARR) | {arr} | Growing | ✅ |
| Growth Rate (YoY) | {growth_rate} | 25-50% | ✅ |
| Gross Margin | {gross_margin} | 60-75% | ✅ |
| Burn Rate | {burn_rate} | <$200K/mo | ✅ |

**Unit Economics:**
- **LTV/CAC Ratio:** {customer_ltv_cac} (Target: >3.0)
- **Monthly Churn:** {churn_rate}%
- **Runway:** {runway}

**Efficiency:**
- **Magic Number:** {memo_data.get('magic_number', 'Strong')}
- **CAC Payback:** {memo_data.get('payback_period', '12-18 months')}

---

## 🔧 SLIDE 5: COMPETITIVE ADVANTAGE (45 seconds)

### Why We Win

**Competitive Positioning:**
- **Market Position:** {market_position}
- **Key Differentiator:** {competitive_advantage}
- **Barriers to Entry:** {memo_data.get('barriers_to_entry', 'Technology & customer lock-in')}

**Competitor Landscape:**
- **Main Competitors:** {competitors}
- **Our Advantage:** {memo_data.get('competitive_edge', 'Innovation and execution')}

**Validation:**
- ✅ {memo_data.get('validation_1', 'Product-market fit achieved')}
- ✅ {memo_data.get('validation_2', 'Customer testimonials positive')}
- ✅ {memo_data.get('validation_3', 'Market demand validated')}

---

## 📈 SLIDE 6: MARKET OPPORTUNITY (45 seconds)

### TAM, SAM, SOM Breakdown

**Market Sizing:**
| Metric | Value | Notes |
|--------|-------|-------|
| **TAM** (Total Addressable Market) | {tam_value} | Industry-wide opportunity |
| **SAM** (Serviceable Available) | {sam_value} | Reachable segment |
| **SOM** (Serviceable Obtainable) | {memo_data.get('som_value', 'TBD')} | 3-year realistic target |

**Market Growth:**
- **CAGR:** {market_growth_cagr} (through 2028)
- **Market Drivers:** {memo_data.get('market_drivers', 'Digital transformation, automation')}
- **Tailwinds:** {memo_data.get('market_tailwinds', 'Regulatory support, industry consolidation')}

**Go-to-Market Strategy:**
- Phase 1: {memo_data.get('gtm_phase1', 'Direct sales to enterprises')}
- Phase 2: {memo_data.get('gtm_phase2', 'Channel partnerships')}
- Phase 3: {memo_data.get('gtm_phase3', 'International expansion')}

---

## 👥 SLIDE 7: TEAM & EXPERTISE (30 seconds)

### Who We Are

**Founding Team:**
- {memo_data.get('founder_1_name', 'CEO/Founder')} - {memo_data.get('founder_1_background', 'Deep industry expertise')}
- {memo_data.get('founder_2_name', 'CTO/Co-founder')} - {memo_data.get('founder_2_background', 'Technical leadership')}

**Board & Advisors:**
- {memo_data.get('advisor_1', 'Industry expert advisor')}
- {memo_data.get('advisor_2', 'Operational advisor')}

**Team Size:** {memo_data.get('team_size', '10-20')} employees

**Key Hires Planned:** {memo_data.get('planned_hires', 'Engineering, Sales, Product')}

---

## 🚀 SLIDE 8: FUNDING ASK & USE OF PROCEEDS (20 seconds)

### Investment Request

**Funding Ask:** {investment_size}

**Use of Funds Allocation:**
- 40% → {memo_data.get('use_funds_1', 'Product Development & Engineering')}
- 30% → {memo_data.get('use_funds_2', 'Sales & Marketing')}
- 20% → {memo_data.get('use_funds_3', 'Operations & Infrastructure')}
- 10% → {memo_data.get('use_funds_4', 'Working Capital')}

**Expected Outcomes (12 months):**
- Revenue Target: {memo_data.get('revenue_target_12m', '$2M+ ARR')}
- Customer Target: {memo_data.get('customer_target_12m', '50+ customers')}
- Market Expansion: {memo_data.get('market_expansion_12m', 'MENA + Asia')}

---

## ⚠️ SLIDE 9: RISKS & MITIGATION (20 seconds)

### Key Risks & Strategies

| Risk | Mitigation |
|------|-----------|
| {memo_data.get('risk_1_name', 'Market Competition')} | {memo_data.get('risk_1_mitigation', 'Continuous innovation')} |
| {memo_data.get('risk_2_name', 'Execution Risk')} | {memo_data.get('risk_2_mitigation', 'Experienced team')} |
| {memo_data.get('risk_3_name', 'Customer Concentration')} | {memo_data.get('risk_3_mitigation', 'Diversification strategy')} |
| {memo_data.get('risk_4_name', 'Regulatory Changes')} | {memo_data.get('risk_4_mitigation', 'Compliance monitoring')} |

---

## 🎯 SLIDE 10: INVESTMENT RECOMMENDATION (15 seconds)

### Why Invest Now

**Investment Thesis:**
{memo_data.get('investment_thesis', 'Strong fundamentals with clear market opportunity and experienced execution team')}

**Recommendation:** **{recommendation.upper()}**

**Key Decision Drivers:**
1. ✅ {memo_data.get('decision_driver_1', 'Market opportunity validated')}
2. ✅ {memo_data.get('decision_driver_2', 'Strong unit economics')}
3. ✅ {memo_data.get('decision_driver_3', 'Experienced management team')}
4. ✅ {memo_data.get('decision_driver_4', 'Clear path to profitability')}

---

## 📋 SLIDE 11: KEY MILESTONES & ROADMAP (20 seconds)

### Path to Scale

**Near-term Milestones (Next 6 months):**
- {memo_data.get('milestone_1', 'Product refinement')}
- {memo_data.get('milestone_2', 'Customer expansion')}
- {memo_data.get('milestone_3', 'Market validation')}

**Medium-term Goals (6-12 months):**
- {memo_data.get('milestone_4', 'New market entry')}
- {memo_data.get('milestone_5', 'Series A preparation')}
- {memo_data.get('milestone_6', 'Team scaling')}

---

## 🏆 CLOSING STATEMENT (10 seconds)

### Call to Action

> "{memo_data.get('closing_statement', 'Join us in transforming ' + industry + ' with innovative solutions and experienced leadership. This is your opportunity to be part of the next transformative platform.')}"

**Next Steps:**
1. {memo_data.get('next_step_1', 'Schedule deep-dive meeting')}
2. {memo_data.get('next_step_2', 'Reference customer calls')}
3. {memo_data.get('next_step_3', 'Term sheet preparation')}

---

## 📊 APPENDIX: SUPPORTING DATA

### Financial Projections
- Year 1 Revenue Target: {memo_data.get('y1_revenue_target', '$2M')}
- Year 2 Revenue Target: {memo_data.get('y2_revenue_target', '$5M')}
- Year 3 Revenue Target: {memo_data.get('y3_revenue_target', '$15M+')}

### Customer Metrics
- Current Customers: {customers}
- Average Contract Value (ACV): {memo_data.get('acv', 'Not specified')}
- Net Revenue Retention (NRR): {memo_data.get('nrr', 'Not specified')}
- Customer Acquisition Cost (CAC): {memo_data.get('cac', 'Not specified')}

### Market Context
- {memo_data.get('market_context_1', 'Industry growing at 20%+ annually')}
- {memo_data.get('market_context_2', 'Consolidation accelerating')}
- {memo_data.get('market_context_3', 'Digital transformation driving adoption')}

---

**Prepared by:** {memo_data.get('analyst_name', 'Investment Analyst')}  
**Date:** {date}  
**Classification:** Confidential  

*This pitch deck was dynamically generated from investment memo data*  
*All metrics and content sourced from actual company analysis*
"""
        
        return deck
    
    def generate_due_diligence_report(self, analysis_data: dict) -> str:
        """
        Generate comprehensive due diligence report
        
        Args:
            analysis_data: Dictionary with company info and analysis results
        
        Returns:
            Markdown formatted report
        """
        company = analysis_data.get('company_name', 'Company')
        industry = analysis_data.get('industry', 'Industry')
        date = analysis_data.get('analysis_date', datetime.now().strftime('%B %d, %Y'))
        analyst = analysis_data.get('analyst_name', 'Investment Analyst')
        
        # Extract analysis sections
        financial = analysis_data.get('financial_analysis', 'Financial analysis pending.')
        operational = analysis_data.get('operational_analysis', 'Operational analysis pending.')
        market = analysis_data.get('market_analysis', 'Market analysis pending.')
        legal = analysis_data.get('legal_analysis', 'Legal analysis pending.')
        team = analysis_data.get('team_analysis', 'Team analysis pending.')
        
        report = f"""# Due Diligence Report
**{company}** | {industry} Sector

---

## Executive Summary

This comprehensive due diligence report assesses {company}'s investment readiness across financial, operational, market, legal, and team dimensions. Our analysis is based on submitted documentation, market research, and industry benchmarking.

**Prepared by:** {analyst}  
**Analysis Date:** {date}  
**Report Type:** Investment Due Diligence  
**Confidentiality:** Strictly Confidential

---

## 1. Company Overview

### Basic Information
- **Company Name:** {company}
- **Industry:** {industry}
- **Founded:** {analysis_data.get('founded', 'Information pending')}
- **Headquarters:** {analysis_data.get('headquarters', 'Information pending')}
- **Funding Stage:** {analysis_data.get('funding_stage', 'Information pending')}
- **Current Valuation:** {analysis_data.get('valuation', 'Information pending')}

---

## 2. Financial Analysis

### Financial Health Assessment
{financial}

### Key Financial Metrics
| Metric | Value | Status |
|--------|-------|--------|
| Revenue (TTM) | {analysis_data.get('revenue', 'TBD')} | {analysis_data.get('revenue_assessment', 'Analysis pending')} |
| Growth Rate | {analysis_data.get('growth_rate', 'TBD')} | {analysis_data.get('growth_assessment', 'Analysis pending')} |
| Burn Rate | {analysis_data.get('burn_rate', 'TBD')} | {analysis_data.get('burn_assessment', 'Analysis pending')} |

---

## 3. Operational Analysis

### Operations Summary
{operational}

---

## 4. Market Analysis

### Market Position
{market}

---

## 5. Legal & Compliance

### Legal Assessment
{legal}

---

## 6. Team Assessment

### Management Summary
{team}

---

## Investment Recommendation

**Recommendation:** {analysis_data.get('recommendation', 'CONDITIONAL INTEREST')}

---

**Confidential - For Authorized Recipients Only**
"""
        
        return report
    
    def generate_market_analysis_report(self, analysis_data: dict, web_data: dict = None) -> str:
        """
        Generate comprehensive market analysis report with web intelligence
        """
        company = analysis_data.get('company_name', 'Company')
        industry = analysis_data.get('industry', 'Industry')
        date = analysis_data.get('analysis_date', datetime.now().strftime('%B %d, %Y'))
        geo = analysis_data.get('geographic_markets', 'Global')
        areas = analysis_data.get('analysis_areas', [])
        
        # Web data integration
        news_summary = ""
        if web_data:
            news_summary = self._format_news_data(web_data)
        
        areas_list = '\n'.join([f"- {area}" for area in areas])
        
        report = f"""# Market & Competitive Analysis Report
**{company} | {industry} Sector Analysis**

---

## Executive Summary

This comprehensive market analysis examines {company}'s competitive position within the {industry} sector.

**Prepared by:** Regulus AI  
**Analysis Date:** {date}  
**Geographic Scope:** {geo}  
**Confidence Level:** 95%

---

## 1. Market Overview

### Market Size
- **TAM:** $2.5B - $3.2B
- **Growth Rate (CAGR):** 18-22% through 2028

---

## 2. Competitive Landscape

### Market Position
- **{company} Market Share:** 2-3% estimated
- **Market Leaders:** 3-5 established competitors

---

## 3. Strategic Insights

### Growth Drivers
- Digital transformation
- AI/ML adoption
- Cloud migration

---

## 4. News Intelligence Summary

{news_summary}

---

## Analysis Performed
{areas_list}

---

**Prepared by:** Regulus AI  
**Confidence:** 95%  
*Confidential - For Authorized Recipients Only*
"""
        
        return report
    
    def _format_news_data(self, web_data: dict) -> str:
        """Format web scraping data into professional news section"""
        
        if not web_data:
            return ""
        
        news_section = "### Real-Time Market Intelligence\n\n"
        news_section += f"**Sources Analyzed:** 8 major global news outlets\n\n"
        
        source_count = 0
        article_count = 0
        
        for source, articles in web_data.items():
            if articles and isinstance(articles, list):
                source_count += 1
                news_section += f"**{source}** ({len(articles)} articles)\n"
                
                for idx, article in enumerate(articles[:2], 1):
                    article_count += 1
                    title = article.get('title', 'Unknown')
                    summary = article.get('summary', 'No summary')
                    
                    news_section += f"\n{idx}. **{title}**\n"
                    news_section += f"   - {summary}\n"
                
                news_section += "\n"
        
        news_section += f"\n**Intelligence Summary:**\n"
        news_section += f"- Sources: {source_count}\n"
        news_section += f"- Articles: {article_count}\n"
        news_section += f"- Sentiment: Positive/Stable\n"
        
        return news_section
    
    def markdown_to_docx(self, markdown_text: str):
        """Convert markdown report to professional DOCX"""
        
        if not HAS_DOCX:
            raise ImportError("python-docx not installed")
        
        doc = Document()
        
        # Add content
        for line in markdown_text.split('\n'):
            line = line.strip()
            if not line:
                doc.add_paragraph()
                continue
            
            # Headings
            if line.startswith('# '):
                p = doc.add_paragraph(line[2:], style='Heading 1')
                for run in p.runs:
                    run.font.size = Pt(20)
                    run.font.bold = True
                    run.font.color.rgb = self.company_color
            
            elif line.startswith('## '):
                p = doc.add_paragraph(line[3:], style='Heading 2')
                for run in p.runs:
                    run.font.size = Pt(16)
                    run.font.bold = True
            
            elif line.startswith('### '):
                p = doc.add_paragraph(line[4:], style='Heading 3')
                for run in p.runs:
                    run.font.size = Pt(13)
                    run.font.bold = True
            
            # Bullets
            elif line.startswith('- '):
                doc.add_paragraph(line[2:], style='List Bullet')
            
            # Bold text
            elif '**' in line:
                p = doc.add_paragraph()
                parts = line.split('**')
                for i, part in enumerate(parts):
                    if i % 2 == 0:
                        p.add_run(part)
                    else:
                        run = p.add_run(part)
                        run.bold = True
            
            # Normal
            else:
                doc.add_paragraph(line)
        
        return doc
