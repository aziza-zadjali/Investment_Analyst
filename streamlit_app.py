"""
Investment Analyst AI – Regulus Edition (Final)
Fully professional UI with native navigation and extended full-width footer
"""

import streamlit as st
import base64
import os
from utils.qdb_styling import (
    apply_qdb_styling,
    QDB_DARK_BLUE,
    qdb_section_start,
    qdb_section_end,
)

# --- Page Setup ---
st.set_page_config(
    page_title="Investment Analyst AI - Regulus",
    layout="wide",
    initial_sidebar_state="collapsed",
)
apply_qdb_styling()


def encode_image(path):
    """Encode image to base64 HTML inline"""
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
    overflow: hidden;
">

  <!-- QDB Logo -->
  <div style="position:absolute; top:25px; left:35px;">
    {"<img src='"+qdb_logo+"' style='max-height:70px;'>" if qdb_logo else "<b>QDB</b>"}
  </div>

  <!-- Headline -->
  <div style="max-width:950px; margin:0 auto;">
    <h1 style="font-size:2.5rem; font-weight:700; letter-spacing:-0.3px;">
      Investment Analyst AI
    </h1>
    <p style="color:#E2E8F0; font-size:1.05rem; margin-bottom:8px;">
      Supporting Qatar’s Economic Vision with Data‑Driven Investment Insights
    </p>
    <p style="color:#CBD5E0; font-size:0.95rem; line-height:1.6; max-width:720px; margin:0 auto 30px;">
      End‑to‑End AI Platform for Deal Sourcing, Due Diligence, Market Analysis & Investment Memoranda
    </p>
  </div>

  <!-- Wave Divider -->
  <svg viewBox="0 0 1440 140" xmlns="http://www.w3.org/2000/svg" style="position:absolute; bottom:-1px; left:0; width:100%;">
    <path fill="#F6F5F2" d="M0,32L80,42.7C160,53,320,75,480,80C640,85,800,75,960,69.3C1120,64,1280,75,1360,80L1440,85L1440,140L0,140Z"></path>
  </svg>
</div>
""",
    unsafe_allow_html=True,
)

# ===== NAVIGATION BAR =====
st.markdown(
    f"""
<style>
.navbar {{
  background-color:#F6F5F2;
  display:flex;
  justify-content:center;
  gap:40px;
  padding:18px 10px;
  margin:-10px -3rem 4px -3rem;
  font-size:1.07rem;
}}
.nav-item {{
  font-weight:600;
  color:{QDB_DARK_BLUE};
  cursor:pointer;
  border-bottom:2.5px solid transparent;
  transition:color 0.3s, border-color 0.3s;
}}
.nav-item:hover {{
  color:#319795;
  border-color:#319795;
}}
</style>
""",
    unsafe_allow_html=True,
)

# --- Nav Bar Buttons (native navigation instead of HTML) ---
nav_col1, nav_col2, nav_col3, nav_col4, nav_col5 = st.columns(5)

with nav_col1:
    if st.button("Deal Sourcing"):
        st.switch_page("pages/1_Deal_Sourcing.py")
with nav_col2:
    if st.button("Due Diligence"):
        st.switch_page("pages/2_Due_Diligence.py")
with nav_col3:
    if st.button("Market Analysis"):
        st.switch_page("pages/3_Market_Analysis.py")
with nav_col4:
    if st.button("Financial Modeling"):
        st.switch_page("pages/4_Financial_Modeling.py")
with nav_col5:
    if st.button("Investment Memo"):
        st.switch_page("pages/5_Investment_Memo.py")

# ===== CHOOSE PATH SECTION =====
qdb_section_start("light")
st.markdown(
    f"""
<div style="text-align:center; max-width:950px; margin:0 auto 35px auto;">
  <h2 style="color:{QDB_DARK_BLUE}; font-size:2rem; font-weight:700; margin-bottom:10px;">
    Choose Your Analysis Path
  </h2>
  <p style="color:#555; font-size:1.05rem;">Select your starting point to launch a guided AI workflow.</p>
</div>
""",
    unsafe_allow_html=True,
)

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown(
        """
        <div style="background:white; border-radius:16px; padding:35px;
                    box-shadow:0 5px 20px rgba(0,0,0,0.08);
                    border-top:4px solid #2C3E5E; height:420px;
                    display:flex; flex-direction:column; justify-content:space-between;">
            <div>
                <h3 style="color:#1B2B4D;font-size:1.6rem;margin-bottom:16px;">Deal Sourcing Path</h3>
                <p style="color:#333; line-height:1.7;">
                  Identify promising startups and investment opportunities powered by data‑driven search and scoring models.
                </p>
            </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Start Deal Sourcing", use_container_width=True):
        st.switch_page("pages/1_Deal_Sourcing.py")

    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown(
        """
        <div style="background:white; border-radius:16px; padding:35px;
                    box-shadow:0 5px 20px rgba(0,0,0,0.08);
                    border-top:4px solid #2C3E5E; height:420px;
                    display:flex; flex-direction:column; justify-content:space-between;">
            <div>
                <h3 style="color:#1B2B4D;font-size:1.6rem;margin-bottom:16px;">Due Diligence Path</h3>
                <p style="color:#333; line-height:1.7;">
                  Perform structured due‑diligence analysis with automated parsing of financials, operations, and compliance reports.
                </p>
            </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Start Due Diligence", use_container_width=True):
        st.switch_page("pages/2_Due_Diligence.py")

    st.markdown("</div>", unsafe_allow_html=True)

qdb_section_end()

# ===== FULL-WIDTH FOOTER (aligned & professional) =====
st.markdown(
    f"""
<div style="
    background-color:#1B2B4D;
    color:#E2E8F0;
    padding:35px 50px;
    margin:0 -3rem -2rem -3rem;
    width:calc(100% + 6rem);
    font-size:0.95rem;">
  <div style="max-width:100%; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap;">
    <div style="flex:3;">
      <ul style="list-style:none; display:flex; gap:30px; flex-wrap:wrap; padding:0; margin:0;">
        <li><a href='#' style='text-decoration:none; color:#E2E8F0;'>About Regulus</a></li>
        <li><a href='#' style='text-decoration:none; color:#E2E8F0;'>Careers</a></li>
        <li><a href='#' style='text-decoration:none; color:#E2E8F0;'>Contact Us</a></li>
        <li><a href='#' style='text-decoration:none; color:#E2E8F0;'>Privacy Policy</a></li>
        <li><a href='#' style='text-decoration:none; color:#E2E8F0;'>Terms & Conditions</a></li>
      </ul>
    </div>
    <div style="flex:1; text-align:right;">
      <div style="display:flex; align-items:center; justify-content:flex-end; gap:10px;">
        {"<p style='margin:0; color:#A0AEC0;'>Powered by Regulus AI</p><img src='"+regulus_logo+"' style='max-height:55px; opacity:0.95;'>" if regulus_logo else "<p>Powered by Regulus AI</p>"}
      </div>
    </div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)
