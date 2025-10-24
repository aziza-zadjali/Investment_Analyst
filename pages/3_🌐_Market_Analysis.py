"""
Market Analysis Page
"""

import streamlit as st
import sys
sys.path.append('.')
from utils.web_scraper import WebScraper
from utils.llm_handler import LLMHandler

st.set_page_config(page_title="Market Analysis", page_icon="🌐", layout="wide")

st.title("🌐 Market & Competitive Analysis")
st.markdown("AI-powered market research and competitive intelligence")

# Initialize
scraper = WebScraper()
llm = LLMHandler()

# Input section
col1, col2 = st.columns(2)

with col1:
    company_name = st.text_input("Company Name", placeholder="Enter company name")

with col2:
    industry = st.selectbox(
        "Industry",
        ["Technology", "FinTech", "HealthTech", "CleanTech", "E-commerce", "SaaS"]
    )

if st.button("🔍 Conduct Market Analysis", type="primary"):
    if company_name:
        with st.spinner("Conducting market analysis..."):
            # Search market data
            market_data = scraper.search_market_data(f"{company_name} {industry}")
            
            # Generate analysis
            analysis = llm.conduct_market_analysis(
                company_name=company_name,
                industry=industry,
                market_data=str(market_data)
            )
            
            st.markdown("### Market Analysis Report")
            st.markdown(analysis)
            
            # Additional insights
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📈 Market Trends")
                st.markdown("""
                - Digital transformation acceleration
                - Increased M&A activity
                - ESG focus growing
                """)
            
            with col2:
                st.subheader("🎯 Key Opportunities")
                st.markdown("""
                - Market expansion potential
                - Product diversification
                - Strategic partnerships
                """)
    else:
        st.warning("Please enter a company name")
