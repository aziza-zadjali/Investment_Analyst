"""
Investment Analyst AI – Regulus Edition
Original design preserved | Functional navigation via st.switch_page()
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

# ----- CONFIG -----
st.set_page_config(
    page_title="Investment Analyst AI - Regulus",
    layout="wide",
    initial_sidebar_state="collapsed",
)
apply_qdb_styling()


def encode_image(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f"data:image/png;base64,{base64.b64encode(f.read()).decode()}"
    return None


qdb_logo = encode_image("QDB_Logo.png")
regulus_logo = encode_image("regulus_logo.png")

# ================= HERO SECTION =================
st.markdown(f"""
<div style="background:linear-gradient(135deg,#1B2B4D 0%,#2C3E5E 100%);
    color:white;text-align:center;margin:0 -3rem;padding:110px 20px 100px 20px;position:relative;overflow:hidden;">
  <div style="position:absolute;top:25px;left:35px;">
    {"<img src='"+qdb_logo+"' style='max-height:70px;'>" if qdb_logo else "<b>QDB</b>"}
  </div>
  <div style="max-width:950px;margin:0 auto;">
    <h1 style="font-size:2.5rem;font-weight:700;">Investment Analyst AI</h1>
    <p style="color:#E2E8F0;font-size:1.05rem;margin-bottom:8px;">
      Supporting Qatar’s Economic Vision with Data‑Driven Investment Insights
    </p>
    <p style="color:#CBD5E0;font-size:0.95rem;line-height:1.6;max-width:720px;margin:0 auto 30px auto;">
      End‑to‑End AI Platform for Deal Sourcing, Due Diligence, Market Analysis & Investment Memoranda
    </p>
  </div>
  <svg viewBox="0 0 1440 140" xmlns="http://www.w3.org/2000/svg" 
       style="position:absolute;bottom:-1px;left:0;width:100%;">
    <path fill="#F6F5F2" d="M0,32L80,42.7C160,53,320,75,480,80C640,85,800,75,960,69.3C1120,64,1280,75,
    1360,80L1440,85L1440,140L0,140Z"></path>
  </svg>
</div>
""", unsafe_allow_html=True)

# ================= NAVIGATION BAR with POPUPS =================
st.markdown(f"""
<style>
.qdb-nav {{
  background-color:#F6F5F2;
  display:flex;justify-content:center;gap:40px;
  padding:18px 10px;margin:-10px -3rem 4px -3rem;font-size:1.07rem;
}}
.qdb-nav-item {{
  position:relative;text-align:center;font-weight:600;
  color:{QDB_DARK_BLUE};padding:7px 0 5px;
  cursor:pointer;border-bottom:2.5px solid transparent;
  transition:color 0.3s,border-color 0.3s;
}}
.qdb-nav-item:hover {{color:#319795;border-bottom:2.5px solid #319795;}}
.qdb-hover-card {{
  position:absolute;top:38px;left:50%;transform:translateX(-50%);
  width:320px;background:white;border-radius:12px;box-shadow:0 8px 32px rgba(0,0,0,0.1);
  opacity:0;visibility:hidden;transition:all 0.25s ease;z-index:10;pointer-events:none;
}}
.qdb-nav-item:hover .qdb-hover-card{{opacity:1;visibility:visible;transform:translate(-50%,15px);
pointer-events:auto;}}
.qdb-hover-card h4{{margin:0;font-size:1.05rem;color:{QDB_DARK_BLUE};}}
.qdb-hover-card p{{margin:6px 0 10px;color:#555;font-size:0.9rem;line-height:1.4;}}
</style>
<div class="qdb-nav">
  <div class="qdb-nav-item" id="nav-deal">Deal Sourcing
    <div class="qdb-hover-card"><h4>Deal Sourcing</h4>
      <p>Discover and rank investment opportunities using AI filters and dataset matching.</p>
    </div>
  </div>
  <div class="qdb-nav-item" id="nav-dd">Due Diligence
    <div class="qdb-hover-card"><h4>Due Diligence</h4>
      <p>Perform automated diligence checks, document review and risk summaries.</p>
    </div>
  </div>
  <div class="qdb-nav-item" id="nav-market">Market Analysis
    <div class="qdb-hover-card"><h4>Market Analysis</h4>
      <p>Analyze industry data and competitors to inform deal decisions.</p>
    </div>
  </div>
  <div class="qdb-nav-item" id="nav-fin">Financial Modeling
    <div class="qdb-hover-card"><h4>Financial Modeling</h4>
      <p>Generate forecasts and valuations with AI-integrated financial models.</p>
    </div>
  </div>
  <div class="qdb-nav-item" id="nav-memo">Investment Memo
    <div class="qdb-hover-card"><h4>Investment Memo</h4>
      <p>Create executive memos and summaries automatically from analysis data.</p>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ===== Streamlit triggers for each nav hover (JS cannot directly trigger switch_page)
nav_cols = st.columns(5)
with nav_cols[0]:
    if st.button("Open Deal Sourcing", key="deal_full_nav"):
        st.switch_page("pages/1_Deal_Sourcing.py")
with nav_cols[1]:
    if st.button("Open Due Diligence", key="dd_full_nav"):
        st.switch_page("pages/2_Due_Diligence.py")
with nav_cols[2]:
    if st.button("Open Market Analysis", key="market_full_nav"):
        st.switch_page("pages/3_Market_Analysis.py")
with nav_cols[3]:
    if st.button("Open Financial Modeling", key="fin_full_nav"):
        st.switch_page("pages/4_Financial_Modeling.py")
with nav_cols[4]:
    if st.button("Open Investment Memo", key="memo_full_nav"):
        st.switch_page("pages/5_Investment_Memo.py")

# ================= CHOOSE PATH SECTION =================
qdb_section_start("light")
st.markdown(f"""
<div style="text-align:center;max-width:950px;margin:0 auto 35px auto;">
  <h2 style="color:{QDB_DARK_BLUE};font-size:2rem;font-weight:700;margin-bottom:10px;">
    Choose Your Analysis Path
  </h2>
  <p style="color:#555;font-size:1.05rem;">Start a workflow below or hover above for module summaries.</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")
with col1:
    st.markdown("""
    <div style="background:white;border-radius:16px;padding:35px;height:390px;
                box-shadow:0 5px 20px rgba(0,0,0,0.08);border-top:4px solid #2C3E5E;
                display:flex;flex-direction:column;justify-content:space-between;">
      <div>
        <h3 style="color:#1B2B4D;font-size:1.6rem;font-weight:600;">Deal Sourcing Path</h3>
        <ul style="margin-top:10px;line-height:1.9;color:#333;">
          <li>AI-driven deal identification</li>
          <li>Smart ranking and scoring</li>
          <li>Workflow handoff to Due Diligence</li>
        </ul>
      </div>
    """, unsafe_allow_html=True)
    if st.button("Start Deal Sourcing", use_container_width=True):
        st.switch_page("pages/1_Deal_Sourcing.py")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background:white;border-radius:16px;padding:35px;height:390px;
                box-shadow:0 5px 20px rgba(0,0,0,0.08);border-top:4px solid #2C3E5E;
                display:flex;flex-direction:column;justify-content:space-between;">
      <div>
        <h3 style="color:#1B2B4D;font-size:1.6rem;font-weight:600;">Due Diligence Path</h3>
        <ul style="margin-top:10px;line-height:1.9;color:#333;">
          <li>Smart document analysis</li>
          <li>Guided AI review steps</li>
          <li>Generate Investment Memo</li>
        </ul>
      </div>
    """, unsafe_allow_html=True)
    if st.button("Start Due Diligence", use_container_width=True):
        st.switch_page("pages/2_Due_Diligence.py")
    st.markdown("</div>", unsafe_allow_html=True)

qdb_section_end()

# ================= FOOTER =================
st.markdown(f"""
<div style="background-color:#1B2B4D;color:#E2E8F0;padding:35px 40px;
    margin:0 -3rem -2rem -3rem;font-size:0.94rem;">
  <div style="max-width:1100px;margin:0 auto;display:flex;justify-content:space-between;
      align-items:center;flex-wrap:wrap;">
    <div style="flex:3;">
      <ul style="list-style:none;display:flex;gap:25px;flex-wrap:wrap;
          padding:0;margin:0;color:#E2E8F0;">
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
        {"<img src='"+regulus_logo+"' style='max-height:55px;opacity:0.95;'>" if regulus_logo else "<strong>Regulus</strong>"}
      </div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)
