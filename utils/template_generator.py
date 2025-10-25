"""
Template Generator - QDB / Regulus Branded Professional Reports
Handles Markdown and DOCX generation with logos, layout, and formatting
"""

import markdown
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
import os
from io import BytesIO


class TemplateGenerator:
    def __init__(self):
        self.qdb_logo_path = "QDB_Logo.png"
        self.regulus_logo_path = "regulus_logo.png"

    # ---------------------------
    # MAIN GENERATION METHODS
    # ---------------------------

    def generate_due_diligence_report(self, data):
        """Generate Markdown report text for Due Diligence"""
        report = f"""# 🌍 DUE DILIGENCE REPORT
### {data['company_name']}

**Industry:** {data.get('industry', 'N/A')}  
**Analyst:** {data.get('analyst_name', 'Regulus AI')}  
**Date:** {data.get('analysis_date', 'N/A')}  

---

## 1. EXECUTIVE SUMMARY
{data.get('executive_summary', 'No summary available.')}

---

## 2. FINANCIAL ANALYSIS
{data.get('financial_analysis', 'Not provided.')}

---

## 3. LEGAL AND COMPLIANCE
{data.get('legal_analysis', 'N/A')}

---

## 4. OPERATIONAL EVALUATION
{data.get('operational_analysis', 'N/A')}

---

## 5. RISK ASSESSMENT
{data.get('risk_assessment', 'N/A')}

---

## 6. RECOMMENDATIONS
{data.get('recommendations', 'N/A')}

---

### 📑 SCREENING RESULTS
- **Sanctions List:** {data.get('sanctions_screening', 'N/A')}
- **PEP Check:** {data.get('pep_screening', 'N/A')}
- **Adverse Media:** {data.get('adverse_media', 'N/A')}
- **FATCA Compliance:** {data.get('fatca_compliance', 'N/A')}

---

### 📊 SOURCES
{", ".join(data.get('data_sources', [])) if data.get('data_sources') else 'Documents and public records'}

---

**Prepared by Regulus AI | Qatar Development Bank (QDB)**  
"""
        return report

    def generate_market_analysis_report(self, data):
        """Generate Markdown for Market Analysis"""
        report = f"""# 📈 MARKET ANALYSIS REPORT
### {data['company_name']}

**Industry:** {data['industry']} | **Sector:** {data['sector']}  
**Date:** {data.get('analysis_date', 'N/A')}  

---

## 1. EXECUTIVE SUMMARY
{data.get('executive_summary', 'Overview not provided.')}

---

## 2. MARKET OVERVIEW
{data.get('market_overview', '')}

---

## 3. MARKET SIZE AND OPPORTUNITY
{data.get('market_size', '')}

---

## 4. COMPETITIVE ANALYSIS
{data.get('competitive_analysis', '')}

---

## 5. REGULATORY ENVIRONMENT
{data.get('regulatory_environment', '')}

---

## 6. TRENDS AND DRIVERS
{data.get('trends', '')}

---

## 7. SWOT ANALYSIS
{data.get('swot_analysis', '')}

---

## 8. RECOMMENDATIONS
{data.get('recommendations', 'Further investigation recommended.')}

---

**Prepared by Regulus AI | Qatar Development Bank (QDB)**  
"""
        return report

    def generate_investment_memo(self, data):
        """Generate Markdown for Investment Memo with optional scoring framework"""
        base = f"""# 📝 INVESTMENT MEMORANDUM
### {data['company_name']}

**Stage:** {data['stage']}  
**Analysis Date:** {data['analysis_date']}  
**Investment Amount:** {data['investment_size']} | **Valuation:** {data['valuation']} | **Ownership:** {data['ownership']}  
**Recommendation:** **{data['recommendation']}**

---

## 1. EXECUTIVE SUMMARY
{data.get('investment_thesis', '')}

---

## 2. KEY HIGHLIGHTS
{data.get('key_highlights', '')}

---

## 3. BUSINESS OVERVIEW
### Model
{data.get('business_model', '')}

### Products & Services
{data.get('products_services', '')}

---

## 4. MARKET ANALYSIS
### TAM / SAM / SOM
- **TAM:** {data.get('tam', 'N/A')}
- **SAM:** {data.get('sam', 'N/A')}
- **SOM:** {data.get('som', 'N/A')}

### Competitive Landscape
{data.get('competitive_landscape', '')}

---

## 5. FINANCIAL OVERVIEW
- **Annual Revenue (ARR):** {data.get('current_revenue', 'N/A')}
- **Growth Rate:** {data.get('revenue_growth', 'N/A')}
- **Gross Margin:** {data.get('gross_margin', 'N/A')}
- **Runway:** {data.get('runway', 'N/A')}
- **LTV/CAC:** {data.get('unit_economics', 'N/A')}

---

## 6. TEAM OVERVIEW
{data.get('team_info', '')}

---

## 7. RISKS & MITIGATION
- **Risks:** {data.get('business_risks', '')}  
- **Mitigation:** {data.get('risk_mitigation', '')}

---
"""

        # Include scoring if available
        if data.get('scoring'):
            s = data['scoring']
            base += f"""## 8. STRATEGIC ASSESSMENT
### Gulf Resonance Scoring

| Dimension | Score | Description |
|------------|--------|-------------|
| Strategic Clarity | {s['strategic_clarity']}/10 | Vision and mission clarity |
| Symbolic Fluency | {s['symbolic_fluency']}/10 | Communication & branding |
| Execution Discipline | {s['execution_discipline']}/10 | Team consistency |
| Archetypal Fit | {s['archetypal_fit']}/10 | Alignment with QDB strategy |
| Gulf Resonance | {s['gulf_resonance']}/10 | Regional cultural fit |

**Composite Score:** {s['composite_score']:.1f}/10

---
"""
        base += "\n**Prepared by Regulus AI | Qatar Development Bank (QDB)**"
        return base

    # ---------------------------
    # MARKDOWN TO DOCX CONVERTER
    # ---------------------------

    def markdown_to_docx(self, markdown_text):
        """Convert markdown text to styled DOCX with logos and brand formatting"""
        html = markdown.markdown(markdown_text)
        document = Document()

        # Insert header with logos
        header = document.sections[0].header
        header_para = header.paragraphs[0]
        header_para.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        if os.path.exists(self.qdb_logo_path) and os.path.exists(self.regulus_logo_path):
            run = header_para.add_run()
            run.add_picture(self.qdb_logo_path, width=Inches(1.2))
            run.add_text("  " * 5)
            run.add_picture(self.regulus_logo_path, width=Inches(1.2))
        else:
            header_para.add_run("Qatar Development Bank | Regulus AI")

        document.add_paragraph()

        # Add HTML text
        paragraphs = html.split("\n")
        for p in paragraphs:
            if p.strip():
                para = document.add_paragraph()
                run = para.add_run(p)
                para_format = para.paragraph_format
                para_format.space_after = Pt(6)
                font = run.font
                font.name = "Calibri"
                font.size = Pt(11)
                if p.startswith("#"):
                    para.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
                    font.size = Pt(14)
                    font.bold = True

        # Footer
        section = document.sections[0]
        footer = section.footer
        footer_para = footer.paragraphs[0]
        footer_para.text = "CONFIDENTIAL | Qatar Development Bank (QDB) | Regulus AI"
        footer_para.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        footer_para.runs[0].font.size = Pt(9)
        footer_para.runs[0].font.color.rgb = RGBColor(100, 100, 100)

        return document
