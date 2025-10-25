"""
Investment Analyst AI - Streamlined QDB UI with Wave Separator
"""

import streamlit as st
import base64
import os
from utils.qdb_styling import apply_qdb_styling, QDB_PURPLE, QDB_DARK_BLUE, QDB_CREAM, qdb_section_start, qdb_section_end

# Page configuration
st.set_page_config(page_title="Investment Analyst AI - QDB", layout="wide", initial_sidebar_state="collapsed")
apply_qdb_styling()

def encode_image(path):
    """Safely encode image for base64 HTML embedding"""
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f"data:image/png;base64,{base64.b64encode(f.read()).decode()}"
    return None

qdb_logo = encode_image("QDB_Logo.png")
regulus_logo = encode_image("regulus_logo.png")

# ===== HERO SECTION (Dark gradient header) =====
st.markdown(f"""
<div style="
    background: linear-gradient(135deg, #1B2B4D 0%, #2C3E5E 100%);
    color: white;
    padding: 70px 20px;
    text-align: center;
    margin: 0 -3rem;
    position: relative;
    overflow: hidden;
">
  <div style="max-width: 1100px; margin: 0 auto;">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; margin-bottom: 35px;">
      <div style="flex:1; text-align:center;">
        {"<img src='"+qdb_logo+"' style='max-height:75px; opacity:0.95;'>" if qdb_logo else "<strong>QDB</strong>"}
      </div>
      <div style="flex:2; text-align:center;">
        <h1 style="font-size:2.5rem; font-weight:700; letter-spacing:-0.3px;">Investment Analyst AI</h1>
        <p style="color:#E2E8F0; font-size:1.05rem; max-width:700px; margin:10px auto;">
          Supporting Qatar’s Economic Vision with Data‑Driven Investment Insights
        </p>
        <p style="color:#CBD5E0; font-size:0.95rem; line-height:1.6; max-width:700px; margin:6px auto 30px auto;">
          End‑to‑End AI Platform for Deal Sourcing, Due Diligence, Market Analysis & Investment Memoranda
        </p>
        <a href="#choose-path" style="
            background-color: #CBD5E0;
            color: #1B2B4D;
            border-radius: 40px;
            padding: 12px 36px;
            font-weight:600;
            font-size:0.95rem;
            text-decoration:none;
            display:inline-block;
            box-shadow:0 4px 14px rgba(203,213,224,0.3);
            transition: all 0.3s ease;
        " onmouseover="this.style.backgroundColor='#E2E8F0';"
          onmouseout="this.style.backgroundColor='#CBD5E0';">
          ↓ Explore Analysis Workflows
        </a>
      </div>
      <div style="flex:1; text-align:center;">
        {"<img src='"+regulus_logo+"' style='max-height:75px; opacity:0.95;'>" if regulus_logo else "<strong>Regulus</strong>"}
      </div>
    </div>
  </div>

  <!-- SVG WAVE SEPARATOR -->
  <svg viewBox="0 0 1440 150" xmlns="http://www.w3.org/2000/svg" style="position:absolute;bottom:-1px;left:0;width:100%;">
    <path fill="#F6F5F2" d="M0,32L60,26.7C120,21,240,11,360,32C480,53,600,107,720,112C840,117,960,75,1080,64C1200,53,1320,75,1380,85.3L1440,96L1440,160L1380,160C1320,160,1200,160,1080,160C960,160,840,160,720,160C600,160,480,160,360,160C240,160,120,160,60,160L0,160Z"></path>
  </svg>
</div>
""", unsafe_allow_html=True)

# ===== SECTION 2: CHOOSE PATH (Cream background) =====
st.markdown("<div id='choose-path'></div>", unsafe_allow_html=True)
qdb_section_start("light")

st.markdown(f"""
<div style="text-align:center; max-width:1000px; margin:0 auto 50px auto;">
  <h2 style="color:{QDB_DARK_BLUE}; font-size:2rem; font-weight:700; margin-bottom:10px;">
    Choose Your Analysis Path
  </h2>
  <p style="color:#555; font-size:1.05rem;">
    Select your starting point to begin your guided investment workflow.
  </p>
</div>
""", unsafe_allow_html=True)

# Global teal button styling for light section
BTN_TEAL = """
  background-color:#319795;
  color:white;
  border:none;
  border-radius:40px;
  padding:12px 30px;
  font-size:0.95rem;
  font-weight:600;
  box-shadow:0 3px 12px rgba(49,151,149,0.3);
  transition: all 0.25s ease;
  text-decoration:none;
"""
HOVER_ON = "this.style.backgroundColor='#2C7A7B'"
HOVER_OUT = "this.style.backgroundColor='#319795'"

col1, col2 = st.columns(2, gap="large")

# ===== CARD 1: Deal Sourcing Path =====
with col1:
    st.markdown(f"""
    <div style="
      background: white;
      border-radius: 16px;
      padding: 35px;
      height: 390px;
      box-shadow: 0 5px 20px rgba(0,0,0,0.08);
      border-top: 4px solid #2C3E5E;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    ">
      <div>
        <h3 style="color:#1B2B4D; font-size:1.6rem; font-weight:600; margin-bottom:16px;">
          Deal Sourcing Path
        </h3>
        <ul style="margin-top:10px; line-height:1.8; color:#333;">
          <li>Looking for new investment opportunities</li>
          <li>Building your deal pipeline</li>
          <li>Discovering and filtering potential deals</li>
        </ul>
      </div>
      <div style="margin-top:auto; text-align:center;">
        <a href="?page=deal" style="{BTN_TEAL}"
           onmouseover="{HOVER_ON}" onmouseout="{HOVER_OUT}">
           Start Deal Sourcing
        </a>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ===== CARD 2: Due Diligence Path =====
with col2:
    st.markdown(f"""
    <div style="
      background: white;
      border-radius: 16px;
      padding: 35px;
      height: 390px;
      box-shadow: 0 5px 20px rgba(0,0,0,0.08);
      border-top: 4px solid #2C3E5E;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    ">
      <div>
        <h3 style="color:#1B2B4D; font-size:1.6rem; font-weight:600; margin-bottom:16px;">
          Due Diligence Path
        </h3>
        <ul style="margin-top:10px; line-height:1.8; color:#333;">
          <li>Received investment proposals</li>
          <li>Company documents ready for analysis</li>
          <li>Need deep-dive due diligence review</li>
        </ul>
      </div>
      <div style="margin-top:auto; text-align:center;">
        <a href="?page=dd" style="{BTN_TEAL}"
           onmouseover="{HOVER_ON}" onmouseout="{HOVER_OUT}">
           Start Due Diligence
        </a>
      </div>
    </div>
    """, unsafe_allow_html=True)

qdb_section_end()
