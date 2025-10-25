"""
Template Generator for Investment Analysis Reports
Generates professional reports in multiple formats with justified text alignment
"""

from typing import Dict, Any, List
from datetime import datetime
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH  # For justified text
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import re


class TemplateGenerator:
    """Generate professional investment analysis reports"""
    
    def __init__(self):
        self.company_name = ""
        
    def generate_due_diligence_report(self, analysis_data: Dict[str, Any]) -> str:
        """Generate comprehensive due diligence report in markdown"""
        
        company = analysis_data.get('company_name', 'Company')
        analyst = analysis_data.get('analyst_name', 'Regulus AI')
        date = analysis_data.get('analysis_date', datetime.now().strftime('%B %d, %Y'))
        
        # Extract analysis sections
        financial_analysis = analysis_data.get('financial_analysis', 'Analysis pending')
        legal_analysis = analysis_data.get('legal_analysis', 'Analysis pending')
        operational_analysis = analysis_data.get('operational_analysis', 'Analysis pending')
        risk_assessment = analysis_data.get('risk_assessment', 'Assessment pending')
        recommendations = analysis_data.get('recommendations', 'Recommendations pending')
        
        report = f"""# Due Diligence Report
## {company}

**Prepared by:** {analyst}  
**Date:** {date}  
**Report Type:** Comprehensive Due Diligence Assessment

---

## Executive Summary

This report presents a comprehensive due diligence analysis of {company}, covering financial health, legal compliance, operational capabilities, and strategic positioning. The assessment provides actionable insights for investment decision-making.

---

## 1. Financial Analysis

{financial_analysis}

---

## 2. Legal & Compliance Review

{legal_analysis}

---

## 3. Operational Assessment

{operational_analysis}

---

## 4. Risk Assessment

{risk_assessment}

---

## 5. Investment Recommendations

{recommendations}

---

## Conclusion

Based on the comprehensive analysis conducted, this report provides the foundation for informed investment decision-making regarding {company}. All findings have been thoroughly evaluated and cross-referenced with supporting documentation.

**Report Status:** Complete  
**Confidence Level:** High  
**Next Steps:** Review findings with investment committee

---

*This report is confidential and intended solely for internal use by authorized personnel.*
"""
        return report
    
    def generate_investment_memo(self, analysis_data: Dict[str, Any]) -> str:
        """Generate investment memorandum in markdown"""
        
        company = analysis_data.get('company_name', 'Company')
        analyst = analysis_data.get('analyst_name', 'Regulus AI')
        date = analysis_data.get('analysis_date', datetime.now().strftime('%B %d, %Y'))
        
        opportunity = analysis_data.get('opportunity_overview', 'Investment opportunity analysis')
        market = analysis_data.get('market_analysis', 'Market analysis')
        financials = analysis_data.get('financial_highlights', 'Financial overview')
        risks = analysis_data.get('risk_factors', 'Risk assessment')
        recommendation = analysis_data.get('investment_recommendation', 'Investment recommendation')
        
        memo = f"""# Investment Memorandum
## {company}

**Prepared by:** {analyst}  
**Date:** {date}  
**Document Type:** Investment Analysis Memo

---

## Executive Summary

This investment memorandum evaluates {company} as a potential investment opportunity. The analysis covers market positioning, financial performance, growth potential, and associated risks.

---

## Investment Opportunity

{opportunity}

---

## Market Analysis

{market}

---

## Financial Highlights

{financials}

---

## Risk Factors

{risks}

---

## Investment Recommendation

{recommendation}

---

## Conclusion

This memorandum provides a comprehensive assessment of the investment opportunity presented by {company}. The recommendation is based on thorough analysis of available data and market conditions.

---

*This document is confidential and intended for authorized recipients only.*
"""
        return memo
    
    def generate_market_analysis_report(self, analysis_data: Dict[str, Any]) -> str:
        """Generate market & competitive analysis report in markdown"""
        
        company = analysis_data.get('company_name', 'Company')
        analyst = analysis_data.get('analyst_name', 'Regulus AI')
        date = datetime.now().strftime('%B %d, %Y')
        
        market_overview = analysis_data.get('market_overview', 'Market overview analysis')
        competitive_landscape = analysis_data.get('competitive_landscape', 'Competitive analysis')
        market_trends = analysis_data.get('market_trends', 'Market trends analysis')
        positioning = analysis_data.get('market_positioning', 'Market positioning assessment')
        
        report = f"""# Market & Competitive Analysis Report
## {company}

**Prepared by:** {analyst}  
**Date:** {date}  
**Report Type:** Market Intelligence Assessment

---

## Executive Summary

This report provides comprehensive market and competitive analysis for {company}, examining market dynamics, competitive positioning, industry trends, and strategic opportunities.

---

## 1. Market Overview

{market_overview}

---

## 2. Competitive Landscape

{competitive_landscape}

---

## 3. Market Trends & Dynamics

{market_trends}

---

## 4. Competitive Positioning

{positioning}

---

## Strategic Insights

The analysis reveals key market dynamics and competitive factors that influence {company}'s strategic positioning and growth potential. These insights inform investment evaluation and strategic planning.

---

*This report contains confidential market intelligence and competitive analysis.*
"""
        return report
    
    def markdown_to_docx(self, markdown_content: str) -> Document:
        """Convert markdown to DOCX with justified text alignment"""
        
        doc = Document()
        
        # Set default font
        style = doc.styles['Normal']
        font = style.font
        font.name = 'Calibri'
        font.size = Pt(11)
        
        lines = markdown_content.split('\n')
        in_table = False
        table_rows = []
        
        for line in lines:
            line_stripped = line.strip()
            
            # Skip empty lines
            if not line_stripped:
                if in_table:
                    self._create_table(doc, table_rows)
                    table_rows = []
                    in_table = False
                continue
            
            # Headers
            if line_stripped.startswith('# '):
                if in_table:
                    self._create_table(doc, table_rows)
                    table_rows = []
                    in_table = False
                h = doc.add_heading(line_stripped[2:], level=1)
                h.alignment = WD_ALIGN_PARAGRAPH.CENTER
                
            elif line_stripped.startswith('## '):
                if in_table:
                    self._create_table(doc, table_rows)
                    table_rows = []
                    in_table = False
                h = doc.add_heading(line_stripped[3:], level=2)
                h.alignment = WD_ALIGN_PARAGRAPH.LEFT
                
            elif line_stripped.startswith('### '):
                if in_table:
                    self._create_table(doc, table_rows)
                    table_rows = []
                    in_table = False
                h = doc.add_heading(line_stripped[4:], level=3)
                h.alignment = WD_ALIGN_PARAGRAPH.LEFT
                
            elif line_stripped.startswith('#### '):
                if in_table:
                    self._create_table(doc, table_rows)
                    table_rows = []
                    in_table = False
                h = doc.add_heading(line_stripped[5:], level=4)
                h.alignment = WD_ALIGN_PARAGRAPH.LEFT
            
            # Horizontal rule
            elif line_stripped.startswith('---'):
                if in_table:
                    self._create_table(doc, table_rows)
                    table_rows = []
                    in_table = False
                doc.add_paragraph('_' * 50)
            
            # Tables
            elif '|' in line_stripped:
                if not in_table:
                    in_table = True
                if not line_stripped.startswith('|---'):  # Skip separator lines
                    cells = [cell.strip() for cell in line_stripped.split('|')[1:-1]]
                    table_rows.append(cells)
            
            # Bold text (standalone)
            elif line_stripped.startswith('**') and line_stripped.endswith('**'):
                if in_table:
                    self._create_table(doc, table_rows)
                    table_rows = []
                    in_table = False
                p = doc.add_paragraph()
                run = p.add_run(line_stripped.strip('*'))
                run.bold = True
                p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY  # Justified
            
            # Bullet points
            elif line_stripped.startswith('- ') or line_stripped.startswith('* '):
                if in_table:
                    self._create_table(doc, table_rows)
                    table_rows = []
                    in_table = False
                p = doc.add_paragraph(line_stripped[2:], style='List Bullet')
                p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY  # Justified bullets
            
            # Numbered lists
            elif len(line_stripped) > 2 and line_stripped[0].isdigit() and line_stripped[1:3] == '. ':
                if in_table:
                    self._create_table(doc, table_rows)
                    table_rows = []
                    in_table = False
                p = doc.add_paragraph(line_stripped[3:], style='List Number')
                p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY  # Justified numbers
            
            # Regular paragraphs (MAIN CONTENT - JUSTIFIED)
            else:
                if in_table:
                    self._create_table(doc, table_rows)
                    table_rows = []
                    in_table = False
                p = doc.add_paragraph()
                self._process_inline_formatting(p, line_stripped)
                p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY  # JUSTIFIED TEXT
        
        # Handle remaining table
        if in_table and table_rows:
            self._create_table(doc, table_rows)
        
        return doc
    
    def _process_inline_formatting(self, paragraph, text):
        """Process inline markdown formatting (bold, italic)"""
        
        # Pattern for bold and italic
        pattern = r'(\*\*.*?\*\*|\*.*?\*|`.*?`)'
        parts = re.split(pattern, text)
        
        for part in parts:
            if not part:
                continue
            
            if part.startswith('**') and part.endswith('**'):
                # Bold
                run = paragraph.add_run(part[2:-2])
                run.bold = True
            elif part.startswith('*') and part.endswith('*'):
                # Italic
                run = paragraph.add_run(part[1:-1])
                run.italic = True
            elif part.startswith('`') and part.endswith('`'):
                # Code
                run = paragraph.add_run(part[1:-1])
                run.font.name = 'Courier New'
                run.font.size = Pt(10)
            else:
                # Regular text
                paragraph.add_run(part)
    
    def _create_table(self, doc, table_data):
        """Create a formatted table in the document"""
        
        if not table_data:
            return
        
        # Create table
        table = doc.add_table(rows=len(table_data), cols=len(table_data[0]))
        table.style = 'Light Grid Accent 1'
        
        # Fill table
        for i, row_data in enumerate(table_data):
            row = table.rows[i]
            for j, cell_text in enumerate(row_data):
                cell = row.cells[j]
                cell.text = cell_text
                
                # Header row formatting
                if i == 0:
                    for paragraph in cell.paragraphs:
                        for run in paragraph.runs:
                            run.font.bold = True
                        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                else:
                    # Data rows - justified
                    for paragraph in cell.paragraphs:
                        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        
        # Add spacing after table
        doc.add_paragraph()
    
    def save_as_docx(self, markdown_content: str, filename: str):
        """Save markdown content as DOCX file"""
        doc = self.markdown_to_docx(markdown_content)
        doc.save(filename)
        return filename
    
    def generate_deal_sourcing_report(self, deals_data: List[Dict[str, Any]]) -> str:
        """Generate daily potential deals report in markdown"""
        
        date = datetime.now().strftime('%B %d, %Y')
        
        report = f"""# Daily Potential Deals Report
**Date:** {date}  
**Prepared by:** Regulus AI  
**Report Type:** Deal Flow Analysis

---

## Executive Summary

This report presents {len(deals_data)} potential investment opportunities identified through systematic deal sourcing across multiple channels. Each opportunity has been preliminarily evaluated based on sector fit, stage, and strategic alignment.

---

## Deal Pipeline Overview

"""
        
        for i, deal in enumerate(deals_data, 1):
            company_name = deal.get('company_name', f'Company {i}')
            sector = deal.get('sector', 'Not specified')
            stage = deal.get('stage', 'Not specified')
            description = deal.get('description', 'No description available')
            source = deal.get('source', 'Internal sourcing')
            
            report += f"""### Deal {i}: {company_name}

**Sector:** {sector}  
**Stage:** {stage}  
**Source:** {source}

**Overview:**  
{description}

**Next Steps:** Initial screening and preliminary assessment

---

"""
        
        report += """## Recommendations

1. Conduct detailed screening of high-priority opportunities
2. Schedule preliminary discussions with founders/management
3. Request pitch decks and financial information
4. Evaluate against investment thesis and criteria

---

*This report is confidential and intended for internal deal flow management.*
"""
        
        return report
