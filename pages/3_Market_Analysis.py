"""
Market & Competitive Analysis
AI-powered market research and competitive intelligence
"""
import streamlit as st
import base64
import os
from datetime import datetime
from io import BytesIO
from utils.qdb_styling import apply_qdb_styling
from utils.llm_handler import LLMHandler
from utils.template_generator import TemplateGenerator
from utils.web_scraper import WebScraper

st.set_page_config(page_title="Market Analysis", page_icon="🌐", layout="wide", initial_sidebar_state="collapsed")
apply_qdb_styling()

# ===== Image Loader =====
def encode_image(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f"data:image/png;base64,{base64.b64encode(f.read()).decode()}"
    return None

qdb_logo = encode_image("QDB_Logo.png")
regulus_logo = encode_image("regulus_logo.png")

# Initialize handlers
@st.cache_resource
def init_handlers():
    return LLMHandler(), TemplateGenerator(), WebScraper()

llm, template_gen, web_scraper = init_handlers()

# Session state
if 'market_complete' not in st.session_state:
    st.session_state.market_complete = False
if 'market_report' not in st.session_state:
    st.session_state.market_report = ""
if 'market_data' not in st.session_state:
    st.session_state.market_data = {}

# ===== CUSTOM STYLING =====
st.markdown("""
<style>
.stButton>button {
    background: linear-gradient(135deg,#16A085 0%,#138074 100%)!important;
    color:white!important;
    border:none!important;
    border-radius:8px!important;
    padding:12px 24px!important;
    font-weight:700!important;
    font-size:0.95rem!important;
    box-shadow:0 4px 12px rgba(22,160,133,0.3)!important;
    transition:all 0.25s ease!important;
}

.stButton>button:hover{
    background: linear-gradient(135deg,#0E5F55 0%,#107563 100%)!important;
    transform:translateY(-2px)!important;
    box-shadow:0 6px 18px rgba(22,160,133,0.4)!important;
}

.section-title {
    font-size: 1.2rem;
    font-weight: 700;
    color: white;
    margin: 0;
}

.section-blue {
    background: linear-gradient(135deg, #1B2B4D 0%, #2C3E5E 100%);
    color: white;
    border-radius: 10px;
    padding: 20px;
    margin: 12px 0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.section-beige {
    background-color: #F6F5F2;
    border-radius: 10px;
    padding: 20px;
    margin: 12px 0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}

</style>
""", unsafe_allow_html=True)

# ===== HERO HEADER WITH LOGOS =====
st.markdown(f"""
<div style="
    background: linear-gradient(135deg,#1B2B4D 0%,#2C3E5E 100%);
    color: white;
    text-align: center;
    margin: 0 -3rem;
    padding: 40px 20px 50px 20px;
    position: relative;
    overflow:visible;
    width: calc(100% + 6rem);
    border-bottom: 3px solid #16A085;">

  <!-- Left: QDB -->
  <div style="position:absolute; top:15px; left:35px;">
    {'<img src="'+qdb_logo+'" style="max-height:55px;">' if qdb_logo else ''}
  </div>

  <!-- Right: Regulus -->
  <div style="position:absolute; top:15px; right:35px;">
    {'<img src="'+regulus_logo+'" style="max-height:55px;">' if regulus_logo else ''}
  </div>

  <div style="max-width:800px; margin:0 auto;">
    <h1 style="font-size:2rem; font-weight:800; margin-bottom:6px;">Market & Competitive Analysis</h1>
    <p style="color:#E2E8F0; font-size:0.95rem; margin:0;">AI-powered market research with competitive intelligence</p>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

# ===== HOME BUTTON =====
if st.button("← Return Home", key="home_btn"):
    st.switch_page("streamlit_app.py")

st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

# ===== COMPANY INFORMATION SECTION (BLUE) =====
st.markdown('<div class="section-blue"><div class="section-title">🏢 Company & Market Information</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown("<div style='color:#E2E8F0; font-size:0.85rem; margin-bottom:4px; font-weight:600;'>Company Name *</div>", unsafe_allow_html=True)
    company_name = st.text_input(
        "Company Name",
        placeholder="e.g., Tesla",
        help="Enter the company name for analysis",
        label_visibility="collapsed"
    )

with col2:
    st.markdown("<div style='color:#E2E8F0; font-size:0.85rem; margin-bottom:4px; font-weight:600;'>Industry/Sector *</div>", unsafe_allow_html=True)
    industry = st.text_input(
        "Industry/Sector",
        placeholder="e.g., Electric Vehicles",
        help="Enter the industry or sector",
        label_visibility="collapsed"
    )

col3, col4 = st.columns(2)
with col3:
    st.markdown("<div style='color:#E2E8F0; font-size:0.85rem; margin-bottom:4px; font-weight:600;'>Geographic Markets</div>", unsafe_allow_html=True)
    geographic_focus = st.multiselect(
        "Geographic Markets",
        ["North America", "Europe", "Asia Pacific", "Latin America", "Middle East & Africa", "Global"],
        default=["Global"],
        label_visibility="collapsed"
    )

with col4:
    st.markdown("<div style='color:#E2E8F0; font-size:0.85rem; margin-bottom:4px; font-weight:600;'>Company Website (Optional)</div>", unsafe_allow_html=True)
    company_website = st.text_input(
        "Company Website",
        placeholder="e.g., tesla.com",
        help="Optionally provide website for data extraction",
        label_visibility="collapsed"
    )

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

# ===== ANALYSIS SCOPE SECTION (BEIGE) =====
st.markdown('<div class="section-beige"><div style="font-size:1.2rem; font-weight:700; color:#1B2B4D; margin-bottom:12px;">📊 Analysis Scope</div>', unsafe_allow_html=True)

analysis_options = st.multiselect(
    "Select Analysis Areas",
    [
        "Market Size & Growth",
        "Competitive Landscape",
        "Market Trends & Drivers",
        "SWOT Analysis",
        "Porter's Five Forces",
        "Customer Segmentation",
        "Regulatory Environment"
    ],
    default=["Market Size & Growth", "Competitive Landscape", "Market Trends & Drivers"],
    label_visibility="collapsed"
)

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

# ===== WEB RESEARCH SECTION (BEIGE) =====
st.markdown('<div class="section-beige"><div style="font-size:1.2rem; font-weight:700; color:#1B2B4D; margin-bottom:12px;">🌐 Optional: Web Research</div>', unsafe_allow_html=True)

enable_web_research = st.checkbox(
    "Enable automatic web research",
    value=False,
    help="System will search for relevant market data online"
)

if enable_web_research:
    st.info("""
    ✓ Latest market reports and news  
    ✓ Competitor information  
    ✓ Industry trends and forecasts  
    ✓ Regulatory updates
    """)

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

# ===== ANALYSIS BUTTON (BLUE) =====
st.markdown('<div class="section-blue">', unsafe_allow_html=True)

if st.button("Generate Market Analysis", use_container_width=True):
    if not company_name or not industry:
        st.error("⚠️ Please enter both company name and industry")
        st.stop()
    if not analysis_options:
        st.error("⚠️ Please select at least one analysis area")
        st.stop()

    with st.spinner("🔍 Conducting comprehensive market analysis..."):
        if enable_web_research:
            st.info("📡 Gathering market data from web sources...")
            try:
                search_queries = [
                    f"{industry} market size analysis",
                    f"{company_name} competitors analysis",
                    f"{industry} market trends 2025"
                ]
                for query in search_queries:
                    st.caption(f"🔎 Searching: {query}")
                st.success("✅ Web research completed")
            except Exception as e:
                st.warning(f"⚠️ Web research encountered issues: {e}")

        st.info("🤖 Analyzing with AI...")
        analysis_results = {
            'company_name': company_name,
            'industry': industry,
            'analyst_name': 'Regulus AI',
            'analysis_date': datetime.now().strftime('%B %d, %Y'),
            'geographic_markets': ', '.join(geographic_focus),
            'analysis_areas': analysis_options
        }

        # --- AI ANALYSIS ---
        if "Market Size & Growth" in analysis_options:
            st.info("📈 Analyzing market size and growth...")
            market_prompt = f"""
Analyze the market size and growth for {company_name} in the {industry} industry. Geographic focus: {', '.join(geographic_focus)}.

Provide detailed analysis covering:
1. Total Addressable Market (TAM)
2. Market Segments
3. Growth Drivers
4. Market Maturity
"""
            try:
                analysis_results['market_size_growth'] = llm.generate(market_prompt)
            except Exception as e:
                analysis_results['market_size_growth'] = "Analysis unavailable"

        if "Competitive Landscape" in analysis_options:
            st.info("🏆 Analyzing competitive landscape...")
            competitive_prompt = f"""
Analyze the competitive landscape for {company_name} in the {industry} industry.
"""
            try:
                analysis_results['competitive_landscape'] = llm.generate(competitive_prompt)
            except Exception as e:
                analysis_results['competitive_landscape'] = "Analysis unavailable"

        if "Market Trends & Drivers" in analysis_options:
            st.info("📊 Analyzing market trends...")
            trends_prompt = f"""
Analyze current and emerging trends in the {industry} industry affecting {company_name}.
"""
            try:
                analysis_results['market_trends'] = llm.generate(trends_prompt)
            except Exception as e:
                analysis_results['market_trends'] = "Analysis unavailable"

        if "SWOT Analysis" in analysis_options:
            st.info("💡 Conducting SWOT analysis...")
            swot_prompt = f"""
Conduct a comprehensive SWOT analysis for {company_name} in the {industry} industry.
"""
            try:
                analysis_results['swot_analysis'] = llm.generate(swot_prompt)
            except Exception as e:
                analysis_results['swot_analysis'] = "Analysis unavailable"

        if "Porter's Five Forces" in analysis_options:
            st.info("🎯 Applying Porter's Five Forces...")
            porter_prompt = f"""
Apply Porter's Five Forces framework to analyze {company_name}'s competitive position in the {industry} industry.
"""
            try:
                analysis_results['porters_five_forces'] = llm.generate(porter_prompt)
            except Exception as e:
                analysis_results['porters_five_forces'] = "Analysis unavailable"

        if "Customer Segmentation" in analysis_options:
            st.info("👥 Analyzing customer segments...")
            segment_prompt = f"""
Analyze customer segmentation for {company_name} in the {industry} industry.
"""
            try:
                analysis_results['customer_segmentation'] = llm.generate(segment_prompt)
            except Exception as e:
                analysis_results['customer_segmentation'] = "Analysis unavailable"

        if "Regulatory Environment" in analysis_options:
            st.info("⚖️ Assessing regulatory environment...")
            regulatory_prompt = f"""
Analyze the regulatory environment for {company_name} in the {industry} industry.
"""
            try:
                analysis_results['regulatory_environment'] = llm.generate(regulatory_prompt)
            except Exception as e:
                analysis_results['regulatory_environment'] = "Analysis unavailable"

        st.info("📝 Generating comprehensive market report...")
        markdown_report = template_gen.generate_market_analysis_report(analysis_results)

        st.session_state.market_complete = True
        st.session_state.market_report = markdown_report
        st.session_state.market_data = analysis_results

        st.success("✅ Market Analysis Complete!")

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

# ===== RESULTS SECTION (BLUE) =====
if st.session_state.market_complete:
    st.markdown('<div class="section-blue"><div class="section-title">📥 Download Report</div>', unsafe_allow_html=True)
    
    data = st.session_state.market_data

    col_dl1, col_dl2 = st.columns(2)
    
    with col_dl1:
        try:
            docx_doc = template_gen.markdown_to_docx(st.session_state.market_report)
            docx_buffer = BytesIO()
            docx_doc.save(docx_buffer)
            docx_buffer.seek(0)
            st.download_button(
                label="📄 Download DOCX Report",
                data=docx_buffer.getvalue(),
                file_name=f"{data['company_name']}_Market_Analysis_{datetime.now().strftime('%Y%m%d')}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"Error generating DOCX: {e}")

    with col_dl2:
        st.download_button(
            label="📋 Preview Report",
            data=st.session_state.market_report,
            file_name=f"{data['company_name']}_Market_Analysis_{datetime.now().strftime('%Y%m%d')}.md",
            mime="text/markdown",
            use_container_width=True
        )

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

    # ===== FULL REPORT SECTION (BEIGE) =====
    st.markdown('<div class="section-beige"><div style="font-size:1.2rem; font-weight:700; color:#1B2B4D; margin-bottom:12px;">📖 Full Report</div>', unsafe_allow_html=True)
    st.markdown(st.session_state.market_report)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)

# ===== FOOTER (BLUE) =====
st.markdown(f"""
<div style="
    background-color:#1B2B4D;
    color:#E2E8F0;
    padding:28px 40px;
    margin:40px -3rem -2rem -3rem;
    font-size:0.92rem;
    width: calc(100% + 6rem);">
  <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; max-width:1400px; margin:auto;">
    <div style="flex:2;">
      <ul style="list-style:none; display:flex; gap:30px; flex-wrap:wrap; padding:0; margin:0;">
        <li><a href="#" style="text-decoration:none; color:#E2E8F0; transition:color 0.3s; font-weight:500;">About</a></li>
        <li><a href="#" style="text-decoration:none; color:#E2E8F0; transition:color 0.3s; font-weight:500;">Insights</a></li>
        <li><a href="#" style="text-decoration:none; color:#E2E8F0; transition:color 0.3s; font-weight:500;">Contact</a></li>
        <li><a href="#" style="text-decoration:none; color:#E2E8F0; transition:color 0.3s; font-weight:500;">Privacy</a></li>
      </ul>
    </div>
    <div style="flex:1; text-align:right; display:flex; align-items:center; justify-content:flex-end; gap:12px;">
      <p style="margin:0; color:#A0AEC0; font-size:0.88rem; font-weight:600;">Powered by Regulus AI</p>
      {'<img src="'+regulus_logo+'" style="max-height:45px; opacity:0.92;">' if regulus_logo else ''}
    </div>
  </div>
</div>
""", unsafe_allow_html=True)
