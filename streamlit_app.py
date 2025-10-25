"""
Investment Analyst AI - QDB Official Branding
Hero section redesign with alternating QDB-style sections
"""

import streamlit as st
import base64
import os
from utils.qdb_styling import apply_qdb_styling, QDB_PURPLE, QDB_GOLD, QDB_DARK_BLUE, QDB_CREAM, qdb_section_start, qdb_section_end

st.set_page_config(page_title="Investment Analyst AI - QDB", layout="wide", initial_sidebar_state="collapsed")
apply_qdb_styling()

def encode_image(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f"data:image/png;base64,{base64.b64encode(f.read()).decode()}"
    return None

qdb_logo = encode_image("QDB_Logo.png")
regulus_logo = encode_image("regulus_logo.png")

# ===== HERO SECTION (Dark Gradient Full Height) =====
st.markdown(f"""
<div style='
    background: linear-gradient(135deg, #1B2B4D 0%, #2C3E5E 100%);
    color: white;
    padding: 80px 20px 90px 20px;
    text-align: center;
    margin: 0 -3rem;
'>
    <div style='max-width: 1400px; margin: 0 auto;'>
        <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:60px;'>
            <div style='flex:1; text-align:center;'>
                {"<img src='"+qdb_logo+"' style='max-height:90px;'>" if qdb_logo else "<strong>QDB</strong>"}
            </div>
            <div style='flex:2;'>
                <h1 style='font-size:2.8rem; font-weight:700; line-height:1.3;'>
                    Investment Analyst AI
                </h1>
                <p style='color:{QDB_GOLD}; font-size:1.15rem; font-weight:600; margin: 16px 0;'>
                    Supporting Qatar’s Economic Vision with Data-Driven Investment Insights
                </p>
                <p style='color:#F0F0F0; font-size:1.05rem;'>
                    End-to-End AI Platform for Deal Sourcing, Due Diligence, Market Analysis & Investment Memoranda
                </p>
            </div>
            <div style='flex:1; text-align:center;'>
                {"<img src='"+regulus_logo+"' style='max-height:90px;'>" if regulus_logo else "<strong>Regulus</strong>"}
            </div>
        </div>
        <div style='margin-top:40px;'>
            <a href='#choose-your-analysis-path' style='
                background: linear-gradient(135deg, {QDB_PURPLE} 0%, #764BA2 100%);
                color: white;
                border-radius: 50px;
                padding: 16px 40px;
                font-weight: 600;
                text-decoration: none;
                box-shadow: 0 5px 20px rgba(94,42,132,0.4);
                transition: all 0.3s ease;
            ' onmouseover="this.style.background='linear-gradient(135deg,#764BA2 0%,{QDB_PURPLE} 100%)'; this.style.transform='translateY(-3px)';" 
               onmouseout="this.style.background='linear-gradient(135deg,{QDB_PURPLE} 0%,#764BA2 100%)'; this.style.transform='translateY(0)';">
               ↓ Explore Analysis Workflows
            </a>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ===== ANALYSIS PATH SECTION (Cream Background) =====
st.markdown("<div id='choose-your-analysis-path'></div>", unsafe_allow_html=True)
qdb_section_start("light")

st.markdown(f"""
<div style='text-align:center; margin-bottom:50px;'>
    <h2 style='color:{QDB_DARK_BLUE}; font-size:2.3rem; font-weight:700; margin-bottom:15px;'>
        Choose Your Analysis Path
    </h2>
    <p style='color:#777; font-size:1.15rem;'>
        Select your investment workflow to begin comprehensive analysis
    </p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown(f"""
    <div style='background:white;border-radius:12px;padding:35px;height:420px;
                box-shadow:0 5px 20px rgba(0,0,0,0.08);border-left:5px solid {QDB_PURPLE};
                display:flex;flex-direction:column;'>
        <h2 style='color:{QDB_PURPLE};font-size:1.9rem;font-weight:700;margin-bottom:18px;'>Deal Sourcing Path</h2>
        <p><strong>Start here if you are:</strong></p>
        <ul style='margin-top:12px;line-height:2;'>
            <li>Looking for new investment opportunities</li>
            <li>Building your deal pipeline</li>
            <li>Discovering and filtering potential deals</li>
        </ul>
        <div style='margin-top:auto;padding-top:20px;border-top:2px solid #eee;
                    font-size:0.95rem;color:{QDB_GOLD};font-weight:600;'>
            <strong>Workflow:</strong> Deal Discovery → Due Diligence → Market → Financial → Memo
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚀 Start Deal Sourcing", use_container_width=True, key="btn_deal"):
        st.switch_page("pages/1_Deal_Sourcing.py")

with col2:
    st.markdown(f"""
    <div style='background:white;border-radius:12px;padding:35px;height:420px;
                box-shadow:0 5px 20px rgba(0,0,0,0.08);border-left:5px solid {QDB_PURPLE};
                display:flex;flex-direction:column;'>
        <h2 style='color:{QDB_PURPLE};font-size:1.9rem;font-weight:700;margin-bottom:18px;'>Due Diligence Path</h2>
        <p><strong>Start here if you have:</strong></p>
        <ul style='margin-top:12px;line-height:2;'>
            <li>Received investment proposals</li>
            <li>Company documents to analyze</li>
            <li>Need deep-dive due diligence</li>
        </ul>
        <div style='margin-top:auto;padding-top:20px;border-top:2px solid #eee;
                    font-size:0.95rem;color:{QDB_GOLD};font-weight:600;'>
            <strong>Workflow:</strong> Due Diligence → Market → Financial → Memo
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("📋 Start Due Diligence", use_container_width=True, key="btn_dd"):
        st.switch_page("pages/2_Due_Diligence_Analysis.py")

qdb_section_end()
