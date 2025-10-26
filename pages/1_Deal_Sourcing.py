"""
Deal Discovery & Sourcing | Regulus x QDB
Enhanced version – Consistent UI, modern workflow visuals, and smooth UX
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import os, base64

from utils.qdb_styling import apply_qdb_styling, QDB_DARK_BLUE, qdb_section_start, qdb_section_end
from utils.llm_handler import LLMHandler

# -------------- PAGE SETUP --------------
st.set_page_config(page_title="Deal Discovery & Sourcing", layout="wide", initial_sidebar_state="collapsed")
apply_qdb_styling()

# -------------- IMAGE ENCODER --------------
def encode_image(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f"data:image/png;base64," + base64.b64encode(f.read()).decode()
    return None

qdb_logo = encode_image("QDB_Logo.png")

# -------------- HERO SECTION --------------
st.markdown(
    f"""
<div style="background:linear-gradient(135deg,#1B2B4D 0%,#2C3E5E 100%);
    color:white;text-align:center;margin:0 -3rem;padding:70px 20px 65px 20px;position:relative;">
  <div style="position:absolute;top:25px;left:35px;">
    {"<img src='"+qdb_logo+"' style='max-height:70px;'>" if qdb_logo else "<b>QDB</b>"}
  </div>
  <h1 style="font-size:2.2rem;font-weight:700;">Deal Discovery & Sourcing</h1>
  <p style="color:#CBD5E0;font-size:1rem;">AI‑powered investment opportunity identification and qualification platform.</p>
</div>
""",
    unsafe_allow_html=True,
)

# -------------- STEP TRACKER --------------
st.markdown(
    """
<style>
.step-container{background-color:#F6F5F2;margin:0 -3rem;padding:20px 40px;display:flex;
                justify-content:center;align-items:center;gap:50px;flex-wrap:wrap;}
.step{display:flex;flex-direction:column;align-items:center;gap:6px;}
.circle{width:40px;height:40px;border-radius:50%;display:flex;justify-content:center;
        align-items:center;font-weight:700;}
.active{background-color:#138074;color:#fff;box-shadow:0 3px 8px rgba(19,128,116,0.3);}
.inactive{background-color:#CBD5E0;color:#2D3748;}
.label{font-size:0.8rem;font-weight:600;margin-top:5px;}
.label.active{color:#138074;}
.label.inactive{color:#A0AEC0;}
.connector{width:60px;height:2px;background-color:#CBD5E0;}
</style>

<div class="step-container">
  <div class="step"><div class="circle active">1</div><div class="label active">Deal Sourcing</div></div>
  <div class="connector"></div>
  <div class="step"><div class="circle inactive">2</div><div class="label inactive">Due Diligence</div></div>
  <div class="connector"></div>
  <div class="step"><div class="circle inactive">3</div><div class="label inactive">Market Analysis</div></div>
  <div class="connector"></div>
  <div class="step"><div class="circle inactive">4</div><div class="label inactive">Financial Modeling</div></div>
  <div class="connector"></div>
  <div class="step"><div class="circle inactive">5</div><div class="label inactive">Investment Memo</div></div>
</div>
""",
    unsafe_allow_html=True,
)

# -------------- FILTERS FORM --------------
qdb_section_start("light")

st.markdown(
    f"""
<div style='text-align:center;max-width:950px;margin:0 auto 35px;'>
  <h2 style='color:{QDB_DARK_BLUE};font-weight:700;font-size:1.8rem;margin-bottom:6px;'>Intelligent Deal Discovery</h2>
  <p style='color:#555;font-size:1.05rem;'>Customize your search filters to identify high‑potential deals across preferred industries and regions.</p>
</div>
""",
    unsafe_allow_html=True,
)

with st.container():
    with st.expander("🎯 Define Investment Criteria", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            industries = st.multiselect(
                "Industries", ["Technology", "Healthcare", "Energy", "Finance", "Manufacturing"],
                default=["Technology"]
            )
        with col2:
            geography = st.multiselect(
                "Regions", ["MENA", "Europe", "North America", "Asia Pacific"], default=["MENA"]
            )
        with col3:
            stage = st.selectbox("Funding Stage", ["Seed", "Series A", "Series B", "Growth"])

        keywords = st.text_input("Keywords or Themes (Optional)", placeholder="AI, Fintech, SaaS Growth, Sustainability…")
        deal_count = st.slider("Number of Deals to Fetch", 5, 50, 10, 5)

# -------------- ACTION BUTTON --------------
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(
    """
<style>
div.stButton>button:first-child{
  background:linear-gradient(135deg,#138074,#0e5f55)!important;
  color:#fff!important;border:none!important;
  border-radius:40px!important;padding:12px 30px!important;
  font-weight:700!important;font-size:0.95rem!important;
  box-shadow:0 4px 12px rgba(19,128,116,0.25)!important;transition:0.2s ease-in!important;}
div.stButton>button:first-child:hover{
  transform:translateY(-2px)!important;
  box-shadow:0 6px 14px rgba(19,128,116,0.35)!important;}
</style>
""",
    unsafe_allow_html=True,
)
center = st.columns([1, 0.8, 1])[1]
with center:
    discover = st.button("Discover Deals 🚀", use_container_width=True)

# -------------- RESULT PLACEHOLDER --------------
if discover:
    handler = LLMHandler()
    with st.spinner("Analyzing deal flow and market feeds..."):
        results = handler.generate_text(
            f"Provide 10 example investment opportunities in {', '.join(industries)} for {stage} startups in {', '.join(geography)}. Focus on themes: {keywords}"
        )

    st.success("✅ Top matching investment opportunities identified.")
    st.markdown("<br>", unsafe_allow_html=True)

    st.subheader("Recommended Deals 📊")
    st.markdown(results if results else "_No deal results returned._")

qdb_section_end()

# -------------- FOOTER --------------
st.markdown(
    """
<div style="background-color:#1B2B4D;color:#E2E8F0;padding:35px 40px;margin:60px -3rem -2rem -3rem;font-size:0.94rem;">
  <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;">
    <div style="flex:3;">
      <ul style="list-style:none;display:flex;gap:25px;flex-wrap:wrap;padding:0;margin:0;">
        <li><a href='#' style='text-decoration:none;color:#E2E8F0;'>About Regulus</a></li>
        <li><a href='#' style='text-decoration:none;color:#E2E8F0;'>Careers</a></li>
        <li><a href='#' style='text-decoration:none;color:#E2E8F0;'>Contact Us</a></li>
        <li><a href='#' style='text-decoration:none;color:#E2E8F0;'>Privacy Policy</a></li>
        <li><a href='#' style='text-decoration:none;color:#E2E8F0;'>Terms & Conditions</a></li>
      </ul>
    </div>
    <div style="flex:1;text-align:right;">
      <div style="display:flex;align-items:center;justify-content:flex-end;gap:10px;">
        <p style="margin:0;color:#A0AEC0;font-size:0.9rem;">Powered by Regulus AI</p>
        <img src="regulus_logo.png" style="max-height:50px;opacity:0.95;" />
      </div>
    </div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)
