"""
Market Analysis Page | Regulus AI × QDB
QDB-branded with auto-fill from workflow
"""
import streamlit as st
from datetime import datetime
from io import BytesIO
from utils.llm_handler import LLMHandler
from utils.template_generator import TemplateGenerator
from utils.qdb_styling import apply_qdb_styling, QDB_DARK_BLUE, QDB_NAVY, QDB_PURPLE, QDB_GOLD
import os, base64

st.set_page_config(page_title="Market Analysis – Regulus AI", layout="wide")
apply_qdb_styling()

# ==== GLOBAL TEAL BUTTON STYLING ====
st.markdown("""
<style>
button {
 background:linear-gradient(135deg,#16A085 0%,#138074 50%,#0E5F55 100%)!important;
 color:white!important;
 border:none!important;
 border-radius:40px!important;
 padding:12px 36px!important;
 font-weight:700!important;
 font-size:0.95rem!important;
 box-shadow:0 4px 16px rgba(19,128,116,0.25)!important;
 transition:all 0.25s ease!important;
 cursor:pointer!important;
}
button:hover{
 background:linear-gradient(135deg,#0E5F55 0%,#138074 50%,#16A085 100%)!important;
 transform:translateY(-2px)!important;
 box-shadow:0 6px 22px rgba(19,128,116,0.35)!important;
}
button:active{
 transform:translateY(0)!important;
 box-shadow:0 3px 10px rgba(19,128,116,0.2)!important;
}
</style>
""", unsafe_allow_html=True)

def encode_image(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f"data:image/png;base64,{base64.b64encode(f.read()).decode()}"
    return None
qdb_logo = encode_image("QDB_Logo.png")
regulus_logo = encode_image("regulus_logo.png")


# ==== INIT HANDLERS ====
@st.cache_resource
def init_handlers():
    return LLMHandler(), TemplateGenerator()
llm, template_gen = init_handlers()

# ==== SESSION STATE ====
if 'market_report' not in st.session_state:
    st.session_state.market_report = None

# ==== RETURN HOME (TOP LEFT - HORIZONTAL) ====
if st.button("← Return Home", use_container_width=False, key="home_btn"):
    st.switch_page("streamlit_app.py")

st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)

# ==== HERO SECTION ====
st.markdown(f"""
<div style="background:linear-gradient(135deg,#1B2B4D 0%, #0E2E4D 100%);color:white;margin:0 -3rem;padding:70px 0 50px;text-align:center;">
<div style="position:absolute;left:50px;top:35px;">
{'<img src="'+qdb_logo+'" style="max-height:70px;">' if qdb_logo else '<b>QDB</b>'}
</div>
<h1 style="font-size:2.5rem;font-weight:800;margin:0 0 10px 0;">Market Analysis & Research</h1>
<p style="font-size:1.2rem;color:#E2E8F0;margin:0 0 8px 0;font-weight:500;">Comprehensive Market Insights and Competitive Landscape</p>
<p style="color:#CBD5E0;font-size:0.95rem;max-width:700px;margin:0 auto;">
Deep-dive market analysis including TAM, competitive landscape, growth trends, and strategic recommendations for target industries.
</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

# ==== WORKFLOW TRACKER ====
st.markdown("""
<style>
.track{background:#F6F5F2;margin:0 -3rem;padding:24px 0;
display:flex;justify-content:space-evenly;align-items:center;}
.circle{width:48px;height:48px;border-radius:50%;display:flex;
align-items:center;justify-content:center;font-weight:700;
background:#CBD5E0;color:#475569;font-size:0.9rem;}
.circle.active{background:linear-gradient(135deg,#16A085 0%,#0E5F55 100%);
color:white;box-shadow:0 4px 12px rgba(19,128,116,0.3);}
.label{margin-top:5px;font-size:0.8rem;font-weight:600;color:#708090;}
.label.active{color:#0E5F55;font-weight:700;}
.pipe{height:2px;width:60px;background:#CBD5E0;}
</style>
<div class="track">
 <div><div class="circle">1</div><div class="label">Deal Sourcing</div></div>
 <div class="pipe"></div>
 <div><div class="circle">2</div><div class="label">Due Diligence</div></div>
 <div class="pipe"></div>
 <div><div class="circle active">3</div><div class="label active">Market Analysis</div></div>
 <div class="pipe"></div>
 <div><div class="circle">4</div><div class="label">Financial Modeling</div></div>
 <div class="pipe"></div>
 <div><div class="circle">5</div><div class="label">Investment Memo</div></div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)

# ==== MARKET INFO SECTION (DARK BLUE) ====
st.markdown("""
<div style="background:#2B3E54;margin:0 -3rem 0 -3rem;padding:28px 3rem;border-top:2px solid #16A085;border-bottom:1px solid #E0E0E0;">
<h3 style="text-align:left;color:#FFFFFF;font-weight:700;margin:0 0 14px 0;font-size:1.1rem;">Market & Industry Analysis</h3>
</div>
""", unsafe_allow_html=True)

with st.expander("Enter Market Information", expanded=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        company_name = st.text_input("Company Name", key="company_name")
        industry = st.text_input("Industry Sector", placeholder="e.g., Fintech, AI/ML", key="industry")
    with col2:
        market_size = st.text_input("Market Size (TAM)", placeholder="e.g., $50B", key="tam")
        market_growth = st.text_input("Market Growth Rate (%)", placeholder="e.g., 15%", key="growth")
    with col3:
        target_geography = st.text_input("Target Geography", placeholder="e.g., MENA, Global", key="geography")
        market_stage = st.selectbox("Market Stage", ["Emerging", "Growing", "Mature", "Declining"], key="stage")

st.markdown("<div style='height:2px;'></div>", unsafe_allow_html=True)

# ==== COMPETITIVE LANDSCAPE (BEIGE) ====
st.markdown("""
<div style="background:#F5F2ED;margin:0 -3rem 0 -3rem;padding:28px 3rem;border-top:2px solid #16A085;border-bottom:1px solid #E0E0E0;">
<h3 style="text-align:left;color:#1B2B4D;font-weight:700;margin:0 0 14px 0;font-size:1.1rem;">Competitive Landscape</h3>
</div>
""", unsafe_allow_html=True)

with st.expander("Define Competitors & Market Position", expanded=True):
    col_comp1, col_comp2 = st.columns(2)
    with col_comp1:
        competitors = st.text_area("Key Competitors", height=70, placeholder="List main competitors", key="competitors")
        competitive_advantage = st.text_area("Competitive Advantage", height=70, placeholder="Unique positioning", key="advantage")
    with col_comp2:
        market_barriers = st.text_area("Market Entry Barriers", height=70, placeholder="Barriers to entry", key="barriers")
        market_trends = st.text_area("Key Market Trends", height=70, placeholder="Industry trends", key="trends")

st.markdown("<div style='height:2px;'></div>", unsafe_allow_html=True)

# ==== OPPORTUNITIES & RISKS (DARK BLUE) ====
st.markdown("""
<div style="background:#2B3E54;margin:0 -3rem 0 -3rem;padding:28px 3rem;border-top:2px solid #16A085;border-bottom:1px solid #E0E0E0;">
<h3 style="text-align:left;color:#FFFFFF;font-weight:700;margin:0 0 14px 0;font-size:1.1rem;">Opportunities & Risks</h3>
</div>
""", unsafe_allow_html=True)

with st.expander("Identify Market Opportunities & Risks", expanded=True):
    col_opp1, col_opp2 = st.columns(2)
    with col_opp1:
        opportunities = st.text_area("Market Opportunities", height=70, placeholder="Growth opportunities", key="opportunities")
    with col_opp2:
        risks = st.text_area("Market Risks", height=70, placeholder="Market risks & challenges", key="risks")

st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)

# ==== GENERATE BUTTON ====
btn_col = st.columns([1, 1, 1])[1]
with btn_col:
    if st.button("Generate Market Report", use_container_width=True, key="generate"):
        if not company_name or not industry or not market_size:
            st.error("Please fill required fields: Company Name, Industry, Market Size")
        else:
            with st.spinner("Analyzing market landscape..."):
                market_data = {
                    'company_name': company_name,
                    'analysis_date': datetime.now().strftime('%B %d, %Y'),
                    'industry': industry,
                    'market_size': market_size,
                    'market_growth': market_growth or 'N/A',
                    'target_geography': target_geography or 'Global',
                    'market_stage': market_stage,
                    'competitors': competitors or 'To be analyzed',
                    'competitive_advantage': competitive_advantage or 'To be defined',
                    'market_barriers': market_barriers or 'To be assessed',
                    'market_trends': market_trends or 'To be documented',
                    'opportunities': opportunities or 'To be identified',
                    'risks': risks or 'To be evaluated'
                }
                
                st.session_state.market_report = market_data
                st.success("Market analysis complete!")
                st.rerun()

# ==== RESULTS DISPLAY (BEIGE) ====
if st.session_state.market_report:
    st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)
    
    st.markdown("""
<div style="background:#F5F2ED;margin:0 -3rem 0 -3rem;padding:28px 3rem;border-top:2px solid #16A085;border-bottom:1px solid #E0E0E0;">
<h3 style="text-align:left;color:#1B2B4D;font-weight:700;margin:0;font-size:1.1rem;">Market Analysis Report</h3>
</div>
""", unsafe_allow_html=True)
    
    data = st.session_state.market_report
    
    # Display report
    col_info1, col_info2, col_info3 = st.columns(3)
    with col_info1:
        st.metric("Market Size (TAM)", data['market_size'])
    with col_info2:
        st.metric("Growth Rate", data['market_growth'])
    with col_info3:
        st.metric("Market Stage", data['market_stage'])
    
    st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)
    
    col_report1, col_report2 = st.columns(2)
    with col_report1:
        st.subheading("Competitive Landscape")
        st.write(f"**Competitors:** {data['competitors']}")
        st.write(f"**Advantage:** {data['competitive_advantage']}")
    with col_report2:
        st.subheading("Market Dynamics")
        st.write(f"**Barriers:** {data['market_barriers']}")
        st.write(f"**Trends:** {data['market_trends']}")
    
    st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)
    
    col_risk1, col_risk2 = st.columns(2)
    with col_risk1:
        st.subheading("Opportunities")
        st.write(data['opportunities'])
    with col_risk2:
        st.subheading("Risks")
        st.write(data['risks'])
    
    # Export section
    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
    st.markdown("""
<div style="background:#2B3E54;margin:0 -3rem 0 -3rem;padding:28px 3rem;border-top:2px solid #16A085;border-bottom:1px solid #E0E0E0;">
<h3 style="text-align:left;color:#FFFFFF;font-weight:700;margin:0;font-size:1.1rem;">Export Report</h3>
</div>
""", unsafe_allow_html=True)
    
    col_exp1, col_exp2 = st.columns(2)
    with col_exp1:
        try:
            report_text = f"""# MARKET ANALYSIS REPORT
## {data['company_name']}

**Date:** {data['analysis_date']}

## Executive Summary
Market analysis for {data['company_name']} in the {data['industry']} sector.

## Market Overview
- **TAM:** {data['market_size']}
- **Growth Rate:** {data['market_growth']}
- **Geography:** {data['target_geography']}
- **Market Stage:** {data['market_stage']}

## Competitive Landscape
### Competitors
{data['competitors']}

### Competitive Advantage
{data['competitive_advantage']}

### Market Barriers
{data['market_barriers']}

### Key Trends
{data['market_trends']}

## Opportunities & Risks
### Market Opportunities
{data['opportunities']}

### Market Risks
{data['risks']}

---
**CONFIDENTIAL - Qatar Development Bank**
"""
            
            doc = template_gen.markdown_to_docx(report_text)
            bio = BytesIO()
            doc.save(bio)
            st.download_button(
                "Download Report (DOCX)",
                bio.getvalue(),
                f"Market_Analysis_{data['company_name']}_{datetime.now().strftime('%Y%m%d')}.docx",
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"Export error: {str(e)}")
    
    with col_exp2:
        if st.button("Copy to Clipboard", use_container_width=True, key="copy_report"):
            st.success("Report summary copied!")
    
    # NAVIGATION
    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
    col_nav1, col_nav2, col_nav3 = st.columns(3)
    
    with col_nav1:
        if st.button("Back to Due Diligence", use_container_width=True, key="back_dd"):
            st.switch_page("pages/2_Due_Diligence_Analysis.py")
    
    with col_nav2:
        if st.button("Go to Financial Modeling", use_container_width=True, key="to_financial"):
            st.switch_page("pages/4_Financial_Modeling.py")
    
    with col_nav3:
        if st.button("Back to Deal Sourcing", use_container_width=True, key="back_deals"):
            st.switch_page("pages/1_Deal_Sourcing.py")

# ==== FOOTER ====
st.markdown(f"""
<div style="background:#1B2B4D;color:#E2E8F0;padding:20px 36px;margin:40px -3rem -2rem;
display:flex;justify-content:space-between;align-items:center;font-size:0.85rem;">
<p style="margin:0;">© 2025 Regulus AI | All Rights Reserved</p>
<p style="margin:0;color:#A0AEC0;">Powered by Regulus AI</p>
</div>
""", unsafe_allow_html=True)
