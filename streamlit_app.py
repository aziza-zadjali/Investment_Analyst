"""
Investment Analyst AI – Regulus Edition
Enhanced with Analyst Dashboard + Improved Section Padding
"""
import streamlit as st
import base64
import os
from datetime import datetime, timedelta
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

# ===== HERO SECTION (PADDED) =====
st.markdown(f"""
<div style="
    background: linear-gradient(135deg,#1B2B4D 0%,#2C3E5E 100%);
    color: white;
    text-align: center;
    margin: 0 -3rem;
    padding: 130px 20px 120px 20px;
    position: relative;
    overflow:hidden;">

  <!-- Left: QDB -->
  <div style="position:absolute; top:30px; left:40px;">
    {'<img src="'+qdb_logo+'" style="max-height:75px;">' if qdb_logo else '<b>QDB</b>'}
  </div>

  <!-- Right: Regulus -->
  <div style="position:absolute; top:30px; right:40px;">
    {'<img src="'+regulus_logo+'" style="max-height:75px;">' if regulus_logo else '<b>Regulus</b>'}
  </div>

  <div style="max-width:950px; margin:0 auto;">
    <h1 style="font-size:2.8rem; font-weight:800; margin-bottom:12px;">Investment Analyst AI – Regulus Edition</h1>
    <p style="color:#E2E8F0; font-size:1.1rem; margin-bottom:16px;">Supporting Qatar's Economic Vision with Data‑Driven Investment Insights</p>
    <p style="color:#CBD5E0; font-size:0.98rem; line-height:1.7; max-width:750px; margin:auto 0 35px;">
      End‑to‑End AI Platform for Deal Sourcing, Due Diligence, Market Analysis & Investment Memoranda
    </p>
    <a href="#dashboard" style="
        background-color:#16A085;
        color:white;
        border-radius:40px;
        padding:14px 40px;
        font-weight:700;
        font-size:0.97rem;
        text-decoration:none;
        display:inline-block;
        box-shadow:0 5px 18px rgba(22,160,133,0.4);
        transition:all 0.3s ease;">
        View My Dashboard ↓
    </a>
  </div>

  <!-- Decorative Divider -->
  <svg viewBox="0 0 1440 140" xmlns="http://www.w3.org/2000/svg" style="position:absolute; bottom:-1px; left:0; width:100%;">
    <path fill="#F6F5F2" d="M0,32L80,42.7C160,53,320,75,480,80C640,85,800,75,960,69.3C1120,64,1280,75,1360,80L1440,85L1440,140L0,140Z"></path>
  </svg>
</div>
""", unsafe_allow_html=True)

# ===== STYLE: Consistent Navigation & Dashboard =====
st.markdown("""
<style>
.nav-container {
    background-color: #F6F5F2;
    margin: 0 -3rem;
    padding: 32px 0 36px 0;
    text-align: center;
}

.stButton>button {
    background: linear-gradient(135deg,#16A085 0%,#138074 100%)!important;
    color:white!important;
    border:none!important;
    border-radius:50px!important;
    padding:16px 42px!important;
    font-weight:700!important;
    font-size:0.99rem!important;
    box-shadow:0 5px 16px rgba(22,160,133,0.35)!important;
    width:230px!important;
    height:62px!important;
    display:flex!important;
    align-items:center!important;
    justify-content:center!important;
    text-align:center!important;
    white-space:nowrap!important;
    margin:auto!important;
    transition:all 0.3s ease!important;
}

.stButton>button:hover{
    background: linear-gradient(135deg,#0E5F55 0%,#107563 100%)!important;
    transform:translateY(-3px)!important;
    box-shadow:0 8px 24px rgba(22,160,133,0.45)!important;
}

.stButton>button:active{
    transform:translateY(-1px)!important;
    box-shadow:0 4px 12px rgba(22,160,133,0.3)!important;
}

div[data-testid="column"] {display:flex; justify-content:center;}

.dashboard-card {
    background: white;
    border-radius: 12px;
    padding: 24px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.08);
    border-left: 5px solid #16A085;
    margin-bottom: 16px;
    transition: all 0.3s ease;
}

.dashboard-card:hover {
    box-shadow: 0 4px 20px rgba(22,160,133,0.15);
    transform: translateY(-2px);
}

.metric-box {
    background: linear-gradient(135deg, #16A085 0%, #138074 100%);
    color: white;
    padding: 24px;
    border-radius: 12px;
    text-align: center;
    box-shadow: 0 4px 16px rgba(22,160,133,0.25);
}

.metric-number {
    font-size: 2.2rem;
    font-weight: 800;
    margin: 8px 0;
}

.metric-label {
    font-size: 0.95rem;
    opacity: 0.95;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# ===== NAVIGATION BAR =====
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

st.markdown("<div id='dashboard'></div>", unsafe_allow_html=True)

# ===== ANALYST DASHBOARD SECTION =====
st.markdown(f"""
<div style="margin: 0 -3rem; padding: 48px 3rem; background: linear-gradient(135deg, #F8F7F5 0%, #F5F2ED 100%);">
    <h2 style="color:#1B2B4D; font-size:2rem; font-weight:800; margin-bottom:24px; text-align:center;">
        📊 Your Analysis Dashboard
    </h2>
    <p style="color:#666; text-align:center; font-size:1rem; margin-bottom:40px;">
        Quick overview of your investment pipeline and pending tasks
    </p>
</div>
""", unsafe_allow_html=True)

# Dashboard Metrics Row
metric_cols = st.columns([1, 1, 1, 1])

with metric_cols[0]:
    st.markdown("""
    <div class="metric-box">
        <div style="font-size:1.1rem; opacity:0.9;">⏳ Pending</div>
        <div class="metric-number">5</div>
        <div class="metric-label">Due Diligence Reports</div>
    </div>
    """, unsafe_allow_html=True)

with metric_cols[1]:
    st.markdown("""
    <div class="metric-box">
        <div style="font-size:1.1rem; opacity:0.9;">📈 Active</div>
        <div class="metric-number">12</div>
        <div class="metric-label">Deals in Pipeline</div>
    </div>
    """, unsafe_allow_html=True)

with metric_cols[2]:
    st.markdown("""
    <div class="metric-box">
        <div style="font-size:1.1rem; opacity:0.9;">✅ Completed</div>
        <div class="metric-number">28</div>
        <div class="metric-label">This Quarter</div>
    </div>
    """, unsafe_allow_html=True)

with metric_cols[3]:
    st.markdown("""
    <div class="metric-box">
        <div style="font-size:1.1rem; opacity:0.9;">⏱️ Avg Time</div>
        <div class="metric-number">2.3h</div>
        <div class="metric-label">Per Analysis</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height:28px;'></div>", unsafe_allow_html=True)

# Dashboard Cards - Pending Tasks
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="dashboard-card">
        <h3 style="color:#1B2B4D; margin-top:0; font-size:1.2rem;">🔴 Action Required</h3>
        <div style="border-top:2px solid #E0E0E0; padding-top:16px; margin-top:12px;">
            <p style="margin:0 0 12px 0; color:#333;"><strong>GreenTech Solutions</strong><br>
            <span style="color:#E74C3C;">Due: Tomorrow</span> - Financial review pending</p>
            <p style="margin:0 0 12px 0; color:#333;"><strong>CloudFlow AI</strong><br>
            <span style="color:#E74C3C;">Due: Oct 28</span> - Legal compliance check needed</p>
            <p style="margin:0; color:#333;"><strong>SustainBox Inc</strong><br>
            <span style="color:#E74C3C;">Due: Oct 29</span> - Market analysis incomplete</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="dashboard-card">
        <h3 style="color:#1B2B4D; margin-top:0; font-size:1.2rem;">🟡 In Progress</h3>
        <div style="border-top:2px solid #E0E0E0; padding-top:16px; margin-top:12px;">
            <p style="margin:0 0 12px 0; color:#333;"><strong>DataFlow Systems</strong><br>
            <span style="color:#F39C12;">75% Complete</span> - Awaiting final review</p>
            <p style="margin:0 0 12px 0; color:#333;"><strong>FinTech Innovations</strong><br>
            <span style="color:#F39C12;">50% Complete</span> - Due diligence analysis ongoing</p>
            <p style="margin:0; color:#333;"><strong>EcoEnergy Solutions</strong><br>
            <span style="color:#F39C12;">90% Complete</span> - Memo generation in progress</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

# Recent Activity
st.markdown("""
<div class="dashboard-card">
    <h3 style="color:#1B2B4D; margin-top:0; font-size:1.2rem;">📋 Recent Activity</h3>
    <div style="border-top:2px solid #E0E0E0; padding-top:16px; margin-top:12px;">
        <div style="display:flex; justify-content:space-between; margin-bottom:12px; padding-bottom:12px; border-bottom:1px solid #F0F0F0;">
            <span style="color:#333;"><strong>✅ Completed DD Report</strong><br><span style="font-size:0.9rem; color:#666;">Baladna Q.P.S.C.</span></span>
            <span style="color:#666; font-size:0.9rem;">Today, 10:30 AM</span>
        </div>
        <div style="display:flex; justify-content:space-between; margin-bottom:12px; padding-bottom:12px; border-bottom:1px solid #F0F0F0;">
            <span style="color:#333;"><strong>📊 Generated Financial Model</strong><br><span style="font-size:0.9rem; color:#666;">Emirates Tech Ventures</span></span>
            <span style="color:#666; font-size:0.9rem;">Yesterday, 3:45 PM</span>
        </div>
        <div style="display:flex; justify-content:space-between;">
            <span style="color:#333;"><strong>📈 Market Analysis Complete</strong><br><span style="font-size:0.9rem; color:#666;">Aquaculture Innovations</span></span>
            <span style="color:#666; font-size:0.9rem;">Oct 23, 2:15 PM</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)

# ===== CHOOSE PATH SECTION =====
qdb_section_start("light")
st.markdown(f"""
<div style="text-align:center; max-width:950px; margin:0 auto 48px auto;">
  <h2 style="color:{QDB_DARK_BLUE}; font-size:2rem; font-weight:800; margin-bottom:12px;">
    ➜ Start Your Analysis
  </h2>
  <p style="color:#666; font-size:1rem; margin:0;">Choose a workflow to begin investment analysis</p>
</div>
""", unsafe_allow_html=True)

cols = st.columns([0.5, 2, 2, 0.5])
with cols[1]:
    st.markdown(f"""
        <div style="background:white; border-radius:14px; padding:40px 28px; height:320px;
                    box-shadow:0 6px 24px rgba(0,0,0,0.1); border-top:5px solid #16A085;
                    display:flex; flex-direction:column; justify-content:space-between;">
            <div>
                <h3 style="color:#1B2B4D; font-size:1.35rem; font-weight:700; margin-bottom:4px;">🔍 Deal Sourcing</h3>
                <p style="color:#666; font-size:0.9rem; margin-top:8px; line-height:1.6;">
                    Discover investment opportunities using AI-powered market scanning and deal identification
                </p>
            </div>
            <ul style="line-height:1.8; color:#555; font-size:0.95rem; margin:12px 0 0 0; padding-left:18px;">
                <li>Automated deal finding</li>
                <li>Market screening</li>
                <li>Pipeline management</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Start Deal Sourcing", key="btn_deal", use_container_width=True):
        st.switch_page("pages/1_Deal_Sourcing.py")

with cols[2]:
    st.markdown(f"""
        <div style="background:white; border-radius:14px; padding:40px 28px; height:320px;
                    box-shadow:0 6px 24px rgba(0,0,0,0.1); border-top:5px solid #16A085;
                    display:flex; flex-direction:column; justify-content:space-between;">
            <div>
                <h3 style="color:#1B2B4D; font-size:1.35rem; font-weight:700; margin-bottom:4px;">⚖️ Due Diligence</h3>
                <p style="color:#666; font-size:0.9rem; margin-top:8px; line-height:1.6;">
                    Deep dive into company analysis: financials, legal, operations & risk assessment
                </p>
            </div>
            <ul style="line-height:1.8; color:#555; font-size:0.95rem; margin:12px 0 0 0; padding-left:18px;">
                <li>Document analysis</li>
                <li>Risk evaluation</li>
                <li>Report generation</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Start Due Diligence", key="btn_dd", use_container_width=True):
        st.switch_page("pages/2_Due_Diligence_Analysis.py")

qdb_section_end()

st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

# ===== FOOTER =====
st.markdown(f"""
<div style="
    background-color:#1B2B4D;
    color:#E2E8F0;
    padding:32px 40px;
    margin:50px -3rem -2rem -3rem;
    font-size:0.94rem;">
  <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; max-width:1400px; margin:auto;">
    <div style="flex:2;">
      <ul style="list-style:none; display:flex; gap:32px; flex-wrap:wrap; padding:0; margin:0;">
        <li><a href="#" style="text-decoration:none; color:#E2E8F0; transition:color 0.3s;">About Regulus</a></li>
        <li><a href="#" style="text-decoration:none; color:#E2E8F0; transition:color 0.3s;">Insights</a></li>
        <li><a href="#" style="text-decoration:none; color:#E2E8F0; transition:color 0.3s;">Careers</a></li>
        <li><a href="#" style="text-decoration:none; color:#E2E8F0; transition:color 0.3s;">Contact</a></li>
        <li><a href="#" style="text-decoration:none; color:#E2E8F0; transition:color 0.3s;">Privacy</a></li>
      </ul>
    </div>
    <div style="flex:1; text-align:right; display:flex; align-items:center; justify-content:flex-end; gap:12px;">
      <p style="margin:0; color:#A0AEC0; font-size:0.9rem; font-weight:600;">Powered by Regulus AI</p>
      {'<img src="'+regulus_logo+'" style="max-height:48px; opacity:0.95;">' if regulus_logo else ''}
    </div>
  </div>
</div>
""", unsafe_allow_html=True)
