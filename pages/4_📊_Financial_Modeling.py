"""
Enhanced Financial Modeling & Scenario Planning
Generates comprehensive Excel models with embedded formulas
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from dateutil.relativedelta import relativedelta
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from io import BytesIO

st.set_page_config(page_title="Financial Modeling", page_icon="📊", layout="wide")

# Session state
if 'model_complete' not in st.session_state:
    st.session_state.model_complete = False
if 'model_data' not in st.session_state:
    st.session_state.model_data = {}

st.markdown("""
<div style="padding: 1.5rem 0; border-bottom: 2px solid #f0f0f0;">
    <h1 style="margin: 0; font-size: 2.5rem;">📊 Financial Modeling & Scenario Planning</h1>
    <p style="margin: 0.5rem 0 0 0; color: #666; font-size: 1.1rem;">
        Generate professional Excel models with embedded formulas
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

col_rev1, col_rev2 = st.columns(2)

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

st.divider()

# Cost Inputs
st.subheader("💸 Cost Assumptions")

col_cost1, col_cost2 = st.columns(2)

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

st.divider()

# Generate Button
if st.button("🚀 Generate Financial Model", type="primary", use_container_width=True):
    
    if not company_name:
        st.error("⚠️ Please enter company name")
    else:
        with st.spinner("🤖 Generating comprehensive financial model..."):
            
            # Calculate monthly data
            months = []
            revenues = []
            cogs_list = []
            gross_profits = []
            opex_list = []
            ebitda_list = []
            cash_balance = [initial_cash]
            
            current_revenue = initial_monthly_revenue
            current_cogs_pct = cogs_percentage / 100
            
            for month in range(int(num_months)):
                month_date = start_month + relativedelta(months=month)
                months.append(month_date.strftime('%Y-%m'))
                
                # Revenue with growth
                revenue = current_revenue * (1 + monthly_growth_rate / 100) ** month
                revenues.append(revenue)
                
                # COGS with annual growth
                annual_cogs_growth = (1 + cogs_growth_rate / 100) ** (month / 12)
                cogs = revenue * current_cogs_pct * annual_cogs_growth
                cogs_list.append(cogs)
                
                # Gross Profit
                gross_profit = revenue - cogs
                gross_profits.append(gross_profit)
                
                # Operating Expenses
                total_opex = salaries + rent + marketing + other_opex
                opex_list.append(total_opex)
                
                # EBITDA
                ebitda = gross_profit - total_opex
                ebitda_list.append(ebitda)
                
                # Cash Flow
                net_cash_flow = ebitda
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
                'cash_balance': cash_balance,
                'salaries': salaries,
                'rent': rent,
                'marketing': marketing,
                'other_opex': other_opex,
                'cogs_percentage': cogs_percentage,
                'monthly_growth_rate': monthly_growth_rate,
                'cogs_growth_rate': cogs_growth_rate,
                'initial_revenue': initial_monthly_revenue
            }
            
            st.session_state.model_complete = True
            st.success("✅ Financial Model Generated!")
            st.rerun()

# Display Results
if st.session_state.model_complete:
    
    st.divider()
    st.subheader("📊 Financial Summary")
    
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
        total_opex = sum(data.get('opex', []))
        st.metric("Total OpEx", f"{user_currency} {total_opex:,.0f}")
    
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
        st.line_chart(chart_data.set_index('Month'))
    
    with col_chart2:
        st.markdown("**💰 Cash Balance Forecast**")
        cash_chart = pd.DataFrame({
            'Month': range(1, len(data.get('cash_balance', [])) + 1),
            'Cash': data.get('cash_balance', [])
        })
        st.line_chart(cash_chart.set_index('Month'))
    
    st.divider()
    
    # Download Section
    st.subheader("📥 Download Financial Model")
    
    st.info(f"💡 **Professional Excel Output**: Multi-sheet model with formulas in {user_currency}")
    
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

# Sidebar
with st.sidebar:
    st.markdown("### 💡 Model Features")
    st.markdown("""
✓ **Multi-Sheet Structure**
✓ **Embedded Formulas**
✓ **Professional Formatting**
✓ **Dynamic Currency**
✓ **Monthly & Annual Views**
""")
    
    if st.session_state.model_complete:
        st.divider()
        st.markdown("### 📋 Your Model")
        model_data = st.session_state.model_data
        st.caption(f"**Company:** {model_data.get('company_name', 'N/A')}")
        st.caption(f"**Currency:** {model_data.get('currency', 'N/A')}")
        st.caption(f"**Periods:** {model_data.get('num_months', 0)} months")


def create_excel_with_formulas(data):
    """Create Excel file with embedded formulas"""
    
    wb = Workbook()
    wb.remove(wb.active)
    
    # Styles
    header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
    header_font = Font(color="FFFFFF", bold=True, size=11)
    title_font = Font(size=14, bold=True)
    center_align = Alignment(horizontal="center", vertical="center")
    
    currency_symbol = data.get('currency', 'USD $').split()[0]
    
    # SHEET 1: Summary
    ws_summary = wb.create_sheet("Summary")
    
    ws_summary['A1'] = "FINANCIAL MODEL SUMMARY"
    ws_summary['A1'].font = title_font
    
    ws_summary['A3'] = "Company:"
    ws_summary['B3'] = data.get('company_name', 'N/A')
    ws_summary['A4'] = "Currency:"
    ws_summary['B4'] = data.get('currency', 'N/A')
    ws_summary['A5'] = "Forecast Period:"
    ws_summary['B5'] = f"{data.get('num_months', 0)} months"
    
    ws_summary['A7'] = "KEY METRICS"
    ws_summary['A7'].font = Font(bold=True)
    
    total_revenue = sum(data.get('revenues', []))
    total_cogs = sum(data.get('cogs', []))
    total_opex = sum(data.get('opex', []))
    total_ebitda = sum(data.get('ebitda', []))
    
    metrics = [
        ("Total Revenue", total_revenue),
        ("Total COGS", total_cogs),
        ("Gross Profit", total_revenue - total_cogs),
        ("Total OpEx", total_opex),
        ("Total EBITDA", total_ebitda),
        ("Final Cash", data.get('cash_balance', [0])[-1])
    ]
    
    row = 8
    for metric, value in metrics:
        ws_summary[f'A{row}'] = metric
        ws_summary[f'B{row}'] = value
        ws_summary[f'B{row}'].number_format = f'"{currency_symbol}"#,##0'
        row += 1
    
    # SHEET 2: P&L Monthly
    ws_pl = wb.create_sheet("P&L Monthly")
    
    headers = ["Month", "Revenue", "COGS", "Gross Profit", "OpEx", "EBITDA"]
    for col_idx, header in enumerate(headers, start=1):
        cell = ws_pl.cell(1, col_idx, header)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = center_align
    
    months = data.get('months', [])
    revenues = data.get('revenues', [])
    cogs = data.get('cogs', [])
    opex = data.get('opex', [])
    
    for i, month in enumerate(months):
        row = i + 2
        ws_pl[f'A{row}'] = month
        ws_pl[f'B{row}'] = revenues[i]
        ws_pl[f'C{row}'] = cogs[i]
        ws_pl[f'D{row}'] = f'=B{row}-C{row}'  # Formula
        ws_pl[f'E{row}'] = opex[i]
        ws_pl[f'F{row}'] = f'=D{row}-E{row}'  # Formula
        
        # Format currency
        for col in ['B', 'C', 'D', 'E', 'F']:
            ws_pl[f'{col}{row}'].number_format = f'"{currency_symbol}"#,##0'
    
    # Totals row
    total_row = len(months) + 2
    ws_pl[f'A{total_row}'] = "TOTAL"
    ws_pl[f'A{total_row}'].font = Font(bold=True)
    for col, col_letter in enumerate(['B', 'C', 'D', 'E', 'F'], start=2):
        ws_pl[f'{col_letter}{total_row}'] = f'=SUM({col_letter}2:{col_letter}{total_row-1})'
        ws_pl[f'{col_letter}{total_row}'].number_format = f'"{currency_symbol}"#,##0'
        ws_pl[f'{col_letter}{total_row}'].font = Font(bold=True)
    
    # SHEET 3: Cash Flow
    ws_cf = wb.create_sheet("Cash Flow")
    
    cf_headers = ["Month", "Opening Cash", "EBITDA", "Net Change", "Closing Cash"]
    for col_idx, header in enumerate(cf_headers, start=1):
        cell = ws_cf.cell(1, col_idx, header)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = center_align
    
    ebitda = data.get('ebitda', [])
    opening_cash = data.get('initial_cash', 0)
    
    for i, month in enumerate(months):
        row = i + 2
        ws_cf[f'A{row}'] = month
        
        if i == 0:
            ws_cf[f'B{row}'] = opening_cash
        else:
            ws_cf[f'B{row}'] = f'=E{row-1}'  # Formula: previous closing
        
        ws_cf[f'C{row}'] = ebitda[i]
        ws_cf[f'D{row}'] = f'=C{row}'  # Formula
        ws_cf[f'E{row}'] = f'=B{row}+D{row}'  # Formula
        
        # Format currency
        for col in ['B', 'C', 'D', 'E']:
            ws_cf[f'{col}{row}'].number_format = f'"{currency_symbol}"#,##0'
    
    # SHEET 4: Assumptions
    ws_assumptions = wb.create_sheet("Assumptions")
    
    ws_assumptions['A1'] = "MODEL ASSUMPTIONS"
    ws_assumptions['A1'].font = title_font
    
    assumptions = [
        ("Company Name", data.get('company_name', 'N/A')),
        ("Currency", data.get('currency', 'N/A')),
        ("Fiscal Year End", data.get('fiscal_year_end', 'N/A')),
        ("Start Month", data.get('start_month', 'N/A')),
        ("Forecast Months", data.get('num_months', 0)),
        ("", ""),
        ("REVENUE", ""),
        ("Initial Monthly Revenue", data.get('initial_revenue', 0)),
        ("Monthly Growth Rate (%)", data.get('monthly_growth_rate', 0)),
        ("", ""),
        ("COSTS", ""),
        ("COGS % of Revenue", data.get('cogs_percentage', 0)),
        ("COGS Annual Growth (%)", data.get('cogs_growth_rate', 0)),
        ("", ""),
        ("OPERATING EXPENSES", ""),
        ("Monthly Salaries", data.get('salaries', 0)),
        ("Monthly Rent", data.get('rent', 0)),
        ("Monthly Marketing", data.get('marketing', 0)),
        ("Other Monthly OpEx", data.get('other_opex', 0)),
        ("", ""),
        ("CASH", ""),
        ("Opening Cash Balance", data.get('initial_cash', 0))
    ]
    
    for row_idx, (label, value) in enumerate(assumptions, start=3):
        ws_assumptions[f'A{row_idx}'] = label
        ws_assumptions[f'B{row_idx}'] = value
        
        if label in ["REVENUE", "COSTS", "OPERATING EXPENSES", "CASH"]:
            ws_assumptions[f'A{row_idx}'].font = Font(bold=True)
    
    # Adjust column widths for all sheets
    for ws in [ws_summary, ws_pl, ws_cf, ws_assumptions]:
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
