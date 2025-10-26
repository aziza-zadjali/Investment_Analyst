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

# ===== Image Loader =====
def encode_image(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f"data:image/png;base64,{base64.b64encode(f.read()).decode()}"
    return None

qdb_logo = encode_image("QDB_Logo.png")
regulus_logo = encode_image("regulus_logo.png")

# ===== HERO SECTION =====
st.markdown(f"""
<div style="
    background: linear-gradient(135deg,#1B2B4D 0%,#2C3E5E 100%);
    color: white;
    text-align: center;
    margin: 0 -3rem;
    padding: 110px 20px 100px 20px;
    position: relative;
    overflow:hidden;">

  <!-- Left: QDB -->
  <div style="position:absolute; top:25px; left:35px;">
    {'<img src="'+qdb_logo+'" style="max-height:70px;">' if qdb_logo else '<b>QDB</b>'}
  </div>

  <!-- Right: Regulus -->
  <div style="position:absolute; top:25px; right:35px;">
    {'<img src="'+regulus_logo+'" style="max-height:70px;">' if regulus_logo else '<b>Regulus</b>'}
  </div>

  <div style="max-width:950px; margin:0 auto;">
    <h1 style="font-size:2.6rem; font-weight:700;">Investment Analyst AI – Regulus Edition</h1>
    <p style="color:#E2E8F0; font-size:1.05rem;">Supporting Qatar's Economic Vision with Data‑Driven Investment Insights</p>
    <p style="color:#CBD5E0; font-size:0.95rem; line-height:1.6; max-width:720px; margin:auto 0 30px;">
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
        box-shadow:0 4px 14px rgba(203,213,224,0.4);
        transition:all 0.3s ease;">
        Explore Analysis Workflows
    </a>
  </div>

  <!-- Decorative Divider -->
  <svg viewBox="0 0 1440 140" xmlns="http://www.w3.org/2000/svg" style="position:absolute; bottom:-1px; left:0; width:100%;">
    <path fill="#F6F5F2" d="M0,32L80,42.7C160,53,320,75,480,80C640,85,800,75,960,69.3C1120,64,1280,75,1360,80L1440,85L1440,140L0,140Z"></path>
  </svg>
</div>
""", unsafe_allow_html=True)

# ===== STYLE: Perfectly Consistent Navigation Buttons =====
st.markdown("""
<style>
.nav-container {
    background-color: #F6F5F2;
    margin: 0 -3rem;
    padding: 26px 0 30px 0;
    text-align: center;
}

/* Pill-shaped buttons consistent in size and spacing */
.stButton>button {
    background: linear-gradient(135deg,#138074 0%,#16967F 100%)!important;
    color:white!important;
    border:none!important;
    border-radius:50px!important;
    padding:15px 40px!important;
    font-weight:700!important;
    font-size:0.98rem!important;
    box-shadow:0 5px 15px rgba(19,128,116,0.3)!important;
    width:220px!important;
    height:60px!important;
    display:flex!important;
    align-items:center!important;
    justify-content:center!important;
    text-align:center!important;
    white-space:nowrap!important;
    margin:auto!important;
    transition:all 0.3s ease!important;
}

/* Hover and press effects */
.stButton>button:hover{
    background: linear-gradient(135deg,#0E5F55 0%,#107563 100%)!important;
    transform:translateY(-2px)!important;
    box-shadow:0 8px 22px rgba(19,128,116,0.45)!important;
}
.stButton>button:active{
    transform:translateY(0)!important;
    box-shadow:0 3px 10px rgba(19,128,116,0.25)!important;
}

/* Equal spacing between buttons */
div[data-testid="column"] {display:flex; justify-content:center;}
</style>
""", unsafe_allow_html=True)

# ===== NAVIGATION BAR (UNIFORM BUTTONS) =====
st.markdown('<div class="nav-container">', unsafe_allow_html=True)
nav_cols = st.columns(5)
buttons = [
    ("Deal Sourcing", "pages/1_Deal_Sourcing.py"),
    ("Due Diligence", "pages/2_Due_Diligence_Analysis.py"),
    ("Market Analysis", "pages/3_Market_Analysis.py"),
    ("Financial Modeling", "pages/4_Financial_Modeling.py"),
    ("Investment Memo", "pages/5_Investment_Memo.py")
]
for i, (label, path) in enumerate(buttons):
    with nav_cols[i]:
        if st.button(label, key=f"nav_{i}"):
            st.switch_page(path)
st.markdown('</div>', unsafe_allow_html=True)

# ===== CHOOSE PATH SECTION =====
st.markdown("<div id='choose-path'></div>", unsafe_allow_html=True)
qdb_section_start("light")
st.markdown(f"""
<div style="text-align:center; max-width:950px; margin:0 auto 35px auto;">
  <h2 style="color:{QDB_DARK_BLUE}; font-size:2rem; font-weight:700; margin-bottom:10px;">
    Choose Your Analysis Path
  </h2>
</div>
""", unsafe_allow_html=True)

cols = st.columns([0.5, 2, 2, 0.5])
with cols[1]:
    st.markdown(f"""
        <div style="background:white; border-radius:16px; padding:30px; height:280px;
                    box-shadow:0 5px 20px rgba(0,0,0,0.08); border-top:4px solid #138074;
                    display:flex; flex-direction:column; justify-content:space-between;">
            <h3 style="color:#1B2B4D; font-size:1.4rem; font-weight:600;">Deal Sourcing Path</h3>
            <ul style="line-height:1.7; color:#333; font-size:0.95rem;">
                <li>AI‑powered deal identification</li>
                <li>Market handoff integration</li>
                <li>Proceed to due diligence</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Start Deal Sourcing", key="btn_deal", use_container_width=True):
        st.switch_page("pages/1_Deal_Sourcing.py")

with cols[2]:
    st.markdown(f"""
        <div style="background:white; border-radius:16px; padding:30px; height:280px;
                    box-shadow:0 5px 20px rgba(0,0,0,0.08); border-top:4px solid #138074;
                    display:flex; flex-direction:column; justify-content:space-between;">
            <h3 style="color:#1B2B4D; font-size:1.4rem; font-weight:600;">Due Diligence Path</h3>
            <ul style="line-height:1.7; color:#333; font-size:0.95rem;">
                <li>Analyze company data</li>
                <li>Review legal & financials</li>
                <li>Generate Investment Memo</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Start Due Diligence", key="btn_dd", use_container_width=True):
        st.switch_page("pages/2_Due_Diligence_Analysis.py")

qdb_section_end()

# ===== FOOTER =====
st.markdown(f"""
<div style="
    background-color:#1B2B4D;
    color:#E2E8F0;
    padding:28px 40px;
    margin:40px -3rem -2rem -3rem;
    font-size:0.94rem;">
  <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; max-width:1400px; margin:auto;">
    <div style="flex:2;">
      <ul style="list-style:none; display:flex; gap:30px; flex-wrap:wrap; padding:0; margin:0;">
        <li><a href="#" style="text-decoration:none; color:#E2E8F0;">About Regulus</a></li>
        <li><a href="#" style="text-decoration:none; color:#E2E8F0;">Insights</a></li>
        <li><a href="#" style="text-decoration:none; color:#E2E8F0;">Careers</a></li>
        <li><a href="#" style="text-decoration:none; color:#E2E8F0;">Contact</a></li>
        <li><a href="#" style="text-decoration:none; color:#E2E8F0;">Privacy</a></li>
      </ul>
    </div>
    <div style="flex:1; text-align:right; display:flex; align-items:center; justify-content:flex-end; gap:12px;">
      <p style="margin:0; color:#A0AEC0; font-size:0.9rem;">Powered by Regulus AI</p>
      {'<img src="'+regulus_logo+'" style="max-height:45px; opacity:0.95;">' if regulus_logo else ''}
    </div>
  </div>
</div>
""", unsafe_allow_html=True)
