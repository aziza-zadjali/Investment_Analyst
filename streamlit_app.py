"""
Investment Analyst AI - QDB Official Branding
"""

import streamlit as st
import base64
import os
from utils.qdb_styling import apply_qdb_styling, QDB_PURPLE, QDB_GOLD, QDB_DARK_BLUE, QDB_LIGHT_GRAY, qdb_section_start, qdb_section_end

st.set_page_config(page_title="Investment Analyst AI - QDB", layout="wide", initial_sidebar_state="collapsed")
apply_qdb_styling()

def encode_image(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f"data:image/png;base64,{base64.b64encode(f.read()).decode()}"
    return None

qdb_logo = encode_image("QDB_Logo.png")
regulus_logo = encode_image("regulus_logo.png")

# ===== SECTION 1: HEADER (Light Background) =====
qdb_section_start("light")

st.markdown(f"""
<div style='display:grid;grid-template-columns:1fr 2.5fr 1fr;align-items:center;padding:25px 0;border-bottom:3px solid {QDB_PURPLE};'>
    <div style='text-align:center;'>{"<img src='"+qdb_logo+"' style='max-height:90px;'>" if qdb_logo else "<strong>QDB</strong>"}</div>
    <div style='text-align:center;'>
        <h1 style='font-size:2.8rem;font-weight:700;color:{QDB_DARK_BLUE};margin-bottom:10px;'>Investment Analyst AI</h1>
        <p style='color:{QDB_GOLD};font-weight:600;font-size:1.18rem;margin-bottom:6px;'>Supporting Qatar's Economic Vision with Data-Driven Investment Analysis & Strategic Decision Intelligence</p>
        <p style='color:#666;font-size:1.05rem;margin:0;'>End-to-End AI Platform for Deal Sourcing, Due Diligence, Market Analysis & Investment Memoranda</p>
    </div>
    <div style='text-align:center;'>{"<img src='"+regulus_logo+"' style='max-height:90px;'>" if regulus_logo else "<strong>Regulus</strong>"}</div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"<div style='text-align:center;margin:40px 0 35px 0;'><h2 style='color:{QDB_DARK_BLUE};font-size:2.2rem;margin-bottom:12px;font-weight:600;'>Choose Your Analysis Path</h2><p style='color:#777;font-size:1.15rem;'>Select your investment workflow to begin comprehensive analysis</p></div>", unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown(f"""
    <div style='background:white;border-radius:12px;padding:35px;height:420px;box-shadow:0 5px 20px rgba(0,0,0,0.08);border-left:5px solid {QDB_PURPLE};display:flex;flex-direction:column;'>
        <h2 style='color:{QDB_PURPLE};font-size:1.9rem;font-weight:700;margin-bottom:18px;'>Deal Sourcing Path</h2>
        <p><strong>Start here if you are:</strong></p>
        <ul style='margin-top:12px;line-height:2;'><li>Looking for new investment opportunities</li><li>Building your deal pipeline</li><li>Discovering and filtering potential deals</li></ul>
        <div style='margin-top:auto;padding-top:20px;border-top:2px solid {QDB_LIGHT_GRAY};font-size:0.95rem;color:{QDB_GOLD};font-weight:600;'><strong>Workflow:</strong> Deal Discovery → Due Diligence → Market → Financial → Memo</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚀 Start Deal Sourcing", use_container_width=True, key="btn_deal"):
        st.switch_page("pages/1_Deal_Sourcing.py")

with col2:
    st.markdown(f"""
    <div style='background:white;border-radius:12px;padding:35px;height:420px;box-shadow:0 5px 20px rgba(0,0,0,0.08);border-left:5px solid {QDB_PURPLE};display:flex;flex-direction:column;'>
        <h2 style='color:{QDB_PURPLE};font-size:1.9rem;font-weight:700;margin-bottom:18px;'>Due Diligence Path</h2>
        <p><strong>Start here if you have:</strong></p>
        <ul style='margin-top:12px;line-height:2;'><li>Received investment proposals</li><li>Company documents to analyze</li><li>Need deep-dive due diligence</li></ul>
        <div style='margin-top:auto;padding-top:20px;border-top:2px solid {QDB_LIGHT_GRAY};font-size:0.95rem;color:{QDB_GOLD};font-weight:600;'><strong>Workflow:</strong> Due Diligence → Market → Financial → Memo</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("📋 Start Due Diligence", use_container_width=True, key="btn_dd"):
        st.switch_page("pages/2_Due_Diligence_Analysis.py")

qdb_section_end()

# ===== SECTION 2: QUICK TOOLS (Dark Background - Pure HTML) =====
st.markdown(f"""
<div style='background: linear-gradient(135deg, #2C3E5E 0%, {QDB_DARK_BLUE} 100%); padding: 80px 20px; margin: 0 -3rem; margin-bottom: 0;'>
    <div style='max-width: 1400px; margin: 0 auto;'>
        <h2 style='text-align:center; color:white; margin-bottom:50px; font-size:2.2rem; font-weight:600;'>Quick Access Tools</h2>
        <div style='display: grid; grid-template-columns: repeat(3, 1fr); gap: 30px;'>
            <a href="?page=market" style='text-decoration: none;'>
                <div style='background: linear-gradient(135deg, {QDB_PURPLE} 0%, #764BA2 100%); color: white; border-radius: 50px; padding: 20px 40px; text-align: center; font-size: 1.1rem; font-weight: 600; box-shadow: 0 4px 15px rgba(94, 42, 132, 0.3); transition: all 0.3s ease; cursor: pointer;'>
                    📊 Market Analysis
                </div>
            </a>
            <a href="?page=financial" style='text-decoration: none;'>
                <div style='background: linear-gradient(135deg, {QDB_PURPLE} 0%, #764BA2 100%); color: white; border-radius: 50px; padding: 20px 40px; text-align: center; font-size: 1.1rem; font-weight: 600; box-shadow: 0 4px 15px rgba(94, 42, 132, 0.3); transition: all 0.3s ease; cursor: pointer;'>
                    💰 Financial Modeling
                </div>
            </a>
            <a href="?page=memo" style='text-decoration: none;'>
                <div style='background: linear-gradient(135deg, {QDB_PURPLE} 0%, #764BA2 100%); color: white; border-radius: 50px; padding: 20px 40px; text-align: center; font-size: 1.1rem; font-weight: 600; box-shadow: 0 4px 15px rgba(94, 42, 132, 0.3); transition: all 0.3s ease; cursor: pointer;'>
                    📝 Investment Memo
                </div>
            </a>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Handle navigation from HTML buttons
query_params = st.query_params
if "page" in query_params:
    page = query_params["page"]
    if page == "market":
        st.switch_page("pages/3_Market_Analysis.py")
    elif page == "financial":
        st.switch_page("pages/4_Financial_Modeling.py")
    elif page == "memo":
        st.switch_page("pages/5_Investment_Memo.py")

# ===== FOOTER =====
st.markdown(f"<div style='height:3px;background:{QDB_PURPLE};margin:50px 0 25px 0;border-radius:2px;'></div>", unsafe_allow_html=True)
col_f1, col_f2, col_f3 = st.columns([1, 2, 1])
with col_f1:
    st.markdown(f"<p style='text-align:left;color:{QDB_DARK_BLUE};font-weight:500;'>© 2025 Qatar Development Bank</p>", unsafe_allow_html=True)
with col_f2:
    st.markdown("<p style='text-align:center;color:#999;'><strong>Investment Analyst AI</strong> | Version 1.0.0</p>", unsafe_allow_html=True)
with col_f3:
    st.markdown(f"<p style='text-align:right;color:{QDB_GOLD};font-weight:500;'>Powered by Regulus</p>", unsafe_allow_html=True)
