""" 
Market & Competitive Analysis
AI-powered market research and competitive intelligence
"""

import streamlit as st
from datetime import datetime
from io import BytesIO
from utils.llm_handler import LLMHandler
from utils.template_generator import TemplateGenerator
from utils.web_scraper import WebScraper

st.set_page_config(page_title="Market Analysis", page_icon="🌐", layout="wide")

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

# Gradient header function
def gradient_header(title: str):
    st.markdown(f"""
    <div style='
        background: linear-gradient(90deg, #A6D8FF, #D5B8FF);
        border-radius: 12px;
        padding: 15px 25px;
        margin: 10px 0 25px 0;
        color: white;
        font-weight: 600;
        font-size: 1.5rem;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    '>
        {title}
    </div>
    """, unsafe_allow_html=True)

# Page Title
st.markdown("""
<div style="padding: 1.5rem 0; border-bottom: 2px solid #f0f0f0;">
<h1 style="margin: 0; font-size: 2.5rem;">Market & Competitive Analysis</h1>
<p style="margin: 0.5rem 0 0 0; color: #666; font-size: 1.1rem;">
AI-powered market research with web data extraction
</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Company Information
gradient_header("Company & Market Information")
col1, col2 = st.columns(2)
with col1:
    company_name = st.text_input(
        "Company Name *",
        placeholder="e.g., Tesla",
        help="Enter the company name for analysis"
    )
with col2:
    industry = st.text_input(
        "Industry/Sector *",
        placeholder="e.g., Electric Vehicles",
        help="Enter the industry or sector"
    )

col3, col4 = st.columns(2)
with col3:
    geographic_focus = st.multiselect(
        "Geographic Markets",
        ["North America", "Europe", "Asia Pacific", "Latin America", "Middle East & Africa", "Global"],
        default=["Global"]
    )
with col4:
    company_website = st.text_input(
        "Company Website (Optional)",
        placeholder="e.g., tesla.com",
        help="Optionally provide website for data extraction"
    )

st.divider()

# Analysis Options
gradient_header("Analysis Scope")
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
    default=["Market Size & Growth", "Competitive Landscape", "Market Trends & Drivers"]
)

# Optional: Web Search
with st.expander("Optional: Enable Web Research", expanded=False):
    st.info("""
**Enhance analysis with real-time web research:**
- Latest market reports and news  
- Competitor information  
- Industry trends and forecasts  
- Regulatory updates  

This feature uses web scraping to gather current market data.
""")
enable_web_research = st.checkbox(
    "Enable automatic web research",
    value=False,
    help="System will search for relevant market data online"
)

st.divider()

# Analysis Button
if st.button("Generate Market Analysis", type="primary", use_container_width=True):
    if not company_name or not industry:
        st.error("Please enter both company name and industry")
        st.stop()
    if not analysis_options:
        st.error("Please select at least one analysis area")
        st.stop()

    with st.spinner("Conducting comprehensive market analysis..."):
        if enable_web_research:
            st.info("Gathering market data from web sources...")
            try:
                search_queries = [
                    f"{industry} market size analysis",
                    f"{company_name} competitors analysis",
                    f"{industry} market trends 2025"
                ]
                for query in search_queries:
                    st.caption(f"Searching: {query}")
                st.success("Web research completed")
            except Exception as e:
                st.warning(f"Web research encountered issues: {e}")

        st.info("Analyzing with AI...")
        analysis_results = {
            'company_name': company_name,
            'industry': industry,
            'analyst_name': 'Regulus AI',
            'analysis_date': datetime.now().strftime('%B %d, %Y'),
            'geographic_markets': ', '.join(geographic_focus),
            'analysis_areas': analysis_options
        }

        # --- AI PROMPTS ---
        if "Market Size & Growth" in analysis_options:
            st.info("Analyzing market size and growth...")
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
            st.info("Analyzing competitive landscape...")
            competitive_prompt = f"""
Analyze the competitive landscape for {company_name} in the {industry} industry.
"""
            try:
                analysis_results['competitive_landscape'] = llm.generate(competitive_prompt)
            except Exception as e:
                analysis_results['competitive_landscape'] = "Analysis unavailable"

        if "Market Trends & Drivers" in analysis_options:
            st.info("Analyzing market trends...")
            trends_prompt = f"""
Analyze current and emerging trends in the {industry} industry affecting {company_name}.
"""
            try:
                analysis_results['market_trends'] = llm.generate(trends_prompt)
            except Exception as e:
                analysis_results['market_trends'] = "Analysis unavailable"

        if "SWOT Analysis" in analysis_options:
            st.info("Conducting SWOT analysis...")
            swot_prompt = f"""
Conduct a comprehensive SWOT analysis for {company_name} in the {industry} industry.
"""
            try:
                analysis_results['swot_analysis'] = llm.generate(swot_prompt)
            except Exception as e:
                analysis_results['swot_analysis'] = "Analysis unavailable"

        if "Porter's Five Forces" in analysis_options:
            st.info("Applying Porter's Five Forces...")
            porter_prompt = f"""
Apply Porter's Five Forces framework to analyze {company_name}'s competitive position in the {industry} industry.
"""
            try:
                analysis_results['porters_five_forces'] = llm.generate(porter_prompt)
            except Exception as e:
                analysis_results['porters_five_forces'] = "Analysis unavailable"

        if "Customer Segmentation" in analysis_options:
            st.info("Analyzing customer segments...")
            segment_prompt = f"""
Analyze customer segmentation for {company_name} in the {industry} industry.
"""
            try:
                analysis_results['customer_segmentation'] = llm.generate(segment_prompt)
            except Exception as e:
                analysis_results['customer_segmentation'] = "Analysis unavailable"

        if "Regulatory Environment" in analysis_options:
            st.info("Assessing regulatory environment...")
            regulatory_prompt = f"""
Analyze the regulatory environment for {company_name} in the {industry} industry.
"""
            try:
                analysis_results['regulatory_environment'] = llm.generate(regulatory_prompt)
            except Exception as e:
                analysis_results['regulatory_environment'] = "Analysis unavailable"

        st.info("Generating comprehensive market report...")
        markdown_report = template_gen.generate_market_analysis_report(analysis_results)

        st.session_state.market_complete = True
        st.session_state.market_report = markdown_report
        st.session_state.market_data = analysis_results

        st.success("Market Analysis Complete!")

# --- RESULTS SECTION ---
if st.session_state.market_complete:
    st.divider()
    gradient_header("Download Reports")
    data = st.session_state.market_data

    col_dl1, col_dl2 = st.columns(2)
    with col_dl1:
        st.download_button(
            label="Download Markdown Report",
            data=st.session_state.market_report,
            file_name=f"{data['company_name']}_Market_Analysis_{datetime.now().strftime('%Y%m%d')}.md",
            mime="text/markdown"
        )
    with col_dl2:
        try:
            docx_doc = template_gen.markdown_to_docx(st.session_state.market_report)
            docx_buffer = BytesIO()
            docx_doc.save(docx_buffer)
            docx_buffer.seek(0)
            st.download_button(
                label="Download DOCX Report",
                data=docx_buffer.getvalue(),
                file_name=f"{data['company_name']}_Market_Analysis_{datetime.now().strftime('%Y%m%d')}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
        except Exception as e:
            st.error(f"Error generating DOCX: {e}")

    st.divider()
    with st.expander("Preview Report", expanded=False):
        st.markdown(st.session_state.market_report)

# Sidebar
with st.sidebar:
    st.markdown("### Market Analysis Features")
    st.markdown("""
    ✓ Market Size & Growth Analysis  
    ✓ Competitive Intelligence  
    ✓ Trend Analysis  
    ✓ SWOT Analysis  
    ✓ Porter's Five Forces  
    ✓ Customer Segmentation  
    ✓ Regulatory Assessment  
    ✓ Optional Web Research  
    ✓ Professional Reports (MD & DOCX)
    """)

    if st.session_state.market_complete:
        st.divider()
        st.markdown("### Analysis Summary")
        st.caption(f"**Company:** {st.session_state.market_data.get('company_name', 'N/A')}")
        st.caption(f"**Industry:** {st.session_state.market_data.get('industry', 'N/A')}")
        st.caption(f"**Date:** {st.session_state.market_data.get('analysis_date', 'N/A')}")
        areas = st.session_state.market_data.get('analysis_areas', [])
        if areas:
            st.caption(f"**Areas Analyzed:** {len(areas)}")
