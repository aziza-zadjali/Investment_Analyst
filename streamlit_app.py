"""
Investment Analyst AI – Regulus Edition
Final Version: Clickable Buttons + Footer Branding
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

# Page config
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
  
  <!-- QDB Logo (Left Corner) -->
  <div style="position:absolute; top:25px; left:35px;">
    {"<img src='"+qdb_logo+"' style='max-height:70px;'>" if qdb_logo else "<b>QDB</b>"}
  </div>

  <!-- Central Hero Text -->
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
        Explore Analysis Workflows
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
  position:relative;
  font-weight:600;
  color:{QDB_DARK_BLUE};
  cursor:pointer;
  border-bottom:2.5px solid transparent;
  transition:color 0.3s, border-color 0.3s;
}}
.nav-item:hover {{color:#319795; border-color:#319795;}}
.card {{
  position:absolute; top:38px; left:50%;
  transform:translateX(-50%);
  width:320px; background:white;
  border-radius:12px; box-shadow:0 8px 32px rgba(0,0,0,0.1);
  opacity:0; visibility:hidden;
  transition:all 0.25s ease; z-index:10; pointer-events:none;
}}
.nav-item:hover .card {{opacity:1; visibility:visible; transform:translate(-50%,15px); pointer-events:auto;}}
.card a {{display:block; padding:17px; text-decoration:none; color:{QDB_DARK_BLUE};}}
.card a:hover {{background-color:#F0F9F8; border-radius:12px; color:#319795;}}
.card h4 {{margin:0; font-size:1.05rem;}}
.card p {{margin:6px 0 10px; font-size:0.9rem; color:#555; line-height:1.4;}}
</style>

<div class="navbar">
  <div class="nav-item">Deal Sourcing
    <div class="card">
      <a href="?page=deal">
        <h4>Deal Sourcing</h4>
        <p>Discover, qualify, and manage investment opportunities with AI‑based scoring.</p>
      </a>
    </div>
  </div>
  <div class="nav-item">Due Diligence
    <div class="card">
      <a href="?page=dd">
        <h4>Due Diligence</h4>
        <p>Perform automated financial, operational, and regulatory due diligence workflows.</p>
      </a>
    </div>
  </div>
  <div class="nav-item">Market Analysis
    <div class="card">
      <a href="?page=market">
        <h4>Market Analysis</h4>
        <p>Analyze market trends, competitors, and sector intelligence in minutes.</p>
      </a>
    </div>
  </div>
  <div class="nav-item">Financial Modeling
    <div class="card">
      <a href="?page=fin">
        <h4>Financial Modeling</h4>
        <p>Generate and validate financial models with automated Excel integration.</p>
      </a>
    </div>
  </div>
  <div class="nav-item">Investment Memo
    <div class="card">
      <a href="?page=memo">
        <h4>Investment Memo</h4>
        <p>Consolidate findings into a professional investor‑ready memorandum.</p>
      </a>
    </div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

# ===== CHOOSE PATH SECTION =====
st.markdown("<div id='choose-path'></div>", unsafe_allow_html=True)
qdb_section_start("light")
st.markdown(
    f"""
<div style="text-align:center; max-width:950px; margin:0 auto 35px auto;">
  <h2 style="color:{QDB_DARK_BLUE}; font-size:2rem; font-weight:700; margin-bottom:10px;">Choose Your Analysis Path</h2>
  <p style="color:#555; font-size:1.05rem;">Start your workflow below or navigate via top menu.</p>
</div>
""",
    unsafe_allow_html=True,
)

button_style = """
  background-color:#319795;
  color:white;
  border:none;
  border-radius:40px;
  padding:12px 30px;
  font-size:0.95rem;
  font-weight:600;
  box-shadow:0 3px 12px rgba(49,151,149,0.3);
  text-decoration:none;
  transition:all 0.25s;
"""
hover_in = "this.style.backgroundColor='#2C7A7B'"
hover_out = "this.style.backgroundColor='#319795'"

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown(
        f"""
        <div style="background:white; border-radius:16px; padding:35px; height:390px;
                    box-shadow:0 5px 20px rgba(0,0,0,0.08); border-top:4px solid #2C3E5E;
                    display:flex; flex-direction:column; justify-content:space-between;">
            <div>
                <h3 style="color:#1B2B4D; font-size:1.6rem; font-weight:600; margin-bottom:16px;">Deal Sourcing Path</h3>
                <ul style="margin-top:10px; line-height:1.9; color:#333;">
                    <li><a href='?page=deal' style='color:#1B2B4D; text-decoration:none;'>AI‑powered deal identification</a></li>
                    <li><a href='?page=market' style='color:#1B2B4D; text-decoration:none;'>Handoff to Market Analysis</a></li>
                    <li><a href='?page=dd' style='color:#1B2B4D; text-decoration:none;'>Proceed to Due Diligence</a></li>
                </ul>
            </div>
            <div style="margin-top:auto;text-align:center;">
                <a href="?page=deal" style="{button_style}" onmouseover="{hover_in}" onmouseout="{hover_out}">Start Deal Sourcing</a>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        f"""
        <div style="background:white; border-radius:16px; padding:35px; height:390px;
                    box-shadow:0 5px 20px rgba(0,0,0,0.08); border-top:4px solid #2C3E5E;
                    display:flex; flex-direction:column; justify-content:space-between;">
            <div>
                <h3 style="color:#1B2B4D; font-size:1.6rem; font-weight:600; margin-bottom:16px;">Due Diligence Path</h3>
                <ul style="margin-top:10px; line-height:1.9; color:#333;">
                    <li><a href='?page=dd' style='color:#1B2B4D; text-decoration:none;'>Upload & analyze company files</a></li>
                    <li><a href='?page=market' style='color:#1B2B4D; text-decoration:none;'>Access Market Comparables</a></li>
                    <li><a href='?page=memo' style='color:#1B2B4D; text-decoration:none;'>Generate Investment Memo</a></li>
                </ul>
            </div>
            <div style="margin-top:auto;text-align:center;">
                <a href="?page=dd" style="{button_style}" onmouseover="{hover_in}" onmouseout="{hover_out}">Start Due Diligence</a>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
qdb_section_end()

# ===== FOOTER (with Regulus branding) =====
st.markdown(
    f"""
<div style="background-color:#1B2B4D; color:#E2E8F0; padding:40px 20px; margin:0 -3rem -2rem -3rem; font-size:0.94rem;">
  <div style="max-width:1100px; margin:0 auto; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap;">
    <div style="flex:3;">
      <ul style="list-style:none; display:flex; gap:25px; flex-wrap:wrap; padding:0; margin:0; color:#E2E8F0;">
        <li><a href="#" style="text-decoration:none; color:#E2E8F0;">About Regulus</a></li>
        <li><a href="#" style="text-decoration:none; color:#E2E8F0;">Careers</a></li>
        <li><a href="#" style="text-decoration:none; color:#E2E8F0;">Contact Us</a></li>
        <li><a href="#" style="text-decoration:none; color:#E2E8F0;">Privacy Policy</a></li>
        <li><a href="#" style="text-decoration:none; color:#E2E8F0;">Terms & Conditions</a></li>
        <li><a href="#" style="text-decoration:none; color:#E2E8F0;">Security Tips</a></li>
      </ul>
    </div>
    <div style="flex:1; text-align:right;">
      <p style="margin:0; color:#A0AEC0; font-size:0.9rem;">Powered by Regulus AI</p>
      {"<img src='"+regulus_logo+"' style='max-height:55px; margin-top:6px; opacity:0.95;'>" if regulus_logo else "<b>Regulus</b>"}
      <p style="margin-top:8px; color:#A0AEC0;">© Regulus 2025</p>
    </div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)
