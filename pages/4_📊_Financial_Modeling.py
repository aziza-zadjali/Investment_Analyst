"""
Financial Modeling Page
"""

import streamlit as st
import sys
sys.path.append('.')
from utils.financial_analyzer import FinancialAnalyzer
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(page_title="Financial Modeling", page_icon="📊", layout="wide")

st.title("📊 Financial Modeling & Scenario Planning")
st.markdown("Build financial models and run scenario analyses")

analyzer = FinancialAnalyzer()

# Input parameters
st.header("📝 Model Inputs")

col1, col2, col3 = st.columns(3)

with col1:
    revenue = st.number_input("Current Revenue ($M)", min_value=0.0, value=10.0, step=0.5)

with col2:
    scenario = st.selectbox("Growth Scenario", ["conservative", "moderate", "aggressive"])

with col3:
    years = st.slider("Projection Years", 3, 10, 5)

analyzer.projection_years = years

if st.button("🚀 Generate Model", type="primary"):
    with st.spinner("Building financial model..."):
        # Create projections
        base_data = {'revenue': revenue * 1000000}
        projections = analyzer.create_projection_model(base_data, scenario)
        
        # Display results
        st.header("📈 Financial Projections")
        
        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Year 5 Revenue", f"${projections['Revenue'].iloc[-1]/1e6:.1f}M")
        with col2:
            st.metric("Year 5 EBITDA", f"${projections['EBITDA'].iloc[-1]/1e6:.1f}M")
        with col3:
            st.metric("Avg Margin", f"{projections['EBITDA_Margin'].mean():.1f}%")
        with col4:
            cagr = ((projections['Revenue'].iloc[-1]/projections['Revenue'].iloc[0])**(1/years) - 1) * 100
            st.metric("Revenue CAGR", f"{cagr:.1f}%")
        
        # Chart
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=projections['Year'], y=projections['Revenue']/1e6, 
                                name='Revenue', mode='lines+markers'))
        fig.add_trace(go.Scatter(x=projections['Year'], y=projections['EBITDA']/1e6, 
                                name='EBITDA', mode='lines+markers'))
        fig.update_layout(title="Revenue & EBITDA Projections", 
                         xaxis_title="Year", yaxis_title="$ Millions")
        st.plotly_chart(fig, use_container_width=True)
        
        # Data table
        st.subheader("Detailed Projections")
        display_df = projections.copy()
        for col in display_df.columns:
            if col != 'Year' and col != 'EBITDA_Margin':
                display_df[col] = display_df[col].apply(lambda x: f"${x/1e6:.2f}M")
        st.dataframe(display_df, use_container_width=True)
        
        # Download
        csv = projections.to_csv(index=False)
        st.download_button("📥 Download Model", csv, "financial_model.csv", "text/csv")
