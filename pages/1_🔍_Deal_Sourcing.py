import streamlit as st
from utils.web_scraper import WebScraper
from utils.llm_handler import LLMHandler
from config.data_sources import FUNDING_PLATFORMS
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Deal Discovery", page_icon="🔍", layout="wide")

# Initialize handlers
scraper = WebScraper()
llm = LLMHandler()

st.title("🔍 Deal Discovery & Sourcing")
st.markdown("Discover and qualify investment opportunities from leading global platforms")

# ========================================
# SECTION 1: Investment Criteria
# ========================================
st.markdown("### 🎯 Define Investment Criteria")

col1, col2, col3 = st.columns(3)

with col1:
    sectors = st.multiselect(
        "Target Sectors",
        ["Fintech", "ClimateTech", "HealthTech", "Enterprise SaaS", "AI/ML", 
         "E-commerce", "Logistics", "Agritech", "EdTech", "Biotech"],
        default=["Fintech", "ClimateTech"]
    )

with col2:
    stage = st.multiselect(
        "Funding Stage",
        ["Pre-Seed", "Seed", "Series A", "Series B", "Series C+", "Growth"],
        default=["Seed", "Series A"]
    )

with col3:
    geography = st.multiselect(
        "Geography",
        ["North America", "Europe", "MENA", "Asia Pacific", "Latin America", "Global"],
        default=["North America", "MENA"]
    )

revenue_range = st.select_slider(
    "Annual Revenue Range (USD)",
    options=["Pre-revenue", "$0-500K", "$500K-$2M", "$2M-$10M", "$10M-$50M", "$50M+"],
    value=("$500K-$2M", "$10M-$50M")
)

st.divider()

# ========================================
# SECTION 2: Data Source Selection (Industry Standard)
# ========================================
st.markdown("### 🌐 Select Data Sources")
st.caption("Choose one or more platforms to aggregate deal flow from")

# Define sources with metadata
DEAL_SOURCES = {
    "🔷 Crunchbase": {
        "url": "https://www.crunchbase.com/",
        "description": "70M+ profiles, funding rounds, and acquisitions",
        "best_for": "Comprehensive startup database"
    },
    "💼 AngelList": {
        "url": "https://www.angellist.com/",
        "description": "Startup jobs, funding, and investors",
        "best_for": "Early-stage startups and angel networks"
    },
    "📊 PitchBook": {
        "url": "https://pitchbook.com/",
        "description": "Private equity and VC deal database",
        "best_for": "PE/VC-backed companies"
    },
    "🧭 Magnitt": {
        "url": "https://magnitt.com/",
        "description": "MENA startup and investor platform",
        "best_for": "Middle East & North Africa deals"
    },
    "🌍 Wamda": {
        "url": "https://www.wamda.com/",
        "description": "MENA ecosystem intelligence",
        "best_for": "Regional market insights"
    },
    "📈 Dealroom": {
        "url": "https://dealroom.co/",
        "description": "Global startup intelligence",
        "best_for": "European and global trends"
    },
    "🏦 Bloomberg": {
        "url": "https://www.bloomberg.com/",
        "description": "Financial markets and companies",
        "best_for": "Public market and late-stage data"
    }
}

# Multi-select with enhanced UI
selected_sources = st.multiselect(
    "Active Data Providers",
    options=list(DEAL_SOURCES.keys()),
    default=["🔷 Crunchbase", "💼 AngelList", "🧭 Magnitt"],
    help="Select multiple sources for broader deal coverage"
)

# Display source info cards
if selected_sources:
    cols = st.columns(len(selected_sources))
    for idx, source in enumerate(selected_sources):
        with cols[idx]:
            with st.container():
                st.markdown(f"**{source}**")
                st.caption(DEAL_SOURCES[source]["description"])
                st.link_button("Visit", DEAL_SOURCES[source]["url"])

st.divider()

# ========================================
# SECTION 3: Deal Discovery Execution
# ========================================
if st.button("🚀 Discover Deals", type="primary", use_container_width=True):
    
    with st.spinner("Fetching deals from selected sources..."):
        
        all_deals = []
        
        # Scrape from each selected source
        for source in selected_sources:
            source_url = DEAL_SOURCES[source]["url"]
            st.info(f"🔍 Scanning {source}...")
            
            try:
                # Scrape data
                content = scraper.scrape_url(source_url)
                
                # Simulate deal extraction (replace with actual parsing logic)
                deals = [
                    {
                        "company": f"Startup {i+1}",
                        "sector": sectors[i % len(sectors)],
                        "stage": stage[i % len(stage)],
                        "source": source,
                        "url": source_url
                    }
                    for i in range(3)  # Demo: 3 deals per source
                ]
                
                all_deals.extend(deals)
                
            except Exception as e:
                st.warning(f"⚠️ Could not fetch from {source}: {str(e)}")
        
        st.success(f"✅ Discovered {len(all_deals)} potential deals")
        
        # ========================================
        # SECTION 4: AI Qualification
        # ========================================
        st.markdown("### 🤖 AI-Powered Deal Qualification")
        
        qualified_deals = []
        
        for deal in all_deals:
            with st.expander(f"📋 {deal['company']} ({deal['sector']})"):
                
                # AI qualification
                criteria = {
                    "sectors": sectors,
                    "stage_range": ", ".join(stage),
                    "revenue_range": f"{revenue_range[0]} to {revenue_range[1]}",
                    "geography": geography
                }
                
                qualification = llm.qualify_deal(deal, criteria)
                
                st.markdown(qualification)
                
                # Add to qualified list
                if "qualified" in qualification.lower() or "match" in qualification.lower():
                    qualified_deals.append(deal)
        
        # ========================================
        # SECTION 5: Export Results
        # ========================================
        if qualified_deals:
            st.markdown("### 📥 Export Qualified Deals")
            
            df = pd.DataFrame(qualified_deals)
            
            csv = df.to_csv(index=False).encode('utf-8')
            
            st.download_button(
                label="📄 Download as CSV",
                data=csv,
                file_name=f"qualified_deals_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
            )
            
            st.dataframe(df, use_container_width=True)

# ========================================
# SIDEBAR: Tips & Resources
# ========================================
with st.sidebar:
    st.markdown("### 💡 Deal Sourcing Tips")
    st.info("""
    **Best Practices:**
    - Use multiple sources for broader coverage
    - Refine criteria based on thesis fit
    - Schedule regular deal flow reviews
    - Track source quality over time
    """)
    
    st.markdown("### 📚 Resources")
    st.markdown("- [Crunchbase Pro](https://www.crunchbase.com/)")
    st.markdown("- [AngelList Venture](https://www.angellist.com/)")
    st.markdown("- [Magnitt Reports](https://magnitt.com/)")
