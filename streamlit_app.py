"""
Investment Analyst AI – Regulus Edition
Footer refined | Powered by Regulus AI only
"""

import streamlit as st
import base64
import os
from utils.qdb_styling import (
    apply_qdb_styling,
    QDB_PURPLE,
    QDB_DARK_BLUE,
    qdb_section_start,
    qdb_section_end,
)

# --- Page configuration
st.set_page_config(
    page_title="Investment Analyst AI - Regulus",
    layout="wide",
    initial_sidebar_state="collapsed",
)
apply_qdb_styling()


def encode_image(path):
    """Safely embed logos"""
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f"data:image/png;base64,{base64.b64encode(f.read()).decode()}"
    return None


qdb_logo = encode_image("QDB_Logo.png")
regulus_logo = encode_image("regulus_logo.png")

# ===== HERO SECTION =====
st.markdown(
    f"""
<div style="
    background: linear-gradient(135deg, #1B2B4D 0%, #2C3E5E 100%);
    color: white;
    text-align: center;
    margin: 0 -3rem;
    padding: 110px 20px 100px 20px;
    position: relative;
    overflow: hidden;">
  
  <!-- QDB Logo -->
  <div style="position:absolute; top:25px; left:35px;">
    {"<img src='"+qdb_logo+"' style='max-height:70px;'>" if qdb_logo else "<b>QDB</b>"}
  </div>

  <!-- Central Content -->
  <div style="max-width:950px; margin:0 auto;">
    <h1 style="font-size:2.5rem; font-weight:700; letter-spacing:-0.3px;">
      Investment Analyst AI
    </h1>
    <p style="color:#E2E8F0; font-size:1.05rem; margin-bottom:8px;">
      Supporting Qatar's Economic Vision with Data‑Driven Investment Insights
    </p>
    <p style="color:#CBD5E0; font-size:0.95rem; line-height:1.6; max-width:720px; margin:0 auto 30px;">
      End‑to‑End AI Platform for Deal Sourcing, Due Diligence, Market Analysis & Investment Memoranda
    </p>
    <a href="#choose-path" style="
        background-color:#CBD5E0;
        color:#1B2B4D;
        border-radius:40px;
        padding:12px 34px;
        font-weight:600;
        font-size:0.95rem;
        text-decoration:none;
        display:inline-block;
        box-shadow:0 4px 14px rgba(203,213,224,0.3);
        transition:all 0.3s ease;">
        Explore Analysis Workflows
    </a>
  </div>

  <!-- Wave Divider -->
  <svg viewBox="0 0 1440 140" xmlns="http://www.w3.org/2000/svg" style="position:absolute; bottom:-1px; left:0; width:100%;">
    <path fill="#F6F5F2" d="M0,32L80,42.7C160,53,320,75,480,80C640,85,800,75,960,69.3C1120,64,1280,75,1360,80L1440,85L1440,140L0,140Z"></path>
  </svg>
</div>
""",
    unsafe_allow_html=True,
)

# ===== OVERRIDE WITH DARKER TEAL COLOR =====
st.markdown(
    """
<style>
/* Navigation container */
.nav-container {
    background-color: #F6F5F2;
    margin: 0 -3rem;
    padding: 20px 0;
    text-align: center;
}

/* Make all buttons same width */
div[data-testid="column"] {
    display: flex;
    justify-content: center;
    align-items: center;
}

/* FORCE DARKER TEAL COLOR - Override QDB purple styling */
div[data-testid="column"] > div > div > div > div > button,
div[data-testid="column"] button,
.stButton > button,
button[kind="secondary"],
button[kind="primary"] {
    background: linear-gradient(135deg, #138074 0%, #16967F 100%) !important;
    background-color: #138074 !important;
    color: white !important;
    border: none !important;
    border-radius: 32px !important;
    padding: 10px 28px !important;
    min-width: 160px !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 3px 14px rgba(19,128,116,0.35) !important;
    letter-spacing: 0.02em !important;
    line-height: 1.3 !important;
    text-transform: none !important;
    white-space: pre-line !important;
}

div[data-testid="column"] > div > div > div > div > button:hover,
div[data-testid="column"] button:hover,
.stButton > button:hover,
button[kind="secondary"]:hover,
button[kind="primary"]:hover {
    background: linear-gradient(135deg, #0e5f55 0%, #107563 100%) !important;
    background-color: #0e5f55 !important;
    box-shadow: 0 6px 18px rgba(19,128,116,0.5) !important;
    transform: translateY(-2px) !important;
}

div[data-testid="column"] > div > div > div > div > button:active,
div[data-testid="column"] button:active,
.stButton > button:active {
    transform: translateY(0px) !important;
}
</style>
""",
    unsafe_allow_html=True,
)

# ===== TOP NAVIGATION - CENTERED WITH EQUAL WIDTHS =====
st.markdown('<div class="nav-container">', unsafe_allow_html=True)

# Add empty columns for centering with equal button widths
nav_cols = st.columns([0.5, 1, 1, 1, 1, 1, 0.5])

with nav_cols[1]:
    if st.button("Deal\nSourcing", key="nav_deal", type="primary", use_container_width=True):
        st.switch_page("pages/1_Deal_Sourcing.py")

with nav_cols[2]:
    if st.button("Due\nDiligence", key="nav_dd", type="primary", use_container_width=True):
        st.switch_page("pages/2_Due_Diligence_Analysis.py")

with nav_cols[3]:
    if st.button("Market\nAnalysis", key="nav_market", type="primary", use_container_width=True):
        st.switch_page("pages/3_Market_Analysis.py")

with nav_cols[4]:
    if st.button("Financial\nModeling", key="nav_fin", type="primary", use_container_width=True):
        st.switch_page("pages/4_Financial_Modeling.py")

with nav_cols[5]:
    if st.button("Investment\nMemo", key="nav_memo", type="primary", use_container_width=True):
        st.switch_page("pages/5_Investment_Memo.py")

st.markdown("</div>", unsafe_allow_html=True)

# ===== CHOOSE PATH SECTION =====
st.markdown("<div id='choose-path'></div>", unsafe_allow_html=True)
qdb_section_start("light")
st.markdown(
    f"""
<div style="text-align:center; max-width:950px; margin:0 auto 35px auto;">
  <h2 style="color:{QDB_DARK_BLUE}; font-size:2rem; font-weight:700; margin-bottom:10px;">
    Choose Your Analysis Path
  </h2>
  <p style="color:#555; font-size:1.05rem;">Start your workflow below or use the navigation above.</p>
</div>
""",
    unsafe_allow_html=True,
)

# Add empty columns to center the two path boxes
path_cols = st.columns([0.5, 2, 2, 0.5])

with path_cols[1]:
    st.markdown(
        f"""
        <div style="background:white; border-radius:16px; padding:30px; height:280px;
                    box-shadow:0 5px 20px rgba(0,0,0,0.08); border-top:4px solid #138074;
                    display:flex; flex-direction:column; justify-content:space-between;">
            <div>
                <h3 style="color:#1B2B4D; font-size:1.4rem; font-weight:600; margin-bottom:14px;">Deal Sourcing Path</h3>
                <ul style="margin-top:8px; line-height:1.7; color:#333; font-size:0.95rem;">
                    <li>AI‑powered deal identification</li>
                    <li>Market analysis handoff</li>
                    <li>Proceed to due diligence</li>
                </ul>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<div style='text-align:center; margin-top:18px;'>", unsafe_allow_html=True)
    if st.button("Start Deal Sourcing", key="deal_btn", type="primary"):
        st.switch_page("pages/1_Deal_Sourcing.py")
    st.markdown("</div>", unsafe_allow_html=True)

with path_cols[2]:
    st.markdown(
        f"""
        <div style="background:white; border-radius:16px; padding:30px; height:280px;
                    box-shadow:0 5px 20px rgba(0,0,0,0.08); border-top:4px solid #138074;
                    display:flex; flex-direction:column; justify-content:space-between;">
            <div>
                <h3 style="color:#1B2B4D; font-size:1.4rem; font-weight:600; margin-bottom:14px;">Due Diligence Path</h3>
                <ul style="margin-top:8px; line-height:1.7; color:#333; font-size:0.95rem;">
                    <li>Upload and analyze company data</li>
                    <li>Market fit comparatives</li>
                    <li>Create Investment Memo</li>
                </ul>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<div style='text-align:center; margin-top:18px;'>", unsafe_allow_html=True)
    if st.button("Start Due Diligence", key="dd_btn", type="primary"):
        st.switch_page("pages/2_Due_Diligence_Analysis.py")
    st.markdown("</div>", unsafe_allow_html=True)

qdb_section_end()

# ===== FOOTER (FULL PAGE WIDTH) =====
st.markdown(
    f"""
<div style="
    background-color:#1B2B4D;
    color:#E2E8F0;
    padding:30px 40px;
    margin:40px -3rem 0 -3rem;
    font-size:0.94rem;">
  <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; max-width:1400px; margin:0 auto;">
    <div style="flex:2;">
      <ul style="list-style:none; display:flex; gap:30px; flex-wrap:wrap; padding:0; margin:0;">
        <li><a href="#" style="text-decoration:none; color:#E2E8F0; transition:color 0.3s;">About Regulus</a></li>
        <li><a href="#" style="text-decoration:none; color:#E2E8F0; transition:color 0.3s;">Careers</a></li>
        <li><a href="#" style="text-decoration:none; color:#E2E8F0; transition:color 0.3s;">Contact Us</a></li>
        <li><a href="#" style="text-decoration:none; color:#E2E8F0; transition:color 0.3s;">Privacy Policy</a></li>
        <li><a href="#" style="text-decoration:none; color:#E2E8F0; transition:color 0.3s;">Terms & Conditions</a></li>
      </ul>
    </div>
    <div style="flex:1; text-align:right; display:flex; align-items:center; justify-content:flex-end; gap:12px;">
      <p style="margin:0; color:#A0AEC0; font-size:0.9rem;">Powered by Regulus AI</p>
      {"<img src='"+regulus_logo+"' style='max-height:45px; opacity:0.95;'>" if regulus_logo else ""}
    </div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)
