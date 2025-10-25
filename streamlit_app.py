"""
Investment Analyst AI – Regulus Edition
Original Design | Working Page Navigation
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

# --- CONFIG ---
st.set_page_config(page_title="Investment Analyst AI - Regulus", layout="wide", initial_sidebar_state="collapsed")
apply_qdb_styling()


def encode_image(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f"data:image/png;base64,{base64.b64encode(f.read()).decode()}"
    return None


qdb_logo = encode_image("QDB_Logo.png")
regulus_logo = encode_image("regulus_logo.png")

# ===== HERO SECTION =====
st.markdown(f"""
<div style="background: linear-gradient(135deg,#1B2B4D 0%,#2C3E5E 100%);
    color:white;text-align:center;margin:0 -3rem;padding:110px 20px 100px 20px;
    position:relative;overflow:hidden;">
  <div style="position:absolute;top:25px;left:35px;">
    {"<img src='"+qdb_logo+"' style='max-height:70px;'>" if qdb_logo else "<b>QDB</b>"}
  </div>
  <div style="max-width:950px;margin:0 auto;">
    <h1 style="font-size:2.5rem;font-weight:700;">Investment Analyst AI</h1>
    <p style="color:#E2E8F0;font-size:1.05rem;margin-bottom:8px;">
      Supporting Qatar’s Economic Vision with Data‑Driven Investment Insights
    </p>
    <p style="color:#CBD5E0;font-size:0.95rem;line-height:1.6;max-width:720px;margin:0 auto 30px;">
      End‑to‑End AI Platform for Deal Sourcing, Due Diligence, Market Analysis & Investment Memoranda
    </p>
    <a href="#choose-path" style="
        background-color:#CBD5E0;color:#1B2B4D;border-radius:40px;padding:12px 34px;
        font-weight:600;font-size:0.95rem;text-decoration:none;display:inline-block;
        box-shadow:0 4px 14px rgba(203,213,224,0.3);transition:all 0.3s ease;">
        Explore Analysis Workflows</a>
  </div>
  <svg viewBox="0 0 1440 140" xmlns="http://www.w3.org/2000/svg"
       style="position:absolute;bottom:-1px;left:0;width:100%;">
    <path fill="#F6F5F2"
     d="M0,32L80,42.7C160,53,320,75,480,80C640,85,800,75,960,69.3C1120,64,
     1280,75,1360,80L1440,85L1440,140L0,140Z"></path>
  </svg>
</div>
""", unsafe_allow_html=True)

# ===== TOP NAVIGATION BAR =====
st.markdown(f"""
<style>
.navbar {{
  background-color:#F6F5F2;display:flex;justify-content:center;gap:40px;
  padding:18px 10px;margin:-10px -3rem 4px -3rem;font-size:1.07rem;
}}
.nav-item {{
  position:relative;font-weight:600;color:{QDB_DARK_BLUE};
  cursor:pointer;border-bottom:2.5px solid transparent;
  transition:color 0.3s,border-color 0.3s;
}}
.nav-item:hover{{color:#319795;border-color:#319795;}}
.card {{
  position:absolute;top:38px;left:50%;transform:translateX(-50%);
  width:320px;background:white;border-radius:12px;
  box-shadow:0 8px 32px rgba(0,0,0,0.1);
  opacity:0;visibility:hidden;transition:all 0.25s ease;
  z-index:10;pointer-events:none;
}}
.nav-item:hover .card {{
  opacity:1;visibility:visible;transform:translate(-50%,15px);
  pointer-events:auto;
}}
.card a {{
  display:block;padding:17px;text-decoration:none;color:{QDB_DARK_BLUE};
}}
.card a:hover {{
  background-color:#F0F9F8;border-radius:12px;color:#319795;
}}
.card h4{{margin:0;font-size:1.05rem;}}
.card p{{margin:6px 0 10px;font-size:0.9rem;color:#555;line-height:1.4;}}
</style>

<div class="navbar">
  <div class="nav-item" onclick="window.parent.postMessage('deal','*')">Deal Sourcing
    <div class="card"><a><h4>Deal Sourcing</h4>
      <p>Discover and qualify investment opportunities using AI‑based ranking.</p></a>
    </div>
  </div>
  <div class="nav-item" onclick="window.parent.postMessage('dd','*')">Due Diligence
    <div class="card"><a><h4>Due Diligence</h4>
      <p>Run comprehensive due diligence across financial, legal, and operational data.</p></a>
    </div>
  </div>
  <div class="nav-item" onclick="window.parent.postMessage('market','*')">Market Analysis
    <div class="card"><a><h4>Market Analysis</h4>
      <p>Extract actionable insights and competitive landscape summaries instantly.</p></a>
    </div>
  </div>
  <div class="nav-item" onclick="window.parent.postMessage('fin','*')">Financial Modeling
    <div class="card"><a><h4>Financial Modeling</h4>
      <p>Build predictive financial models with AI‑powered accuracy checks.</p></a>
    </div>
  </div>
  <div class="nav-item" onclick="window.parent.postMessage('memo','*')">Investment Memo
    <div class="card"><a><h4>Investment Memo</h4>
      <p>Create professional‑grade summary memos ready for executive review.</p></a>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ===== Handle Link Redirection =====
nav_message = st.session_state.get("nav_select", "")
st_js = """
<script>
window.addEventListener("message", (e) => {
    if (e.data == "deal") window.parent.location.href = "?nav=deal";
    if (e.data == "dd") window.parent.location.href = "?nav=dd";
    if (e.data == "market") window.parent.location.href = "?nav=market";
    if (e.data == "fin") window.parent.location.href = "?nav=fin";
    if (e.data == "memo") window.parent.location.href = "?nav=memo";
});
</script>
"""
st.markdown(st_js, unsafe_allow_html=True)

# ===== Intercept Query for Switching =====
query_params = st.experimental_get_query_params()
if "nav" in query_params:
    page = query_params["nav"][0]
    if page == "deal":
        st.switch_page("pages/1_Deal_Sourcing.py")
    elif page == "dd":
        st.switch_page("pages/2_Due_Diligence.py")
    elif page == "market":
        st.switch_page("pages/3_Market_Analysis.py")
    elif page == "fin":
        st.switch_page("pages/4_Financial_Modeling.py")
    elif page == "memo":
        st.switch_page("pages/5_Investment_Memo.py")

# ===== CHOOSE PATH SECTION (unchanged) =====
st.markdown("<div id='choose-path'></div>", unsafe_allow_html=True)
qdb_section_start("light")
st.markdown(
    f"""
<div style="text-align:center;max-width:950px;margin:0 auto 35px auto;">
  <h2 style="color:{QDB_DARK_BLUE};font-size:2rem;font-weight:700;margin-bottom:10px;">
    Choose Your Analysis Path</h2>
  <p style="color:#555;font-size:1.05rem;">Start your workflow below or use navigation above.</p>
</div>
""",
    unsafe_allow_html=True,
)

col1, col2 = st.columns(2, gap="large")
with col1:
    st.markdown("""
    <div style="background:white;border-radius:16px;padding:35px;height:390px;
                box-shadow:0 5px 20px rgba(0,0,0,0.08);border-top:4px solid #2C3E5E;
                display:flex;flex-direction:column;justify-content:space-between;">
      <h3 style="color:#1B2B4D;font-size:1.6rem;font-weight:600;">Deal Sourcing Path</h3>
      <ul style="line-height:1.9;color:#333;">
        <li><a href="?nav=deal" style="color:#1B2B4D;text-decoration:none;">AI deal identification</a></li>
        <li><a href="?nav=market" style="color:#1B2B4D;text-decoration:none;">Market handoff</a></li>
        <li><a href="?nav=dd" style="color:#1B2B4D;text-decoration:none;">Due diligence workflow</a></li>
      </ul>
      <div style="text-align:center;">
        <a href="?nav=deal" style="
          background-color:#319795;color:white;border:none;border-radius:40px;
          padding:12px 30px;font-size:0.95rem;font-weight:600;box-shadow:0 3px 12px rgba(49,151,149,0.3);
          text-decoration:none;">Start Deal Sourcing</a>
      </div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div style="background:white;border-radius:16px;padding:35px;height:390px;
                box-shadow:0 5px 20px rgba(0,0,0,0.08);border-top:4px solid #2C3E5E;
                display:flex;flex-direction:column;justify-content:space-between;">
      <h3 style="color:#1B2B4D;font-size:1.6rem;font-weight:600;">Due Diligence Path</h3>
      <ul style="line-height:1.9;color:#333;">
        <li><a href="?nav=dd" style="color:#1B2B4D;text-decoration:none;">Upload & analyze data</a></li>
        <li><a href="?nav=market" style="color:#1B2B4D;text-decoration:none;">Market comparisons</a></li>
        <li><a href="?nav=memo" style="color:#1B2B4D;text-decoration:none;">Generate Investment Memo</a></li>
      </ul>
      <div style="text-align:center;">
        <a href="?nav=dd" style="
          background-color:#319795;color:white;border:none;border-radius:40px;
          padding:12px 30px;font-size:0.95rem;font-weight:600;box-shadow:0 3px 12px rgba(49,151,149,0.3);
          text-decoration:none;">Start Due Diligence</a>
      </div>
    </div>
    """, unsafe_allow_html=True)
qdb_section_end()

# ===== FOOTER =====
st.markdown(f"""
<div style="background-color:#1B2B4D;color:#E2E8F0;padding:25px 20px;margin:0 auto;width:85%;
border-radius:15px 15px 0 0;font-size:0.94rem;">
  <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;">
    <div style="flex:3;">
      <ul style="list-style:none;display:flex;gap:25px;flex-wrap:wrap;padding:0;margin:0;">
        <li><a href="#" style="text-decoration:none;color:#E2E8F0;">About Regulus</a></li>
        <li><a href="#" style="text-decoration:none;color:#E2E8F0;">Careers</a></li>
        <li><a href="#" style="text-decoration:none;color:#E2E8F0;">Contact Us</a></li>
        <li><a href="#" style="text-decoration:none;color:#E2E8F0;">Privacy Policy</a></li>
        <li><a href="#" style="text-decoration:none;color:#E2E8F0;">Terms & Conditions</a></li>
      </ul>
    </div>
    <div style="flex:1;text-align:right;">
      <p style="margin:0;color:#A0AEC0;font-size:0.9rem;">Powered by Regulus AI</p>
      {"<img src='"+regulus_logo+"' style='max-height:55px;margin-top:6px;opacity:0.95;'>" if regulus_logo else "<strong>Regulus</strong>"}
    </div>
  </div>
</div>
""", unsafe_allow_html=True)
