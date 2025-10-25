"""
Financial Modeling Page
QDB-branded with auto-fill from workflow and Excel export
"""

import streamlit as st
from datetime import datetime
import pandas as pd
import numpy as np
from utils.llm_handler import LLMHandler
from utils.financial_analyzer import FinancialAnalyzer
import io
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils.dataframe import dataframe_to_rows
from utils.qdb_styling import apply_qdb_styling, QDB_PURPLE, QDB_GOLD, QDB_DARK_BLUE, qdb_header, qdb_divider

st.set_page_config(page_title="Financial Modeling - QDB", layout="wide", initial_sidebar_state="collapsed")
apply_qdb_styling()  # ✅ QDB styling

@st.cache_resource
def init_handlers():
    return LLMHandler(), FinancialAnalyzer()

llm, fin_analyzer = init_handlers()

if 'financial_model' not in st.session_state:
    st.session_state.financial_model = None

# Top Navigation
col_nav1, col_nav2, col_nav3 = st.columns([1, 2, 1])
with col_nav1:
    if st.button("← Back to Market"):
        st.switch_page("pages/3_Market_Analysis.py")
with col_nav2:
    st.markdown(f"<p style='text-align: center; color:{QDB_DARK_BLUE}; font-weight: 600;'>Step 4 of 5: Financial Modeling</p>", unsafe_allow_html=True)
with col_nav3:
    st.markdown("<p style='text-align: right; color: #999;'>QDB Analyst</p>", unsafe_allow_html=True)

qdb_divider()

# HEADER
qdb_header("Financial Modeling & Projections", "Build comprehensive financial models and forecasts")

# Auto-fill from selected deal
selected_deal = st.session_state.get('selected_deal')

if selected_deal:
    st.success(f"📊 Financial Model for: **{selected_deal['company']}** ({selected_deal['sector']})")
    company_name = selected_deal['company']
    sector = selected_deal['sector']
else:
    st.warning("⚠️ No company selected")
    company_name = st.text_input("Company Name", value="")
    sector = "Technology"

qdb_divider()

# Model Parameters
qdb_header("Model Parameters", "Configure financial assumptions and projections")

col_param1, col_param2, col_param3 = st.columns(3)

with col_param1:
    currency = st.selectbox("Currency", ["USD", "EUR", "GBP", "QAR", "AED"], index=0)
    forecast_years = st.selectbox("Forecast Period", [3, 5, 7], index=1)

with col_param2:
    revenue_start = st.number_input("Current Revenue (M)", min_value=0.0, value=5.0, step=0.5)
    growth_rate = st.slider("Annual Growth Rate (%)", 0, 100, 30)

with col_param3:
    gross_margin = st.slider("Gross Margin (%)", 0, 100, 70)
    opex_percent = st.slider("OpEx (% of Revenue)", 0, 100, 40)

st.markdown("<br>", unsafe_allow_html=True)

# Generate Model Button
if st.button("🚀 Generate Financial Model", type="primary", use_container_width=True):
    
    with st.spinner("Building financial model..."):
        
        # Generate projections
        years = list(range(datetime.now().year, datetime.now().year + forecast_years))
        revenue = [revenue_start * ((1 + growth_rate/100) ** i) for i in range(forecast_years)]
        cogs = [r * (1 - gross_margin/100) for r in revenue]
        gross_profit = [r - c for r, c in zip(revenue, cogs)]
        opex = [r * opex_percent/100 for r in revenue]
        ebitda = [gp - op for gp, op in zip(gross_profit, opex)]
        
        # Create DataFrame
        df = pd.DataFrame({
            'Year': years,
            'Revenue': revenue,
            'COGS': cogs,
            'Gross Profit': gross_profit,
            'OpEx': opex,
            'EBITDA': ebitda,
            'EBITDA Margin %': [(e/r)*100 for e, r in zip(ebitda, revenue)]
        })
        
        st.session_state.financial_model = df
        st.success("✅ Financial model generated!")

# Display Model
if st.session_state.financial_model is not None:
    qdb_divider()
    qdb_header("Financial Projections", "Review and analyze projected financial performance")
    
    df = st.session_state.financial_model
    
    # Format display
    df_display = df.copy()
    for col in ['Revenue', 'COGS', 'Gross Profit', 'OpEx', 'EBITDA']:
        df_display[col] = df_display[col].apply(lambda x: f"{currency} {x:,.2f}M")
    df_display['EBITDA Margin %'] = df_display['EBITDA Margin %'].apply(lambda x: f"{x:.1f}%")
    
    st.dataframe(df_display, use_container_width=True)
    
    # Charts
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.markdown("### Revenue Growth")
        st.line_chart(df.set_index('Year')['Revenue'])
    
    with col_chart2:
        st.markdown("### EBITDA Trend")
        st.line_chart(df.set_index('Year')['EBITDA'])
    
    # Key Metrics
    st.markdown("<br>", unsafe_allow_html=True)
    col_metric1, col_metric2, col_metric3, col_metric4 = st.columns(4)
    
    with col_metric1:
        st.metric("Year 1 Revenue", f"{currency} {df.iloc[0]['Revenue']:.1f}M")
    with col_metric2:
        st.metric("Year End Revenue", f"{currency} {df.iloc[-1]['Revenue']:.1f}M")
    with col_metric3:
        st.metric("CAGR", f"{growth_rate}%")
    with col_metric4:
        st.metric("Avg EBITDA Margin", f"{df['EBITDA Margin %'].mean():.1f}%")
    
    # Export Excel
    qdb_divider()
    
    def create_excel():
        output = io.BytesIO()
        wb = Workbook()
        ws = wb.active
        ws.title = "Financial Model"
        
        # Header
        ws['A1'] = f"{company_name} - Financial Projections"
        ws['A1'].font = Font(bold=True, size=14, color="5E2A84")
        
        # Data
        for r_idx, row in enumerate(dataframe_to_rows(df, index=False, header=True), 3):
            for c_idx, value in enumerate(row, 1):
                cell = ws.cell(row=r_idx, column=c_idx, value=value)
                if r_idx == 3:
                    cell.font = Font(bold=True, color="FFFFFF")
                    cell.fill = PatternFill(start_color="5E2A84", end_color="5E2A84", fill_type="solid")
        
        wb.save(output)
        return output.getvalue()
    
    col_export1, col_export2 = st.columns(2)
    
    with col_export1:
        csv = df.to_csv(index=False)
        st.download_button(
            "📥 Download CSV",
            csv,
            f"Financial_Model_{company_name}_{datetime.now().strftime('%Y%m%d')}.csv",
            "text/csv",
            use_container_width=True
        )
    
    with col_export2:
        excel_data = create_excel()
        st.download_button(
            "📥 Download Excel",
            excel_data,
            f"Financial_Model_{company_name}_{datetime.now().strftime('%Y%m%d')}.xlsx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
    
    # WORKFLOW NAVIGATION
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div style='
            background: linear-gradient(135deg, {QDB_PURPLE} 0%, {QDB_DARK_BLUE} 100%);
            border-radius: 12px;
            padding: 25px;
            color: white;
            text-align: center;
        '>
            <h3 style='margin: 0 0 10px 0;'>Financial Model Complete!</h3>
            <p style='margin: 0; font-size: 1.1rem;'>Proceed to generate Investment Memorandum</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_nav_btn1, col_nav_btn2, col_nav_btn3 = st.columns([1, 2, 1])
    
    with col_nav_btn1:
        if st.button("← Back to Market", use_container_width=True):
            st.switch_page("pages/3_Market_Analysis.py")
    
    with col_nav_btn2:
        if st.button("Proceed to Investment Memo →", type="primary", use_container_width=True):
            st.switch_page("pages/5_Investment_Memo.py")
    
    with col_nav_btn3:
        if st.button("Back to Home", use_container_width=True):
            st.switch_page("Main_Page.py")

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(f"<div style='text-align: center; color:{QDB_GOLD}; font-size: 0.9rem;'>Financial Modeling | Powered by Regulus AI</div>", unsafe_allow_html=True)
