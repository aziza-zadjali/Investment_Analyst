"""
Enhanced Financial Modeling & Scenario Planning
Generates comprehensive Excel models with embedded formulas and advanced analysis
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from dateutil.relativedelta import relativedelta
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from io import BytesIO
import plotly.express as px
import plotly.graph_objects as go

# Import the financial analyzer
try:
    from utils.financial_analyzer import FinancialAnalyzer
    FINANCIAL_ANALYZER_AVAILABLE = True
except ImportError:
    FINANCIAL_ANALYZER_AVAILABLE = False
    st.warning("⚠️ FinancialAnalyzer module not available. Some advanced features will be limited.")

st.set_page_config(page_title="Financial Modeling", layout="wide")

# Optional top-right image (e.g., logo)
st.markdown("""
<style>
.gradient-header {
    background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
    padding: 1.5rem;
    border-radius: 10px;
    color: white;
    position: relative;
}
.gradient-header img {
    position: absolute;
    top: 15px;
    right: 20px;
    height: 60px;
}
</style>
<div class="gradient-header">
    <h1 style="margin: 0; font-size: 2.5rem;">Financial Modeling & Scenario Planning</h1>
    <p style="margin: 0.5rem 0 0 0; font-size: 1.1rem;">
        Generate comprehensive Excel models with advanced analytics, DCF valuation, and scenario planning
    </p>
    <img src="https://upload.wikimedia.org/wikipedia/commons/a/ab/Logo_TV_2022.svg" alt="Logo">
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- Session State ---
if 'model_complete' not in st.session_state:
    st.session_state.model_complete = False
if 'model_data' not in st.session_state:
    st.session_state.model_data = {}

# --- Company Info ---
st.markdown("""
<div style="
    background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
    padding: 1rem;
    border-radius: 10px;
    color: white;
">
    <h2 style="margin: 0;">Company Information</h2>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    company_name = st.text_input(
        "Company Name *",
        value=st.session_state.model_data.get('company_name', ''),
        placeholder="e.g., Tech Startup Inc."
    )
with col2:
    currency = st.selectbox(
        "Currency *",
        ["USD $", "EUR €", "GBP £", "QAR ﷼", "AED د.إ", "SAR ﷼", "AUD $", "CAD $"],
        index=0
    )

st.divider()

# --- Forecast Parameters ---
st.markdown("""
<div style="
    background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
    padding: 1rem;
    border-radius: 10px;
    color: white;
">
    <h2 style="margin: 0;">Forecast Parameters</h2>
</div>
""", unsafe_allow_html=True)

col_params1, col_params2, col_params3 = st.columns(3)
with col_params1:
    fiscal_year_end = st.date_input("Fiscal Year End *", value=datetime(2024, 12, 31))
with col_params2:
    start_month = st.date_input("First Forecast Month *", value=datetime.now().replace(day=1))
with col_params3:
    num_months = st.number_input("Forecast Period (months) *", min_value=12, max_value=60, value=36, step=12)

initial_cash = st.number_input(
    f"Opening Cash Balance ({currency}) *",
    min_value=0.0,
    value=100000.0,
    step=10000.0,
    format="%.2f"
)

st.divider()

# --- Revenue Inputs ---
st.markdown("""
<div style="
    background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
    padding: 1rem;
    border-radius: 10px;
    color: white;
">
    <h2 style="margin: 0;">Revenue Assumptions</h2>
</div>
""", unsafe_allow_html=True)

col_rev1, col_rev2, col_rev3 = st.columns(3)
with col_rev1:
    initial_monthly_revenue = st.number_input(f"Initial Monthly Revenue ({currency})", value=50000.0, step=5000.0)
with col_rev2:
    monthly_growth_rate = st.number_input("Monthly Revenue Growth Rate (%)", value=5.0, step=0.5)
with col_rev3:
    revenue_seasonality = st.number_input(
        "Revenue Seasonality Factor (%)",
        value=10.0,
        help="Percentage variation due to seasonal effects"
    )

st.divider()

# --- Cost Inputs ---
st.markdown("""
<div style="
    background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
    padding: 1rem;
    border-radius: 10px;
    color: white;
">
    <h2 style="margin: 0;">Cost Assumptions</h2>
</div>
""", unsafe_allow_html=True)

col_cost1, col_cost2, col_cost3 = st.columns(3)
with col_cost1:
    cogs_percentage = st.number_input("COGS as % of Revenue", value=40.0, step=1.0)
with col_cost2:
    cogs_growth_rate = st.number_input("COGS Annual Growth Rate (%)", value=3.0, step=0.5)
with col_cost3:
    margin_improvement = st.number_input("Annual Margin Improvement (%)", value=0.5)

st.divider()

# --- Operating Expenses ---
st.markdown("""
<div style="
    background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
    padding: 1rem;
    border-radius: 10px;
    color: white;
">
    <h2 style="margin: 0;">Operating Expenses</h2>
</div>
""", unsafe_allow_html=True)

col_opex1, col_opex2 = st.columns(2)
with col_opex1:
    salaries = st.number_input(f"Monthly Salaries ({currency})", value=20000.0, step=1000.0)
    rent = st.number_input(f"Monthly Rent ({currency})", value=5000.0, step=500.0)
with col_opex2:
    marketing = st.number_input(f"Monthly Marketing ({currency})", value=3000.0, step=500.0)
    other_opex = st.number_input(f"Other Monthly OpEx ({currency})", value=2000.0, step=500.0)

st.divider()

# --- Advanced Parameters ---
with st.expander("Advanced Parameters"):
    col_adv1, col_adv2 = st.columns(2)
    with col_adv1:
        discount_rate = st.number_input("Discount Rate for DCF (%)", value=12.0, step=0.5)
        terminal_growth_rate = st.number_input("Terminal Growth Rate (%)", value=3.0, step=0.5)
    with col_adv2:
        tax_rate = st.number_input("Tax Rate (%)", value=25.0, step=1.0)
        capex_percentage = st.number_input("CapEx as % of Revenue", value=2.0, step=0.5)

st.divider()

# --- Generate Button ---
if st.button("Generate Advanced Financial Model", type="primary", use_container_width=True):
    if not company_name:
        st.error("Please enter company name")
    else:
        with st.spinner("Generating comprehensive financial model with advanced analytics..."):
            # keep your full calculation + session state storage logic here
            st.success("Financial Model Generated!")

# --- Sidebar ---
with st.sidebar:
    st.markdown("### Model Features")
    st.markdown("""
✓ Multi-Sheet Excel Model  
✓ Embedded Formulas  
✓ Dynamic Currency  
✓ Monthly & Annual Views  
✓ DCF Valuation  
✓ Scenario Analysis  
✓ Sensitivity Testing  
✓ Financial Ratios
""")
