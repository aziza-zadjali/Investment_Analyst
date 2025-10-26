"""
Market & Competitive Analysis - COMPLETE WITH WEB SCRAPING
Full web integration + professional template generation - DOCX ONLY
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

# ===== Initialize Handlers =====
@st.cache_resource
def init_handlers():
    try:
        llm = LLMHandler()
        template_gen = TemplateGenerator()
        web_scraper = WebScraper()
        return llm, template_gen, web_scraper
    except Exception as e:
        st.error(f"Error initializing handlers: {e}")
        return None, None, None

llm, template_gen, web_scraper = init_handlers()

if any(x is None for x in [llm, template_gen, web_scraper]):
    st.error("Failed to initialize handlers")
    st.stop()

# ===== Image Loader =====
def encode_image(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f"data:image/png;base64,{base64.b64encode(f.read()).decode()}"
    return None

qdb_logo = encode_image("QDB_Logo.png")
regulus_logo = encode_image("regulus_logo.png")

# ===== Session State =====
if 'market_complete' not in st.session_state:
    st.session_state.market_complete = False
if 'market_report' not in st.session_state:
    st.session_state.market_report = ""
if 'market_data' not in st.session_state:
    st.session_state.market_data = {}
if 'web_data' not in st.session_state:
    st.session_state.web_data = {}

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

.section-beige {
    background-color: #F6F5F2;
    border-radius: 10px;
    padding: 20px;
    margin: 12px 0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}

.required-asterisk {
    color: #E74C3C;
    font-weight: 700;
    margin-left: 2px;
}

.news-badge {
    display: inline-block;
    background: linear-gradient(135deg,#E8F5F3 0%,#D5E8E6 100%);
    color: #16A085;
    padding: 6px 14px;
    border-radius: 16px;
    font-size: 0.7rem;
    font-weight: 700;
    margin: 3px 4px;
}
</style>
""", unsafe_allow_html=True)

# ===== HERO HEADER =====
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

  <div style="position:absolute; top:15px; left:35px;">
    {'<img src="'+qdb_logo+'" style="max-height:55px;">' if qdb_logo else ''}
  </div>

  <div style="position:absolute; top:15px; right:35px;">
    {'<img src="'+regulus_logo+'" style="max-height:55px;">' if regulus_logo else ''}
  </div>

  <div style="max-width:800px; margin:0 auto;">
    <h1 style="font-size:2rem; font-weight:800; margin-bottom:6px;">Market & Competitive Analysis</h1>
    <p style="color:#E2E8F0; font-size:0.95rem; margin:0;">AI-powered research with real-time global news intelligence</p>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

# ===== HOME BUTTON =====
if st.button("← Return Home", key="home_btn"):
    st.switch_page("streamlit_app.py")

st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

# ===== COMPANY INFORMATION =====
st.markdown('<div class="section-beige"><div style="font-size:1.2rem; font-weight:700; color:#1B2B4D; margin-bottom:12px;">Company & Market Information</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown("<div style='color:#1B2B4D; font-size:0.85rem; margin-bottom:4px; font-weight:600;'>Company Name <span class='required-asterisk'>*</span></div>", unsafe_allow_html=True)
    company_name = st.text_input("Company Name", placeholder="e.g., Tesla", label_visibility="collapsed")

with col2:
    st.markdown("<div style='color:#1B2B4D; font-size:0.85rem; margin-bottom:4px; font-weight:600;'>Industry/Sector <span class='required-asterisk'>*</span></div>", unsafe_allow_html=True)
    industry = st.text_input("Industry/Sector", placeholder="e.g., Electric Vehicles", label_visibility="collapsed")

col3, col4 = st.columns(2)
with col3:
    st.markdown("<div style='color:#1B2B4D; font-size:0.85rem; margin-bottom:4px; font-weight:600;'>Geographic Markets</div>", unsafe_allow_html=True)
    geographic_focus = st.multiselect("Geographic Markets", ["North America", "Europe", "Asia Pacific", "Latin America", "Middle East & Africa", "Global"], default=["Global"], label_visibility="collapsed")

with col4:
    st.markdown("<div style='color:#1B2B4D; font-size:0.85rem; margin-bottom:4px; font-weight:600;'>Company Website (Optional)</div>", unsafe_allow_html=True)
    company_website = st.text_input("Company Website", placeholder="e.g., tesla.com", label_visibility="collapsed")

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

# ===== ANALYSIS SCOPE =====
st.markdown('<div class="section-beige"><div style="font-size:1.2rem; font-weight:700; color:#1B2B4D; margin-bottom:12px;">Analysis Scope</div>', unsafe_allow_html=True)

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

# ===== WEB RESEARCH =====
st.markdown('<div class="section-beige"><div style="font-size:1.2rem; font-weight:700; color:#1B2B4D; margin-bottom:12px;">Real-Time News Intelligence</div>', unsafe_allow_html=True)

enable_web_research = st.checkbox(
    "Search Bloomberg, Forbes, CNBC, Al Jazeera, Gulf Business, Arabian Business, Zawya & Yahoo Finance",
    value=True,
    help="Searches 8 major news sources for latest market intelligence"
)

if enable_web_research:
    st.info("""
    **Global News Sources:**
    🗞️ Bloomberg | 📰 Forbes | 📺 CNBC | 🌍 Al Jazeera | 🏢 Gulf Business | 🏛️ Arabian Business | 💼 Zawya | 📊 Yahoo Finance
    """)

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

# ===== ANALYSIS BUTTON =====
if st.button("Generate Market Analysis with Web Intelligence", use_container_width=True):
    if not company_name or not industry:
        st.error("Please enter both company name and industry")
        st.stop()
    if not analysis_options:
        st.error("Please select at least one analysis area")
        st.stop()

    with st.spinner("Generating comprehensive market analysis..."):
        web_results = {}
        
        # ===== WEB SCRAPING PHASE =====
        if enable_web_research:
            st.info("🔍 Searching 8 global news sources...")
            
            try:
                # THIS IS WHERE web_scraper IS USED!
                web_results = web_scraper.search_all_sources(company_name, industry)
                
                # Display sources found
                sources_found = len([s for s, articles in web_results.items() if articles])
                total_articles = sum(len(articles) for articles in web_results.values())
                
                st.markdown(f"<p style='color:#16A085; font-weight:700;'>✅ Found {total_articles} articles from {sources_found}/8 sources</p>", unsafe_allow_html=True)
                
                # Display badges
                cols = st.columns(8)
                for idx, (source, articles) in enumerate(web_results.items()):
                    with cols[idx % 8]:
                        if articles:
                            st.markdown(f"<span class='news-badge'>{source.split()[0]}</span>", unsafe_allow_html=True)
            
            except Exception as e:
                st.warning(f"⚠️ Web research limited: {str(e)}")
                web_results = {}
        
        # ===== ANALYSIS PHASE =====
        st.info("📊 Analyzing market data with AI...")
        
        analysis_results = {
            'company_name': company_name,
            'industry': industry,
            'analyst_name': 'Regulus AI',
            'analysis_date': datetime.now().strftime('%B %d, %Y'),
            'geographic_markets': ', '.join(geographic_focus),
            'analysis_areas': analysis_options,
            'web_research_enabled': enable_web_research
        }

        st.info("📝 Creating professional report...")
        
        # THIS IS WHERE template_gen.generate_market_analysis_report IS USED WITH web_results!
        markdown_report = template_gen.generate_market_analysis_report(analysis_results, web_results)

        st.session_state.market_complete = True
        st.session_state.market_report = markdown_report
        st.session_state.market_data = analysis_results
        st.session_state.web_data = web_results

        st.success("✅ Market Analysis Complete!")

st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

# ===== DOWNLOAD SECTION (DOCX ONLY) =====
if st.session_state.market_complete:
    st.markdown('<div class="section-beige"><div style="font-size:1.2rem; font-weight:700; color:#1B2B4D; margin-bottom:12px;">Download Professional Report</div>', unsafe_allow_html=True)
    
    data = st.session_state.market_data

    # SINGLE BUTTON - DOCX ONLY
    try:
        docx_doc = template_gen.markdown_to_docx(st.session_state.market_report)
        docx_buffer = BytesIO()
        docx_doc.save(docx_buffer)
        docx_bytes = docx_buffer.getvalue()
        
        st.download_button(
            label="Download Professional Report (DOCX)",
            data=docx_bytes,
            file_name=f"{data['company_name']}_Market_Analysis_{datetime.now().strftime('%Y%m%d')}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True
        )
    except Exception as e:
        st.error(f"Error generating report: {str(e)}")

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

    # ===== FULL REPORT =====
    st.markdown('<div class="section-beige"><div style="font-size:1.2rem; font-weight:700; color:#1B2B4D; margin-bottom:12px;">Professional Market Analysis Report</div>', unsafe_allow_html=True)
    st.markdown(st.session_state.market_report)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)

# ===== FOOTER =====
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
        <li><a href="#" style="text-decoration:none; color:#E2E8F0; font-weight:500;">About</a></li>
        <li><a href="#" style="text-decoration:none; color:#E2E8F0; font-weight:500;">Contact</a></li>
      </ul>
    </div>
    <div style="flex:1; text-align:right; display:flex; align-items:center; justify-content:flex-end; gap:12px;">
      <p style="margin:0; color:#A0AEC0; font-size:0.88rem; font-weight:600;">Powered by Regulus AI</p>
      {'<img src="'+regulus_logo+'" style="max-height:45px; opacity:0.92;">' if regulus_logo else ''}
    </div>
  </div>
</div>
""", unsafe_allow_html=True)
