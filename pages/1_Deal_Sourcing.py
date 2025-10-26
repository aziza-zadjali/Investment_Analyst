"""
Deal Discovery & Sourcing – Regulus | QDB Branded
Aligned with main-page colors, layout, typography, and step visualization
"""

import streamlit as st
from datetime import datetime
from utils.llm_handler import LLMHandler
from utils.qdb_styling import apply_qdb_styling, qdb_section_start, qdb_section_end, QDB_DARK_BLUE

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Deal Sourcing | Regulus", layout="wide", initial_sidebar_state="collapsed")
apply_qdb_styling()

# --- TITLE & SUBHEADER ---
st.markdown(
    f"""
<div style="background: linear-gradient(135deg, #1B2B4D 0%, #2C3E5E 100%);
            color:white; text-align:center; margin:0 -3rem; padding:90px 20px 80px;">
  <h1 style="font-size:2.2rem; font-weight:700; margin-bottom:6px;">
    Deal Discovery & Sourcing
  </h1>
  <p style="font-size:1.05rem; color:#E2E8F0;">
    AI-enabled deal sourcing and qualification engine powered by Regulus AI | Qatar Development Bank (QDB)
  </p>
</div>

<svg viewBox="0 0 1440 100" xmlns="http://www.w3.org/2000/svg" style="position:relative; top:-1px; width:100%;">
  <path fill="#F6F5F2" d="M0,32L80,42.7C160,53,320,75,480,80C640,85,800,75,960,69.3C1120,64,1280,75,1360,80L1440,85L1440,100L0,100Z"></path>
</svg>
""",
    unsafe_allow_html=True,
)

# ====== STEP VISUAL ======
st.markdown(
    """
<div style="display:flex; justify-content:center; align-items:center; gap:40px;
            margin:30px 0 50px 0;">
  <div style="text-align:center;">
    <div style="background-color:#319795; color:white; border-radius:50%; width:40px; height:40px;
                display:flex; align-items:center; justify-content:center; margin:0 auto;">
      1
    </div>
    <p style="margin-top:10px; font-weight:600;">Search Deals</p>
  </div>
  <div style="height:2px; background-color:#A0AEC0; width:80px;"></div>
  <div style="text-align:center;">
    <div style="background-color:#CBD5E0; color:#2D3748; border-radius:50%; width:40px; height:40px;
                display:flex; align-items:center; justify-content:center; margin:0 auto;">
      2
    </div>
    <p style="margin-top:10px;">Analyze Opportunities</p>
  </div>
  <div style="height:2px; background-color:#A0AEC0; width:80px;"></div>
  <div style="text-align:center;">
    <div style="background-color:#CBD5E0; color:#2D3748; border-radius:50%; width:40px; height:40px;
                display:flex; align-items:center; justify-content:center; margin:0 auto;">
      3
    </div>
    <p style="margin-top:10px;">Export Leads</p>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

# ====== MAIN CONTENT ======
qdb_section_start("light")

st.markdown(
    f"""
<div style="text-align:center; max-width:1000px; margin:0 auto 40px;">
  <h2 style="color:{QDB_DARK_BLUE}; font-size:1.8rem; font-weight:700; margin-bottom:8px;">
    Intelligent Deal Discovery
  </h2>
  <p style="color:#555; font-size:1.05rem;">Upload your criteria or keywords and let Regulus AI identify top matching investment opportunities across global sources.</p>
</div>
""",
    unsafe_allow_html=True,
)

# ====== INPUT SECTION ======
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Define Search Parameters ↓")
    with st.form("deal_search_form"):
        industry = st.text_input("Target Industry (Manufacturing, Fintech, Healthcare…)", "")
        geography = st.text_input("Geography (Region / Country)", "")
        stage = st.selectbox("Funding Stage", ["Seed", "Series A", "Series B", "Growth Stage", "Pre‑IPO"])
        keywords = st.text_area("Optional Keywords", "AI, Cleantech, SaaS Scaleups…")
        submitted = st.form_submit_button("Run Intelligent Deal Search 🚀")

    if submitted:
        with st.spinner("Analyzing deal flow and intelligence feeds via Regulus LLM agents …"):
            handler = LLMHandler()
            response = handler.generate_text(
                f"Find investment opportunities for industry {industry}, stage {stage}, region {geography}, keywords: {keywords}"
            )
        qdb_section_end()
        qdb_section_start("white")
        st.subheader("Recommended Deals 📊")
        st.markdown(response)
        st.markdown("---")

with col2:
    st.markdown("<br/>", unsafe_allow_html=True)
    st.image("QDB_Logo.png", width=80)
    st.image("regulus_logo.png", width=80)
    st.info(
        "Regulus Deal Sourcing Agent leverages LLM‑driven market data and APIs to identify relevant companies, startups and SME growth targets."
    )

qdb_section_end()

# ====== NEXT STEP SECTION ======
st.markdown(
    f"""
<div style="background-color:#F6F5F2; padding:60px 20px; margin:0 -3rem;">
  <h3 style="text-align:center; color:{QDB_DARK_BLUE}; font-size:1.6rem; margin-bottom:15px;">
    Workflow Next Steps
  </h3>
  <p style="text-align:center; color:#555; margin-bottom:35px;">
    Proceed to the next analysis phase using your curated deal dataset.
  </p>
  <div style="display:flex; justify-content:center; flex-wrap:wrap; gap:30px;">
    <a href="?page=dd" style="
        background-color:#319795; color:white; border:none;
        border-radius:40px; padding:12px 35px; text-decoration:none;
        font-weight:600; box-shadow:0 3px 12px rgba(49,151,149,0.3);">
        → Continue to Due Diligence
    </a>
  </div>
</div>
""",
    unsafe_allow_html=True,
)
