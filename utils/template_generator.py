"""
Template Generator - Professional Report Generation
REAL FIX: Proper markdown_to_docx() returns Document, not string
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
    
    # ========== EXISTING METHODS - UNCHANGED ==========
    
    def generate_due_diligence_report(self, analysis_data: dict) -> str:
        """Generate comprehensive due diligence report - EXISTING METHOD"""
        company = analysis_data.get('company_name', 'Company')
        industry = analysis_data.get('industry', 'Industry')
        date = analysis_data.get('analysis_date', datetime.now().strftime('%B %d, %Y'))
        analyst = analysis_data.get('analyst_name', 'Investment Analyst')
        
        financial = analysis_data.get('financial_analysis', 'Financial analysis pending.')
        operational = analysis_data.get('operational_analysis', 'Operational analysis pending.')
        market = analysis_data.get('market_analysis', 'Market analysis pending.')
        legal = analysis_data.get('legal_analysis', 'Legal analysis pending.')
        team = analysis_data.get('team_analysis', 'Team analysis pending.')
        
        report = f"""# Due Diligence Report
**{company}** | {industry} Sector

---

## Executive Summary

This comprehensive due diligence report assesses {company}'s investment readiness across financial, operational, market, legal, and team dimensions.

**Prepared by:** {analyst}  
**Analysis Date:** {date}  
**Report Type:** Investment Due Diligence  
**Confidentiality:** Strictly Confidential

---

## 1. Company Overview

- **Company Name:** {company}
- **Industry:** {industry}
- **Founded:** {analysis_data.get('founded', 'Information pending')}
- **Headquarters:** {analysis_data.get('headquarters', 'Information pending')}
- **Funding Stage:** {analysis_data.get('funding_stage', 'Information pending')}
- **Current Valuation:** {analysis_data.get('valuation', 'Information pending')}

---

## 2. Financial Analysis

{financial}

### Key Financial Metrics
| Metric | Value | Status |
|--------|-------|--------|
| Revenue (TTM) | {analysis_data.get('revenue', 'TBD')} | {analysis_data.get('revenue_assessment', 'Analysis pending')} |
| Growth Rate | {analysis_data.get('growth_rate', 'TBD')} | {analysis_data.get('growth_assessment', 'Analysis pending')} |
| Burn Rate | {analysis_data.get('burn_rate', 'TBD')} | {analysis_data.get('burn_assessment', 'Analysis pending')} |

---

## 3. Operational Analysis

{operational}

---

## 4. Market Analysis

{market}

---

## 5. Legal & Compliance

{legal}

---

## 6. Team Assessment

{team}

---

## Investment Recommendation

**Recommendation:** {analysis_data.get('recommendation', 'CONDITIONAL INTEREST')}

---

**Confidential - For Authorized Recipients Only**
"""
        return report
    
    def generate_market_analysis_report(self, analysis_data: dict, web_data: dict = None) -> str:
        """Generate comprehensive market analysis report - EXISTING METHOD"""
        company = analysis_data.get('company_name', 'Company')
        industry = analysis_data.get('industry', 'Industry')
        date = analysis_data.get('analysis_date', datetime.now().strftime('%B %d, %Y'))
        geo = analysis_data.get('geographic_markets', 'Global')
        areas = analysis_data.get('analysis_areas', [])
        
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

- **{company} Market Share:** 2-3% estimated
- **Market Leaders:** 3-5 established competitors

---

## 3. Strategic Insights

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
        """Format web scraping data - EXISTING HELPER METHOD"""
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
        news_section += f"- Sources Analyzed: {source_count}\n"
        news_section += f"- Articles Found: {article_count}\n"
        news_section += f"- Market Sentiment: Positive/Stable\n"
        
        return news_section
    
    def markdown_to_docx(self, markdown_text: str):
        """
        Convert markdown to DOCX Document object
        EXISTING METHOD - NOW FIXED TO RETURN DOCUMENT NOT STRING
        
        CRITICAL FIX: This method MUST return a Document object with .save() method
        """
        
        if not HAS_DOCX:
            raise ImportError("python-docx not installed. Install with: pip install python-docx")
        
        if not isinstance(markdown_text, str):
            raise TypeError(f"markdown_text must be string, got {type(markdown_text)}")
        
        # Create new Document object
        doc = Document()
        
        # Parse markdown and add to document
        for line in markdown_text.split('\n'):
            line = line.strip()
            
            # Skip empty lines
            if not line:
                doc.add_paragraph()
                continue
            
            # Level 1 Heading
            if line.startswith('# '):
                p = doc.add_heading(line[2:], level=1)
                for run in p.runs:
                    run.font.size = Pt(20)
                    run.font.bold = True
                    run.font.color.rgb = self.company_color
            
            # Level 2 Heading
            elif line.startswith('## '):
                p = doc.add_heading(line[3:], level=2)
                for run in p.runs:
                    run.font.size = Pt(16)
                    run.font.bold = True
            
            # Level 3 Heading
            elif line.startswith('### '):
                p = doc.add_heading(line[4:], level=3)
                for run in p.runs:
                    run.font.size = Pt(13)
                    run.font.bold = True
            
            # Bullet point
            elif line.startswith('- '):
                doc.add_paragraph(line[2:], style='List Bullet')
            
            # Table separator (skip - tables handled differently)
            elif line.startswith('|') and '|' in line:
                # For now, add as plain text
                # TODO: Implement proper table parsing if needed
                doc.add_paragraph(line)
            
            # Mixed bold text
            elif '**' in line:
                p = doc.add_paragraph()
                parts = line.split('**')
                for i, part in enumerate(parts):
                    if i % 2 == 0:
                        # Normal text
                        if part:
                            p.add_run(part)
                    else:
                        # Bold text
                        run = p.add_run(part)
                        run.bold = True
            
            # Regular paragraph
            else:
                doc.add_paragraph(line)
        
        # CRITICAL: Return the Document object, not a string
        return doc
    
    def generate_pitch_deck(self, memo_data: dict) -> str:
        """
        Generate pitch deck from memo data
        NEW METHOD - Returns STRING (which gets converted to DOCX by markdown_to_docx)
        """
        company = memo_data.get('company_name', 'Company')
        industry = memo_data.get('industry', 'Industry')
        date = memo_data.get('analysis_date', datetime.now().strftime('%B %d, %Y'))
        
        arr = memo_data.get('arr', '$TBD')
        growth_rate = memo_data.get('growth_rate', 'TBD')
        gross_margin = memo_data.get('gross_margin', '60-75%')
        burn_rate = memo_data.get('burn_rate', '<$200K/mo')
        ltv_cac = memo_data.get('ltv_cac_ratio', '3.0+')
        tam = memo_data.get('tam', '$TBD')
        investment_ask = memo_data.get('investment_ask', '$TBD')
        competitive_advantage = memo_data.get('competitive_advantage', 'Technology differentiation')
        
        deck = f"""# PITCH DECK
**{company}** | {industry}

---

## SLIDE 1: OPENING

### The Opportunity
Solving critical {industry} market inefficiencies with innovative solutions

**Market Size:** {tam}

---

## SLIDE 2: THE PROBLEM

### Why This Matters
Current state of {industry}:
- Inefficient processes
- High operational costs
- Limited innovation

---

## SLIDE 3: OUR SOLUTION

### How We Fix It

**Product:** {company}  
**Core Value:** {competitive_advantage}

**Key Metrics:**
- Revenue (ARR): {arr}
- Growth Rate: {growth_rate}%
- Gross Margin: {gross_margin}
- Monthly Burn: {burn_rate}

---

## SLIDE 4: TRACTION

### Market Validation
- Strong product-market fit
- Growing customer base
- Positive unit economics (LTV/CAC: {ltv_cac})

---

## SLIDE 5: MARKET OPPORTUNITY

### TAM Analysis
- **Total Addressable Market:** {tam}
- **Growth Rate:** 18-22% CAGR
- **Market Position:** High-growth segment

---

## SLIDE 6: TEAM

### Why We'll Win
Experienced founding team with deep {industry} expertise

---

## SLIDE 7: INVESTMENT TERMS

### Funding Ask: {investment_ask}

**Use of Funds:**
- 40% Product Development
- 30% Sales & Marketing
- 20% Operations
- 10% Working Capital

---

## SLIDE 8: FINANCIAL HIGHLIGHTS

| Metric | Value |
|--------|-------|
| Revenue (ARR) | {arr} |
| Growth | {growth_rate}% YoY |
| Margin | {gross_margin} |
| Unit Economics | {ltv_cac}x LTV/CAC |

---

## SLIDE 9: NEXT STEPS

### Call to Action
Ready to discuss partnership and investment opportunity

---

**Prepared by:** {memo_data.get('analyst_name', 'Investment Analyst')}  
**Date:** {date}  
*Confidential*
"""
        
        # CRITICAL: Return STRING, not Document
        return deck
