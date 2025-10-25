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
                gross_profits.append(gross_profit)
                
                # Operating Expenses (with some growth)
                opex_growth = 1 + (2.0 / 100) ** (month / 12)  # 2% annual growth
                total_opex = (salaries + rent + marketing + other_opex) * opex_growth
                opex_list.append(total_opex)
                
                # EBITDA
                ebitda = gross_profit - total_opex
                ebitda_list.append(ebitda)
                
                # EBIT (same as EBITDA for simplicity)
                ebit = ebitda
                ebit_list.append(ebit)
                
                # Taxes
                taxes = max(0, ebit * tax_rate / 100)
                taxes_list.append(taxes)
                
                # Net Income
                net_income = ebit - taxes
                net_income_list.append(net_income)
                
                # CapEx
                capex = revenue * capex_percentage / 100
                capex_list.append(capex)
                
                # Cash Flow
                net_cash_flow = net_income + capex  # Adding back CapEx for cash flow
                new_cash = cash_balance[-1] + net_cash_flow
                cash_balance.append(new_cash)
            
            # Remove initial cash from balance for display
            cash_balance = cash_balance[1:]
            
            # Store in session state
            st.session_state.model_data = {
                'company_name': company_name,
                'currency': currency,
                'fiscal_year_end': fiscal_year_end.strftime('%Y-%m-%d'),
                'start_month': start_month.strftime('%Y-%m-%d'),
                'num_months': int(num_months),
                'initial_cash': initial_cash,
                'months': months,
                'revenues': revenues,
                'cogs': cogs_list,
                'gross_profits': gross_profits,
                'opex': opex_list,
                'ebitda': ebitda_list,
                'ebit': ebit_list,
                'taxes': taxes_list,
                'net_income': net_income_list,
                'capex': capex_list,
                'cash_balance': cash_balance,
                'salaries': salaries,
                'rent': rent,
                'marketing': marketing,
                'other_opex': other_opex,
                'cogs_percentage': cogs_percentage,
                'monthly_growth_rate': monthly_growth_rate,
                'cogs_growth_rate': cogs_growth_rate,
                'initial_revenue': initial_monthly_revenue,
                'discount_rate': discount_rate,
                'terminal_growth_rate': terminal_growth_rate,
                'tax_rate': tax_rate,
                'capex_percentage': capex_percentage
            }
            
            st.session_state.model_complete = True
            st.success("✅ Advanced Financial Model Generated!")
            st.rerun()

# Display Results
if st.session_state.model_complete:
    
    st.divider()
    st.subheader("📊 Financial Dashboard")
    
    data = st.session_state.model_data
    user_currency = data.get('currency', 'USD $')
    
    # Key Metrics
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    
    with col_m1:
        total_revenue = sum(data.get('revenues', []))
        st.metric("Total Revenue", f"{user_currency} {total_revenue:,.0f}")
    
    with col_m2:
        avg_ebitda = np.mean(data.get('ebitda', [0]))
        st.metric("Avg Monthly EBITDA", f"{user_currency} {avg_ebitda:,.0f}")
    
    with col_m3:
        total_net_income = sum(data.get('net_income', []))
        st.metric("Total Net Income", f"{user_currency} {total_net_income:,.0f}")
    
    with col_m4:
        final_cash = data.get('cash_balance', [0])[-1] if data.get('cash_balance') else 0
        st.metric("Final Cash", f"{user_currency} {final_cash:,.0f}")
    
    # Charts
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.markdown("**📈 Revenue & EBITDA Trend**")
        chart_data = pd.DataFrame({
            'Month': range(1, len(data.get('revenues', [])) + 1),
            'Revenue': data.get('revenues', []),
            'EBITDA': data.get('ebitda', [])
        })
        
        fig = px.line(chart_data, x='Month', y=['Revenue', 'EBITDA'], 
                      title="Revenue & EBITDA Forecast")
        st.plotly_chart(fig, use_container_width=True)
    
    with col_chart2:
        st.markdown("**💰 Cash Balance Forecast**")
        cash_chart = pd.DataFrame({
            'Month': range(1, len(data.get('cash_balance', [])) + 1),
            'Cash': data.get('cash_balance', [])
        })
        
        fig2 = px.line(cash_chart, x='Month', y='Cash', 
                       title="Cash Balance Projection")
        st.plotly_chart(fig2, use_container_width=True)
    
    # Advanced Analysis Section
    if FINANCIAL_ANALYZER_AVAILABLE:
        st.divider()
        st.subheader("📈 Advanced Financial Analysis")
        
        # Initialize analyzer
        analyzer = FinancialAnalyzer()
        
        # Create tabs for different analyses
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Scenarios", "💰 DCF Valuation", "📉 Ratios", "⚡ Sensitivity"])
        
        with tab1:
            st.markdown("### Multi-Scenario Analysis")
            
            base_data = {
                'revenue': data.get('initial_revenue', 50000) * 12  # Annual
            }
            
            try:
                scenarios = analyzer.run_scenario_analysis(base_data)
                
                # Display scenarios
                col_s1, col_s2, col_s3 = st.columns(3)
                
                scenario_names = ['conservative', 'moderate', 'aggressive']
                scenario_colors = ['red', 'blue', 'green']
                
                for i, (scenario_name, color) in enumerate(zip(scenario_names, scenario_colors)):
                    with [col_s1, col_s2, col_s3][i]:
                        st.markdown(f"**{scenario_name.title()}**")
                        if scenario_name in scenarios:
                            scenario_df = scenarios[scenario_name]
                            st.dataframe(scenario_df[['Year', 'Revenue', 'EBITDA']], use_container_width=True)
                            
                            # Show total values
                            total_rev = scenario_df['Revenue'].sum()
                            total_ebitda = scenario_df['EBITDA'].sum()
                            st.caption(f"Total Revenue: {user_currency} {total_rev:,.0f}")
                            st.caption(f"Total EBITDA: {user_currency} {total_ebitda:,.0f}")
                
                # Scenario comparison chart
                st.markdown("### Scenario Comparison")
                
                fig_scenarios = go.Figure()
                
                for scenario_name, color in zip(scenario_names, scenario_colors):
                    if scenario_name in scenarios:
                        scenario_df = scenarios[scenario_name]
                        fig_scenarios.add_trace(go.Scatter(
                            x=scenario_df['Year'],
                            y=scenario_df['Revenue'],
                            mode='lines+markers',
                            name=f'{scenario_name.title()} Revenue',
                            line=dict(color=color)
                        ))
                
                fig_scenarios.update_layout(
                    title="Revenue Scenarios Comparison",
                    xaxis_title="Year",
                    yaxis_title=f"Revenue ({user_currency})",
                    height=400
                )
                
                st.plotly_chart(fig_scenarios, use_container_width=True)
                
            except Exception as e:
                st.error(f"Error in scenario analysis: {e}")
        
        with tab2:
            st.markdown("### DCF Valuation Analysis")
            
            # Convert monthly to annual cash flows
            monthly_ebitda = data.get('ebitda', [])
            if len(monthly_ebitda) >= 12:
                annual_cash_flows = []
                for year in range(0, len(monthly_ebitda), 12):
                    year_end = min(year + 12, len(monthly_ebitda))
                    annual_cf = sum(monthly_ebitda[year:year_end])
                    annual_cash_flows.append(annual_cf)
                
                # Limit to 5 years for DCF
                annual_cash_flows = annual_cash_flows[:5]
                
                if len(annual_cash_flows) >= 3:
                    try:
                        terminal_growth = data.get('terminal_growth_rate', 3.0) / 100
                        
                        dcf_result = analyzer.calculate_dcf_valuation(annual_cash_flows, terminal_growth)
                        
                        col_dcf1, col_dcf2 = st.columns(2)
                        
                        with col_dcf1:
                            st.metric("Enterprise Value", f"{user_currency} {dcf_result['enterprise_value']:,.0f}")
                            st.metric("PV of Cash Flows", f"{user_currency} {dcf_result['pv_cash_flows']:,.0f}")
                        
                        with col_dcf2:
                            st.metric("Terminal Value", f"{user_currency} {dcf_result['terminal_value']:,.0f}")
                            st.metric("PV of Terminal Value", f"{user_currency} {dcf_result['pv_terminal_value']:,.0f}")
                        
                        # DCF breakdown chart
                        st.markdown("### DCF Value Breakdown")
                        
                        dcf_breakdown = pd.DataFrame({
                            'Component': ['PV of Cash Flows', 'PV of Terminal Value'],
                            'Value': [dcf_result['pv_cash_flows'], dcf_result['pv_terminal_value']]
                        })
                        
                        fig_dcf = px.pie(dcf_breakdown, values='Value', names='Component',
                                        title="Enterprise Value Components")
                        st.plotly_chart(fig_dcf, use_container_width=True)
                        
                    except Exception as e:
                        st.error(f"Error in DCF calculation: {e}")
                else:
                    st.info("Need at least 3 years of projections for DCF analysis")
            else:
                st.info("Need at least 12 months of projections for DCF analysis")
        
        with tab3:
            st.markdown("### Financial Ratios Analysis")
            
            try:
                # Calculate ratios from your data
                total_revenue = sum(data.get('revenues', []))
                total_cogs = sum(data.get('cogs', []))
                gross_profit = total_revenue - total_cogs
                total_net_income = sum(data.get('net_income', []))
                
                financial_data = {
                    'revenue': total_revenue,
                    'gross_profit': gross_profit,
                    'net_income': total_net_income
                }
                
                ratios = analyzer.calculate_financial_ratios(financial_data)
                
                if ratios:
                    col_r1, col_r2, col_r3 = st.columns(3)
                    
                    with col_r1:
                        if 'gross_margin' in ratios:
                            st.metric("Gross Margin", f"{ratios['gross_margin']:.1f}%")
                    
                    with col_r2:
                        if 'net_margin' in ratios:
                            st.metric("Net Margin", f"{ratios['net_margin']:.1f}%")
                    
                    with col_r3:
                        st.caption("Add balance sheet data for more ratios")
                    
                    # Ratios over time
                    st.markdown("### Margin Trends")
                    
                    monthly_gross_margins = [(rev - cogs) / rev * 100 for rev, cogs in 
                                           zip(data.get('revenues', []), data.get('cogs', []))]
                    monthly_net_margins = [ni / rev * 100 for ni, rev in 
                                         zip(data.get('net_income', []), data.get('revenues', []))]
                    
                    margin_chart = pd.DataFrame({
                        'Month': range(1, len(monthly_gross_margins) + 1),
                        'Gross Margin %': monthly_gross_margins,
                        'Net Margin %': monthly_net_margins
                    })
                    
                    fig_margins = px.line(margin_chart, x='Month', y=['Gross Margin %', 'Net Margin %'],
                                        title="Margin Trends Over Time")
                    st.plotly_chart(fig_margins, use_container_width=True)
                    
                else:
                    st.info("Provide balance sheet data for comprehensive ratio analysis")
            
            except Exception as e:
                st.error(f"Error in ratios calculation: {e}")
        
        with tab4:
            st.markdown("### Sensitivity Analysis")
            
            try:
                base_value = sum(data.get('ebitda', [0]))
                
                # Define variables to test
                variables = {
                    'Revenue Growth': [-0.2, -0.1, -0.05, 0, 0.05, 0.1, 0.2],
                    'COGS Change': [-0.1, -0.05, -0.025, 0, 0.025, 0.05, 0.1],
                    'OpEx Change': [-0.15, -0.1, -0.05, 0, 0.05, 0.1, 0.15]
                }
                
                sensitivity_df = analyzer.perform_sensitivity_analysis(base_value, variables)
                
                st.dataframe(sensitivity_df, use_container_width=True)
                
                # Sensitivity visualization
                fig_sensitivity = px.bar(sensitivity_df, x='Variable', y='New_Value', color='Change_%',
                                       title='Sensitivity Analysis Results',
                                       color_continuous_scale='RdYlGn')
                
                fig_sensitivity.update_layout(height=400)
                st.plotly_chart(fig_sensitivity, use_container_width=True)
                
                # Tornado chart
                st.markdown("### Tornado Chart")
                
                tornado_data = []
                for var in variables.keys():
                    var_data = sensitivity_df[sensitivity_df['Variable'] == var]
                    min_val = var_data['New_Value'].min()
                    max_val = var_data['New_Value'].max()
                    tornado_data.append({
                        'Variable': var,
                        'Low': min_val - base_value,
                        'High': max_val - base_value
                    })
                
                tornado_df = pd.DataFrame(tornado_data)
                
                fig_tornado = go.Figure()
                
                for _, row in tornado_df.iterrows():
                    fig_tornado.add_trace(go.Bar(
                        name=row['Variable'],
                        y=[row['Variable']],
                        x=[row['High']],
                        orientation='h',
                        marker_color='green',
                        showlegend=False
                    ))
                    
                    fig_tornado.add_trace(go.Bar(
                        name=row['Variable'],
                        y=[row['Variable']],
                        x=[row['Low']],
                        orientation='h',
                        marker_color='red',
                        showlegend=False
                    ))
                
                fig_tornado.update_layout(
                    title="Tornado Chart - Impact on EBITDA",
                    xaxis_title=f"Impact on EBITDA ({user_currency})",
                    barmode='overlay',
                    height=300
                )
                
                st.plotly_chart(fig_tornado, use_container_width=True)
                
            except Exception as e:
                st.error(f"Error in sensitivity analysis: {e}")
    
    else:
        st.info("📊 Advanced analytics require the FinancialAnalyzer module")
    
    st.divider()
    
    # Download Section
    st.subheader("📥 Download Financial Model")
    
    st.info(f"💡 **Professional Excel Output**: Multi-sheet model with formulas in {user_currency}")
    
    col_download1, col_download2 = st.columns(2)
    
    with col_download1:
        if st.button("📊 Generate Excel Model", type="primary"):
            
            with st.spinner("Creating Excel file with formulas..."):
                
                # Create Excel with formulas
                excel_file = create_excel_with_formulas(data)
                
                st.download_button(
                    label="⬇️ Download Financial Model (Excel)",
                    data=excel_file,
                    file_name=f"{data['company_name']}_Financial_Model_{datetime.now().strftime('%Y%m%d')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
                
                st.success("✅ Excel model ready for download!")
    
    with col_download2:
        # Clear model button
        if st.button("🔄 Start New Model"):
            st.session_state.model_complete = False
            st.session_state.model_data = {}
            st.rerun()

# Sidebar
with st.sidebar:
    st.markdown("### 💡 Model Features")
    st.markdown("""
✓ **Multi-Sheet Structure**
✓ **Embedded Formulas**
✓ **Professional Formatting**
✓ **Dynamic Currency**
✓ **Monthly & Annual Views**
✓ **DCF Valuation**
✓ **Scenario Analysis**
✓ **Sensitivity Testing**
✓ **Financial Ratios**
""")
    
    if st.session_state.model_complete:
        st.divider()
        st.markdown("### 📋 Your Model")
        model_data = st.session_state.model_data
        st.caption(f"**Company:** {model_data.get('company_name', 'N/A')}")
        st.caption(f"**Currency:** {model_data.get('currency', 'N/A')}")
        st.caption(f"**Periods:** {model_data.get('num_months', 0)} months")
        
        # Show key insights
        total_revenue = sum(model_data.get('revenues', []))
        total_ebitda = sum(model_data.get('ebitda', []))
        
        if total_revenue > 0:
            ebitda_margin = (total_ebitda / total_revenue) * 100
            st.caption(f"**EBITDA Margin:** {ebitda_margin:.1f}%")


def create_excel_with_formulas(data):
    """Create Excel file with embedded formulas and enhanced formatting"""
    
    wb = Workbook()
    wb.remove(wb.active)
    
    # Styles
    header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
    header_font = Font(color="FFFFFF", bold=True, size=11)
    title_font = Font(size=14, bold=True)
    center_align = Alignment(horizontal="center", vertical="center")
    
    currency_symbol = data.get('currency', 'USD $').split()[0]
    
    # SHEET 1: Executive Summary
    ws_summary = wb.create_sheet("Executive Summary")
    
    ws_summary['A1'] = "FINANCIAL MODEL - EXECUTIVE SUMMARY"
    ws_summary['A1'].font = title_font
    
    ws_summary['A3'] = "Company:"
    ws_summary['B3'] = data.get('company_name', 'N/A')
    ws_summary['A4'] = "Currency:"
    ws_summary['B4'] = data.get('currency', 'N/A')
    ws_summary['A5'] = "Forecast Period:"
    ws_summary['B5'] = f"{data.get('num_months', 0)} months"
    ws_summary['A6'] = "Model Date:"
    ws_summary['B6'] = datetime.now().strftime('%Y-%m-%d')
    
    ws_summary['A8'] = "KEY METRICS"
    ws_summary['A8'].font = Font(bold=True)
    
    total_revenue = sum(data.get('revenues', []))
    total_cogs = sum(data.get('cogs', []))
    total_opex = sum(data.get('opex', []))
    total_ebitda = sum(data.get('ebitda', []))
    total_net_income = sum(data.get('net_income', []))
    
    metrics = [
        ("Total Revenue", total_revenue),
        ("Total COGS", total_cogs),
        ("Gross Profit", total_revenue - total_cogs),
        ("Total OpEx", total_opex),
        ("Total EBITDA", total_ebitda),
        ("Total Net Income", total_net_income),
        ("Final Cash", data.get('cash_balance', [0])[-1]),
        ("EBITDA Margin", (total_ebitda / total_revenue * 100) if total_revenue > 0 else 0)
    ]
    
    row = 9
    for metric, value in metrics:
        ws_summary[f'A{row}'] = metric
        ws_summary[f'B{row}'] = value
        if 'Margin' not in metric:
            ws_summary[f'B{row}'].number_format = f'"{currency_symbol}"#,##0'
        else:
            ws_summary[f'B{row}'].number_format = '0.0"%"'
        row += 1
    
    # SHEET 2: P&L Monthly
    ws_pl = wb.create_sheet("P&L Monthly")
    
    headers = ["Month", "Revenue", "COGS", "Gross Profit", "OpEx", "EBITDA", "Tax", "Net Income"]
    for col_idx, header in enumerate(headers, start=1):
        cell = ws_pl.cell(1, col_idx, header)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = center_align
    
    months = data.get('months', [])
    revenues = data.get('revenues', [])
    cogs = data.get('cogs', [])
    opex = data.get('opex', [])
    taxes = data.get('taxes', [])
    net_income = data.get('net_income', [])
    
    for i, month in enumerate(months):
        row = i + 2
        ws_pl[f'A{row}'] = month
        ws_pl[f'B{row}'] = revenues[i]
        ws_pl[f'C{row}'] = cogs[i]
        ws_pl[f'D{row}'] = f'=B{row}-C{row}'  # Formula
        ws_pl[f'E{row}'] = opex[i]
        ws_pl[f'F{row}'] = f'=D{row}-E{row}'  # Formula
        ws_pl[f'G{row}'] = taxes[i]
        ws_pl[f'H{row}'] = net_income[i]
        
        # Format currency
        for col in ['B', 'C', 'D', 'E', 'F', 'G', 'H']:
            ws_pl[f'{col}{row}'].number_format = f'"{currency_symbol}"#,##0'
    
    # Totals row
    total_row = len(months) + 2
    ws_pl[f'A{total_row}'] = "TOTAL"
    ws_pl[f'A{total_row}'].font = Font(bold=True)
    for col, col_letter in enumerate(['B', 'C', 'D', 'E', 'F', 'G', 'H'], start=2):
        ws_pl[f'{col_letter}{total_row}'] = f'=SUM({col_letter}2:{col_letter}{total_row-1})'
        ws_pl[f'{col_letter}{total_row}'].number_format = f'"{currency_symbol}"#,##0'
        ws_pl[f'{col_letter}{total_row}'].font = Font(bold=True)
    
    # SHEET 3: Cash Flow
    ws_cf = wb.create_sheet("Cash Flow")
    
    cf_headers = ["Month", "Opening Cash", "Net Income", "CapEx", "Net Change", "Closing Cash"]
    for col_idx, header in enumerate(cf_headers, start=1):
        cell = ws_cf.cell(1, col_idx, header)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = center_align
    
    capex = data.get('capex', [])
    opening_cash = data.get('initial_cash', 0)
    
    for i, month in enumerate(months):
        row = i + 2
        ws_cf[f'A{row}'] = month
        
        if i == 0:
            ws_cf[f'B{row}'] = opening_cash
        else:
            ws_cf[f'B{row}'] = f'=F{row-1}'  # Formula: previous closing
        
        ws_cf[f'C{row}'] = net_income[i]
        ws_cf[f'D{row}'] = -capex[i]  # Negative for cash outflow
        ws_cf[f'E{row}'] = f'=C{row}+D{row}'  # Formula
        ws_cf[f'F{row}'] = f'=B{row}+E{row}'  # Formula
        
        # Format currency
        for col in ['B', 'C', 'D', 'E', 'F']:
            ws_cf[f'{col}{row}'].number_format = f'"{currency_symbol}"#,##0'
    
    # SHEET 4: Assumptions
    ws_assumptions = wb.create_sheet("Assumptions")
    
    ws_assumptions['A1'] = "MODEL ASSUMPTIONS"
    ws_assumptions['A1'].font = title_font
    
    assumptions = [
        ("COMPANY INFORMATION", ""),
        ("Company Name", data.get('company_name', 'N/A')),
        ("Currency", data.get('currency', 'N/A')),
        ("Fiscal Year End", data.get('fiscal_year_end', 'N/A')),
        ("Start Month", data.get('start_month', 'N/A')),
        ("Forecast Months", data.get('num_months', 0)),
        ("", ""),
        ("REVENUE ASSUMPTIONS", ""),
        ("Initial Monthly Revenue", data.get('initial_revenue', 0)),
        ("Monthly Growth Rate (%)", data.get('monthly_growth_rate', 0)),
        ("", ""),
        ("COST ASSUMPTIONS", ""),
        ("COGS % of Revenue", data.get('cogs_percentage', 0)),
        ("COGS Annual Growth (%)", data.get('cogs_growth_rate', 0)),
        ("", ""),
        ("OPERATING EXPENSES", ""),
        ("Monthly Salaries", data.get('salaries', 0)),
        ("Monthly Rent", data.get('rent', 0)),
        ("Monthly Marketing", data.get('marketing', 0)),
        ("Other Monthly OpEx", data.get('other_opex', 0)),
        ("", ""),
        ("ADVANCED PARAMETERS", ""),
        ("Discount Rate (%)", data.get('discount_rate', 12)),
        ("Terminal Growth Rate (%)", data.get('terminal_growth_rate', 3)),
        ("Tax Rate (%)", data.get('tax_rate', 25)),
        ("CapEx % of Revenue", data.get('capex_percentage', 2)),
        ("", ""),
        ("CASH", ""),
        ("Opening Cash Balance", data.get('initial_cash', 0))
    ]
    
    for row_idx, (label, value) in enumerate(assumptions, start=3):
        ws_assumptions[f'A{row_idx}'] = label
        ws_assumptions[f'B{row_idx}'] = value
        
        if label.isupper() and label.endswith(("INFORMATION", "ASSUMPTIONS", "EXPENSES", "PARAMETERS", "CASH")):
            ws_assumptions[f'A{row_idx}'].font = Font(bold=True)
    
    # SHEET 5: Annual Summary
    ws_annual = wb.create_sheet("Annual Summary")
    
    # Group data by year
    annual_data = {}
    for i, month in enumerate(months):
        year = month[:4]
        if year not in annual_data:
            annual_data[year] = {
                'revenue': 0, 'cogs': 0, 'opex': 0, 'ebitda': 0,
                'net_income': 0, 'capex': 0
            }
        annual_data[year]['revenue'] += revenues[i]
        annual_data[year]['cogs'] += cogs[i]
        annual_data[year]['opex'] += opex[i]
        annual_data[year]['ebitda'] += data.get('ebitda', [])[i]
        annual_data[year]['net_income'] += net_income[i]
        annual_data[year]['capex'] += capex[i]
    
    # Headers for annual summary
    annual_headers = ["Year", "Revenue", "COGS", "Gross Profit", "OpEx", "EBITDA", "Net Income", "CapEx"]
    for col_idx, header in enumerate(annual_headers, start=1):
        cell = ws_annual.cell(1, col_idx, header)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = center_align
    
    # Populate annual data
    row = 2
    for year, values in annual_data.items():
        ws_annual[f'A{row}'] = year
        ws_annual[f'B{row}'] = values['revenue']
        ws_annual[f'C{row}'] = values['cogs']
        ws_annual[f'D{row}'] = f'=B{row}-C{row}'
        ws_annual[f'E{row}'] = values['opex']
        ws_annual[f'F{row}'] = values['ebitda']
        ws_annual[f'G{row}'] = values['net_income']
        ws_annual[f'H{row}'] = values['capex']
        
        # Format currency
        for col in ['B', 'C', 'D', 'E', 'F', 'G', 'H']:
            ws_annual[f'{col}{row}'].number_format = f'"{currency_symbol}"#,##0'
        
        row += 1
    
    # Adjust column widths for all sheets
    for ws in [ws_summary, ws_pl, ws_cf, ws_assumptions, ws_annual]:
        for column in ws.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if cell.value and len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            ws.column_dimensions[column_letter].width = adjusted_width
    
    # Save to BytesIO
    excel_buffer = BytesIO()
    wb.save(excel_buffer)
    excel_buffer.seek(0)
    
    return excel_buffer.getvalue()
