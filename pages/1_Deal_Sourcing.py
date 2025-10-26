"""
Deal Discovery & Sourcing | Regulus x QDB
Elegant teal workflow tracker | Filters with ticket size | Robust LLM handler
"""

import streamlit as st
import pandas as pd
import os, base64
from datetime import datetime
from utils.qdb_styling import apply_qdb_styling, qdb_section_start, qdb_section_end, QDB_DARK_BLUE
from utils.llm_handler import LLMHandler

# ---------- PAGE CONFIGURATION ----------
st.set_page_config(page_title="Deal Sourcing — Regulus AI", layout="wide", initial_sidebar_state="collapsed")
apply_qdb_styling()

# ---------- UTILITY ----------
def encode_image(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return "data:image/png;base64," + base64.b64encode(f.read()).decode()
    return None

qdb_logo = encode_image("QDB_Logo.png")

# ========== HERO ==========
st.markdown(
    f"""
<div style="background:linear-gradient(135deg,#1B2B4D 0%,#2C3E5E 100%);
    color:white;text-align:center;margin:0 -3rem;
    padding:75px 20px 70px;position:relative;">
  <div style="position:absolute;top:25px;left:35px;">
    {"<img src='"+qdb_logo+"' style='max-height:65px;'/>" if qdb_logo else "<b>QDB</b>"}
  </div>
  <h1 style="font-size:2.2rem;font-weight:700;">Deal Discovery & Sourcing</h1>
  <p style="color:#CBD5E0;font-size:1rem;max-width:720px;margin:10px auto;">
    Identify and qualify high‑potential investment opportunities with AI automation and Regulus LLM intelligence.
  </p>
</div>
""",
    unsafe_allow_html=True,
)

# ========== WORKFLOW BAR (matches screenshot UI) ==========
st.markdown(
    """
<style>
.workflow{
  background:#F6F5F2;margin:0 -3rem;
  padding:22px 60px;display:flex;
  justify-content:space-between;align-items:center;
  flex-wrap:wrap;
}
.stage{display:flex;flex-direction:column;align-items:center;font-weight:600;text-align:center;}
.circle{
  width:46px;height:46px;border-radius:50%;
  display:flex;align-items:center;justify-content:center;
  font-size:1.1rem;font-weight:700;margin-bottom:5px;
}
.active{background-color:#138074;color:#fff;box-shadow:0px 3px 12px rgba(19,128,116,0.35);}
.inactive{background-color:#CBD5E0;color:#475569;}
.label{font-size:0.85rem;font-weight:600;}
.label.active{color:#138074;}
.label.inactive{color:#A0AEC0;}
.line{flex-grow:1;height:2px;background-color:#CBD5E0;margin:0 5px;}
</style>

<div class="workflow">
  <div class="stage"><div class="circle active">1</div><div class="label active">Deal Sourcing</div></div>
  <div class="line"></div>
  <div class="stage"><div class="circle inactive">2</div><div class="label inactive">Due Diligence</div></div>
  <div class="line"></div>
  <div class="stage"><div class="circle inactive">3</div><div class="label inactive">Market Analysis</div></div>
  <div class="line"></div>
  <div class="stage"><div class="circle inactive">4</div><div class="label inactive">Financial Modeling</div></div>
  <div class="line"></div>
  <div class="stage"><div class="circle inactive">5</div><div class="label inactive">Investment Memo</div></div>
</div>
""",
    unsafe_allow_html=True,
)

# ========== FILTERS SECTION ==========
qdb_section_start("light")

st.markdown(
    f"""
<div style='text-align:center;max-width:950px;margin:auto;'>
  <h2 style='color:{QDB_DARK_BLUE};font-weight:700;font-size:1.8rem;margin-bottom:6px;'>Intelligent Deal Discovery</h2>
  <p style='color:#555;font-size:1.05rem;'>
     Adjust filters to instantly detect aligned deals from trusted databases and market feeds.
  </p>
</div>
""",
    unsafe_allow_html=True,
)

with st.form("filters", clear_on_submit=False):
    c1, c2, c3 = st.columns(3)
    with c1:
        industries = st.multiselect(
            "Target Industries",
            ["Technology", "Healthcare", "Finance", "Energy", "Manufacturing", "Agritech"],
            default=["Technology"],
        )
    with c2:
        regions = st.multiselect(
            "Regions",
            ["MENA", "Europe", "North America", "Asia Pacific"],
            default=["MENA"],
        )
    with c3:
        stage = st.selectbox("Funding Stage", ["Pre‑Seed", "Seed", "Series A", "Series B", "Growth"])
    c4, c5 = st.columns([2, 1])
    with c4:
        keywords = st.text_input("Keywords (Optional)", "AI | Fintech | Sustainability")
    with c5:
        ticket = st.number_input("Ticket Size (USD M)", min_value=0.5, max_value=100.0, value=5.0, step=0.5)
    submitted = st.form_submit_button("🔍 Discover Deals")

qdb_section_end()

# ========== STYLE FOR BUTTON ==========
st.markdown(
    """
<style>
div.stButton>button:first-child{
  background:linear-gradient(135deg,#138074,#0e5f55)!important;
  color:#fff!important;border:none!important;border-radius:40px!important;
  padding:12px 30px!important;font-weight:700!important;font-size:0.95rem!important;
  box-shadow:0 4px 12px rgba(19,128,116,0.25)!important;transition:0.2s ease-in!important;}
div.stButton>button:first-child:hover{
  transform:translateY(-2px)!important;box-shadow:0 6px 16px rgba(19,128,116,0.35)!important;}
</style>
""",
    unsafe_allow_html=True,
)

# ========== ACTION ==========
if submitted:
    qdb_section_start("white")
    st.subheader("AI‑Generated Insights and Recommendations 📊")

    with st.spinner("Analyzing deal flow and market signals … please wait a moment."):
        try:
            llm = LLMHandler()
            query = (
                f"Generate a curated list of investment opportunities in industries {', '.join(industries)} "
                f"for {stage} stage startups in regions {', '.join(regions)}. "
                f"Recommended ticket size ≈ ${ticket} M. "
                f"Keywords: {keywords}. Provide summaries with metrics and contacts."
            )
            response = llm.generate_text(query)
            if not response or response.strip() == "":
                st.warning("⚠️ No results returned from AI sourcing engine.")
            else:
                st.markdown(response, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"🔧 There was an issue processing your query: **{str(e)}**")
    qdb_section_end()

# ========== NAVIGATION TO NEXT STAGE ==========
st.markdown(
    f"""
<div style="background-color:#F6F5F2;padding:60px 20px;margin:60px -3rem -2rem;text-align:center;">
  <h3 style="color:{QDB_DARK_BLUE};font-size:1.6rem;margin-bottom:10px;">Workflow Next Step</h3>
  <p style="color:#555;margin-bottom:25px;">
    Proceed to Due Diligence to assess company fundamentals and compliance risks.
  </p>
  <a href="?page=dd" style="
      background-color:#319795;color:white;text-decoration:none;
      border-radius:40px;padding:12px 35px;font-weight:600;
      box-shadow:0 3px 10px rgba(49,151,149,0.3);">
      → Continue to Due Diligence
  </a>
</div>
""",
    unsafe_allow_html=True,
)
