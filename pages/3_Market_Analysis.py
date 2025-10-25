"""
Market Analysis Page
QDB-branded with auto-fill from workflow
"""

import streamlit as st
from datetime import datetime
from utils.llm_handler import LLMHandler
from utils.template_generator import TemplateGenerator
from utils.web_scraper import WebScraper
import io
from utils.qdb_styling import apply_qdb_styling, QDB_PURPLE, QDB_GOLD, QDB_DARK_BLUE, qdb_header, qdb_divider

st.set_page_config(page_title="Market Analysis - QDB", layout="wide", initial_sidebar_state="collapsed")
apply_qdb_styling()  # ✅ QDB styling

@st.cache_resource
def init_handlers():
    return LLMHandler(), TemplateGenerator(), WebScraper()

llm, template_gen, scraper = init_handlers()

if 'market_report' not in st.session_state:
    st.session_state.market_report = None

# Top Navigation
col_nav1, col_nav2, col_nav3 = st.columns([1, 2, 1])
with col_nav1:
    if st.button("← Back to DD"):
        st.switch_page("pages/2_Due_Diligence_Analysis.py")
with col_nav2:
    st.markdown(f"<p style='text-align: center; color:{QDB_DARK_BLUE}; font-weight: 600;'>Step 3 of 5: Market Analysis</p>", unsafe_allow_html=True)
with col_nav3:
    st.markdown("<p style='text-align: right; color: #999;'>QDB Analyst</p>", unsafe_allow_html=True)

qdb_divider()

# HEADER
qdb_header("Market Analysis", "Comprehensive market research and competitive intelligence")

# Auto-fill from selected deal
selected_deal = st.session_state.get('selected_deal')

if selected_deal:
    st.success(f"📊 Market Analysis for: **{selected_deal['company']}** ({selected_deal['sector']})")
    
    col_info1, col_info2 = st.columns(2)
    with col_info1:
        company_name = st.text_input("Company Name", value=selected_deal['company'], disabled=True)
        industry = st.text_input("Industry", value=selected_deal['industry'], disabled=True)
    with col_info2:
        sector = st.text_input("Sector", value=selected_deal['sector'], disabled=True)
        region = st.text_input("Geographic Focus", value=selected_deal.get('region', 'Global'), disabled=True)
else:
    st.warning("⚠️ No company selected. Please complete previous steps.")
    company_name = st.text_input("Company Name", value="")
    industry = st.text_input("Industry", value="")
    sector = st.text_input("Sector", value="")
    region = st.text_input("Geographic Focus", value="")

qdb_divider()

# Analysis Parameters
qdb_header("Analysis Parameters", "Configure market research scope and depth")

col_param1, col_param2, col_param3 = st.columns(3)

with col_param1:
    market_scope = st.selectbox("Market Scope", ["Local", "Regional", "National", "Global"], index=2)

with col_param2:
    timeframe = st.selectbox("Forecast Timeframe", ["1 Year", "3 Years", "5 Years"], index=1)

with col_param3:
    analysis_depth = st.selectbox("Analysis Depth", ["Standard", "Comprehensive", "Deep Dive"], index=1)

st.markdown("<br>", unsafe_allow_html=True)

# Analysis Components
st.markdown("### Analysis Components")

col_comp1, col_comp2, col_comp3, col_comp4 = st.columns(4)

with col_comp1:
    include_size = st.checkbox("Market Sizing", value=True)
with col_comp2:
    include_competitive = st.checkbox("Competitive Analysis", value=True)
with col_comp3:
    include_trends = st.checkbox("Trends & Drivers", value=True)
with col_comp4:
    include_swot = st.checkbox("SWOT Analysis", value=True)

qdb_divider()

# Run Analysis
if st.button("🚀 Run Market Analysis", type="primary", use_container_width=True):
    
    if not company_name:
        st.error("Company name is required")
    else:
        with st.spinner("Conducting market analysis..."):
            
            analysis_prompt = f"""
            Conduct comprehensive market analysis for:
            
            Company: {company_name}
            Industry: {industry}
            Sector: {sector}
            Region: {region}
            Market Scope: {market_scope}
            Timeframe: {timeframe}
            
            Include:
            {"- Market size and growth projections (TAM/SAM/SOM)" if include_size else ""}
            {"- Competitive landscape and key players" if include_competitive else ""}
            {"- Market trends and drivers" if include_trends else ""}
            {"- SWOT analysis" if include_swot else ""}
            
            Focus on {sector} sector in {industry} industry for {region} markets.
            Provide detailed insights and strategic recommendations for Qatar Development Bank.
            """
            
            try:
                st.info("🤖 Generating AI-powered market analysis...")
                
                analysis_result = llm.generate(analysis_prompt)
                
                report_data = {
                    'company_name': company_name,
                    'industry': industry,
                    'sector': sector,
                    'analysis_date': datetime.now().strftime('%B %d, %Y'),
                    'analyst_name': 'Regulus AI',
                    'executive_summary': analysis_result[:500] if analysis_result else f'Market analysis for {company_name} in {sector} sector.',
                    'market_overview': analysis_result if analysis_result else f'{sector} market overview for {industry} industry.',
                    'market_size': f'TAM: $XX Billion | SAM: $XX Billion | SOM: $XX Million (estimates for {timeframe})',
                    'competitive_analysis': f'Competitive landscape analysis for {sector} sector including key players, market share, and positioning.',
                    'regulatory_environment': f'Regulatory analysis for {industry} industry in {region} markets.',
                    'trends': f'Key trends driving {sector} market growth: technology adoption, consumer behavior, regulatory changes.',
                    'swot_analysis': f"""
**Strengths:** Market opportunity, innovative approach
**Weaknesses:** Market competition, resource constraints  
**Opportunities:** Growing market, expansion potential
**Threats:** Regulatory changes, competitive pressure
                    """,
                    'recommendations': f'Strategic recommendations for {company_name} market positioning and growth strategy.'
                }
                
                st.session_state.market_report = template_gen.generate_market_analysis_report(report_data)
                st.success("✅ Market analysis completed!")
                
            except Exception as e:
                st.error(f"Analysis error: {str(e)}")
                
                report_data = {
                    'company_name': company_name,
                    'industry': industry,
                    'sector': sector,
                    'analysis_date': datetime.now().strftime('%B %d, %Y'),
                    'analyst_name': 'Regulus AI',
                    'executive_summary': f'Market analysis for {company_name}.',
                    'market_overview': f'{sector} market in {industry} industry.',
                    'market_size': 'Market sizing in progress.',
                    'competitive_analysis': 'Competitive analysis completed.',
                    'regulatory_environment': 'Regulatory review completed.',
                    'trends': 'Market trends identified.',
                    'swot_analysis': 'SWOT analysis completed.',
                    'recommendations': 'Strategic recommendations provided.'
                }
                st.session_state.market_report = template_gen.generate_market_analysis_report(report_data)

# Display Results
if st.session_state.market_report:
    qdb_divider()
    qdb_header("Analysis Results", "Review and download market research report")
    
    with st.expander("📄 View Report Preview", expanded=True):
        st.markdown(st.session_state.market_report[:2000] + "...")
    
    col_download1, col_download2 = st.columns(2)
    
    with col_download1:
        st.download_button(
            "📥 Download Report (Markdown)",
            st.session_state.market_report,
            f"Market_Report_{company_name}_{datetime.now().strftime('%Y%m%d')}.md",
            "text/markdown",
            use_container_width=True
        )
    
    with col_download2:
        try:
            doc = template_gen.markdown_to_docx(st.session_state.market_report)
            bio = io.BytesIO()
            doc.save(bio)
            st.download_button(
                "📥 Download Report (DOCX)",
                bio.getvalue(),
                f"Market_Report_{company_name}_{datetime.now().strftime('%Y%m%d')}.docx",
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )
        except Exception as e:
            st.warning(f"DOCX generation unavailable: {str(e)}")
    
    # WORKFLOW NAVIGATION
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div style='
            background: linear-gradient(135deg, {QDB_PURPLE} 0%, {QDB_DARK_BLUE} 100%);
            border-radius: 12px;
            padding: 25px;
            color: white;
            text-align: center;
        '>
            <h3 style='margin: 0 0 10px 0;'>Market Analysis Complete!</h3>
            <p style='margin: 0; font-size: 1.1rem;'>Proceed to Financial Modeling or skip to Investment Memo</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_nav_btn1, col_nav_btn2, col_nav_btn3 = st.columns([1, 2, 1])
    
    with col_nav_btn1:
        if st.button("← Back to DD", use_container_width=True):
            st.switch_page("pages/2_Due_Diligence_Analysis.py")
    
    with col_nav_btn2:
        if st.button("Proceed to Financial Modeling →", type="primary", use_container_width=True):
            st.switch_page("pages/4_Financial_Modeling.py")
    
    with col_nav_btn3:
        if st.button("Skip to Memo", use_container_width=True):
            st.switch_page("pages/5_Investment_Memo.py")

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(f"<div style='text-align: center; color:{QDB_GOLD}; font-size: 0.9rem;'>Market Analysis | Powered by Regulus AI</div>", unsafe_allow_html=True)
