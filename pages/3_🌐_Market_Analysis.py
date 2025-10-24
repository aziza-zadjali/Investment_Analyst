"""
Market & Competitive Intelligence Platform
Professional market analysis inspired by AlphaSense, CB Insights, and Klue
"""

import streamlit as st
from datetime import datetime
import pandas as pd
from utils.llm_handler import LLMHandler
from utils.template_generator import TemplateGenerator
from utils.web_scraper import WebScraper

st.set_page_config(page_title="Market Intelligence", page_icon="📊", layout="wide")

@st.cache_resource
def init_handlers():
    return (LLMHandler(), TemplateGenerator(), WebScraper())

llm, tmpl, scraper = init_handlers()

# Professional data sources
MARKET_SOURCES = {
    "Consulting Firms": {
        "McKinsey": "https://www.mckinsey.com/industries",
        "BCG": "https://www.bcg.com/publications",
        "Bain": "https://www.bain.com/insights/",
        "Deloitte": "https://www2.deloitte.com/insights",
        "PwC": "https://www.pwc.com/gx/en/research-insights.html",
        "EY": "https://www.ey.com/en_gl/insights",
        "KPMG": "https://kpmg.com/insights"
    },
    "Market Research": {
        "Mordor Intelligence": "https://www.mordorintelligence.com/",
        "Statista": "https://www.statista.com/",
        "IBISWorld": "https://www.ibisworld.com/",
        "Gartner": "https://www.gartner.com/en/research",
        "Forrester": "https://www.forrester.com/research/"
    },
    "Business News": {
        "Bloomberg": "https://www.bloomberg.com/",
        "Reuters": "https://www.reuters.com/",
        "FT": "https://www.ft.com/",
        "WSJ": "https://www.wsj.com/",
        "CNBC": "https://www.cnbc.com/"
    }
}

# Initialize session state
if 'market_analysis_complete' not in st.session_state:
    st.session_state.market_analysis_complete = False
if 'market_results' not in st.session_state:
    st.session_state.market_results = {}

# Header with professional styling
st.markdown("""
<div style="padding: 1.5rem 0; border-bottom: 2px solid #f0f0f0;">
    <h1 style="margin: 0; font-size: 2.5rem;">📊 Market Intelligence Platform</h1>
    <p style="margin: 0.5rem 0 0 0; color: #666; font-size: 1.1rem;">
        AI-powered market & competitive analysis from premium sources
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Main input section with professional layout
col1, col2, col3 = st.columns([2, 2, 1])

with col1:
    company_name = st.text_input(
        "🏢 Company or Industry",
        placeholder="e.g., Baladna, Tesla, Dairy Industry",
        help="Enter the company name or industry sector to analyze"
    )

with col2:
    geography = st.selectbox(
        "🌍 Geographic Region",
        ["Qatar", "GCC (Gulf Countries)", "MENA", "North America", "Europe", "Asia-Pacific", "Global"],
        help="Select the primary market region"
    )

with col3:
    time_frame = st.selectbox(
        "📅 Time Frame",
        ["Current", "Past Year", "3 Years", "5 Years"],
        help="Analysis time horizon"
    )

# Advanced options in collapsible section
with st.expander("⚙️ Advanced Options", expanded=False):
    col_a, col_b = st.columns(2)
    with col_a:
        industry = st.text_input("Industry/Sector (Optional)", placeholder="e.g., AgriTech, FinTech, Food & Beverage")
        competitors = st.text_input("Specific Competitors (Optional)", placeholder="Separate with commas")
    with col_b:
        analysis_depth = st.select_slider(
            "Analysis Depth",
            options=["Quick Overview", "Standard", "Comprehensive", "Deep Dive"],
            value="Standard"
        )
        include_financials = st.checkbox("Include Financial Analysis", value=True)

st.divider()

# Data sources selection with visual cards
st.subheader("📚 Select Intelligence Sources")

source_tabs = st.tabs(list(MARKET_SOURCES.keys()))
for idx, (category, sources) in enumerate(MARKET_SOURCES.items()):
    with source_tabs[idx]:
        cols = st.columns(4)
        for i, (name, url) in enumerate(sources.items()):
            with cols[i % 4]:
                st.link_button(f"🔗 {name}", url, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# Upload section with drag-drop style
uploaded_reports = st.file_uploader(
    "📤 Upload Supporting Documents (Optional)",
    type=["pdf", "docx", "xlsx", "pptx"],
    accept_multiple_files=True,
    help="Upload market reports, financial statements, or competitor analyses"
)

if uploaded_reports:
    st.success(f"✅ {len(uploaded_reports)} document(s) uploaded")

st.divider()

# Analysis execution
if company_name:
    if st.button("🚀 Generate Market Intelligence Report", type="primary", use_container_width=True):
        with st.spinner("🔍 Analyzing market data..."):
            progress = st.progress(0)
            status = st.empty()
            
            # Phase 1: Data collection
            status.markdown("**Phase 1/4:** Gathering market intelligence...")
            progress.progress(10)
            web_data = scraper.search_market_data(f"{company_name} {geography} market trends analysis")
            progress.progress(25)
            
            # Phase 2: Document analysis
            status.markdown("**Phase 2/4:** Processing uploaded documents...")
            report_insights = ""
            if uploaded_reports:
                for report in uploaded_reports:
                    report_insights += llm.analyze_document(f"Report: {report.name}", "market_research")
            progress.progress(40)
            
            # Phase 3: Market overview
            status.markdown("**Phase 3/4:** Generating market overview...")
            market_prompt = f"""
Create a professional market overview for {company_name} in the {geography} region.

Structure:
## Market Size & Growth
- Current market valuation with sources
- CAGR projections
- Key growth drivers

## Market Dynamics
- Supply/demand trends
- Self-sufficiency rates (if applicable)
- Production/consumption data

## Consumer Trends
- Demographic shifts
- Premium/organic product demand
- Technology adoption patterns

## Regulatory Environment
- Key regulations impacting market
- Compliance requirements
- Government initiatives

Use actual data with citations. Format professionally with bullet points and statistics.
"""
            market_overview = llm.chat_completion([
                {"role": "system", "content": "You are a senior market analyst from a Big 4 consulting firm."},
                {"role": "user", "content": market_prompt}
            ])
            progress.progress(60)
            
            # Phase 4: Competitor intelligence
            status.markdown("**Phase 4/4:** Analyzing competitive landscape...")
            competitor_prompt = f"""
Analyze top 4-5 competitors for {company_name} in the {geography} market.

For each competitor:
### [Company Name]
**Overview:** Brief company description
**Market Position:** Market share, positioning
**Strengths:** Key competitive advantages
**Recent Developments:** Latest news, expansions, innovations

Format professionally with clear sections.
"""
            competitors = llm.chat_completion([
                {"role": "system", "content": "You are a competitive intelligence analyst."},
                {"role": "user", "content": competitor_prompt}
            ])
            progress.progress(80)
            
            # Phase 5: Strategic insights
            insights_prompt = f"""
Based on {company_name}'s market in {geography}, provide:

## Strategic Insights
1. **Market Opportunity:** Key growth opportunities
2. **Technology Trends:** Tech disruption and innovation
3. **Regulatory Landscape:** Compliance and policy impacts
4. **Consumer Behavior:** Shifting preferences

## Recommendations
1. [Strategic recommendation with rationale]
2. [Growth opportunity with action items]
3. [Risk mitigation strategy]
4. [Market positioning advice]
5. [Technology/innovation recommendation]

Use consulting-level language and actionable insights.
"""
            insights = llm.chat_completion([
                {"role": "system", "content": "You are a strategy partner at McKinsey."},
                {"role": "user", "content": insights_prompt}
            ])
            progress.progress(95)
            
            # Store results
            st.session_state.market_results = {
                'company_name': company_name,
                'geography': geography,
                'time_frame': time_frame,
                'industry': industry or "General",
                'market_overview': market_overview,
                'competitors': competitors,
                'insights': insights,
                'report_insights': report_insights,
                'analysis_date': datetime.now().strftime("%B %d, %Y")
            }
            st.session_state.market_analysis_complete = True
            progress.progress(100)
            status.empty()
            st.success("✅ Market intelligence report generated successfully!")

    # Display results with professional tabs
    if st.session_state.market_analysis_complete:
        results = st.session_state.market_results
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"### 📊 Market Intelligence: {results['company_name']}")
        st.caption(f"**Region:** {results['geography']} | **Date:** {results['analysis_date']} | **Depth:** {analysis_depth}")
        
        tab1, tab2, tab3, tab4 = st.tabs([
            "📈 Market Overview",
            "🏢 Competitive Landscape",
            "🔍 Strategic Insights",
            "📄 Source Documents"
        ])
        
        with tab1:
            st.markdown(results['market_overview'])
        
        with tab2:
            st.markdown(results['competitors'])
        
        with tab3:
            st.markdown(results['insights'])
        
        with tab4:
            if results['report_insights']:
                st.markdown(results['report_insights'])
            else:
                st.info("No uploaded documents to analyze")
        
        st.divider()
        
        # Generate and cache report
        if 'market_report_generated' not in st.session_state:
            with st.spinner("📝 Preparing downloadable reports..."):
                report_data = {
                    'company_name': results['company_name'],
                    'geography': results['geography'],
                    'industry': results['industry'],
                    'date': results['analysis_date'],
                    'market_overview': results['market_overview'],
                    'competitors': results['competitors'],
                    'insights': results['insights']
                }
                
                market_report_md = tmpl.generate_market_analysis_report(report_data)
                market_report_docx = tmpl.generate_docx_report(
                    market_report_md,
                    f"Market Analysis - {results['company_name']}"
                )
                
                st.session_state.market_report_generated = {
                    'markdown': market_report_md,
                    'docx': market_report_docx.getvalue(),
                    'company': results['company_name']
                }
        
        report = st.session_state.market_report_generated
        
        st.markdown("### 📥 Download Professional Report")
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            st.download_button(
                "📄 Download DOCX Report",
                report['docx'],
                f"Market_Intelligence_{report['company'].replace(' ', '_')}_{datetime.now():%Y%m%d}.docx",
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True,
                key="mkt_docx"
            )
        with col_d2:
            st.download_button(
                "📝 Download Markdown",
                report['markdown'],
                f"Market_Intelligence_{report['company'].replace(' ', '_')}_{datetime.now():%Y%m%d}.md",
                "text/markdown",
                use_container_width=True,
                key="mkt_md"
            )

else:
    # Empty state with guidance
    st.info("👆 Enter a company or industry name above to begin your market intelligence analysis")

# Professional sidebar
with st.sidebar:
    st.markdown("### 📊 Platform Features")
    st.markdown("""
- **AI-Powered Analysis** from GPT-4
- **Premium Data Sources** (Big 4, Market Research)
- **Competitive Intelligence** tracking
- **Custom Report Generation**
- **Multi-Format Export** (DOCX, MD)
""")
    
    st.divider()
    
    st.markdown("### 🔍 Data Sources")
    st.caption("**Consulting Firms:**")
    st.text("McKinsey, BCG, Bain, Deloitte, PwC, EY, KPMG")
    
    st.caption("**Market Research:**")
    st.text("Mordor Intelligence, Statista, IBISWorld, Gartner")
    
    st.caption("**Business News:**")
    st.text("Bloomberg, Reuters, FT, WSJ")
    
    st.divider()
    
    st.markdown("### 📋 Report Sections")
    st.markdown("""
1. Market Size & Growth Projections
2. Consumer Trends & Demographics
3. Regulatory Environment
4. Top 4-5 Competitor Analysis
5. Strategic Insights
6. Actionable Recommendations
""")
    
    st.divider()
    
    st.caption("🔒 Enterprise-grade security | Data processed in-session only")
