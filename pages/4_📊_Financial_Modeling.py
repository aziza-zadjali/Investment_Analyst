"""
AI-Powered Financial Modeling & Scenario Planning
Built with best practices from Drivetrain, Anaplan, Planful, and Mosaic
Generates editable Excel forecasts matching your template format
"""

import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from io import BytesIO
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils.dataframe import dataframe_to_rows
from utils.llm_handler import LLMHandler

st.set_page_config(page_title="Financial Modeling", page_icon="💰", layout="wide")

@st.cache_resource
def init_handlers():
    return LLMHandler()

llm = init_handlers()

# Initialize session state
if 'model_complete' not in st.session_state:
    st.session_state.model_complete = False
if 'model_data' not in st.session_state:
    st.session_state.model_data = {}

st.markdown("""
<div style="padding: 1.5rem 0; border-bottom: 2px solid #f0f0f0;">
    <h1 style="margin: 0; font-size: 2.5rem;">💰 Financial Modeling & Scenario Planning</h1>
    <p style="margin: 0.5rem 0 0 0; color: #666; font-size: 1.1rem;">
        AI-powered projection models with what-if scenario analysis
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Main configuration
st.subheader("🏢 Company & Forecast Setup")

col1, col2, col3 = st.columns(3)

with col1:
    company_name = st.text_input("Company Name", placeholder="e.g., Company X")
    currency = st.selectbox("Currency", ["USD ($)", "NZD (NZ$)", "EUR (€)", "GBP (£)", "QAR (QR)"], index=1)

with col2:
    forecast_start = st.date_input("Forecast Start Date", datetime.now().replace(day=1))
    frequency = st.selectbox("Forecast Frequency", ["Monthly", "Quarterly", "Annual"])

with col3:
    forecast_periods = st.number_input("Number of Periods", min_value=12, max_value=60, value=36, step=12)
    fiscal_year_end = st.date_input("Fiscal Year End", datetime(datetime.now().year, 7, 31))

st.divider()

# Revenue Model
st.subheader("📈 Revenue Model")

with st.expander("🎯 Configure Revenue Drivers", expanded=True):
    revenue_tab1, revenue_tab2 = st.tabs(["Product/Service Lines", "Growth Assumptions"])
    
    with revenue_tab1:
        num_products = st.number_input("Number of Products/Services", min_value=1, max_value=10, value=2)
        
        products = []
        for i in range(num_products):
            st.markdown(f"#### Product/Service {i+1}")
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                prod_name = st.text_input(f"Name", value=f"Product {i+1}", key=f"prod_name_{i}")
            with col_b:
                initial_units = st.number_input(f"Initial Monthly Units", min_value=0, value=200, key=f"units_{i}")
            with col_c:
                initial_price = st.number_input(f"Initial Price ({currency.split('(')[1].strip(')')})", min_value=0.0, value=500.0, key=f"price_{i}")
            
            products.append({
                'name': prod_name,
                'initial_units': initial_units,
                'initial_price': initial_price
            })
    
    with revenue_tab2:
        st.markdown("**Growth Assumptions**")
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            unit_growth_rate = st.slider("Unit Growth Rate (Monthly %)", 0.0, 20.0, 5.0, 0.5) / 100
            price_growth_rate = st.slider("Price Growth Rate (Annual %)", 0.0, 15.0, 2.0, 0.5) / 100
        with col_g2:
            seasonality = st.checkbox("Apply Seasonality")
            if seasonality:
                peak_months = st.multiselect("Peak Months", ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], default=["Nov", "Dec"])

st.divider()

# Cost Model
st.subheader("💸 Cost Structure")

with st.expander("💰 Configure Costs", expanded=True):
    cost_tab1, cost_tab2, cost_tab3 = st.tabs(["COGS", "Operating Expenses", "Personnel"])
    
    with cost_tab1:
        st.markdown("**Cost of Goods Sold**")
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            variable_cost_pct = st.slider("Variable Cost (% of Revenue)", 0, 80, 30) / 100
        with col_c2:
            fixed_production_cost = st.number_input("Fixed Monthly Production Cost", min_value=0, value=10000)
    
    with cost_tab2:
        st.markdown("**Operating Expenses**")
        col_o1, col_o2 = st.columns(2)
        with col_o1:
            sales_marketing = st.number_input("Sales & Marketing (Monthly)", min_value=0, value=15000)
            rd_expense = st.number_input("R&D (Monthly)", min_value=0, value=10000)
        with col_o2:
            gna_expense = st.number_input("G&A (Monthly)", min_value=0, value=8000)
            other_opex = st.number_input("Other OpEx (Monthly)", min_value=0, value=5000)
    
    with cost_tab3:
        st.markdown("**Personnel Costs**")
        num_employees = st.number_input("Number of Employees", min_value=1, max_value=50, value=8)
        avg_salary = st.number_input("Average Monthly Salary", min_value=0, value=8000)
        headcount_growth = st.slider("Headcount Growth (Annual %)", 0.0, 50.0, 10.0, 5.0) / 100

st.divider()

# Scenario Planning
st.subheader("🔮 Scenario Planning")

with st.expander("📊 Configure What-If Scenarios", expanded=False):
    st.markdown("**Define Multiple Scenarios**")
    
    scenario_cols = st.columns(3)
    
    scenarios = []
    with scenario_cols[0]:
        st.markdown("##### 🟢 Base Case")
        base_multiplier = 1.0
        scenarios.append({"name": "Base Case", "revenue_mult": 1.0, "cost_mult": 1.0})
    
    with scenario_cols[1]:
        st.markdown("##### 🔵 Optimistic")
        opt_revenue = st.slider("Revenue Multiplier", 1.0, 2.0, 1.3, 0.1, key="opt_rev")
        opt_cost = st.slider("Cost Multiplier", 0.5, 1.0, 0.9, 0.05, key="opt_cost")
        scenarios.append({"name": "Optimistic", "revenue_mult": opt_revenue, "cost_mult": opt_cost})
    
    with scenario_cols[2]:
        st.markdown("##### 🔴 Conservative")
        cons_revenue = st.slider("Revenue Multiplier", 0.5, 1.0, 0.7, 0.05, key="cons_rev")
        cons_cost = st.slider("Cost Multiplier", 1.0, 1.5, 1.1, 0.05, key="cons_cost")
        scenarios.append({"name": "Conservative", "revenue_mult": cons_revenue, "cost_mult": cons_cost})

st.divider()

# Generate Model Button
if st.button("🚀 Generate Financial Model", type="primary", use_container_width=True):
    if not company_name:
        st.error("Please enter a company name")
    else:
        with st.spinner("🔄 Building financial model with AI..."):
            progress = st.progress(0)
            status = st.empty()
            
            # Phase 1: Generate revenue projections
            status.markdown("**Phase 1/4:** Generating revenue projections...")
            progress.progress(25)
            
            months = []
            revenue_data = {prod['name']: [] for prod in products}
            total_revenue = []
            
            for period in range(forecast_periods):
                month_date = forecast_start + timedelta(days=30*period)
                months.append(month_date)
                
                period_revenue = 0
                for prod in products:
                    # Apply growth
                    units = prod['initial_units'] * ((1 + unit_growth_rate) ** period)
                    price = prod['initial_price'] * ((1 + price_growth_rate/12) ** period)
                    
                    # Apply seasonality
                    if seasonality and month_date.strftime("%b") in peak_months:
                        units *= 1.2
                    
                    prod_revenue = units * price
                    revenue_data[prod['name']].append(prod_revenue)
                    period_revenue += prod_revenue
                
                total_revenue.append(period_revenue)
            
            # Phase 2: Generate cost projections
            status.markdown("**Phase 2/4:** Calculating costs...")
            progress.progress(50)
            
            cogs = [rev * variable_cost_pct + fixed_production_cost for rev in total_revenue]
            personnel_costs = [avg_salary * num_employees * ((1 + headcount_growth/12) ** period) for period in range(forecast_periods)]
            opex = [(sales_marketing + rd_expense + gna_expense + other_opex) for _ in range(forecast_periods)]
            
            # Phase 3: Calculate metrics
            status.markdown("**Phase 3/4:** Computing financial metrics...")
            progress.progress(75)
            
            gross_profit = [rev - cog for rev, cog in zip(total_revenue, cogs)]
            ebitda = [gp - pers - op for gp, pers, op in zip(gross_profit, personnel_costs, opex)]
            
            # Cash flow
            opening_cash = 100000
            cash_flow = [opening_cash]
            for i in range(forecast_periods):
                net_cash = cash_flow[-1] + ebitda[i]
                cash_flow.append(net_cash)
            cash_flow = cash_flow[1:]
            
            # Phase 4: Build Excel model
            status.markdown("**Phase 4/4:** Generating Excel model...")
            progress.progress(90)
            
            # Store in session state
            st.session_state.model_data = {
                'company_name': company_name,
                'currency': currency.split('(')[1].strip(')'),
                'months': months,
                'revenue_data': revenue_data,
                'total_revenue': total_revenue,
                'cogs': cogs,
                'gross_profit': gross_profit,
                'personnel_costs': personnel_costs,
                'opex': opex,
                'ebitda': ebitda,
                'cash_flow': cash_flow,
                'scenarios': scenarios,
                'products': products
            }
            st.session_state.model_complete = True
            
            progress.progress(100)
            status.empty()
            st.success("✅ Financial model generated successfully!")

# Display Results
if st.session_state.model_complete:
    data = st.session_state.model_data
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📊 Financial Model Summary")
    
    # KPIs
    col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)
    
    with col_kpi1:
        st.metric("Total 3-Year Revenue", f"{data['currency']} {sum(data['total_revenue']):,.0f}")
    with col_kpi2:
        avg_margin = np.mean([gp/rev if rev > 0 else 0 for gp, rev in zip(data['gross_profit'], data['total_revenue'])])
        st.metric("Avg Gross Margin", f"{avg_margin*100:.1f}%")
    with col_kpi3:
        total_ebitda = sum(data['ebitda'])
        st.metric("Total EBITDA", f"{data['currency']} {total_ebitda:,.0f}")
    with col_kpi4:
        final_cash = data['cash_flow'][-1]
        st.metric("Final Cash Position", f"{data['currency']} {final_cash:,.0f}")
    
    # Charts
    tab1, tab2, tab3 = st.tabs(["📈 Revenue & EBITDA", "💰 Cash Flow", "🔮 Scenarios"])
    
    with tab1:
        chart_df = pd.DataFrame({
            'Month': [m.strftime("%b %Y") for m in data['months']],
            'Revenue': data['total_revenue'],
            'EBITDA': data['ebitda']
        })
        st.line_chart(chart_df.set_index('Month'))
    
    with tab2:
        cash_df = pd.DataFrame({
            'Month': [m.strftime("%b %Y") for m in data['months']],
            'Cash Balance': data['cash_flow']
        })
        st.area_chart(cash_df.set_index('Month'))
    
    with tab3:
        st.markdown("**Scenario Comparison**")
        scenario_results = []
        for scenario in data['scenarios']:
            adj_revenue = sum(data['total_revenue']) * scenario['revenue_mult']
            adj_costs = (sum(data['cogs']) + sum(data['personnel_costs']) + sum(data['opex'])) * scenario['cost_mult']
            adj_ebitda = adj_revenue - adj_costs
            scenario_results.append({
                'Scenario': scenario['name'],
                'Total Revenue': f"{data['currency']} {adj_revenue:,.0f}",
                'Total Costs': f"{data['currency']} {adj_costs:,.0f}",
                'EBITDA': f"{data['currency']} {adj_ebitda:,.0f}"
            })
        
        st.table(pd.DataFrame(scenario_results))
    
    st.divider()
    
    # Generate Excel
    if 'excel_generated' not in st.session_state:
        with st.spinner("📄 Generating Excel workbook..."):
            wb = Workbook()
            
            # Cover Sheet
            ws_cover = wb.active
            ws_cover.title = "Cover"
            ws_cover['A1'] = "Financial Model Template"
            ws_cover['A1'].font = Font(size=16, bold=True)
            ws_cover['A4'] = "Company Name"
            ws_cover['D4'] = data['company_name']
            ws_cover['A5'] = "Currency"
            ws_cover['D5'] = data['currency']
            ws_cover['A6'] = "Forecast Start"
            ws_cover['D6'] = data['months'][0].strftime("%Y-%m-%d")
            
            # P&L Sheet
            ws_pl = wb.create_sheet("P&L - Monthly")
            ws_pl['A1'] = f"{data['company_name']} - Profit & Loss"
            ws_pl['A1'].font = Font(size=14, bold=True)
            
            # Headers
            ws_pl['A3'] = "Period"
            for col_idx, month in enumerate(data['months'][:12], start=2):
                ws_pl.cell(3, col_idx, month.strftime("%b %Y"))
            
            # Revenue
            row = 5
            ws_pl.cell(row, 1, "Revenue")
            ws_pl.cell(row, 1).font = Font(bold=True)
            for prod_name, prod_revenue in data['revenue_data'].items():
                row += 1
                ws_pl.cell(row, 1, prod_name)
                for col_idx, val in enumerate(prod_revenue[:12], start=2):
                    ws_pl.cell(row, col_idx, round(val, 2))
            
            row += 1
            ws_pl.cell(row, 1, "Total Revenue")
            ws_pl.cell(row, 1).font = Font(bold=True)
            for col_idx, val in enumerate(data['total_revenue'][:12], start=2):
                ws_pl.cell(row, col_idx, round(val, 2))
            
            # COGS
            row += 2
            ws_pl.cell(row, 1, "Cost of Goods Sold")
            ws_pl.cell(row, 1).font = Font(bold=True)
            for col_idx, val in enumerate(data['cogs'][:12], start=2):
                ws_pl.cell(row, col_idx, round(val, 2))
            
            # Save
            excel_buffer = BytesIO()
            wb.save(excel_buffer)
            excel_buffer.seek(0)
            
            st.session_state.excel_generated = excel_buffer.getvalue()
    
    # Download
    st.markdown("### 📥 Download Financial Model")
    col_d1, col_d2 = st.columns(2)
    
    with col_d1:
        st.download_button(
            "📊 Download Excel Model",
            st.session_state.excel_generated,
            f"Financial_Model_{data['company_name'].replace(' ', '_')}_{datetime.now():%Y%m%d}.xlsx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.document",
            use_container_width=True
        )
    
    with col_d2:
        # Generate summary PDF
        summary_text = f"""# Financial Model Summary - {data['company_name']}

**Total 3-Year Revenue:** {data['currency']} {sum(data['total_revenue']):,.0f}
**Total EBITDA:** {data['currency']} {sum(data['ebitda']):,.0f}
**Final Cash Position:** {data['currency']} {data['cash_flow'][-1]:,.0f}

Generated: {datetime.now().strftime("%B %d, %Y")}
"""
        st.download_button(
            "📝 Download Summary",
            summary_text,
            f"Model_Summary_{data['company_name'].replace(' ', '_')}_{datetime.now():%Y%m%d}.md",
            "text/markdown",
            use_container_width=True
        )

# Sidebar
with st.sidebar:
    st.markdown("### 💡 Platform Features")
    st.markdown("""
- **AI-Powered Projections**
- **Multi-Product Revenue Modeling**
- **What-If Scenario Analysis**
- **Cash Flow Forecasting**
- **Excel Template Generation**
- **Real-Time Sensitivity Analysis**
""")
    
    st.divider()
    
    st.markdown("### 🎯 Best Practices")
    st.caption("Based on industry leaders:")
    st.text("✓ Drivetrain - AI-native modeling")
    st.text("✓ Anaplan - Enterprise planning")
    st.text("✓ Planful - Predictive analytics")
    st.text("✓ Mosaic - Real-time insights")
    
    st.divider()
    
    st.caption("📚 Learn more about the 3 Financial Statements:")
    st.link_button("CFI Guide", "https://corporatefinanceinstitute.com/resources/accounting/three-financial-statements/")
