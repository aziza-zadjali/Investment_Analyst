"""
Unified Template & Report Generator
Generates investment memos, due diligence reports, market analysis, and DOCX exports
"""

from datetime import datetime
from typing import Dict, List, Any
from io import BytesIO
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font


class TemplateGenerator:
    """Generate professional reports with dynamic content from analysis"""

    # =========================================================================
    # DUE DILIGENCE REPORTS
    # =========================================================================
    
    def generate_due_diligence_report_solartech_format(self, data: Dict[str, Any]) -> str:
        """Generate Corporate DD Report - all fields populated from data"""
        date_now = datetime.now().strftime("%B %d, %Y")
        
        report = f"""# Due Diligence Report

**Company:** {data.get('company_name')}  
**Report Date:** {date_now}  
**Prepared by:** {data.get('analyst_name')}

---

## 1. Executive Summary

This report summarizes the due diligence findings for **{data.get('company_name')}** conducted on {data.get('review_dates', date_now)}. The analysis assessed key risks, liabilities, and opportunities based on comprehensive document review.

---

## 2. Scope of Review

- **Financial:** {data.get('financial_scope')}
- **Legal:** {data.get('legal_scope')}
- **Operational:** {data.get('operational_scope')}
- **Commercial:** {data.get('commercial_scope')}

---

## 3. Key Findings

| Category | Findings | Risk Level |
|----------|----------|------------|
| **Financial** | {data.get('financial_findings')} | {data.get('financial_risk')} |
| **Legal** | {data.get('legal_findings')} | {data.get('legal_risk')} |
| **Operational** | {data.get('operational_findings')} | {data.get('operational_risk')} |
| **Commercial** | {data.get('commercial_findings')} | {data.get('commercial_risk')} |

---

## 4. Recommendations

{data.get('recommendations')}

---

## 5. Conclusion

{data.get('conclusion')}

---

**Authorized by:** {data.get('analyst_name')}  
**Date:** {date_now}
"""
        return report

    def generate_due_diligence_report_early_stage_format(self, data: Dict[str, Any]) -> str:
        """Generate Early-Stage Investor DD Report - all fields from data"""
        date_now = datetime.now().strftime("%B %d, %Y")
        
        report = f"""# Due Diligence Report for Early Stage Investors

**Company:** {data.get('company_name')}  
**CEO:** {data.get('ceo_name', 'To be confirmed')}  
**Report Date:** {date_now}

---

## Company Description

{data.get('company_description')}

---

## Due Diligence Assessment

| **Topic** | **Rating** | **Remarks** |
|-----------|------------|-------------|
| **Investment Thesis** | {data.get('investment_thesis_rating')} | {data.get('investment_thesis')} |
| **What Needs To Be Believed** | {data.get('wntbb_rating')} | {data.get('wntbb')} |
| **Failure Risk** | {data.get('failure_risk_rating')} | {data.get('failure_risk')} |
| **Leadership Assessment** | {data.get('leadership_rating')} | {data.get('leadership_assessment')} |
| **Technology and IP** | {data.get('tech_rating')} | {data.get('tech_assessment')} |
| **Go-To-Market Plan** | {data.get('gtm_rating')} | {data.get('gtm_assessment')} |
| **Competition** | {data.get('competition_rating')} | {data.get('competition_assessment')} |
| **Market Size** | {data.get('market_rating')} | {data.get('market_assessment')} |
| **Financial Projections** | {data.get('financial_rating')} | {data.get('financial_assessment')} |
| **Exit Strategy** | {data.get('exit_rating')} | {data.get('exit_assessment')} |
| **Deal Terms** | {data.get('terms_rating')} | {data.get('terms_assessment')} |

---

### Rating Key

**(++)** Very Positive | **(+)** Positive | **(0)** Neutral | **(--)** Negative | **( / )** Critical

---

**Prepared by:** {data.get('analyst_name')}  
**Date:** {date_now}
"""
        return report

    # =========================================================================
    # MARKET ANALYSIS REPORTS
    # =========================================================================
    
    def generate_market_analysis_report(self, data: Dict[str, Any]) -> str:
        """Generate professional market analysis report matching consulting firm standards"""
        
        report = f"""# Market & Competitive Intelligence Report

**Company/Industry:** {data.get('company_name')}  
**Geographic Region:** {data.get('geography')}  
**Sector:** {data.get('industry')}  
**Report Date:** {data.get('date')}  
**Prepared by:** AI Investment Analyst Platform

---

## Executive Summary

This report provides comprehensive market intelligence for **{data.get('company_name')}** operating in the **{data.get('geography')}** region. Analysis draws from leading consulting firm publications, market research platforms, and real-time business intelligence.

---

## 📈 Market Overview

{data.get('market_overview')}

---

## 🏢 Competitive Landscape

{data.get('competitors')}

---

## 🔍 Strategic Insights & Recommendations

{data.get('insights')}

---

## Methodology

This analysis synthesizes data from multiple premium sources:
- **Consulting Research:** McKinsey, BCG, Bain, Deloitte, PwC, EY, KPMG
- **Market Intelligence:** Mordor Intelligence, Statista, IBISWorld, Gartner
- **Business News:** Bloomberg, Reuters, Financial Times, Wall Street Journal

**AI-Powered Analysis:** GPT-4 advanced reasoning for insight generation

---

**Confidentiality Notice:** This report contains proprietary analysis. Distribution restricted to authorized personnel only.
"""
        return report

    # =========================================================================
    # DOCX GENERATION WITH TABLE SUPPORT
    # =========================================================================
    
    def generate_docx_report(self, report_text: str, report_title: str = "Report") -> BytesIO:
        """Convert markdown to professional DOCX with tables"""
        try:
            import markdown
            from bs4 import BeautifulSoup
            from docx import Document
            from docx.shared import Pt
            from docx.enum.text import WD_ALIGN_PARAGRAPH
            
            html_content = markdown.markdown(report_text, extensions=['tables', 'nl2br'])
            soup = BeautifulSoup(html_content, 'html.parser')
            doc = Document()
            
            title_para = doc.add_heading(report_title, level=0)
            title_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            
            for element in soup.children:
                if element.name == 'h1':
                    doc.add_heading(element.get_text(), level=1)
                elif element.name == 'h2':
                    doc.add_heading(element.get_text(), level=2)
                elif element.name == 'h3':
                    doc.add_heading(element.get_text(), level=3)
                elif element.name == 'h4':
                    doc.add_heading(element.get_text(), level=4)
                elif element.name == 'p':
                    text = element.get_text()
                    if text.strip():
                        if element.find('strong'):
                            p = doc.add_paragraph()
                            for child in element.children:
                                if child.name == 'strong':
                                    run = p.add_run(child.get_text())
                                    run.bold = True
                                elif isinstance(child, str):
                                    p.add_run(child)
                        else:
                            doc.add_paragraph(text)
                elif element.name == 'ul':
                    for li in element.find_all('li', recursive=False):
                        doc.add_paragraph(li.get_text(), style='List Bullet')
                elif element.name == 'ol':
                    for li in element.find_all('li', recursive=False):
                        doc.add_paragraph(li.get_text(), style='List Number')
                elif element.name == 'table':
                    rows = element.find_all('tr')
                    if rows:
                        cols = rows[0].find_all(['td', 'th'])
                        table = doc.add_table(rows=len(rows), cols=len(cols))
                        table.style = 'Table Grid'
                        
                        for i, row in enumerate(rows):
                            cells = row.find_all(['td', 'th'])
                            for j, cell in enumerate(cells):
                                cell_text = cell.get_text().strip()
                                table_cell = table.cell(i, j)
                                table_cell.text = cell_text
                                if i == 0:
                                    for paragraph in table_cell.paragraphs:
                                        for run in paragraph.runs:
                                            run.bold = True
                elif element.name == 'hr':
                    doc.add_paragraph('_' * 60)
            
            buffer = BytesIO()
            doc.save(buffer)
            buffer.seek(0)
            return buffer
            
        except ImportError:
            from docx import Document
            doc = Document()
            doc.add_heading(report_title, level=0)
            doc.add_paragraph(report_text)
            buffer = BytesIO()
            doc.save(buffer)
            buffer.seek(0)
            return buffer
        except Exception:
            return BytesIO(report_text.encode('utf-8'))

    # =========================================================================
    # LEGACY & BACKWARDS COMPATIBILITY
    # =========================================================================
    
    def generate_due_diligence_report(self, data: Dict[str, Any]) -> str:
        """Main DD report generator"""
        return self.generate_due_diligence_report_solartech_format(data)

    def generate_investment_memo(self, data: Dict[str, Any]) -> str:
        """Investment memo from data"""
        date_now = datetime.now().strftime("%B %d, %Y")
        return f"""# Investment Memo — {data.get('company_name')}

**Date:** {date_now}  
**Analyst:** {data.get('analyst_name')}

## Executive Summary
{data.get('executive_summary')}

## Investment Rationale
{data.get('rationale')}

## Recommendation
{data.get('recommendation')}
"""

    def generate_daily_deals_report(self, deals: List[Dict[str, Any]], criteria: Dict[str, Any]) -> str:
        """Daily deals report from data"""
        date_today = datetime.now().strftime("%B %d, %Y")
        report = f"""# Daily Potential Deals Report  
**Date:** {date_today}  

### Criteria
- **Sectors:** {', '.join(criteria.get('sectors', []))}
- **Stage:** {criteria.get('stage_range', 'All')}

---

"""
        for i, deal in enumerate(deals, start=1):
            report += f"### {i}. {deal.get('company')}\n- **Sector:** {deal.get('sector')}\n---\n"
        return report

    def generate_financial_model(self, data: Dict[str, Any]) -> BytesIO:
        """Excel financial model"""
        wb = Workbook()
        ws = wb.active
        ws.title = "Summary"
        ws["A1"] = "Financial Model"
        ws["A1"].font = Font(size=16, bold=True)
        
        buffer = BytesIO()
        wb.save(buffer)
        buffer.seek(0)
        return buffer
