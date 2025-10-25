"""
Template Generator for Investment Analysis Reports
Generates professional reports with justified text and proper formatting
"""

from typing import Dict, Any
from datetime import datetime
import markdown
from bs4 import BeautifulSoup
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH


class TemplateGenerator:
    """Generate professional investment analysis reports"""
    
    def __init__(self):
        self.company_name = ""
    
    def generate_due_diligence_report(self, analysis_data: Dict[str, Any]) -> str:
        """Generate comprehensive due diligence report with AML/compliance screening"""
        
        company = analysis_data.get('company_name', 'Company')
        analyst = analysis_data.get('analyst_name', 'Investment Analyst')
        date = analysis_data.get('analysis_date', datetime.now().strftime('%B %d, %Y'))
        website = analysis_data.get('company_website', 'N/A')
        sources = analysis_data.get('data_sources', [])
        
        report = f"""# DUE DILIGENCE REPORT
## {company}

**Prepared by:** {analyst}  
**Date:** {date}  
**Company Website:** {website}

---

## EXECUTIVE SUMMARY

This comprehensive due diligence report provides an in-depth analysis of {company}, covering financial performance, legal compliance, operational capabilities, risk assessment, and AML/KYC screening.

**Data Sources:** {', '.join(sources) if sources else 'Uploaded documents and analysis'}

---

## 1. FINANCIAL ANALYSIS

{analysis_data.get('financial_analysis', 'Financial analysis pending')}

---

## 2. LEGAL & COMPLIANCE REVIEW

{analysis_data.get('legal_analysis', 'Legal analysis pending')}

---

## 3. OPERATIONAL ASSESSMENT

{analysis_data.get('operational_analysis', 'Operational analysis pending')}

---

## 4. RISK ASSESSMENT

{analysis_data.get('risk_assessment', 'Risk assessment pending')}

---

## 5. AML/KYC SCREENING

### 5.1 Sanctions Screening

{analysis_data.get('sanctions_screening', 'Sanctions screening pending')}

### 5.2 PEP Screening

{analysis_data.get('pep_screening', 'PEP screening pending')}

### 5.3 FATCA Compliance

{analysis_data.get('fatca_compliance', 'FATCA review pending')}

### 5.4 Adverse Media Check

{analysis_data.get('adverse_media', 'Adverse media screening pending')}

### 5.5 AML Risk Rating

{analysis_data.get('aml_risk_rating', 'Risk rating to be determined based on findings')}

---

## 6. RECOMMENDATIONS

{analysis_data.get('recommendations', 'Recommendations pending')}

---

## CONCLUSION

This due diligence report provides a comprehensive assessment of {company} based on available information. All findings should be reviewed in conjunction with additional verification and professional legal/financial advice.

---

**Report Generated:** {datetime.now().strftime('%B %d, %Y at %H:%M')}  
**Prepared by:** {analyst}

---

*This report is confidential and intended solely for the use of authorized personnel.*
"""
        
        return report
    
    def generate_market_analysis_report(self, analysis_data: Dict[str, Any]) -> str:
        """Generate market analysis report"""
        
        company = analysis_data.get('company_name', 'Company')
        analyst = analysis_data.get('analyst_name', 'Market Analyst')
        date = analysis_data.get('analysis_date', datetime.now().strftime('%B %d, %Y'))
        
        report = f"""# MARKET & COMPETITIVE ANALYSIS REPORT
## {company}

**Prepared by:** {analyst}  
**Date:** {date}

---

## EXECUTIVE SUMMARY

{analysis_data.get('executive_summary', 'Market analysis summary pending')}

---

## 1. MARKET OVERVIEW

{analysis_data.get('market_overview', 'Market overview pending')}

---

## 2. COMPETITIVE LANDSCAPE

{analysis_data.get('competitive_analysis', 'Competitive analysis pending')}

---

## 3. MARKET TRENDS

{analysis_data.get('market_trends', 'Market trends analysis pending')}

---

## 4. COMPANY POSITIONING

{analysis_data.get('company_position', 'Company positioning analysis pending')}

---

## 5. KEY INSIGHTS & RECOMMENDATIONS

{analysis_data.get('recommendations', 'Recommendations pending')}

---

**Report Generated:** {datetime.now().strftime('%B %d, %Y at %H:%M')}  
**Prepared by:** {analyst}
"""
        
        return report
    
    def generate_investment_memo(self, analysis_data: Dict[str, Any]) -> str:
        """Generate investment memorandum"""
        
        company = analysis_data.get('company_name', 'Company')
        analyst = analysis_data.get('analyst_name', 'Investment Analyst')
        date = analysis_data.get('analysis_date', datetime.now().strftime('%B %d, %Y'))
        
        report = f"""# INVESTMENT MEMORANDUM
## {company}

**Prepared by:** {analyst}  
**Date:** {date}

---

## INVESTMENT THESIS

{analysis_data.get('investment_thesis', 'Investment thesis pending')}

---

## COMPANY OVERVIEW

{analysis_data.get('company_overview', 'Company overview pending')}

---

## MARKET OPPORTUNITY

{analysis_data.get('market_opportunity', 'Market opportunity analysis pending')}

---

## FINANCIAL PERFORMANCE

{analysis_data.get('financial_performance', 'Financial performance analysis pending')}

---

## RISKS & MITIGATION

{analysis_data.get('risks', 'Risk analysis pending')}

---

## RECOMMENDATION

{analysis_data.get('recommendation', 'Investment recommendation pending')}

---

**Report Generated:** {datetime.now().strftime('%B %d, %Y at %H:%M')}  
**Prepared by:** {analyst}
"""
        
        return report
    
    def markdown_to_docx(self, markdown_text: str) -> Document:
        """Convert markdown text to DOCX document with proper formatting"""
        
        # Convert markdown to HTML
        html = markdown.markdown(markdown_text, extensions=['tables', 'fenced_code'])
        
        # Parse HTML
        soup = BeautifulSoup(html, 'html.parser')
        
        # Create DOCX document
        doc = Document()
        
        # Set default font
        style = doc.styles['Normal']
        font = style.font
        font.name = 'Calibri'
        font.size = Pt(11)
        
        # Set margins
        sections = doc.sections
        for section in sections:
            section.top_margin = Inches(1)
            section.bottom_margin = Inches(1)
            section.left_margin = Inches(1)
            section.right_margin = Inches(1)
        
        # Process each element
        for element in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'p', 'ul', 'ol', 'table', 'pre', 'hr']):
            
            if element.name == 'h1':
                heading = doc.add_heading(element.get_text(), level=1)
                heading.alignment = WD_ALIGN_PARAGRAPH.LEFT
                for run in heading.runs:
                    run.font.size = Pt(18)
                    run.font.bold = True
            
            elif element.name == 'h2':
                heading = doc.add_heading(element.get_text(), level=2)
                heading.alignment = WD_ALIGN_PARAGRAPH.LEFT
                for run in heading.runs:
                    run.font.size = Pt(16)
                    run.font.bold = True
            
            elif element.name == 'h3':
                heading = doc.add_heading(element.get_text(), level=3)
                heading.alignment = WD_ALIGN_PARAGRAPH.LEFT
                for run in heading.runs:
                    run.font.size = Pt(14)
                    run.font.bold = True
            
            elif element.name == 'h4':
                heading = doc.add_heading(element.get_text(), level=4)
                heading.alignment = WD_ALIGN_PARAGRAPH.LEFT
                for run in heading.runs:
                    run.font.size = Pt(12)
                    run.font.bold = True
            
            elif element.name == 'h5':
                para = doc.add_paragraph(element.get_text())
                para.alignment = WD_ALIGN_PARAGRAPH.LEFT
                for run in para.runs:
                    run.font.bold = True
            
            elif element.name == 'p':
                text = element.get_text().strip()
                if text:
                    para = doc.add_paragraph(text)
                    # Justify paragraphs unless they're short headings or single lines
                    if len(text) > 50:
                        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                    else:
                        para.alignment = WD_ALIGN_PARAGRAPH.LEFT
            
            elif element.name in ['ul', 'ol']:
                for li in element.find_all('li', recursive=False):
                    text = li.get_text().strip()
                    if text:
                        para = doc.add_paragraph(text, style='List Bullet' if element.name == 'ul' else 'List Number')
                        # Justify list items if they're long
                        if len(text) > 50:
                            para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            
            elif element.name == 'table':
                # Extract table data
                rows = element.find_all('tr')
                if rows:
                    # Determine number of columns
                    max_cols = max(len(row.find_all(['th', 'td'])) for row in rows)
                    
                    # Create table
                    table = doc.add_table(rows=len(rows), cols=max_cols)
                    table.style = 'Light Grid Accent 1'
                    
                    # Fill table
                    for i, row in enumerate(rows):
                        cells = row.find_all(['th', 'td'])
                        for j, cell in enumerate(cells):
                            if j < max_cols:
                                table.rows[i].cells[j].text = cell.get_text().strip()
                                # Bold header row
                                if i == 0:
                                    for paragraph in table.rows[i].cells[j].paragraphs:
                                        for run in paragraph.runs:
                                            run.font.bold = True
            
            elif element.name == 'pre':
                # Code block - use monospace font
                text = element.get_text()
                para = doc.add_paragraph(text)
                for run in para.runs:
                    run.font.name = 'Courier New'
                    run.font.size = Pt(9)
            
            elif element.name == 'hr':
                # Horizontal rule - add paragraph border
                para = doc.add_paragraph()
                para.paragraph_format.border_bottom = True
        
        return doc
    
    def generate_daily_deals_report(self, deals_data: list) -> str:
        """Generate daily potential deals report"""
        
        date = datetime.now().strftime('%B %d, %Y')
        
        report = f"""# DAILY POTENTIAL DEALS REPORT
**Date:** {date}  
**Prepared by:** Regulus AI

---

## SUMMARY

Found {len(deals_data)} potential investment opportunities matching search criteria.

---

## DEALS

"""
        
        for idx, deal in enumerate(deals_data, 1):
            report += f"""### {idx}. {deal.get('name', 'Company')}

**Industry:** {deal.get('industry', 'N/A')}  
**Stage:** {deal.get('stage', 'N/A')}  
**Funding:** {deal.get('funding', 'N/A')}  
**Location:** {deal.get('location', 'N/A')}  

**Description:** {deal.get('description', 'No description available')}

---

"""
        
        report += f"""
**Report Generated:** {datetime.now().strftime('%B %d, %Y at %H:%M')}  
**Prepared by:** Regulus AI
"""
        
        return report
