"""
Template Generator with PPTX Pitch Deck Support
Generates DOCX reports and professional pitch decks for analyst review
"""
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from pptx import Presentation
from pptx.util import Inches as PPTInches, Pt as PPTPt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor as PPTRGBColor
import io

class TemplateGenerator:
    """Generate professional documents and presentations"""
    
    def markdown_to_docx(self, markdown_content):
        """Convert markdown to DOCX"""
        doc = Document()
        lines = markdown_content.split('\n')
        
        for line in lines:
            if line.startswith('# '):
                p = doc.add_heading(line[2:], level=1)
                p.runs[0].font.color.rgb = RGBColor(27, 43, 77)
            elif line.startswith('## '):
                p = doc.add_heading(line[3:], level=2)
                p.runs[0].font.color.rgb = RGBColor(22, 160, 133)
            elif line.startswith('### '):
                p = doc.add_heading(line[4:], level=3)
            elif line.startswith('| '):
                continue
            elif line.startswith('---'):
                doc.add_paragraph()
            elif line.strip():
                doc.add_paragraph(line)
        
        return doc
    
    def generate_pitch_deck(self, company_data):
        """Generate professional PPTX pitch deck"""
        prs = Presentation()
        prs.slide_width = PPTInches(10)
        prs.slide_height = PPTInches(7.5)
        
        # Define colors (matching app theme)
        DARK_BLUE = PPTRGBColor(27, 43, 77)
        TEAL = PPTRGBColor(22, 160, 133)
        WHITE = PPTRGBColor(255, 255, 255)
        LIGHT_GRAY = PPTRGBColor(224, 232, 240)
        
        def add_title_slide(title, subtitle):
            """Slide 1: Title"""
            slide = prs.slides.add_slide(prs.slide_layouts[6])
            background = slide.background
            fill = background.fill
            fill.solid()
            fill.fore_color.rgb = DARK_BLUE
            
            title_box = slide.shapes.add_textbox(PPTInches(0.5), PPTInches(2.5), PPTInches(9), PPTInches(1.5))
            title_frame = title_box.text_frame
            title_frame.word_wrap = True
            p = title_frame.paragraphs[0]
            p.text = title
            p.font.size = PPTPt(54)
            p.font.bold = True
            p.font.color.rgb = WHITE
            
            subtitle_box = slide.shapes.add_textbox(PPTInches(0.5), PPTInches(4.2), PPTInches(9), PPTInches(1))
            subtitle_frame = subtitle_box.text_frame
            p = subtitle_frame.paragraphs[0]
            p.text = subtitle
            p.font.size = PPTPt(24)
            p.font.color.rgb = TEAL
        
        def add_content_slide(title, content_dict):
            """Slide: Content with bullets"""
            slide = prs.slides.add_slide(prs.slide_layouts[6])
            background = slide.background
            fill = background.fill
            fill.solid()
            fill.fore_color.rgb = WHITE
            
            # Title bar
            title_shape = slide.shapes.add_shape(1, PPTInches(0), PPTInches(0), PPTInches(10), PPTInches(0.8))
            title_shape.fill.solid()
            title_shape.fill.fore_color.rgb = DARK_BLUE
            title_shape.line.fill.background()
            
            title_box = slide.shapes.add_textbox(PPTInches(0.5), PPTInches(0.15), PPTInches(9), PPTInches(0.6))
            title_frame = title_box.text_frame
            p = title_frame.paragraphs[0]
            p.text = title
            p.font.size = PPTPt(32)
            p.font.bold = True
            p.font.color.rgb = WHITE
            
            # Content
            content_box = slide.shapes.add_textbox(PPTInches(0.8), PPTInches(1.2), PPTInches(8.4), PPTInches(5.8))
            text_frame = content_box.text_frame
            text_frame.word_wrap = True
            
            for key, value in content_dict.items():
                p = text_frame.add_paragraph()
                p.text = f"{key}: {value}"
                p.font.size = PPTPt(14)
                p.font.color.rgb = DARK_BLUE
                p.space_before = PPTPt(8)
                p.space_after = PPTPt(8)
        
        # Slide 1: Title
        add_title_slide(
            company_data['company_name'],
            f"{company_data['stage']} | {company_data['industry']}"
        )
        
        # Slide 2: Company Overview
        add_content_slide("Company Overview", {
            "Founded": company_data.get('founded', 'N/A'),
            "Location": company_data.get('location', 'N/A'),
            "Industry": company_data.get('industry', 'N/A'),
            "Business Model": company_data.get('business_model', 'To be documented')[:100]
        })
        
        # Slide 3: Investment Opportunity
        add_content_slide("Investment Opportunity", {
            "Investment Amount": company_data.get('deal_size', 'N/A'),
            "Pre-Money Valuation": company_data.get('valuation', 'N/A'),
            "Ownership Stake": f"{company_data.get('ownership', 'TBD')}%",
            "Investment Thesis": company_data.get('investment_thesis', 'To be developed')[:100]
        })
        
        # Slide 4: Market Opportunity
        add_content_slide("Market Opportunity", {
            "TAM": company_data.get('tam', 'N/A'),
            "Current Revenue": company_data.get('current_revenue', 'N/A'),
            "Revenue Growth": company_data.get('growth_rate', 'N/A'),
            "Key Highlights": company_data.get('key_highlights', 'To be documented')[:100]
        })
        
        # Slide 5: Products & Services
        add_content_slide("Products & Services", {
            "Offering": company_data.get('products_services', 'To be documented')[:150],
            "Unique Value Prop": "Market-leading technology and team",
            "Competitive Advantage": "Strong IP and customer base"
        })
        
        # Slide 6: Recommendation
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = TEAL
        
        rec_box = slide.shapes.add_textbox(PPTInches(1), PPTInches(3), PPTInches(8), PPTInches(1.5))
        rec_frame = rec_box.text_frame
        rec_frame.word_wrap = True
        p = rec_frame.paragraphs[0]
        p.text = f"RECOMMENDATION: {company_data.get('recommendation', 'BUY')}"
        p.font.size = PPTPt(48)
        p.font.bold = True
        p.font.color.rgb = WHITE
        p.alignment = PP_ALIGN.CENTER
        
        # Footer
        footer_box = slide.shapes.add_textbox(PPTInches(0.5), PPTInches(6.8), PPTInches(9), PPTInches(0.5))
        footer_frame = footer_box.text_frame
        p = footer_frame.paragraphs[0]
        p.text = "Confidential - Qatar Development Bank | Powered by Regulus AI"
        p.font.size = PPTPt(10)
        p.font.color.rgb = WHITE
        p.alignment = PP_ALIGN.CENTER
        
        return prs
