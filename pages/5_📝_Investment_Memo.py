"""
Investment Memo Generation Page
"""

import streamlit as st
import sys
sys.path.append('.')
from utils.report_generator import ReportGenerator
from utils.llm_handler import LLMHandler

st.set_page_config(page_title="Investment Memo", page_icon="📝", layout="wide")

st.title("📝 Investment Memo Generator")
st.markdown("Create professional investment memos automatically")

generator = ReportGenerator()
llm = LLMHandler()

# Memo inputs
st.header("📋 Memo Information")

col1, col2 = st.columns(2)

with col1:
    company_name = st.text_input("Company Name")
    investment_size = st.text_input("Investment Size", "$5M")
    analyst_name = st.text_input("Analyst Name", "Investment Team")

with col2:
    valuation = st.text_input("Valuation", "$50M")
    stage = st.selectbox("Deal Stage", ["Seed", "Series A", "Series B", "Growth"])
    recommendation = st.selectbox("Recommendation", ["STRONG BUY", "BUY", "HOLD", "PASS"])

# Additional details
with st.expander("📝 Additional Details"):
    key_highlights = st.text_area("Key Highlights", height=100)
    investment_thesis = st.text_area("Investment Thesis", height=150)
    business_model = st.text_area("Business Model", height=100)

if st.button("🚀 Generate Investment Memo", type="primary"):
    if company_name:
        with st.spinner("Generating investment memo..."):
            # Prepare data
            memo_data = {
                'company_name': company_name,
                'investment_size': investment_size,
                'valuation': valuation,
                'stage': stage,
                'analyst_name': analyst_name,
                'recommendation': recommendation,
                'key_highlights': key_highlights or "To be completed",
                'investment_thesis': investment_thesis or "To be developed",
                'business_model': business_model or "To be analyzed",
                'founded': "N/A",
                'location': "N/A",
                'industry': "Technology",
                'products_services': "To be documented",
                'team_info': "To be documented",
                'tam': "N/A",
                'sam': "N/A",
                'som': "N/A",
                'market_trends': "To be analyzed",
                'competitive_landscape': "To be researched",
                'historical_performance': "To be reviewed",
                'projections': "See financial model",
                'key_metrics': "To be calculated",
                'valuation_analysis': "To be completed",
                'business_risks': "To be identified",
                'financial_risks': "To be assessed",
                'market_risks': "To be evaluated",
                'risk_mitigation': "To be developed",
                'confidence_level': "Medium",
                'recommendation_rationale': f"Based on analysis, recommend {recommendation}",
                'terms_conditions': "Standard terms",
                'next_steps': "Schedule management meeting",
                'sources': "Various internal and external sources"
            }
            
            # Generate memo
            memo = generator.generate_complete_memo(memo_data)
            
            # Display
            st.markdown("---")
            st.markdown(memo)
            
            # Download button
            st.download_button(
                label="📥 Download Memo (Markdown)",
                data=memo,
                file_name=f"{company_name.replace(' ', '_')}_investment_memo.md",
                mime="text/markdown"
            )
    else:
        st.warning("Please enter a company name")
