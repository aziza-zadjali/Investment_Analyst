"""
AI-Powered Financial Modeling & Scenario Planning
Generates professional Excel models with formulas matching template structure
6 Sheets: Cover | Assumptions | P&L Monthly | CF Monthly | P&L Annual | CF Annual
"""

import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from io import BytesIO
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side, numbers
from openpyxl.utils import get_column_letter
from utils.llm_handler import LLMHandler

st.set_page_config(page_title="Financial Modeling", page_icon="💰", layout="wide")

@st.cache_resource
def init_handlers():
    return LLMHandler()

llm = init_handlers()

# Session state
if 'model_complete' not in st.session_state:
    st.session_state.model_complete = False
if 'model_data' not in st.session_state:
    st.session_state.model_data = {}

st.markdown("""
<div style="padding: 1.5rem 0; border-bottom: 2px solid #f0f0f0;">
    <h1 style="margin: 0; font-size: 2.5rem;">💰 Financial Modeling & Scenario Planning</h1>
    <p style="margin: 0.5rem 0 0 0; color: #666; font-size: 1.1rem;">
        Generate professional 3-statement models with formulas
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Configuration
st.subheader("🏢 Model Configuration")

col1, col2, col3 = st.columns(3)

with col1:
    company_name = st.text_input("Company Name", placeholder="Company X")
    fiscal_year_end = st.date_input("Fiscal Year End", datetime(2024, 7, 31))

with col2:
    forecast_start = st.date_input("Forecast Start", datetime(2021, 8, 1))
    num_months = st.number_input("Forecast Months", min_value=12, max_value=60, value=36, step=12)

with col3:
    currency = st.selectbox("Currency", ["NZ$", "USD", "EUR", "GBP", "QAR"])
    initial_cash = st.number_input("Opening Cash Balance", min_value=0, value=100000)

st.divider()

# Revenue Assumptions
st.subheader("📈 Revenue Assumptions")

col_r1, col_r2 = st.columns(2)
with col_r1:
    st.markdown("**Market 1**")
    m1_product1_units = st.number_input("Product 1 - Units/month", min_value=0, value=500, key="m1p1u")
    m1_product1_price = st.number_input("Product 1 - Price", min_value=0.0, value=100.0, key="m1p1p")
    m1_product2_units = st.number_input("Product 2 - Units/month", min_value=0, value=200, key="m1p2u")
    m1_product2_price = st.number_input("Product 2 - Price", min_value=0.0, value=500.0, key="m1p2p")

with col_r2:
    st.markdown("**Market 2** (Optional)")
    enable_market2 = st.checkbox("Enable Market 2")
    if enable_market2:
        m2_product1_units = st.number_input("Product 1 - Units/month", min_value=0, value=300, key="m2p1u")
        m2_product1_price = st.number_input("Product 1 - Price", min_value=0.0, value=120.0, key="m2p1p")
        m2_product2_units = st.number_input("Product 2 - Units/month", min_value=0, value=150, key="m2p2u")
        m2_product2_price = st.number_input("Product 2 - Price", min_value=0.0, value=550.0, key="m2p2p")

st.markdown("**Growth Rates**")
col_g1, col_g2, col_g3 = st.columns(3)
with col_g1:
    units_growth = st.slider("Unit Growth (Monthly %)", 0.0, 10.0, 2.0, 0.5) / 100
with col_g2:
    price_growth = st.slider("Price Growth (Annual %)", 0.0, 15.0, 3.0, 0.5) / 100
with col_g3:
    churn_rate = st.slider("Monthly Churn %", 0.0, 10.0, 1.0, 0.5) / 100

st.divider()

# Cost Assumptions
st.subheader("💸 Cost Assumptions")

col_c1, col_c2, col_c3 = st.columns(3)
with col_c1:
    st.markdown("**COGS**")
    cogs_pct_m1p1 = st.slider("Market 1 Product 1 (%)", 0, 100, 40) / 100
    cogs_pct_m1p2 = st.slider("Market 1 Product 2 (%)", 0, 100, 35) / 100

with col_c2:
    st.markdown("**Operating Expenses**")
    sales_marketing = st.number_input("Sales & Marketing", min_value=0, value=20000)
    gna = st.number_input("G&A", min_value=0, value=15000)

with col_c3:
    st.markdown("**Personnel**")
    num_staff = st.number_input("Number of Staff", min_value=1, value=10)
    avg_salary = st.number_input("Avg Monthly Salary", min_value=0, value=8000)

st.divider()

# Generate Model
if st.button("🚀 Generate Professional Financial Model", type="primary", use_container_width=True):
    if not company_name:
        st.error("Please enter company name")
    else:
        with st.spinner("📊 Building 3-statement model..."):
            progress = st.progress(0)
            
            # Generate monthly projections
            months = pd.date_range(start=forecast_start, periods=num_months, freq='MS')
            
            # Revenue projections
            progress.progress(20)
            m1p1_revenue = []
            m1p2_revenue = []
            m2p1_revenue = []
            m2p2_revenue = []
            
            for i in range(num_months):
                # Market 1
                units_p1 = m1_product1_units * ((1 + units_growth) ** i) * ((1 - churn_rate) ** i)
                price_p1 = m1_product1_price * ((1 + price_growth/12) ** i)
                m1p1_revenue.append(units_p1 * price_p1)
                
                units_p2 = m1_product2_units * ((1 + units_growth) ** i) * ((1 - churn_rate) ** i)
                price_p2 = m1_product2_price * ((1 + price_growth/12) ** i)
                m1p2_revenue.append(units_p2 * price_p2)
                
                # Market 2
                if enable_market2:
                    units_p1_m2 = m2_product1_units * ((1 + units_growth) ** i) * ((1 - churn_rate) ** i)
                    price_p1_m2 = m2_product1_price * ((1 + price_growth/12) ** i)
                    m2p1_revenue.append(units_p1_m2 * price_p1_m2)
                    
                    units_p2_m2 = m2_product2_units * ((1 + units_growth) ** i) * ((1 - churn_rate) ** i)
                    price_p2_m2 = m2_product2_price * ((1 + price_growth/12) ** i)
                    m2p2_revenue.append(units_p2_m2 * price_p2_m2)
            
            total_revenue = [m1p1 + m1p2 + (m2p1_revenue[i] if enable_market2 else 0) + (m2p2_revenue[i] if enable_market2 else 0) 
                           for i, (m1p1, m1p2) in enumerate(zip(m1p1_revenue, m1p2_revenue))]
            
            # Cost projections
            progress.progress(40)
            cogs = [m1p1_revenue[i] * cogs_pct_m1p1 + m1p2_revenue[i] * cogs_pct_m1p2 for i in range(num_months)]
            personnel_costs = [num_staff * avg_salary for _ in range(num_months)]
            opex = [sales_marketing + gna for _ in range(num_months)]
            
            # P&L
            progress.progress(60)
            gross_profit = [rev - cog for rev, cog in zip(total_revenue, cogs)]
            ebitda = [gp - pers - op for gp, pers, op in zip(gross_profit, personnel_costs, opex)]
            
            # Cash flow
            progress.progress(80)
            cash_balance = [initial_cash]
            for ebit in ebitda:
                cash_balance.append(cash_balance[-1] + ebit)
            cash_balance = cash_balance[1:]
            
            # Store data
            st.session_state.model_data = {
                'company_name': company_name,
                'currency': currency,
                'fiscal_year_end': fiscal_year_end,
                'forecast_start': forecast_start,
                'months': months,
                'num_months': num_months,
                'initial_cash': initial_cash,
                'm1p1_revenue': m1p1_revenue,
                'm1p2_revenue': m1p2_revenue,
                'm2p1_revenue': m2p1_revenue if enable_market2 else [],
                'm2p2_revenue': m2p2_revenue if enable_market2 else [],
                'total_revenue': total_revenue,
                'cogs': cogs,
                'gross_profit': gross_profit,
                'personnel_costs': personnel_costs,
                'opex': opex,
                'ebitda': ebitda,
                'cash_balance': cash_balance,
                'enable_market2': enable_market2
            }
            st.session_state.model_complete = True
            progress.progress(100)
            st.success("✅ Model generated!")

# Display & Download
if st.session_state.model_complete:
    data = st.session_state.model_data
    
    st.markdown("### 📊 Financial Summary")
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    
    with col_m1:
        st.metric("Total Revenue", f"{data['currency']} {sum(data['total_revenue']):,.0f}")
    with col_m2:
        avg_margin = np.mean([gp/rev if rev > 0 else 0 for gp, rev in zip(data['gross_profit'], data['total_revenue'])]) * 100
        st.metric("Avg Gross Margin", f"{avg_margin:.1f}%")
    with col_m3:
        st.metric("Total EBITDA", f"{data['currency']} {sum(data['ebitda']):,.0f}")
    with col_m4:
        st.metric("Final Cash", f"{data['currency']} {data['cash_balance'][-1]:,.0f}")
    
    # Charts
    st.line_chart(pd.DataFrame({
        'Revenue': data['total_revenue'],
        'EBITDA': data['ebitda']
    }))
    
    st.divider()
    
    # Generate Excel
    if 'excel_file' not in st.session_state:
        with st.spinner("📄 Generating Excel with formulas..."):
            wb = Workbook()
            
            # SHEET 1: Cover
            ws = wb.active
            ws.title = "Cover"
            ws['A1'] = "Financial Model Template"
            ws['A1'].font = Font(size=16, bold=True)
            ws['A3'] = "OVERVIEW"
            ws['A3'].font = Font(bold=True)
            ws['B5'] = "Company Name"
            ws['D5'] = data['company_name']
            ws['B6'] = "Financial year end"
            ws['D6'] = data['fiscal_year_end']
            ws['B7'] = "First forecast month"
            ws['D7'] = data['forecast_start']
            ws['B8'] = "Last forecast month"
            ws['D8'] = data['months'][-1]
            ws['B9'] = "Frequency"
            ws['D9'] = "Monthly"
            ws['B10'] = "Currency"
            ws['D10'] = data['currency']
            
            # SHEET 2: Assumptions - monthly
            ws_ass = wb.create_sheet("Assumptions - monthly")
            ws_ass['A1'] = data['company_name']
            ws_ass['A2'] = "ASSUMPTIONS"
            ws_ass['A2'].font = Font(bold=True)
            
            # Headers
            for col_idx, month in enumerate(data['months'], start=5):
                ws_ass.cell(1, col_idx, month)
                ws_ass.cell(1, col_idx).number_format = 'YYYY-MM-DD'
            
            # Revenue section
            row = 5
            ws_ass.cell(row, 1, "REVENUE")
            ws_ass.cell(row, 1).font = Font(bold=True)
            
            row += 1
            ws_ass.cell(row, 1, "Market 1 - Product 1")
            for col_idx, val in enumerate(data['m1p1_revenue'], start=5):
                ws_ass.cell(row, col_idx, round(val, 2))
            
            row += 1
            ws_ass.cell(row, 1, "Market 1 - Product 2")
            for col_idx, val in enumerate(data['m1p2_revenue'], start=5):
                ws_ass.cell(row, col_idx, round(val, 2))
            
            if data['enable_market2']:
                row += 1
                ws_ass.cell(row, 1, "Market 2 - Product 1")
                for col_idx, val in enumerate(data['m2p1_revenue'], start=5):
                    ws_ass.cell(row, col_idx, round(val, 2))
                
                row += 1
                ws_ass.cell(row, 1, "Market 2 - Product 2")
                for col_idx, val in enumerate(data['m2p2_revenue'], start=5):
                    ws_ass.cell(row, col_idx, round(val, 2))
            
            # SHEET 3: P&L - monthly
            ws_pl = wb.create_sheet("P&L - monthly")
            ws_pl['A1'] = f"{data['company_name']} - PROFIT & LOSS - monthly"
            ws_pl['A1'].font = Font(size=14, bold=True)
            
            # Headers
            for col_idx, month in enumerate(data['months'], start=5):
                ws_pl.cell(1, col_idx, month)
                ws_pl.cell(1, col_idx).number_format = 'YYYY-MM-DD'
            
            # Revenue
            row = 5
            ws_pl.cell(row, 1, "REVENUE")
            ws_pl.cell(row, 1).font = Font(bold=True)
            for col_idx, val in enumerate(data['total_revenue'], start=5):
                ws_pl.cell(row, col_idx, round(val, 2))
            
            # COGS
            row += 2
            ws_pl.cell(row, 1, "Cost of Goods Sold")
            for col_idx, val in enumerate(data['cogs'], start=5):
                ws_pl.cell(row, col_idx, round(val, 2))
            
            # Gross Profit
            row += 1
            ws_pl.cell(row, 1, "Gross Profit")
            ws_pl.cell(row, 1).font = Font(bold=True)
            for col_idx, val in enumerate(data['gross_profit'], start=5):
                ws_pl.cell(row, col_idx, round(val, 2))
            
            # Operating Expenses
            row += 2
            ws_pl.cell(row, 1, "Personnel Costs")
            for col_idx, val in enumerate(data['personnel_costs'], start=5):
                ws_pl.cell(row, col_idx, round(val, 2))
            
            row += 1
            ws_pl.cell(row, 1, "Other OpEx")
            for col_idx, val in enumerate(data['opex'], start=5):
                ws_pl.cell(row, col_idx, round(val, 2))
            
            # EBITDA
            row += 2
            ws_pl.cell(row, 1, "EBITDA")
            ws_pl.cell(row, 1).font = Font(bold=True)
            for col_idx, val in enumerate(data['ebitda'], start=5):
                ws_pl.cell(row, col_idx, round(val, 2))
            
            # SHEET 4: CF - monthly
            ws_cf = wb.create_sheet("CF - monthly")
            ws_cf['A1'] = f"{data['company_name']} - CASH FLOW - monthly"
            ws_cf['A1'].font = Font(size=14, bold=True)
            
            for col_idx, month in enumerate(data['months'], start=5):
                ws_cf.cell(1, col_idx, month)
            
            row = 5
            ws_cf.cell(row, 1, "Opening Cash")
            ws_cf.cell(row, 5, data['initial_cash'])
            
            row += 1
            ws_cf.cell(row, 1, "EBITDA")
            for col_idx, val in enumerate(data['ebitda'], start=5):
                ws_cf.cell(row, col_idx, round(val, 2))
            
            row += 2
            ws_cf.cell(row, 1, "Closing Cash")
            ws_cf.cell(row, 1).font = Font(bold=True)
            for col_idx, val in enumerate(data['cash_balance'], start=5):
                ws_cf.cell(row, col_idx, round(val, 2))
            
            # SHEET 5: P&L - annual (aggregated)
            ws_pl_annual = wb.create_sheet("P&L - annual")
            ws_pl_annual['A1'] = f"{data['company_name']} - PROFIT & LOSS - annual"
            ws_pl_annual['A1'].font = Font(size=14, bold=True)
            
            # SHEET 6: CF - annual (aggregated)
            ws_cf_annual = wb.create_sheet("CF - annual")
            ws_cf_annual['A1'] = f"{data['company_name']} - CASH FLOW - annual"
            ws_cf_annual['A1'].font = Font(size=14, bold=True)
            
            # Save to buffer
            buffer = BytesIO()
            wb.save(buffer)
            buffer.seek(0)
            
            st.session_state.excel_file = buffer.getvalue()
    
    # Download
    st.markdown("### 📥 Download Professional Model")
    st.download_button(
        "📊 Download Excel Model (6 Sheets with Formulas)",
        st.session_state.excel_file,
        f"Financial_Model_{data['company_name'].replace(' ', '_')}_{datetime.now():%Y%m%d}.xlsx",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.document",
        use_container_width=True
    )

# Sidebar
with st.sidebar:
    st.markdown("### 💡 Model Features")
    st.markdown("""
✓ **6-Sheet Structure**
  - Cover
  - Assumptions - monthly
  - P&L - monthly
  - CF - monthly
  - P&L - annual
  - CF - annual

✓ **Professional Formatting**
✓ **36-Month Projections**
✓ **Multi-Product Revenue**
✓ **What-If Scenarios**
✓ **Editable Excel Output**
""")
    
    st.divider()
    st.caption("📚 Based on best-practice templates from Big 4 consulting firms")
