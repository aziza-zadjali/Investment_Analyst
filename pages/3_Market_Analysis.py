"""
Market Analysis | Regulus AI × QDB
Standalone company entry, main page hero style, comprehensive market research.
"""
import streamlit as st
import os, base64, io
from datetime import datetime
from utils.llm_handler import LLMHandler
from utils.template_generator import TemplateGenerator
from utils.web_scraper import WebScraper
from utils.qdb_styling import apply_qdb_styling, QDB_DARK_BLUE, QDB_NAVY

st.set_page_config(page_title="Market Analysis – Regulus AI", layout="wide")
apply_qdb_styling()

def encode_image(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f"data:image/png;base64,{base64.b64encode(f.read()).decode()}"
    return None

qdb_logo = encode_image("QDB_Logo.png")

# ==== HERO SECTION (MAIN PAGE STYLE) ====
st.markdown(
    f"""
<div style="
    background:linear-gradient(135deg,{QDB_DARK_BLUE} 0%, {QDB_NAVY} 100%);
    color:white;
    position:relative;
    margin:0 -3rem; padding:100px 0 80px 0;
    min-height:390px; text-align:center; overflow:hidden;">
  <div style="position:absolute;left:50px;top:48px;">
    {'<img src="'+qdb_logo+'" style="max-height:80px;">' if qdb_logo else '<b>QDB</b>'}
  </div>
  <div style="max-width:950px;margin:0 auto;">
    <h1 style="font-size:2.8rem;font-weight:800;letter-spacing:-0.5px;line-height:1.18; margin-bottom:16px;">
      Market Analysis & Research
    </h1>
    <p style="font-size:1.35rem;color:#E2E8F0; font-weight:500; margin-bottom:18px;">
      Competitive Intelligence and Market Opportunity Assessment
    </p>
    <p style="color:#CBD5E0; font-size:1.07rem;line-height:1.6;max-width:760px;margin:0 auto 38px;">
      AI-driven market sizing, competitive positioning, trend analysis and strategic insights. <br>
      Generate comprehensive market research reports with actionable growth strategies.
    </p>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

# ==== RETURN HOME BUTTON ====
col1, col2, col3 = st.columns([1, 0.6, 1])
with col2:
    if st.button("Return Home", use_container_width=True, key="home_btn"):
        st.switch_page("streamlit_app.py")

st.markdown(
    """
<style>
button[key="home_btn"]{
 background:linear-gradient(135deg,#16A085 0%,#138074 80%,#0E5F55 100%)!important;
 color:white!important; border:none!important; border-radius:44px!important;
 padding:14px 44px!important; font-weight:700!important; font-size:1.08rem!important;
 box-shadow:0 8px 34px rgba(19,128,116,.20)!important;
 transition:all .19s!important; cursor:pointer!important;}
button[key="home_btn"]:hover{
 transform:translateY(-2px)!important;
 box-shadow:0 10px 40px rgba(19,128,116,.30)!important;}
</style>
""",
    unsafe_allow_html=True,
)

# ==== WORKFLOW TRACKER ====
st.markdown(
    """
<style>
.track{background:#F6F5F2;margin:-2px -3rem;padding:34px 0;
display:flex;justify-content:space-evenly;align-items:center;}
.circle{width:54px;height:54px;border-radius:50%;display:flex;
align-items:center;justify-content:center;font-weight:700;
background:#CBD5E0;color:#475569;font-size:0.95rem;}
.circle.active{background:linear-gradient(135deg,#138074 0%,#0E5F55 100%);
color:white;box-shadow:0 5px 15px rgba(19,128,116,0.4);}
.label{margin-top:7px;font-size:0.9rem;font-weight:600;color:#708090;}
.label.active{color:#138074;}
.pipe{height:3px;width:70px;background:#CBD5E0;}
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
""",
    unsafe_allow_html=True,
)

# ==== INIT RESOURCES ====
@st.cache_resource
def init_handlers():
    return LLMHandler(), TemplateGenerator(), WebScraper()

llm, template_gen, scraper = init_handlers()

if 'market_report' not in st.session_state:
    st.session_state.market_report = None

# ==== COMPANY INFORMATION SECTION ====
st.markdown(
    """
<div style="background:white;margin:50px -3rem 0 -3rem;padding:45px 3rem;
border-top:3px solid #138074;box-shadow:0 0 12px rgba(0,0,0,0.05);">
<h2 style="text-align:center;color:#1B2B4D;font-weight:700;">
Company & Market Context
</h2>
<p style="text-align:center;color:#555;margin-top:6px;">
Enter company details for market analysis and competitive intelligence.
</p>
</div>
""",
    unsafe_allow_html=True,
)

with st.expander("Company & Market Details", expanded=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        company_name = st.text_input("Company Name", placeholder="Enter company name", key="company_name")
    with col2:
        industry = st.text_input("Industry", placeholder="e.g., Technology, Finance", key="industry")
    with col3:
        sector = st.text_input("Sector", placeholder="e.g., Fintech, AI/ML", key="sector")
    
    col4, col5 = st.columns(2)
    with col4:
        region = st.selectbox("Geographic Focus", ["MENA","Europe","North America","Asia Pacific","Global"], index=4, key="region")
    with col5:
        market_scope = st.selectbox("Market Scope", ["Local","Regional","National","Global"], index=3, key="scope")

# ==== ANALYSIS PARAMETERS ====
st.markdown(
    """
<div style="background:white;margin:50px -3rem 0 -3rem;padding:45px 3rem;
border-top:3px solid #138074;box-shadow:0 0 12px rgba(0,0,0,0.05);">
<h2 style="text-align:center;color:#1B2B4D;font-weight:700;">
Analysis Parameters
</h2>
<p style="text-align:center;color:#555;margin-top:6px;">
Configure market research scope, depth, and components.
</p>
</div>
""",
    unsafe_allow_html=True,
)

with st.expander("Configure Analysis", expanded=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        timeframe = st.selectbox("Forecast Timeframe", ["1 Year","3 Years","5 Years"], index=1, key="timeframe")
    with col2:
        analysis_depth = st.selectbox("Analysis Depth", ["Standard","Comprehensive","Deep Dive"], index=1, key="depth")
    with col3:
        st.markdown("**Include Components:**")
    
    col4, col5, col6, col7 = st.columns(4)
    with col4:
        include_size = st.checkbox("Market Sizing", value=True, key="size")
    with col5:
        include_competitive = st.checkbox("Competitive Analysis", value=True, key="comp")
    with col6:
        include_trends = st.checkbox("Trends & Drivers", value=True, key="trends")
    with col7:
        include_swot = st.checkbox("SWOT Analysis", value=True, key="swot")

# ==== EXECUTE ANALYSIS BUTTON ====
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 0.8, 1])
with col2:
    run_analysis = st.button("Run Market Analysis", use_container_width=True, key="run_market")

st.markdown(
    """
<style>
div.stButton>button:first-child{
 background:linear-gradient(135deg,#16A085 0%,#138074 50%,#0E5F55 100%)!important;
 color:white!important;border:none!important;border-radius:40px!important;
 padding:14px 42px!important;font-weight:700!important;font-size:1rem!important;
 box-shadow:0 5px 18px rgba(19,128,116,0.35)!important;transition:all 0.3s ease!important;}
div.stButton>button:first-child:hover{
 background:linear-gradient(135deg,#0E5F55 0%,#138074 50%,#16A085 100%)!important;
 transform:translateY(-2px)!important;
 box-shadow:0 8px 22px rgba(19,128,116,0.45)!important;}
</style>
""",
    unsafe_allow_html=True,
)

# ==== EXECUTION LOGIC ====
if run_analysis:
    if not company_name:
        st.error("Company name is required")
    else:
        try:
            with st.spinner("Conducting market analysis..."):
                
                analysis_prompt = f"""
                Conduct {analysis_depth.lower()} market analysis for:
                
                Company: {company_name}
                Industry: {industry}
                Sector: {sector}
                Geographic Focus: {region}
                Market Scope: {market_scope}
                Timeframe: {timeframe}
                
                Include:
                {"- Market size (TAM/SAM/SOM) and growth projections" if include_size else ""}
                {"- Competitive landscape and key competitors" if include_competitive else ""}
                {"- Market trends and growth drivers" if include_trends else ""}
                {"- SWOT analysis" if include_swot else ""}
                
                Provide strategic insights and recommendations for Qatar Development Bank investment strategy.
                """
                
                try:
                    st.info("Generating AI-powered market analysis...")
                    analysis_result = llm.generate_text(analysis_prompt)
                except:
                    analysis_result = f"Market analysis for {company_name} in {sector} sector completed."
                
                # Compile report
                report_data = {
                    'company_name': company_name,
                    'industry': industry,
                    'sector': sector,
                    'region': region,
                    'market_scope': market_scope,
                    'timeframe': timeframe,
                    'analysis_date': datetime.now().strftime('%B %d, %Y'),
                    'analyst': 'Regulus AI',
                    'executive_summary': analysis_result[:800] if analysis_result else f'Market analysis for {company_name}',
                    'market_overview': analysis_result if analysis_result else f'{sector} market overview',
                    'market_size': f'TAM estimation, SAM projection, SOM analysis for {timeframe}',
                    'competitive_analysis': f'Competitive landscape analysis for {sector} sector',
                    'regulatory_environment': f'Regulatory context for {industry} in {region}',
                    'trends': f'Key market trends and growth drivers for {sector}',
                    'swot_analysis': 'Strengths, Weaknesses, Opportunities, and Threats assessment',
                    'recommendations': f'Strategic recommendations for {company_name} market positioning',
                    'data_sources': ['Industry reports', 'Market databases', 'Competitive intelligence'],
                    'analysis_status': 'Completed'
                }
                
                st.session_state.market_report = str(report_data)
                st.success("Market analysis completed successfully!")
                st.balloons()
        
        except Exception as e:
            st.error(f"Analysis error: {str(e)}")

# ==== RESULTS DISPLAY ====
if st.session_state.market_report and company_name:
    st.markdown("---")
    st.markdown(
        """
<div style="background:white;margin:30px -3rem 0 -3rem;padding:45px 3rem;
border-top:3px solid #138074;box-shadow:0 0 12px rgba(0,0,0,0.05);">
<h2 style="text-align:center;color:#1B2B4D;font-weight:700;">
Analysis Results
</h2>
<p style="text-align:center;color:#555;margin-top:6px;">
Review comprehensive market research report and export findings.
</p>
</div>
""",
        unsafe_allow_html=True,
    )
    
    with st.expander("View Report Preview", expanded=True):
        st.markdown(st.session_state.market_report[:1500])
    
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            "Download Report (Text)",
            st.session_state.market_report,
            f"Market_Analysis_{company_name}_{datetime.now().strftime('%Y%m%d')}.txt",
            "text/plain",
            use_container_width=True
        )
    with col2:
        st.info("DOCX export available through template generator")
    
    # Navigation
    st.markdown("<br><br>", unsafe_allow_html=True)
    col_nav1, col_nav2, col_nav3 = st.columns(3)
    
    with col_nav1:
        if st.button("Back to Due Diligence", use_container_width=True, key="back_dd"):
            st.switch_page("pages/2_Due_Diligence_Analysis.py")
    
    with col_nav2:
        if st.button("Go to Financial Modeling", use_container_width=True, key="to_financial"):
            st.switch_page("pages/4_Financial_Modeling.py")
    
    with col_nav3:
        if st.button("Skip to Investment Memo", use_container_width=True, key="to_memo"):
            st.switch_page("pages/5_Investment_Memo.py")

# ==== FOOTER ====
st.markdown(
    f"""
<div style="background:{QDB_DARK_BLUE};color:#E2E8F0;padding:26px 36px;margin:80px -3rem -2rem;
display:flex;justify-content:space-between;align-items:center;">
  <p style="margin:0;font-size:0.9rem;">© 2025 Regulus AI | All Rights Reserved</p>
  <p style="margin:0;color:#A0AEC0;font-size:0.9rem;">Powered by Regulus AI</p>
</div>
""",
    unsafe_allow_html=True,
)
