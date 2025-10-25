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

st.set_page_config(page_title="Financial Modeling", page_icon="📊", layout="wide")

# Session state
if 'model_complete' not in st.session_state:
    st.session_state.model_complete = False
if 'model_data' not in st.session_state:
    st.session_state.model_data = {}

st.markdown("""
<div style="padding: 1.5rem 0; border-bottom: 2px solid #f0f0f0;">
    <h1 style="margin: 0; font-size: 2.5rem;">📊 Financial Modeling & Advanced Analytics</h1>
    <p style="margin: 0.5rem 0 0 0; color: #666; font-size: 1.1rem;">
        Professional Excel models with DCF valuation, scenario analysis, and sensitivity testing
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Main Input Section
st.subheader("🏢 Company Information")

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

# Financial Parameters
st.subheader("📅 Forecast Parameters")

col_params1, col_params2, col_params3 = st.columns(3)

with col_params1:
    fiscal_year_end = st.date_input(
        "Fiscal Year End *",
        value=datetime(2024, 12, 31)
    )

with col_params2:
    start_month = st.date_input(
        "First Forecast Month *",
        value=datetime.now().replace(day=1)
    )

with col_params3:
    num_months = st.number_input(
        "Forecast Period (months) *",
        min_value=12,
        max_value=60,
        value=36,
        step=12
    )

initial_cash = st.number_input(
    f"Opening Cash Balance ({currency}) *",
    min_value=0.0,
    value=100000.0,
    step=10000.0,
    format="%.2f"
)

st.divider()

# Revenue Inputs
st.subheader("💰 Revenue Assumptions")

col_rev1, col_rev2, col_rev3 = st.columns(3)

with col_rev1:
    initial_monthly_revenue = st.number_input(
        f"Initial Monthly Revenue ({currency})",
        min_value=0.0,
        value=50000.0,
        step=5000.0
    )

with col_rev2:
    monthly_growth_rate = st.number_input(
        "Monthly Revenue Growth Rate (%)",
        min_value=-50.0,
        max_value=100.0,
        value=5.0,
        step=0.5
    )

with col_rev3:
    revenue_seasonality = st.number_input(
        "Revenue Seasonality Factor (%)",
        min_value=0.0,
        max_value=100.0,
        value=10.0,
        help="Percentage variation due to seasonal effects"
    )

st.divider()

# Cost Inputs
st.subheader("💸 Cost Assumptions")

col_cost1, col_cost2, col_cost3 = st.columns(3)

with col_cost1:
    cogs_percentage = st.number_input(
        "COGS as % of Revenue",
        min_value=0.0,
        max_value=100.0,
        value=40.0,
        step=1.0
    )

with col_cost2:
    cogs_growth_rate = st.number_input(
        "COGS Annual Growth Rate (%)",
        min_value=-20.0,
        max_value=50.0,
        value=3.0,
        step=0.5
    )

with col_cost3:
    margin_improvement = st.number_input(
        "Annual Margin Improvement (%)",
        min_value=-10.0,
        max_value=10.0,
        value=0.5,
        help="Annual improvement in gross margin"
    )

st.divider()

# Operating Expenses
st.subheader("🏢 Operating Expenses")

col_opex1, col_opex2 = st.columns(2)

with col_opex1:
    salaries = st.number_input(
        f"Monthly Salaries ({currency})",
        min_value=0.0,
        value=20000.0,
        step=1000.0
    )
    
    rent = st.number_input(
        f"Monthly Rent ({currency})",
        min_value=0.0,
        value=5000.0,
        step=500.0
    )

with col_opex2:
    marketing = st.number_input(
        f"Monthly Marketing ({currency})",
        min_value=0.0,
        value=3000.0,
        step=500.0
    )
    
    other_opex = st.number_input(
        f"Other Monthly OpEx ({currency})",
        min_value=0.0,
        value=2000.0,
        step=500.0
    )

# Advanced Parameters (collapsible)
with st.expander("🔧 Advanced Parameters"):
    col_adv1, col_adv2 = st.columns(2)
    
    with col_adv1:
        discount_rate = st.number_input(
            "Discount Rate for DCF (%)",
            min_value=1.0,
            max_value=30.0,
            value=12.0,
            step=0.5
        )
        
        terminal_growth_rate = st.number_input(
            "Terminal Growth Rate (%)",
            min_value=0.0,
            max_value=10.0,
            value=3.0,
            step=0.5
        )
    
    with col_adv2:
        tax_rate = st.number_input(
            "Tax Rate (%)",
            min_value=0.0,
            max_value=50.0,
            value=25.0,
            step=1.0
        )
        
        capex_percentage = st.number_input(
            "CapEx as % of Revenue",
            min_value=0.0,
            max_value=20.0,
            value=2.0,
            step=0.5
        )

st.divider()

# Generate Button
if st.button("🚀 Generate Advanced Financial Model", type="primary", use_container_width=True):
    
    if not company_name:
        st.error("⚠️ Please enter company name")
    else:
        with st.spinner("🤖 Generating comprehensive financial model with advanced analytics..."):
            
            # Calculate monthly data
            months = []
            revenues = []
            cogs_list = []
            gross_profits = []
            opex_list = []
            ebitda_list = []
            ebit_list = []
            taxes_list = []
            net_income_list = []
            capex_list = []
            cash_balance = [initial_cash]
            
            current_revenue = initial_monthly_revenue
            current_cogs_pct = cogs_percentage / 100
            
            for month in range(int(num_months)):
                month_date = start_month + relativedelta(months=month)
                months.append(month_date.strftime('%Y-%m'))
                
                # Revenue with growth and seasonality
                revenue = current_revenue * (1 + monthly_growth_rate / 100) ** month
                
                # Add seasonality (simple sine wave)
                seasonal_factor = 1 + (revenue_seasonality / 100) * np.sin(2 * np.pi * month / 12)
                revenue *= seasonal_factor
                
                revenues.append(revenue)
                
                # COGS with annual growth and margin improvement
                annual_factor = (1 + cogs_growth_rate / 100) ** (month / 12)
                margin_factor = (1 - margin_improvement / 100) ** (month / 12)
                cogs = revenue * current_cogs_pct * annual_factor * margin_factor
                cogs_list.append(cogs)
                
                # Gross Profit
                gross_profit = revenue - cogs
                gross_profits.appen
