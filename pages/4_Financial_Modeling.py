"""
Financial Modeling | Regulus AI × QDB
Standalone financial projections with Excel/CSV export. Step 4 of 5.
"""
import streamlit as st
import os, base64, io
from datetime import datetime
import pandas as pd
import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from utils.llm_handler import LLMHandler
from utils.financial_analyzer import FinancialAnalyzer
from utils.qdb_styling import apply_qdb_styling, QDB_DARK_BLUE, QDB_NAVY, QDB_PURPLE, QDB_GOLD

st.set_page_config(page_title="Financial Modeling – Regulus AI", layout="wide")
apply_qdb_styling()

def encode_image(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f"data:image/png;base64,{base64.b64encode(f.read()).decode()}"
    return None
qdb_logo = encode_image("QDB_Logo.png")

# ==== INIT HANDLERS ====
@st.cache_resource
def init_handlers():
    return LLMHandler(), FinancialAnalyzer()
llm, fin_analyzer = init_handlers()

# ==== SESSION STATE ====
if 'financial_model' not in st.session_state:
    st.session_state.financial_model = None

# ==== HERO SECTION ====
st.markdown(f"""
<div style="
background:linear-gradient(135deg,{QDB_DARK_BLUE} 0%, {QDB_NAVY} 100%);
color:white;margin:0 -3rem;padding:100px 0 80px;text-align:center;">
<div style="position:absolute;left:50px;top:48px;">
{'<img src="'+qdb_logo+'" style="max-height:80px;">' if qdb_logo else '<b>QDB</b>'}
</div>
<h1 style="font-size:2.8rem;font-weight:800;">Financial Modeling & Projections</h1>
<p style="font-size:1.35rem;color:#E2E8F0;">Build Comprehensive Financial Models and Forecasts</p>
<p style="color:#CBD5E0;font-size:1.1rem;max-width:750px;margin:auto;">
AI-powered 3-5 year financial projections, revenue forecasting, and profitability analysis. Export models in Excel and CSV formats.
</p>
</div>
""", unsafe_allow_html=True)

# ==== RETURN HOME ====
col1, col2, col3 = st.columns([1, 0.6, 1])
with col2:
    if st.button("Return Home", use_container_width=True, key="home_btn"):
        st.switch_page("streamlit_app.py")

st.markdown("""
<style>
button[key="home_btn"]{
 background:linear-gradient(135deg,#16A085 0%,#138074 80%,#0E5F55 100%)!important;
 color:white!important;border:none!important;border-radius:44px!important;
 padding:14px 44px!important;font-weight:700!important;font-size:1.05rem!important;
 box-shadow:0 8px 34px rgba(19,128,116,.25)!important;
transition:all .2s!important;}
button[key="home_btn"]:hover{transform:translateY(-2px);}
</style>""", unsafe_allow_html=True)

# ==== WORKFLOW TRACKER ====
st.markdown("""
<style>
.track{background:#F6F5F2;margin:-2px -3rem;padding:34px 0;
display:flex;justify-content:space-evenly;align-items:center;}
.circle{width:54px;height:54px;border-radius:50%;display:flex;
align-items:center;justify-content:center;font-weight:700;
background:#CBD5E0;color:#475569;font-size:0.95rem;}
.circle.active{background:linear-gradient(135deg,#138074 0%,#0E5F55 100%);
color:white;box-shadow:0 5px 15px rgba(19,128,116,0.4);}
.label{margin-top:7px;font-size:0.9rem;font-weight:600;color:#708090;}
.label.active{color:#138074;}
.pipe{height:3px;width:70px;background:#CBD5E0;}
</style>
<div class="track">
 <div><div class="circle">1</div><div class="label">Deal Sourcing</div></div>
 <div class="pipe"></div>
 <div><div class="circle">2</div><div class="label">Due Diligence</div></div>
 <div class="pipe"></div>
 <div><div class="circle">3</div><div class="label">Market Analysis</div></div>
 <div class="pipe"></div>
 <div><div class="circle active">4</div><div class="label active">Financial Modeling</div></div>
 <div class="pipe"></div>
 <div><div class="circle">5</div><div class="label">Investment Memo</div></div>
</div>
""", unsafe_allow_html=True)

# ==== COMPANY INFO SECTION ====
st.markdown("""
<div style="background:white;margin:50px -3rem 0 -3rem;padding:45px 3rem;
border-top:3px solid #138074;box-shadow:0 0 12px rgba(0,0,0,0.05);">
<h2 style="text-align:center;color:#1B2B4D;font-weight:700;">Company & Model Setup</h2>
</div>
""", unsafe_allow_html=True)

with st.expander("Enter Company and Financial Assumptions", expanded=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        company_name = st.text_input("Company Name", placeholder="Enter company name", key="company_name")
    with col2:
        sector = st.text_input("Sector", placeholder="e.g., Fintech, AI/ML", key="sector")
    with col3:
        currency = st.selectbox("Currency", ["USD","EUR","GBP","QAR","AED"], index=0, key="currency")

# ==== MODEL PARAMETERS ====
st.markdown("""
<div style="background:white;margin:50px -3rem 0 -3rem;padding:45px 3rem;
border-top:3px solid #138074;box-shadow:0 0 12px rgba(0,0,0,0.05);">
<h2 style="text-align:center;color:#1B2B4D;font-weight:700;">Financial Assumptions</h2>
</div>
""", unsafe_allow_html=True)

with st.expander("Set Financial Parameters and Drivers", expanded=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        forecast_years = st.selectbox("Forecast Period", [3,5,7], index=1, key="forecast_years")
        revenue_start = st.number_input("Current Annual Revenue (Millions)", min_value=0.0, value=5.0, step=0.5, key="revenue")
    with col2:
        growth_rate = st.slider("Annual Revenue Growth Rate (%)", 0, 150, 30, key="growth")
        gross_margin = st.slider("Gross Margin (%)", 0, 100, 70, key="gross_margin")
    with col3:
        opex_percent = st.slider("OpEx (% of Revenue)", 0, 100, 40, key="opex")
        tax_rate = st.slider("Tax Rate (%)", 0, 50, 20, key="tax")

# ==== ACTION BUTTON ====
st.markdown("<br>", unsafe_allow_html=True)
if st.button("Generate Financial Model", use_container_width=True, key="generate"):
    try:
        with st.spinner("Building financial model with AI validation..."):
            
            # Build projections
            years = list(range(datetime.now().year, datetime.now().year + forecast_years))
            revenue = [revenue_start * ((1 + growth_rate/100) ** i) for i in range(forecast_years)]
            cogs = [r * (1 - gross_margin/100) for r in revenue]
            gross_profit = [r - c for r, c in zip(revenue, cogs)]
            opex = [r * opex_percent/100 for r in revenue]
            ebit = [gp - op for gp, op in zip(gross_profit, opex)]
            tax = [e * tax_rate/100 for e in ebit]
            net_income = [e - t for e, t in zip(ebit, tax)]
            
            # Create model
            model_df = pd.DataFrame({
                'Year': years,
                'Revenue': revenue,
                'COGS': cogs,
                'Gross Profit': gross_profit,
                'Gross Margin %': [(gp/r)*100 for gp, r in zip(gross_profit, revenue)],
                'OpEx': opex,
                'EBIT': ebit,
                'EBIT Margin %': [(e/r)*100 for e, r in zip(ebit, revenue)],
                'Tax': tax,
                'Net Income': net_income,
                'Net Margin %': [(n/r)*100 for n, r in zip(net_income, revenue)]
            })
            
            # AI Validation
            try:
                validation_prompt = f"Validate financial model for {company_name}: {forecast_years}yr forecast, {growth_rate}% CAGR. Provide brief assessment."
                ai_validation = llm.generate_text(validation_prompt)
                st.info(f"AI Validation: {ai_validation[:200]}...")
            except:
                st.success("Model generated successfully")
            
            st.session_state.financial_model = model_df
            st.success("Financial model generated!")
        
    except Exception as e:
        st.error(f"Error: {str(e)}")

# ==== RESULTS DISPLAY ====
if st.session_state.get("financial_model") is not None and company_name:
    st.markdown("---")
    st.markdown("""
<div style="background:white;margin:30px -3rem 0 -3rem;padding:45px 3rem;
border-top:3px solid #138074;box-shadow:0 0 12px rgba(0,0,0,0.05);">
<h2 style="text-align:center;color:#1B2B4D;font-weight:700;">Financial Projections</h2>
</div>
""", unsafe_allow_html=True)

    df = st.session_state.financial_model
    
    # Display table
    df_display = df.copy()
    for col in ['Revenue','COGS','Gross Profit','OpEx','EBIT','Tax','Net Income']:
        df_display[col] = df_display[col].apply(lambda x: f"{currency} {x:,.1f}M")
    for col in ['Gross Margin %','EBIT Margin %','Net Margin %']:
        df_display[col] = df_display[col].apply(lambda x: f"{x:.1f}%")
    
    st.dataframe(df_display, use_container_width=True)
    
    # Charts
    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        st.markdown("**Revenue & Profitability Trend**")
        st.line_chart(df.set_index('Year')[['Revenue','EBIT','Net Income']])
    with col_chart2:
        st.markdown("**Margin Analysis**")
        st.line_chart(df.set_index('Year')[['Gross Margin %','EBIT Margin %','Net Margin %']])
    
    # Key metrics
    st.markdown("<br>", unsafe_allow_html=True)
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    with col_m1:
        st.metric("Year 1 Revenue", f"{currency} {df.iloc[0]['Revenue']:.1f}M")
    with col_m2:
        st.metric("Year End Revenue", f"{currency} {df.iloc[-1]['Revenue']:.1f}M")
    with col_m3:
        cagr = ((df.iloc[-1]['Revenue'] / df.iloc[0]['Revenue']) ** (1/(forecast_years-1)) - 1) * 100
        st.metric("CAGR", f"{cagr:.1f}%")
    with col_m4:
        st.metric("Avg Net Margin", f"{df['Net Margin %'].mean():.1f}%")
    
    # EXPORT SECTION
    st.markdown("---")
    st.markdown("""
<div style="background:white;margin:30px -3rem 0 -3rem;padding:45px 3rem;
border-top:3px solid #138074;box-shadow:0 0 12px rgba(0,0,0,0.05);">
<h2 style="text-align:center;color:#1B2B4D;font-weight:700;">Export Financial Model</h2>
</div>
""", unsafe_allow_html=True)

    # CSV Export
    csv_data = df.to_csv(index=False)
    
    # Excel Export with styling
    def create_excel(data):
        output = io.BytesIO()
        wb = Workbook()
        ws = wb.active
        ws.title = "Financial Model"
        
        # Title
        ws['A1'] = f"{company_name} - {sector} | Financial Projections"
        ws['A1'].font = Font(bold=True, size=12, color="FFFFFF")
        ws['A1'].fill = PatternFill(start_color="1B2B4D", end_color="1B2B4D", fill_type="solid")
        
        # Headers
        for col_num, header in enumerate(data.columns, 1):
            cell = ws.cell(row=3, column=col_num, value=header)
            cell.font = Font(bold=True, color="FFFFFF")
            cell.fill = PatternFill(start_color="138074", end_color="138074", fill_type="solid")
        
        # Data
        for r_idx, row in enumerate(data.values, 4):
            for c_idx, value in enumerate(row, 1):
                ws.cell(row=r_idx, column=c_idx, value=value)
        
        wb.save(output)
        return output.getvalue()
    
    excel_bytes = create_excel(df)
    
    col_exp1, col_exp2 = st.columns(2)
    with col_exp1:
        st.download_button(
            "Download Excel (XLSX)",
            excel_bytes,
            f"Financial_Model_{company_name}_{datetime.now().strftime('%Y%m%d')}.xlsx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
    with col_exp2:
        st.download_button(
            "Download CSV",
            csv_data,
            f"Financial_Model_{company_name}_{datetime.now().strftime('%Y%m%d')}.csv",
            "text/csv",
            use_container_width=True
        )
    
    # NAVIGATION
    st.markdown("<br><br>", unsafe_allow_html=True)
    col_nav1, col_nav2, col_nav3 = st.columns(3)
    
    with col_nav1:
        if st.button("Back to Market Analysis", use_container_width=True, key="back_market"):
            st.switch_page("pages/3_Market_Analysis.py")
    
    with col_nav2:
        if st.button("Go to Investment Memo", use_container_width=True, key="to_memo"):
            st.switch_page("pages/5_Investment_Memo.py")
    
    with col_nav3:
        if st.button("Back to Deal Sourcing", use_container_width=True, key="back_deals"):
            st.switch_page("pages/1_Deal_Sourcing.py")

# ==== FOOTER ====
st.markdown(f"""
<div style="background:{QDB_DARK_BLUE};color:#E2E8F0;padding:26px 36px;margin:80px -3rem -2rem;
display:flex;justify-content:space-between;align-items:center;">
<p style="margin:0;font-size:0.9rem;">© 2025 Regulus AI | All Rights Reserved</p>
<p style="margin:0;color:#A0AEC0;font-size:0.9rem;">Powered by Regulus AI</p>
</div>
""", unsafe_allow_html=True)
