"""
Investment Analyst AI - Regulus Edition
Original Design Restored | Functional Page Navigation using st.switch_page()
"""

import streamlit as st
import base64
import os
from utils.qdb_styling import apply_qdb_styling, QDB_DARK_BLUE, qdb_section_start, qdb_section_end

# --- Page Config
st.set_page_config(page_title="Investment Analyst AI - Regulus", layout="wide", initial_sidebar_state="collapsed")
apply_qdb_styling()

def encode_image(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f"data:image/png;base64,{base64.b64encode(f.read()).decode()}"
    return None

qdb_logo = encode_image("QDB_Logo.png")
regulus_logo = encode_image("regulus_logo.png")

# ===== HERO SECTION (Unchanged Design) =====
st.markdown(f"""
<div style="
    background: linear-gradient(135deg, #1B2B4D 0%, #2C3E5E 100%);
    color: white;
    text-align: center;
    margin: 0 -3rem;
    padding: 100px 20px 90px 20px;
    position: relative;
    overflow: hidden;
">
  <div style="max-width: 1100px; margin: 0 auto; position: relative;">
      <div style="position:absolute; top:20px; left:25px;">
          {"<img src='"+qdb_logo+"' style='max-height:65px; opacity:0.95;'>" if qdb_logo else "<strong>QDB</strong>"}
      </div>

      <div style="flex:2; text-align:center;">
          <h1 style="font-size:2.5rem; font-weight:700;">Investment Analyst AI</h1>
          <p style="color:#E2E8F0;">Supporting Qatar’s Economic Vision with Data‑Driven Investment Insights</p>
          <p style="color:#CBD5E0; max-width:700px; margin:10px auto 30px;">
              End‑to‑End AI Platform for Deal Sourcing, Due Diligence, Market Analysis & Investment Memoranda
          </p>
      </div>
  </div>

  <svg viewBox="0 0 1440 150" xmlns="http://www.w3.org/2000/svg" style="position:absolute;bottom:-1px;left:0;width:100%;">
    <path fill="#F6F5F2" d="M0,32L80,42.7C160,53,320,75,480,80C640,85,800,75,960,69.3C1120,64,1280,75,1360,80L1440,85L1440,150L0,150Z"></path>
  </svg>
</div>
""", unsafe_allow_html=True)

# ===== NAVIGATION BAR =====
st.markdown("""
<style>
.qdb-nav {
  background-color:#F6F5F2;
  display:flex;
  justify-content:center;
  gap:40px;
  padding:18px 10px;
  margin:-10px -3rem 4px -3rem;
  font-size:1.07rem;
}
.qdb-button {
  background:none;
  border:none;
  font-weight:600;
  color:#1B2B4D;
  cursor:pointer;
  border-bottom:2.5px solid transparent;
  transition:color 0.3s, border-color 0.3s;
  font-size:1rem;
}
.qdb-button:hover {
  color:#319795;
  border-color:#319795;
}
</style>
""", unsafe_allow_html=True)

nav = st.container()
with nav:
    st.markdown('<div class="qdb-nav">', unsafe_allow_html=True)
    nav_col1, nav_col2, nav_col3, nav_col4, nav_col5 = st.columns(5)
    with nav_col1:
        if st.button("Deal Sourcing", key="nav_deal"):
            st.switch_page("pages/1_Deal_Sourcing.py")
    with nav_col2:
        if st.button("Due Diligence", key="nav_dd"):
            st.switch_page("pages/2_Due_Diligence.py")
    with nav_col3:
        if st.button("Market Analysis", key="nav_market"):
            st.switch_page("pages/3_Market_Analysis.py")
    with nav_col4:
        if st.button("Financial Modeling", key="nav_fin"):
            st.switch_page("pages/4_Financial_Modeling.py")
    with nav_col5:
        if st.button("Investment Memo", key="nav_memo"):
            st.switch_page("pages/5_Investment_Memo.py")
    st.markdown('</div>', unsafe_allow_html=True)

# ===== CHOOSE PATH SECTION (Same Visuals)
st.markdown("<div id='choose-path'></div>", unsafe_allow_html=True)
qdb_section_start("light")

st.markdown(f"""
<div style="text-align:center; max-width:950px; margin:0 auto 35px auto;">
  <h2 style="color:{QDB_DARK_BLUE}; font-size:2rem; font-weight:700;">Choose Your Analysis Path</h2>
  <p style="color:#555;">Start your workflow below or choose from navigation above.</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

# --- Deal Sourcing Path
with col1:
    st.markdown("""
    <div style="background:white; border-radius:16px; padding:35px; height:390px;
                box-shadow:0 5px 20px rgba(0,0,0,0.08); border-top:4px solid #2C3E5E;
                display:flex; flex-direction:column; justify-content:space-between;">
      <div>
        <h3 style="color:#1B2B4D;font-size:1.6rem;font-weight:600;margin-bottom:16px;">Deal Sourcing Path</h3>
        <ul style="margin-top:10px; line-height:1.9; color:#333;">
          <li>AI‑powered deal identification</li>
          <li>Qualitative scoring & filtering</li>
          <li>Direct workflow handoff</li>
        </ul>
      </div>
    """, unsafe_allow_html=True)
    if st.button("Start Deal Sourcing", use_container_width=True):
        st.switch_page("pages/1_Deal_Sourcing.py")
    st.markdown("</div>", unsafe_allow_html=True)

# --- Due Diligence Path
with col2:
    st.markdown("""
    <div style="background:white; border-radius:16px; padding:35px; height:390px;
                box-shadow:0 5px 20px rgba(0,0,0,0.08); border-top:4px solid #2C3E5E;
                display:flex; flex-direction:column; justify-content:space-between;">
      <div>
        <h3 style="color:#1B2B4D;font-size:1.6rem;font-weight:600;margin-bottom:16px;">Due Diligence Path</h3>
        <ul style="margin-top:10px; line-height:1.9; color:#333;">
          <li>Document verification</li>
          <li>Data‑driven insights</li>
          <li>AI risk scoring</li>
        </ul>
      </div>
    """, unsafe_allow_html=True)
    if st.button("Start Due Diligence", use_container_width=True):
        st.switch_page("pages/2_Due_Diligence.py")
    st.markdown("</div>", unsafe_allow_html=True)

qdb_section_end()

# ===== FOOTER (Original Design, Kept Extended)
st.markdown(f"""
<div style="
    background-color:#1B2B4D;
    color:#E2E8F0;
    padding:35px 40px;
    margin:0 -3rem -2rem -3rem;
    font-size:0.94rem;">
  <div style="max-width:1100px;margin:0 auto;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;">
    <div style="flex:3;">
      <ul style="list-style:none;display:flex;gap:25px;flex-wrap:wrap;padding:0;margin:0;color:#E2E8F0;">
        <li><a href="#" style="text-decoration:none;color:#E2E8F0;">About Regulus</a></li>
        <li><a href="#" style="text-decoration:none;color:#E2E8F0;">Careers</a></li>
        <li><a href="#" style="text-decoration:none;color:#E2E8F0;">Contact Us</a></li>
        <li><a href="#" style="text-decoration:none;color:#E2E8F0;">Privacy Policy</a></li>
        <li><a href="#" style="text-decoration:none;color:#E2E8F0;">Terms & Conditions</a></li>
      </ul>
    </div>
    <div style="flex:1;text-align:right;">
      <div style="display:flex;align-items:center;justify-content:flex-end;gap:8px;">
        <p style="margin:0;color:#A0AEC0;">Powered by Regulus AI</p>
        {"<img src='"+regulus_logo+"' style='max-height:55px; opacity:0.95;'>" if regulus_logo else "<strong>Regulus</strong>"}
      </div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)
