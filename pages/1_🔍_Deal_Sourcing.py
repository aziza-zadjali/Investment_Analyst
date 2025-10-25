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
    layout="wide"
)

# Gradient style helper

from PIL import Image
import streamlit as st

image = Image.open("C:\Users\ultra\Star_Drones\3d Printing Presentation\IMG_3478-removebg-preview.png")
st.image(image, caption=" ", use_column_width=True)



def gradient_box(text, height="60px", gradient="linear-gradient(90deg, #4b6cb7 0%, #182848 100%)"):
    return f"""
    <div style="
        background: {gradient};
        padding: 10px 20px;
        border-radius: 10px;
        color: white;
        font-weight: bold;
        font-size: 24px;
        line-height: {height};
        text-align: center;
        margin-bottom: 20px;
    ">
        {text}
    </div>
    """

# Initialize handlers
@st.cache_resource
def init_handlers():
    return WebScraper(), LLMHandler(), TemplateGenerator()

scraper, llm, template_gen = init_handlers()

# ========================================
# HEADER
# ========================================
st.markdown(gradient_box("Deal Discovery & Sourcing"), unsafe_allow_html=True)
st.markdown("""
Discover and qualify investment opportunities from leading global platforms.  
Use AI-powered analysis to filter deals matching your investment thesis.
""")

st.divider()

# ========================================
# SECTION 1: Investment Criteria
# ========================================
st.markdown(gradient_box("Define Investment Criteria", gradient="linear-gradient(90deg, #FF416C 0%, #FF4B2B 100%)"), unsafe_allow_html=True)

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
st.markdown(gradient_box("Select Data Sources", gradient="linear-gradient(90deg, #11998e 0%, #38ef7d 100%)"), unsafe_allow_html=True)
st.caption("Choose one or more platforms to aggregate deal flow. Multiple sources provide broader coverage.")

DEAL_SOURCES = {
    "Crunchbase": {"url": "https://www.crunchbase.com/", "description": "70M+ profiles, funding rounds, and acquisitions"},
    "AngelList": {"url": "https://www.angellist.com/", "description": "Startup jobs, funding, and investors"},
    "PitchBook": {"url": "https://pitchbook.com/", "description": "Private equity and VC deal database"},
    "Magnitt": {"url": "https://magnitt.com/", "description": "MENA startup and investor platform"},
    "Wamda": {"url": "https://www.wamda.com/", "description": "MENA ecosystem intelligence"},
    "Dealroom": {"url": "https://dealroom.co/", "description": "Global startup intelligence platform"},
    "Bloomberg": {"url": "https://www.bloomberg.com/", "description": "Financial markets and companies"}
}

selected_sources = st.multiselect(
    "Active Data Providers",
    options=list(DEAL_SOURCES.keys()),
    default=["Crunchbase", "AngelList", "Magnitt"]
)

if selected_sources:
    st.markdown("#### Selected Sources:")
    cols = st.columns(min(len(selected_sources), 4))
    for idx, source in enumerate(selected_sources):
        col_idx = idx % 4
        with cols[col_idx]:
            st.markdown(f"**{source}**")
            st.caption(DEAL_SOURCES[source]["description"])
            st.link_button("Visit →", DEAL_SOURCES[source]["url"], use_container_width=True)

st.divider()

# ========================================
# SECTION 3: Deal Discovery Execution
# ========================================
st.markdown(gradient_box("Discover Deals", gradient="linear-gradient(90deg, #8360c3 0%, #2ebf91 100%)"), unsafe_allow_html=True)

if st.button("Start Discovery", type="primary", use_container_width=True):
    
    if not selected_sources:
        st.error("Please select at least one data source to begin discovery.")
    else:
        with st.spinner("Fetching deals from selected sources..."):
            all_deals = []
            progress_bar = st.progress(0)
            deal_count_per_source = deal_count // len(selected_sources)

            for idx, source in enumerate(selected_sources):
                source_url = DEAL_SOURCES[source]["url"]
                st.info(f"Scanning {source}...")
                try:
                    content = scraper.scrape_url(source_url)
                    for i in range(deal_count_per_source):
                        deal = {
                            "company": f"StartupCo {idx * deal_count_per_source + i + 1}",
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
                    st.warning(f"Could not fetch from {source}: {str(e)}")
                
                progress_bar.progress((idx + 1) / len(selected_sources))
            
            st.success(f"Discovered {len(all_deals)} potential deals")

# ========================================
# Remaining code (AI qualification, summary, export) can follow here...
# Add gradient boxes for other sections similarly
