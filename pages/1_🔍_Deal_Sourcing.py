"""
Deal Sourcing Page - AI-Powered Deal Discovery
"""

import streamlit as st
import sys
sys.path.append('.')
from utils.web_scraper import WebScraper
from utils.llm_handler import LLMHandler
import pandas as pd

st.set_page_config(page_title="Deal Sourcing", page_icon="🔍", layout="wide")

st.title("🔍 AI-Powered Deal Sourcing")
st.markdown("Discover and qualify investment opportunities automatically")

# Initialize components
if 'deals' not in st.session_state:
    st.session_state.deals = []

scraper = WebScraper()
llm = LLMHandler()

# Sidebar filters
with st.sidebar:
    st.header("Search Criteria")
    
    stage = st.multiselect(
        "Investment Stage",
        ["Seed", "Series A", "Series B", "Series C+", "Growth"],
        default=["Seed", "Series A"]
    )
    
    sectors = st.multiselect(
        "Sectors",
        ["AI/ML", "FinTech", "HealthTech", "CleanTech", "SaaS", "E-commerce"],
        default=["AI/ML", "FinTech"]
    )
    
    geography = st.multiselect(
        "Geography",
        ["North America", "Europe", "Asia", "Middle East"],
        default=["North America"]
    )
    
    min_revenue = st.number_input("Min Revenue ($M)", min_value=0, value=0)
    max_revenue = st.number_input("Max Revenue ($M)", min_value=0, value=100)

# Main content
tab1, tab2, tab3 = st.tabs(["🔎 Discover Deals", "📋 Deal Pipeline", "📊 Analytics"])

with tab1:
    st.header("Deal Discovery")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        platform = st.selectbox(
            "Data Source",
            ["Demo Data", "Crunchbase", "AngelList", "Custom"]
        )
    
    with col2:
        if st.button("🚀 Search for Deals", type="primary"):
            with st.spinner("Searching for deals..."):
                # Scrape deals
                deals = scraper.scrape_startup_data(platform="demo")
                
                # Qualify deals
                qualified_deals = []
                for deal in deals:
                    criteria = {
                        'target_stage': ', '.join(stage),
                        'target_sector': ', '.join(sectors),
                        'revenue_range': f"${min_revenue}M - ${max_revenue}M",
                        'geography': ', '.join(geography)
                    }
                    
                    qualification = llm.qualify_deal(deal, criteria)
                    deal['qualification'] = qualification
                    qualified_deals.append(deal)
                
                st.session_state.deals = qualified_deals
                st.success(f"✅ Found {len(qualified_deals)} potential deals!")
    
    if st.session_state.deals:
        st.markdown("---")
        st.subheader("Discovered Deals")
        
        for idx, deal in enumerate(st.session_state.deals):
            with st.expander(f"💼 {deal['name']} - {deal['industry']}"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Stage", deal['stage'])
                with col2:
                    st.metric("Funding", deal['funding'])
                with col3:
                    st.metric("Location", deal['location'])
                
                st.markdown(f"**Description:** {deal['description']}")
                
                if 'qualification' in deal:
                    st.markdown("### AI Qualification")
                    st.markdown(deal['qualification'])
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("✅ Add to Pipeline", key=f"add_{idx}"):
                        st.success("Added to pipeline!")
                with col2:
                    if st.button("📄 Generate Brief", key=f"brief_{idx}"):
                        st.info("Generating company brief...")
                with col3:
                    if st.button("❌ Reject", key=f"reject_{idx}"):
                        st.warning("Deal rejected")

with tab2:
    st.header("Deal Pipeline")
    
    if st.session_state.deals:
        df = pd.DataFrame(st.session_state.deals)
        st.dataframe(df[['name', 'industry', 'stage', 'funding', 'location']], use_container_width=True)
        
        # Download button
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download Pipeline CSV",
            data=csv,
            file_name="deal_pipeline.csv",
            mime="text/csv"
        )
    else:
        st.info("No deals in pipeline. Start discovering deals in the 'Discover Deals' tab.")

with tab3:
    st.header("Pipeline Analytics")
    
    if st.session_state.deals:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Deals", len(st.session_state.deals))
        with col2:
            industries = [d['industry'] for d in st.session_state.deals]
            st.metric("Industries", len(set(industries)))
        with col3:
            stages = [d['stage'] for d in st.session_state.deals]
            st.metric("Stages", len(set(stages)))
        
        # Industry distribution
        st.subheader("Industry Distribution")
        industry_counts = pd.Series(industries).value_counts()
        st.bar_chart(industry_counts)
    else:
        st.info("No analytics available yet.")
