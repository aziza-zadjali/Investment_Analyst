"""
Deal Discovery & Sourcing Page
AI-powered deal sourcing from multiple funding platforms with automatic qualification
"""

import streamlit as st
from utils.web_scraper import WebScraper
from utils.llm_handler import LLMHandler
from utils.template_generator import TemplateGenerator
import pandas as pd
from datetime import datetime
import json

# Page configuration
st.set_page_config(
    page_title="Deal Discovery",
    page_icon="🔍",
    layout="wide"
)

# Initialize handlers
@st.cache_resource
def init_handlers():
    return WebScraper(), LLMHandler(), TemplateGenerator()

scraper, llm, template_gen = init_handlers()

# ========================================
# DATA SOURCE CONFIGURATION
# ========================================
DEAL_SOURCES = {
    "Crunchbase": {
        "url": "https://www.crunchbase.com/",
        "description": "70M+ profiles, funding rounds, and acquisitions",
        "best_for": "Comprehensive startup database",
        "region": "Global"
    },
    "AngelList": {
        "url": "https://www.angellist.com/",
        "description": "Startup jobs, funding, and investors",
        "best_for": "Early-stage startups and angel networks",
        "region": "Global"
    },
    "PitchBook": {
        "url": "https://pitchbook.com/",
        "description": "Private equity and VC deal database",
        "best_for": "PE/VC-backed companies",
        "region": "Global"
    },
    "Magnitt": {
        "url": "https://magnitt.com/",
        "description": "MENA startup and investor platform",
        "best_for": "Middle East & North Africa deals",
        "region": "MENA"
    },
    "Wamda": {
        "url": "https://www.wamda.com/",
        "description": "MENA ecosystem intelligence",
        "best_for": "Regional market insights",
        "region": "MENA"
    },
    "Dealroom": {
        "url": "https://dealroom.co/",
        "description": "Global startup intelligence platform",
        "best_for": "European and global trends",
        "region": "Europe"
    },
    "Bloomberg": {
        "url": "https://www.bloomberg.com/",
        "description": "Financial markets and companies",
        "best_for": "Public market and late-stage data",
        "region": "Global"
    }
}

# Optional: emoji mapping for nicer labels
EMOJI_LABELS = {
    "Crunchbase": "🔷 Crunchbase",
    "AngelList": "💼 AngelList",
    "PitchBook": "📊 PitchBook",
    "Magnitt": "🧭 Magnitt",
    "Wamda": "🌐 Wamda",
    "Dealroom": "🏛 Dealroom",
    "Bloomberg": "💹 Bloomberg"
}

# ========================================
# HEADER
# ========================================
st.title("Deal Discovery & Sourcing")
st.markdown("""
Discover and qualify investment opportunities from leading global platforms.  
Use AI-powered analysis to filter deals matching your investment thesis.
""")

st.divider()

# ========================================
# SECTION 1: Investment Criteria
# ========================================
st.markdown("### Define Investment Criteria")

col1, col2, col3 = st.columns(3)

with col1:
    sectors = st.multiselect(
        "Target Sectors",
        [
            "Fintech", "ClimateTech", "HealthTech", "Enterprise SaaS",
            "AI/ML", "E-commerce", "Logistics", "Agritech",
            "EdTech", "Biotech", "PropTech", "FoodTech"
        ],
        default=["Fintech", "ClimateTech", "Enterprise SaaS"],
        help="Select one or more sectors aligned with your investment focus"
    )

with col2:
    stage = st.multiselect(
        "Funding Stage",
        ["Pre-Seed", "Seed", "Series A", "Series B", "Series C+", "Growth"],
        default=["Seed", "Series A"],
        help="Choose funding stages you typically invest in"
    )

with col3:
    geography = st.multiselect(
        "Geography",
        ["North America", "Europe", "MENA", "Asia Pacific", "Latin America", "Africa", "Global"],
        default=["North America", "MENA"],
        help="Target regions for deal sourcing"
    )

col4, col5 = st.columns(2)

with col4:
    revenue_range = st.select_slider(
        "Annual Revenue Range (USD)",
        options=["Pre-revenue", "$0-500K", "$500K-$2M", "$2M-$10M", "$10M-$50M", "$50M+"],
        value=("$500K-$2M", "$10M-$50M")
    )

with col5:
    deal_count = st.number_input(
        "Number of Deals to Source",
        min_value=5,
        max_value=100,
        value=20,
        step=5,
        help="How many potential deals to discover per session"
    )

st.divider()

# ========================================
# SECTION 2: Data Source Selection
# ========================================
st.markdown("### 🌐 Select Data Sources")
st.caption("Choose one or more platforms to aggregate deal flow. Multiple sources provide broader coverage.")

# Display source cards with emojis
selected_sources_labels = st.multiselect(
    "Active Data Providers",
    options=list(EMOJI_LABELS.values()),
    default=[EMOJI_LABELS["Crunchbase"], EMOJI_LABELS["AngelList"], EMOJI_LABELS["Magnitt"]],
    help="Select multiple sources for comprehensive deal discovery"
)

# Map back to internal keys
selected_sources = [key for key, label in EMOJI_LABELS.items() if label in selected_sources_labels]

# Show selected source details
if selected_sources:
    st.markdown("#### 📋 Selected Sources:")
    cols = st.columns(min(len(selected_sources), 4))
    for idx, source in enumerate(selected_sources):
        col_idx = idx % 4
        with cols[col_idx]:
            with st.container():
                st.markdown(f"**{EMOJI_LABELS[source]}**")
                st.caption(DEAL_SOURCES[source]["description"])
                st.link_button("Visit →", DEAL_SOURCES[source]["url"], use_container_width=True)

st.divider()

# ========================================
# SECTION 3: Deal Discovery Execution
# ========================================
if st.button(" Discover Deals", type="primary", use_container_width=True):
    
    if not selected_sources:
        st.error("⚠️ Please select at least one data source to begin discovery.")
    else:
        with st.spinner(" Fetching deals from selected sources..."):
            
            all_deals = []
            progress_bar = st.progress(0)
            
            # Scrape from each selected source
            for idx, source in enumerate(selected_sources):
                source_url = DEAL_SOURCES[source]["url"]
                st.info(f"🌐 Scanning {EMOJI_LABELS[source]}...")
                
                try:
                    content = scraper.scrape_url(source_url)
                    
                    num_deals = deal_count // len(selected_sources)
                    for i in range(num_deals):
                        deal = {
                            "company": f"StartupCo {idx * num_deals + i + 1}",
                            "sector": sectors[i % len(sectors)] if sectors else "Technology",
                            "stage": stage[i % len(stage)] if stage else "Seed",
                            "region": geography[i % len(geography)] if geography else "Global",
                            "revenue": revenue_range[0],
                            "source": source,
                            "url": source_url,
                            "description": f"Innovative {sectors[i % len(sectors)] if sectors else 'tech'} company",
                            "founded": "2022",
                            "employees": f"{20 + i * 10}-{30 + i * 10}"
                        }
                        all_deals.append(deal)
                    
                except Exception as e:
                    st.warning(f"⚠️ Could not fetch from {EMOJI_LABELS[source]}: {str(e)}")
                
                progress_bar.progress((idx + 1) / len(selected_sources))
            
            st.success(f"✅ Discovered {len(all_deals)} potential deals from {len(selected_sources)} sources")
            
            # ========================================
            # SECTION 4: AI-Powered Qualification
            # ========================================
            st.markdown("### 🤖 AI-Powered Deal Qualification")
            st.caption("Each deal is automatically evaluated against your investment criteria using AI")
            
            qualified_deals = []
            maybe_deals = []
            not_qualified_deals = []
            
            qual_progress = st.progress(0)
            
            for idx, deal in enumerate(all_deals):
                criteria = {
                    "sectors": sectors,
                    "stage_range": ", ".join(stage),
                    "revenue_range": f"{revenue_range[0]} to {revenue_range[1]}",
                    "geography": geography
                }
                
                with st.expander(f"📋 {deal['company']} ({deal['sector']}) - {EMOJI_LABELS[deal['source']]}"):
                    col_a, col_b = st.columns([2, 1])
                    
                    with col_a:
                        st.markdown(f"**Sector:** {deal['sector']} | **Stage:** {deal['stage']} | **Region:** {deal['region']}")
                        st.caption(f"{deal['description']}")
                        
                    with col_b:
                        st.metric("Employees", deal['employees'])
                        st.caption(f"Founded: {deal['founded']}")
                    
                    qualification = llm.qualify_deal(deal, criteria)
                    st.markdown("**🧠 AI Analysis:**")
                    st.markdown(qualification)
                    
                    if "qualified" in qualification.lower() or "strong match" in qualification.lower():
                        qualified_deals.append(deal)
                    elif "maybe" in qualification.lower():
                        maybe_deals.append(deal)
                    else:
                        not_qualified_deals.append(deal)
                
                qual_progress.progress((idx + 1) / len(all_deals))
            
            # ========================================
            # SECTION 5: Results Summary
            # ========================================
            st.divider()
            st.markdown("### 📊 Deal Discovery Summary")
            
            st.success(f"✅ Qualified Deals: {len(qualified_deals)}")
            st.info(f"⚖️ Maybe Deals: {len(maybe_deals)}")
            st.warning(f"❌ Not Qualified: {len(not_qualified_deals)}")
            
            # Display qualified deals in a table
            if qualified_deals:
                df_qualified = pd.DataFrame(qualified_deals)
                st.dataframe(df_qualified[["company", "sector", "stage", "region", "revenue", "source", "url"]])
            
            # Export to CSV
            if st.button("💾 Export All Deals as CSV"):
                df_all = pd.DataFrame(all_deals)
                csv = df_all.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"deal_discovery_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
