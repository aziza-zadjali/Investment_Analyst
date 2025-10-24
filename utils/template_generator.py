"""
Unified Template & Report Generator
Generates investment memos, due diligence reports, and DOCX exports
"""

from datetime import datetime
from typing import Dict, List, Any
from io import BytesIO
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font


class TemplateGenerator:
    """Generate professional reports matching sample document formats"""

    # =========================================================================
    # DUE DILIGENCE REPORTS (Matching Sample Formats)
    # =========================================================================
    
    def generate_due_diligence_report_solartech_format(self, data: Dict[str, Any]) -> str:
        """
        Generate DD Report matching 'Due_diligence_report.pdf' sample structure
        """
        date_now = datetime.now().strftime("%B %d, %Y")
        
        report = f"""# Due Diligence Report

**Company:** {data.get('company_name', 'Target Company')}  
**Report Date:** {date_now}  
**Prepared by:** {data.get('analyst_name', 'Investment Team')}

---

## 1. Executive Summary

This report summarizes the due diligence findings for **{data.get('company_name', 'the target company')}** conducted on {data.get('review_dates', date_now)}. The goal was to assess key risks, liabilities, and opportunities to ensure informed decision-making.

---

## 2. Scope of Review

- **Financial:** {data.get('financial_scope', 'Reviewed financial statements and cash flow for recent fiscal years.')}
- **Legal:** {data.get('legal_scope', 'Assessed compliance with corporate and regulatory laws.')}
- **Operational:** {data.get('operational_scope', 'Evaluated business processes and operational efficiency.')}
- **Commercial:** {data.get('commercial_scope', 'Analyzed market positioning and competitive landscape.')}

---

## 3. Key Findings

| Category | Findings | Risk Level |
|----------|----------|------------|
| **Financial** | {data.get('financial_findings', 'Consistent revenue growth, stable margins.')} | {data.get('financial_risk', 'Medium')} |
| **Legal** | {data.get('legal_findings', 'No major pending litigation identified.')} | {data.get('legal_risk', 'Low')} |
| **Operational** | {data.get('operational_findings', 'Well-established processes with room for optimization.')} | {data.get('operational_risk', 'Low')} |
| **Commercial** | {data.get('commercial_findings', 'Strong market presence, limited geographic expansion.')} | {data.get('commercial_risk', 'Medium')} |

---

## 4. Recommendations

{data.get('recommendations', '''
1. Address identified legal risks proactively to avoid future complications.
2. Expand market presence through strategic partnerships.
3. Optimize operational capacity to meet future growth demands.
''')}

---

## 5. Conclusion

{data.get('conclusion', f'''
The due diligence process identified strong growth potential in {data.get('company_name', 'the company')}'s market positioning but highlighted certain operational and legal risks. Proceed with the investment while addressing these risks to maximize value.
''')}

---

**Authorized by:**  
{data.get('analyst_name', 'Analyst Name')}  
{data.get('firm_name', 'Your Firm Name')}  
**Date:** {date_now}
"""
        return report

    def generate_due_diligence_report_early_stage_format(self, data: Dict[str, Any]) -> str:
        """
        Generate DD Report matching 'Due-Diligence-Report-Template-for-Early-Stage-Investors.docx' format
        """
        date_now = datetime.now().strftime("%B %d, %Y")
        
        report = f"""# Due Diligence Report Template for Early Stage Investors

**Company:** {data.get('company_name', 'Company Name')}  
**CEO:** {data.get('ceo_name', 'CEO Name')}  
**Report Date:** {date_now}

---

## Company Description

{data.get('company_description', 'Insert 1-2 paragraph summary description of company and its market here.')}

---

## Due Diligence Assessment

| **Topic** | **Rating** | **Remarks** |
|-----------|------------|-------------|
| **Investment Thesis** | {data.get('investment_thesis_rating', 'TBD')} | {data.get('investment_thesis', 'This is where you explain the overall logic of the investment and how investors will make money.')} |
| **What Needs To Be Believed (WNTBB)** | {data.get('wntbb_rating', 'TBD')} | {data.get('wntbb', 'Key risks that need to be assumed in order to invest. If an investor cannot make peace with an item on this list, they should not invest.')} |
| **Failure Risk** | {data.get('failure_risk_rating', 'TBD')} | {data.get('failure_risk', 'Main weaknesses in the plan and the degree to which they are mitigated.')} |
| **Leadership Assessment** | {data.get('leadership_rating', 'TBD')} | {data.get('leadership_assessment', 'Assessment of the management team. Does the CEO possess the experience and leadership abilities to succeed?')} |
| **Technology, IP and Product Roadmap** | {data.get('tech_rating', 'TBD')} | {data.get('tech_assessment', 'Assessment of the technology and technology risk as well as the IP situation.')} |
| **Customer Need and Go-To-Market Plan** | {data.get('gtm_rating', 'TBD')} | {data.get('gtm_assessment', 'Assessment of the plan to take the product to market.')} |
| **Uniqueness and Competition** | {data.get('competition_rating', 'TBD')} | {data.get('competition_assessment', 'Assessment of the overall competitiveness and defensibility of the offering.')} |
| **Market Size and Market Opportunity** | {data.get('market_rating', 'TBD')} | {data.get('market_assessment', 'Assessment of the actual addressable market.')} |
| **Financial Projections and Funding Strategy** | {data.get('financial_rating', 'TBD')} | {data.get('financial_assessment', 'Assessment of the financial plan and capital raising strategy.')} |
| **Exit Strategy** | {data.get('exit_rating', 'TBD')} | {data.get('exit_assessment', 'Assessment of the likely exit opportunities.')} |
| **Deal Terms and Payoff** | {data.get('terms_rating', 'TBD')} | {data.get('terms_assessment', 'Summary of the relationship between the deal terms and the expected investor return.')} |

---

## Individual Assessments

| **Team Member** | **Rating** | **Summary Remarks** |
|-----------------|------------|---------------------|
| {data.get('member1_name', 'Name 1')} | {data.get('member1_rating', '+')} | {data.get('member1_remarks', 'Positive assessment.')} |
| {data.get('member2_name', 'Name 2')} | {data.get('member2_rating', '0')} | {data.get('member2_remarks', 'Neutral assessment.')} |
| {data.get('member3_name', 'Name 3')} | {data.get('member3_rating', '++')} | {data.get('member3_remarks', 'Very positive assessment.')} |

---

### Rating Key

**(++)** = Very Positive  
**(+)** = Positive  
**(0)** = Neutral  
**(--)** = Negative but issues can be overcome  
**( / )** = Very Negative, issues cannot be overcome

---

**Prepared by:** {data.get('analyst_name', 'Analyst Team')}  
**Date:** {date_now}
"""
        return report

    # =========================================================================
    # DOCX GENERATION
    # =========================================================================
    
    def generate_docx_report(self, report_text: str, report_title: str = "Due Diligence Report") -> BytesIO:
        """
        Convert markdown report text to a professional DOCX document
        """
        try:
            from docx import Document
            from docx.shared import Pt, Inches
            from docx.enum.text import WD_ALIGN_PARAGRAPH
            
            doc = Document()
            
            # Document title
            title = doc.add_heading(report_title, level=0)
            title.alignment = WD_ALIGN_PARAGRAPH.CENTER
            
            # Process report text line by line
            lines = report_text.split('\n')
            i = 0
            while i < len(lines):
                line = lines[i].strip()
                i += 1
                
                if not line:
                    continue
                
                # Handle different markdown elements
                if line.startswith('# '):
                    doc.add_heading(line[2:], level=1)
                elif line.startswith('## '):
                    doc.add_heading(line[3:], level=2)
                elif line.startswith('### '):
                    doc.add_heading(line[4:], level=3)
                elif line.startswith('**') and line.endswith('**'):
                    p = doc.add_paragraph()
                    run = p.add_run(line[2:-2])
                    run.bold = True
                elif line.startswith('---'):
                    # Horizontal line
                    doc.add_paragraph('_' * 50)
                elif line.startswith('- '):
                    doc.add_paragraph(line[2:], style='List Bullet')
                elif '|' in line and not line.startswith('|--'):
                    # Table row - skip for now (simplified)
                    continue
                else:
                    doc.add_paragraph(line)
            
            # Save to BytesIO
            buffer = BytesIO()
            doc.save(buffer)
            buffer.seek(0)
            return buffer
            
        except ImportError:
            # Fallback if python-docx not available
            return BytesIO(report_text.encode('utf-8'))

    # =========================================================================
    # LEGACY & BACKWARDS COMPATIBILITY
    # =========================================================================
    
    def generate_due_diligence_report(self, data: Dict[str, Any]) -> str:
        """
        Main DD report generator - defaults to SolarTech format
        """
        report_format = data.get('format', 'solartech')
        
        if report_format == 'early_stage':
            return self.generate_due_diligence_report_early_stage_format(data)
        else:
            return self.generate_due_diligence_report_solartech_format(data)

    def generate_investment_memo(self, data: Dict[str, Any]) -> str:
        """Full professional-grade investment memo"""
        date_now = datetime.now().strftime("%B %d, %Y")

        memo = f"""# Investment Memo — {data.get('company_name', 'Company N/A')}

**Date:** {date_now}  
**Prepared by:** {data.get('analyst_name', 'Analyst Team')}  
**Department:** Corporate Development  
**Industry:** {data.get('industry', 'TBD')}  
**Investment Type:** {data.get('investment_type', 'Equity')}

---

## I. Executive Summary
{data.get('executive_summary', 'Summary pending.')}

---

## II. Investment Rationale

### 1. Market Opportunity
{data.get('market_opportunity', 'Overview pending.')}

### 2. Competitive Advantage
{data.get('competitive_advantage', 'Details pending.')}

### 3. Financial Performance
| Metric | Value |
|--------|--------|
| Revenue | {data.get('revenue', 'N/A')} |
| EBITDA | {data.get('ebitda', 'N/A')} |
| Cash Flow | {data.get('cash_flow', 'N/A')} |

---

## III. Key Investment Terms
| Term | Detail |
|------|--------|
| Investment Size | ${data.get('investment_amount', 'N/A')} |
| Valuation | ${data.get('valuation', 'N/A')} |
| Equity Ownership | {data.get('ownership', 'N/A')}% |

---

## IV. Risk Factors
{data.get('risks', 'No risks identified.')}

## V. Mitigation Plans
{data.get('mitigation', 'To be defined.')}

---

## VI. Recommendation
{data.get('recommendation', 'Pending final review.')}

---

**Prepared By:** {data.get('analyst_name', 'Analyst')}  
**Date:** {date_now}
"""
        return memo

    def generate_daily_deals_report(self, deals: List[Dict[str, Any]], criteria: Dict[str, Any]) -> str:
        """Generate markdown format for Daily Deals reports"""
        date_today = datetime.now().strftime("%B %d, %Y")
        report = f"""# Daily Potential Deals Report  
**Date:** {date_today}  
**Generated By:** AI Investment Analyst  

### Filter Criteria
- **Sectors:** {', '.join(criteria.get('sectors', []))}
- **Stage Range:** {criteria.get('stage_range', 'All')}
- **Revenue Range:** {criteria.get('revenue_range', 'N/A')}
- **Geography:** {', '.join(criteria.get('geography', []))}

---

"""
        for i, deal in enumerate(deals, start=1):
            report += f"""### {i}. {deal.get('company', 'Unnamed Deal')}
- **Sector:** {deal.get('sector', 'N/A')}
- **Stage:** {deal.get('stage', 'N/A')}
- **Region:** {deal.get('region', 'N/A')}
- **Revenue:** {deal.get('revenue', 'N/A')}
- **Source:** {deal.get('source', 'N/A')}
- **Founded:** {deal.get('founded', 'Unknown')}
- **Employees:** {deal.get('employees', 'N/A')}
- **Description:** {deal.get('description', 'Not available')}
- **Link:** {deal.get('url', 'N/A')}

---
"""
        report += "\n\n**End of Report**"
        return report

    def generate_financial_model(self, data: Dict[str, Any]) -> BytesIO:
        """Generate Excel output for deal's financial model"""
        wb = Workbook()
        ws = wb.active
        ws.title = "Summary"

        ws["A1"] = "Financial Model Template"
        ws["A1"].font = Font(size=16, bold=True)

        headers = [
            ("Company Name", "company_name"),
            ("Revenue", "revenue"),
            ("EBITDA", "ebitda"),
            ("Valuation", "valuation"),
            ("Ownership (%)", "ownership"),
            ("Investment Amount", "investment_amount"),
        ]

        row = 3
        for label, key in headers:
            ws[f"A{row}"] = label
            ws[f"B{row}"] = data.get(key, "N/A")
            row += 1

        wb.create_sheet("Assumptions - Monthly")
        wb.create_sheet("P&L - Monthly")
        wb.create_sheet("Cash Flow - Monthly")
        wb.create_sheet("Summary - Annual")

        buffer = BytesIO()
        wb.save(buffer)
        buffer.seek(0)
        return buffer
