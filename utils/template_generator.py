"""
Template Generator for Investment Analyst AI
Handles DOCX report generation and formatting
"""
from datetime import datetime
from io import BytesIO
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

class TemplateGenerator:
    """Generate professional investment analysis reports"""
    
    def __init__(self):
        self.company_color = RGBColor(27, 43, 77)  # QDB dark blue
        self.accent_color = RGBColor(22, 160, 133)  # Teal
    
    def generate_due_diligence_report(self, analysis_data: dict) -> str:
        """
        Generates a detailed Due Diligence markdown report
        """
        try:
            company = analysis_data.get("company_name", "Unknown Company")
            analyst = analysis_data.get("analyst", "Regulus AI")
            date = analysis_data.get("date", datetime.now().strftime("%B %d, %Y"))
            website = analysis_data.get("website", "N/A")
            
            md_report = f"""# Due Diligence Report

**Company:** {company}  
**Analyst:** {analyst}  
**Date:** {date}  
**Website:** {website}  

---

## 1. Financial Analysis

{analysis_data.get('financial', 'No financial data available')}

---

## 2. Legal & Compliance Review

{analysis_data.get('legal', 'No legal data available')}

---

## 3. Operational Overview

{analysis_data.get('operational', 'No operational insights available')}

---

## 4. Risk Assessment

{analysis_data.get('risks', 'No risk data available')}

---

## 5. AML / KYC Screening

{analysis_data.get('aml', 'No AML data available')}

---

## 6. Recommendation Summary

{analysis_data.get('recommendations', 'No recommendations available')}

---

### Summary
Data extracted and analyzed through the Regulus AI Due Diligence Pipeline.  
Includes document ingestion + NLP analysis + compliance screening.  

**Confidential — Qatar Development Bank**  
**Powered by Regulus AI**
"""
            return md_report
        
        except Exception as e:
            print(f"Error generating report: {e}")
            return "# Error\n\nFailed to generate report. Please check input data."
    
    def markdown_to_docx(self, markdown_content: str) -> Document:
        """
        Convert markdown-formatted report to DOCX
        """
        try:
            doc = Document()
            
            # Parse markdown and add to DOCX
            lines = markdown_content.split('\n')
            
            for line in lines:
                line = line.strip()
                
                if not line:
                    continue
                
                # Handle headings
                if line.startswith('# '):
                    heading = line[2:].strip()
                    p = doc.add_heading(heading, level=0)
                    p.runs[0].font.color.rgb = self.company_color
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                
                elif line.startswith('## '):
                    heading = line[3:].strip()
                    p = doc.add_heading(heading, level=1)
                    p.runs[0].font.color.rgb = self.accent_color
                
                elif line.startswith('### '):
                    heading = line[4:].strip()
                    p = doc.add_heading(heading, level=2)
                
                # Handle bold text
                elif line.startswith('**') and line.endswith('**'):
                    p = doc.add_paragraph()
                    run = p.add_run(line[2:-2])
                    run.bold = True
                
                # Handle list items
                elif line.startswith('- '):
                    doc.add_paragraph(line[2:], style='List Bullet')
                
                # Handle separator lines
                elif line.startswith('---'):
                    doc.add_paragraph()
                
                # Regular text
                else:
                    doc.add_paragraph(line)
            
            # Add footer
            doc.add_paragraph()
            footer = doc.add_paragraph("Confidential — Qatar Development Bank | Powered by Regulus AI")
            footer_format = footer.runs[0]
            footer_format.font.size = Pt(9)
            footer_format.font.italic = True
            footer_format.font.color.rgb = RGBColor(128, 128, 128)
            
            return doc
        
        except Exception as e:
            print(f"Error converting to DOCX: {e}")
            # Return basic error document
            doc = Document()
            doc.add_heading("Error", 0)
            doc.add_paragraph(f"Failed to convert report: {str(e)}")
            return doc
    
    def generate_market_analysis_report(self, data: dict) -> str:
        """Generate market analysis report"""
        try:
            company = data.get("company_name", "Unknown")
            date = data.get("date", datetime.now().strftime("%B %d, %Y"))
            
            report = f"""# Market Analysis Report

**Company:** {company}  
**Date:** {date}  

---

## Market Size & Opportunity

{data.get('market_size', 'Analysis pending')}

---

## Competitive Landscape

{data.get('competitors', 'Analysis pending')}

---

## Market Trends

{data.get('trends', 'Analysis pending')}

---

## Growth Drivers

{data.get('growth_drivers', 'Analysis pending')}

---

## Recommendation

{data.get('recommendation', 'Pending')}

---

**Confidential — Qatar Development Bank**
"""
            return report
        except:
            return "# Error\n\nFailed to generate market analysis report."
    
    def generate_financial_model_report(self, data: dict) -> str:
        """Generate financial modeling report"""
        try:
            company = data.get("company_name", "Unknown")
            
            report = f"""# Financial Model Report

**Company:** {company}  
**Generated:** {datetime.now().strftime("%B %d, %Y")}  

---

## Financial Summary

{data.get('summary', 'Pending')}

---

## Projections

{data.get('projections', 'Pending')}

---

## Key Metrics

{data.get('metrics', 'Pending')}

---

## Assumptions

{data.get('assumptions', 'Pending')}

---

**Confidential — Qatar Development Bank**
"""
            return report
        except:
            return "# Error\n\nFailed to generate financial model report."
    
    def generate_investment_memo(self, data: dict) -> str:
        """Generate investment memo"""
        try:
            company = data.get("company_name", "Unknown")
            
            memo = f"""# Investment Memo

**Company:** {company}  
**Date:** {datetime.now().strftime("%B %d, %Y")}  

---

## Executive Summary

{data.get('summary', 'Pending')}

---

## Investment Thesis

{data.get('thesis', 'Pending')}

---

## Financial Highlights

{data.get('financials', 'Pending')}

---

## Risks

{data.get('risks', 'Pending')}

---

## Recommendation

{data.get('recommendation', 'Pending')}

---

**CONFIDENTIAL**  
**Prepared by Regulus AI for Qatar Development Bank**
"""
            return memo
        except:
            return "# Error\n\nFailed to generate investment memo."
