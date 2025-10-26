"""
Deal Discovery & Sourcing | Regulus x QDB
Enhanced QDB‑branded interface with teal workflow visuals, filters, and AI integration
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import base64, os
from utils.llm_handler import LLMHandler
from utils.qdb_styling import apply_qdb_styling, qdb_section_start, qdb_section_end, QDB_DARK_BLUE

# ---------- PAGE SETUP ----------
st.set_page_config(page_title="Deal Sourcing | Regulus", layout="wide", initial_sidebar_state="collapsed")
apply_qdb_styling()

# ---------- IMAGE HELPER ----------
def encode_image(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return "data:image/png;base64," + base64.b64encode(f.read()).decode()
    return None

qdb_logo = encode_image("QDB_Logo.png")

# ---------- HERO SECTION ----------
st.markdown(
    f"""
<div style="background:linear-gradient(135deg,#1B2B4D 0%,#2C3E5E 100%);
  color:white;text-align:center;margin:0 -3rem;padding:75px 20px 70px;position:relative;">
  <div style="position:absolute;top:25px;left:35px;">
    {"<img src='" + qdb_logo + "' style='max-height:70px;'/>" if qdb_logo else "<b>QDB</b>"}
  </div>
  <h1 style="font-size:2.3rem;font-weight:700;">Deal Discovery & Sourcing</h1>
  <p style="color:#CBD5E0;font-size:1rem;max-width:710px;margin:10px auto 0;">
    AI‑powered investment pipeline discovery designed for institutional efficiency.
  </p>
</div>
""",
    unsafe_allow_html=True,
)

# ---------- STEP BAR ----------
st.markdown(
    """
<style>
.progress-bar{
  background-color:#F6F5F2;
  margin:0 -3rem;
  padding:20px 50px;
  display:flex;
  justify-content:center;
  align-items:center;
  gap:55px;
  flex-wrap:wrap;
}
.step{
  text-align:center;
  font-weight:600;
}
.circle{
  width:40px;height:40px;border-radius:50%;
  display:flex;align-items:center;justify-content:center;
  font-weight:700;
}
.active{background-color:#138074;color:white;box-shadow:0 3px 10px rgba(19,128,116,0.4);}
.inactive{background-color:#CBD5E0;color:#2D3748;}
.label{font-size:0.8rem;margin-top:5px;}
.label.active{color:#138074;}
.label.inactive{color:#A0AEC0;}
.line{width:60px;height:2px;background-color:#CBD5E0;}
</style>

<div class="progress-bar">
  <div class="step"><div class="circle active">1</div><div class="label active">Deal Sourcing</div></div>
  <div class="line"></div>
  <div class="step"><div class="circle inactive">2</div><div class="label inactive">Due Diligence</div></div>
  <div class="line"></div>
  <div class="step"><div class="circle inactive">3</div><div class="label inactive">Market Analysis</div></div>
  <div class="line"></div>
  <div class="step"><div class="circle inactive">4</div><div class="label inactive">Financial Modeling</div></div>
  <div class="line"></div>
  <div class="step"><div class="circle inactive">5</div><div class="label inactive">Investment Memo</div></div>
</div>
""",
    unsafe_allow_html=True,
)

# ---------- FILTERS SECTION ----------
qdb_section_start("light")

st.markdown(
    f"""
<div style="text-align:center;max-width:950px;margin:0 auto 30px;">
  <h2 style="color:{QDB_DARK_BLUE};font-weight:700;font-size:1.8rem;">Intelligent Deal Discovery</h2>
  <p style="color:#555;font-size:1.05rem;">Use filters to define investment scope and sourcing parameters.</p>
</div>
""",
    unsafe_allow_html=True,
)

with st.form("filter_form", clear_on_submit=False):
    c1, c2, c3 = st.columns(3)
    with c1:
        industries = st.multiselect(
            "Target Industries",
            ["Technology", "Healthcare", "Energy", "Finance", "Manufacturing", "Agritech"],
            ["Technology", "Finance"],
        )
    with c2:
        regions = st.multiselect(
            "Regions",
            ["MENA", "Europe", "North America", "Asia Pacific"],
            ["MENA"],
        )
    with c3:
        stage = st.selectbox("Funding Stage", ["Seed", "Series A", "Series B", "Growth", "Pre‑IPO"])
    c4, c5 = st.columns([2.5, 1])
    with c4:
        keywords = st.text_input("Keywords (optional)", "AI, Fintech, Sustainability")
    with c5:
        ticket = st.number_input("Ticket Size (USD Million)", min_value=0.5, max_value=50.0, value=5.0, step=0.5)
    submitted = st.form_submit_button("🔍 Discover Deals")

qdb_section_end()

# ---------- HANDLE SEARCH ----------
if submitted:
    st.markdown("<br>", unsafe_allow_html=True)
    with st.spinner("Gathering and analyzing live deal data …"):
        llm = LLMHandler()
        query = (
            f"Find {len(industries)*5 if industries else 10} potential high-quality startup deals "
            f"in industries {', '.join(industries)} in {', '.join(regions)} region "
            f"at {stage} stage, ticket size ≈ ${ticket} M, keywords: {keywords}. "
            "Return summarized investment highlights, growth metrics, and contact placeholders."
        )
        response = llm.generate_text(query) or "No results returned from sourcing engine."
    st.success("✅ Successfully retrieved potential opportunities.")
    qdb_section_start("white")
    st.subheader("Recommended Deals 📊")
    st.markdown(response)
    qdb_section_end()

# ---------- NEXT STEP ----------
st.markdown(
    f"""
<div style="background-color:#F6F5F2;padding:60px 20px;margin:60px -3rem -2rem;text-align:center;">
  <h3 style="color:{QDB_DARK_BLUE};font-size:1.6rem;margin-bottom:10px;">
    Workflow Next Step
  </h3>
  <p style="color:#555;margin-bottom:30px;">
    Proceed to Due Diligence to analyze company fundamentals and operational risk metrics.
  </p>
  <a href="?page=dd" style="
      background-color:#319795;color:white;text-decoration:none;
      border-radius:40px;padding:12px 35px;font-weight:600;
      box-shadow:0 3px 10px rgba(49,151,149,0.3);">→ Continue to Due Diligence</a>
</div>
""",
    unsafe_allow_html=True,
)
