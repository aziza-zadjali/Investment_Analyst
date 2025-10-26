"""
Template Generator - Professional Report Generation
COMPLETE: Includes DOCX + PPTX generation with all existing methods
"""
from io import BytesIO
from datetime import datetime
import os

try:
    from docx import Document
    from docx.shared import Inches, Pt, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.enum.table import WD_ALIGN_VERTICAL
    HAS_DOCX = True
except ImportError:
    HAS_DOCX = False

try:
    from pptx import Presentation
    from pptx.util import Inches as PptxInches, Pt as PptxPt
    from pptx.enum.text import PP_ALIGN
    from pptx.dml.color import RGBColor as PptxRGBColor
    HAS_PPTX = True
except ImportError:
    HAS_PPTX = False


class TemplateGenerator:
    """Professional template generator for all report types"""
    
    def __init__(self):
        self.company_color = RGBColor(27, 43, 77) if HAS_DOCX else None
        self.accent_color = RGBColor(22, 160, 133) if HAS_DOCX else None
        self.qdb_logo_path = "QDB_Logo.png"
    
    # ========== EXISTING METHODS - UNCHANGED ==========
    
    def generate_due_diligence_report(self, analysis_data: dict) -> str:
        """EXISTING - Unchanged for other pages"""
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
**{company}** | {industry}

## Executive Summary
{date} | {analyst}

## 1. Company Overview
- **Company:** {company}
- **Industry:** {industry}

## 2. Financial Analysis
{financial}

## 3. Operational Analysis
{operational}

## 4. Market Analysis
{market}

## 5. Legal & Compliance
{legal}

## 6. Team Assessment
{team}

## Recommendation
**{analysis_data.get('recommendation', 'TBD')}**
"""
        return report
    
    def generate_market_analysis_report(self, analysis_data: dict, web_data: dict = None) -> str:
        """EXISTING - Unchanged for other pages"""
        company = analysis_data.get('company_name', 'Company')
        industry = analysis_data.get('industry', 'Industry')
        date = analysis_data.get('analysis_date', datetime.now().strftime('%B %d, %Y'))
        geo = analysis_data.get('geographic_markets', 'Global')
        areas = analysis_data.get('analysis_areas', [])
        
        news_summary = ""
        if web_data:
            news_summary = self._format_news_data(web_data)
        
        areas_list = '\n'.join([f"- {area}" for area in areas])
        
        report = f"""# Market & Competitive Analysis
**{company}** | {industry}

**Date:** {date}  
**Geographic Scope:** {geo}

## Market Overview
- **TAM:** $2.5B - $3.2B
- **Growth Rate:** 18-22% CAGR

## Competitive Landscape
- Market Share: 2-3%
- Competitors: 3-5 major players

## News Intelligence
{news_summary}

## Analysis Performed
{areas_list}
"""
        return report
    
    def _format_news_data(self, web_data: dict) -> str:
        """EXISTING - Unchanged"""
        if not web_data:
            return "No news data available"
        
        news_section = "**Sources:** 8 major outlets\n\n"
        source_count = 0
        article_count = 0
        
        for source, articles in web_data.items():
            if articles and isinstance(articles, list):
                source_count += 1
                news_section += f"**{source}** ({len(articles)})\n"
                for idx, article in enumerate(articles[:1], 1):
                    article_count += 1
                    title = article.get('title', 'Unknown')
                    news_section += f"- {title}\n"
        
        news_section += f"\n**Summary:** {source_count} sources, {article_count} articles"
        return news_section
    
    def markdown_to_docx(self, markdown_text: str):
        """EXISTING - Unchanged"""
        if not HAS_DOCX:
            raise ImportError("python-docx not installed")
        
        if not isinstance(markdown_text, str):
            raise TypeError(f"Expected string, got {type(markdown_text)}")
        
        doc = Document()
        
        for line in markdown_text.split('\n'):
            line = line.strip()
            
            if not line:
                doc.add_paragraph()
                continue
            
            if line.startswith('# '):
                p = doc.add_heading(line[2:], level=1)
                for run in p.runs:
                    run.font.size = Pt(20)
                    run.font.bold = True
                    run.font.color.rgb = self.company_color
            
            elif line.startswith('## '):
                p = doc.add_heading(line[3:], level=2)
                for run in p.runs:
                    run.font.size = Pt(16)
                    run.font.bold = True
            
            elif line.startswith('- '):
                doc.add_paragraph(line[2:], style='List Bullet')
            
            elif '**' in line:
                p = doc.add_paragraph()
                parts = line.split('**')
                for i, part in enumerate(parts):
                    if i % 2 == 0:
                        if part:
                            p.add_run(part)
                    else:
                        run = p.add_run(part)
                        run.bold = True
            
            else:
                doc.add_paragraph(line)
        
        return doc
    
    # ========== NEW METHODS - INVESTMENT MEMO ONLY ==========
    
    def generate_investment_memo_docx(self, memo_data: dict):
        """Generate professional DOCX memo with QDB logo"""
        
        if not HAS_DOCX:
            raise ImportError("python-docx not installed")
        
        doc = Document()
        
        # Add QDB logo
        if os.path.exists(self.qdb_logo_path):
            try:
                header = doc.sections[0].header
                header_para = header.paragraphs[0]
                header_run = header_para.add_run()
                header_run.add_picture(self.qdb_logo_path, width=Inches(1.5))
                header_para.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            except:
                pass
        
        # Title
        title = doc.add_heading('INVESTMENT MEMORANDUM', 0)
        title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in title.runs:
            run.font.color.rgb = self.company_color
        
        company_p = doc.add_paragraph(memo_data.get('company_name', 'Company'))
        company_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in company_p.runs:
            run.font.size = Pt(18)
            run.font.bold = True
        
        doc.add_paragraph()
        
        # Executive Summary
        doc.add_heading('I. EXECUTIVE SUMMARY', 1)
        
        exec_table = doc.add_table(rows=5, cols=2)
        exec_table.style = 'Light Grid Accent 1'
        
        exec_data = [
            ('Date:', memo_data.get('analysis_date', 'N/A')),
            ('Prepared by:', memo_data.get('analyst_name', 'Investment Team')),
            ('Company:', memo_data.get('company_name', 'N/A')),
            ('Industry:', memo_data.get('industry', 'N/A')),
            ('Stage:', memo_data.get('stage', 'N/A'))
        ]
        
        for idx, (label, value) in enumerate(exec_data):
            exec_table.rows[idx].cells[0].text = label
            exec_table.rows[idx].cells[1].text = str(value)
            exec_table.rows[idx].cells[0].paragraphs[0].runs[0].font.bold = True
        
        doc.add_paragraph()
        doc.add_heading('Investment Opportunity', 2)
        
        opp_table = doc.add_table(rows=5, cols=2)
        opp_table.style = 'Light Grid Accent 1'
        
        opp_data = [
            ('Company:', memo_data.get('company_name', 'N/A')),
            ('Industry:', memo_data.get('industry', 'N/A')),
            ('Investment Type:', 'Equity'),
            ('Amount:', memo_data.get('investment_size', 'N/A')),
            ('Valuation:', memo_data.get('valuation', 'N/A'))
        ]
        
        for idx, (label, value) in enumerate(opp_data):
            opp_table.rows[idx].cells[0].text = label
            opp_table.rows[idx].cells[1].text = str(value)
            opp_table.rows[idx].cells[0].paragraphs[0].runs[0].font.bold = True
        
        doc.add_page_break()
        
        # Investment Rationale
        doc.add_heading('II. INVESTMENT RATIONALE', 1)
        
        doc.add_heading('1. Market Opportunity', 2)
        doc.add_paragraph(memo_data.get('market_trends', 'Market analysis pending'))
        
        doc.add_paragraph().add_run('Market Size:').bold = True
        market_items = [
            f"TAM: {memo_data.get('tam', 'N/A')}",
            f"SAM: {memo_data.get('sam', 'N/A')}",
            f"SOM: {memo_data.get('som', 'N/A')}"
        ]
        for item in market_items:
            doc.add_paragraph(item, style='List Bullet')
        
        doc.add_heading('2. Competitive Advantage', 2)
        doc.add_paragraph(memo_data.get('competitive_landscape', 'Competitive analysis pending'))
        
        doc.add_heading('3. Financial Performance', 2)
        fin_items = [
            f"Revenue (ARR): {memo_data.get('current_revenue', 'N/A')}",
            f"Growth: {memo_data.get('revenue_growth', 'N/A')}",
            f"Gross Margin: {memo_data.get('gross_margin', 'N/A')}",
            f"Burn Rate: {memo_data.get('burn_rate', 'N/A')}",
            f"Runway: {memo_data.get('runway', 'N/A')}",
            f"Unit Economics: {memo_data.get('unit_economics', 'N/A')}"
        ]
        for item in fin_items:
            doc.add_paragraph(item, style='List Bullet')
        
        doc.add_page_break()
        
        # Investment Terms
        doc.add_heading('III. INVESTMENT TERMS', 1)
        
        terms_table = doc.add_table(rows=7, cols=2)
        terms_table.style = 'Medium Grid 1 Accent 1'
        
        terms_data = [
            ('Type', 'Equity'),
            ('Amount', memo_data.get('investment_size', 'N/A')),
            ('Valuation', f"{memo_data.get('valuation', 'N/A')} (Pre-money)"),
            ('Ownership', memo_data.get('ownership', 'N/A')),
            ('Horizon', '5 Years'),
            ('Expected ROI', '25-35%'),
            ('Exit Strategy', 'Acquisition/IPO')
        ]
        
        for idx, (label, value) in enumerate(terms_data):
            terms_table.rows[idx].cells[0].text = label
            terms_table.rows[idx].cells[1].text = str(value)
            terms_table.rows[idx].cells[0].paragraphs[0].runs[0].font.bold = True
        
        doc.add_page_break()
        
        # Risks
        doc.add_heading('IV. RISK FACTORS', 1)
        doc.add_heading('Key Risks', 2)
        doc.add_paragraph(memo_data.get('business_risks', 'Risk analysis pending'))
        
        doc.add_heading('Mitigation Strategies', 2)
        doc.add_paragraph(memo_data.get('risk_mitigation', 'Mitigation strategies pending'))
        
        doc.add_page_break()
        
        # Recommendation
        doc.add_heading('V. RECOMMENDATION', 1)
        
        rec_para = doc.add_paragraph()
        rec_para.add_run('Investment Recommendation: ').bold = True
        rec_para.add_run(memo_data.get('recommendation', 'TBD'))
        
        doc.add_paragraph(memo_data.get('investment_thesis', 'Investment thesis pending'))
        
        doc.add_paragraph()
        doc.add_paragraph()
        
        # Signature
        doc.add_paragraph('Approved by:').runs[0].bold = True
        doc.add_paragraph(memo_data.get('analyst_name', 'Investment Team'))
        doc.add_paragraph('Qatar Development Bank')
        doc.add_paragraph(f"Date: {datetime.now().strftime('%B %d, %Y')}")
        
        return doc
    
    def generate_pitch_deck_pptx(self, memo_data: dict):
        """Generate professional PPTX pitch deck"""
        
        if not HAS_PPTX:
            raise ImportError("python-pptx not installed")
        
        prs = Presentation()
        prs.slide_width = PptxInches(10)
        prs.slide_height = PptxInches(7.5)
        
        # Slide 1: Title
        slide1 = prs.slides.add_slide(prs.slide_layouts[6])
        
        if os.path.exists(self.qdb_logo_path):
            try:
                slide1.shapes.add_picture(self.qdb_logo_path, PptxInches(8.5), PptxInches(0.3), height=PptxInches(0.8))
            except:
                pass
        
        title_box = slide1.shapes.add_textbox(PptxInches(1), PptxInches(2.5), PptxInches(8), PptxInches(1))
        title_frame = title_box.text_frame
        title_p = title_frame.paragraphs[0]
        title_p.text = memo_data.get('company_name', 'Company')
        title_p.font.size = PptxPt(54)
        title_p.font.bold = True
        title_p.font.color.rgb = PptxRGBColor(27, 43, 77)
        title_p.alignment = PP_ALIGN.CENTER
        
        subtitle_box = slide1.shapes.add_textbox(PptxInches(1), PptxInches(3.8), PptxInches(8), PptxInches(0.6))
        subtitle_frame = subtitle_box.text_frame
        subtitle_p = subtitle_frame.paragraphs[0]
        subtitle_p.text = f"{memo_data.get('stage', 'Investment')} | {memo_data.get('industry', 'Industry')}"
        subtitle_p.font.size = PptxPt(24)
        subtitle_p.alignment = PP_ALIGN.CENTER
        
        date_box = slide1.shapes.add_textbox(PptxInches(1), PptxInches(6.5), PptxInches(8), PptxInches(0.5))
        date_frame = date_box.text_frame
        date_p = date_frame.paragraphs[0]
        date_p.text = datetime.now().strftime('%B %d, %Y')
        date_p.font.size = PptxPt(14)
        date_p.alignment = PP_ALIGN.CENTER
        
        # Slide 2: Summary
        slide2 = prs.slides.add_slide(prs.slide_layouts[1])
        title2 = slide2.shapes.title
        title2.text = "Investment Summary"
        content2 = slide2.placeholders[1].text_frame
        content2.text = f"Investment: {memo_data.get('investment_size', 'N/A')}\n"
        content2.text += f"Valuation: {memo_data.get('valuation', 'N/A')}\n"
        content2.text += f"Ownership: {memo_data.get('ownership', 'N/A')}\n"
        content2.text += f"Recommendation: {memo_data.get('recommendation', 'N/A')}"
        
        # Slide 3: Market
        slide3 = prs.slides.add_slide(prs.slide_layouts[1])
        title3 = slide3.shapes.title
        title3.text = "Market Opportunity"
        content3 = slide3.placeholders[1].text_frame
        content3.text = f"TAM: {memo_data.get('tam', 'N/A')}\n"
        content3.text += f"SAM: {memo_data.get('sam', 'N/A')}\n"
        content3.text += f"SOM: {memo_data.get('som', 'N/A')}"
        
        # Slide 4: Financials
        slide4 = prs.slides.add_slide(prs.slide_layouts[1])
        title4 = slide4.shapes.title
        title4.text = "Financial Metrics"
        content4 = slide4.placeholders[1].text_frame
        content4.text = f"Revenue: {memo_data.get('current_revenue', 'N/A')}\n"
        content4.text += f"Growth: {memo_data.get('revenue_growth', 'N/A')}\n"
        content4.text += f"Margin: {memo_data.get('gross_margin', 'N/A')}\n"
        content4.text += f"Burn: {memo_data.get('burn_rate', 'N/A')}"
        
        # Slide 5: Terms
        slide5 = prs.slides.add_slide(prs.slide_layouts[1])
        title5 = slide5.shapes.title
        title5.text = "Terms"
        content5 = slide5.placeholders[1].text_frame
        content5.text = f"Amount: {memo_data.get('investment_size', 'N/A')}\n"
        content5.text += f"Pre-Money: {memo_data.get('valuation', 'N/A')}\n"
        content5.text += f"Type: Equity\n"
        content5.text += f"Horizon: 5 Years"
        
        # Slide 6: Thank You
        slide6 = prs.slides.add_slide(prs.slide_layouts[6])
        thank_box = slide6.shapes.add_textbox(PptxInches(1), PptxInches(3), PptxInches(8), PptxInches(1))
        thank_frame = thank_box.text_frame
        thank_p = thank_frame.paragraphs[0]
        thank_p.text = "Thank You"
        thank_p.font.size = PptxPt(48)
        thank_p.font.bold = True
        thank_p.alignment = PP_ALIGN.CENTER
        
        contact_box = slide6.shapes.add_textbox(PptxInches(1), PptxInches(4.5), PptxInches(8), PptxInches(1))
        contact_frame = contact_box.text_frame
        contact_p = contact_frame.paragraphs[0]
        contact_p.text = "Qatar Development Bank"
        contact_p.font.size = PptxPt(18)
        contact_p.alignment = PP_ALIGN.CENTER
        
        return prs
    
    def generate_pitch_deck(self, memo_data: dict) -> str:
        """Backward compatible - returns markdown"""
        company = memo_data.get('company_name', 'Company')
        industry = memo_data.get('industry', 'Industry')
        
        return f"# {company}\n**{industry}** Investment Opportunity"
