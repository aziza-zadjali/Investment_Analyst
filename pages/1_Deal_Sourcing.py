"""
Deal Discovery & Sourcing | Regulus AI × QDB
Unified QDB theme with blue hero and teal action buttons.
"""

import streamlit as st
import pandas as pd
from utils.web_scraper import WebScraper
from utils.llm_handler import LLMHandler
from utils.template_generator import TemplateGenerator
from utils.qdb_styling import (
    apply_qdb_styling,
    qdb_section_start,
    qdb_section_end,
    QDB_DARK_BLUE,
    QDB_NAVY,
)

# ==== PAGE CONFIG ====
st.set_page_config(page_title="Deal Sourcing – Regulus AI", layout="wide")
apply_qdb_styling()

# ==== INIT HANDLERS ====
@st.cache_resource
def _init():
    return WebScraper(), LLMHandler(), TemplateGenerator()
scraper, llm, template = _init()

# ==== HERO SECTION (BLUE LIKE MAIN PAGE) ====
st.markdown(
    f"""
<div style="
    background:linear-gradient(135deg,{QDB_DARK_BLUE} 0%,{QDB_NAVY} 100%);
    color:white;text-align:center;
    margin:0 -3rem;
    padding:110px 20px 100px 20px;
    position:relative;overflow:hidden;">
  <h1 style="font-size:2.5rem;font-weight:700;letter-spacing:-0.3px;margin-bottom:12px;">
     AI‑Powered Deal Discovery & Sourcing
  </h1>
  <p style="color:#E2E8F0;font-size:1.05rem;max-width:760px;margin:auto;">
     Identify qualified investment opportunities from global startup sources with Regulus AI‑driven analysis.
  </p>
</div>
""",
    unsafe_allow_html=True,
)

# ==== STEP TRACKER ====
st.markdown(
    """
<style>
.track{
 background:#F6F5F2;margin:-2px -3rem 0 -3rem;
 padding:34px 0;display:flex;justify-content:space-evenly;
 align-items:center;}
.step{text-align:center;font-family:'Segoe UI';}
.circle{
 width:54px;height:54px;border-radius:50%;
 display:flex;align-items:center;justify-content:center;
 background:#CBD5E0;color:#475569;font-weight:700;}
.circle.active{
 background:linear-gradient(135deg,#138074 0%,#0E5F55 100%);
 color:white;box-shadow:0 5px 15px rgba(19,128,116,0.4);}
.label{margin-top:6px;font-size:0.9rem;font-weight:600;color:#708090;}
.label.active{color:#138074;}
.pipe{height:3px;width:70px;background:#CBD5E0;}
</style>
<div class="track">
  <div class="step"><div class="circle active">1</div><div class="label active">Deal Sourcing</div></div>
  <div class="pipe"></div>
  <div class="step"><div class="circle">2</div><div class="label">Due Diligence</div></div>
  <div class="pipe"></div>
  <div class="step"><div class="circle">3</div><div class="label">Market Analysis</div></div>
  <div class="pipe"></div>
  <div class="step"><div class="circle">4</div><div class="label">Financial Modeling</div></div>
  <div class="pipe"></div>
  <div class="step"><div class="circle">5</div><div class="label">Investment Memo</div></div>
</div>
""",
    unsafe_allow_html=True,
)

# ==== FILTER SECTION ====
qdb_section_start("light")
st.markdown(
    """
<div style="text-align:center;margin-bottom:30px;">
  <h2 style="color:#1B2B4D;font-weight:700;margin-bottom:6px;">
    Daily Deal Discovery Dashboard
  </h2>
  <p style="color:#555;font-size:1.02rem;">
    Customize your search filters to source qualified startups that match QDB investment criteria.
  </p>
</div>
""",
    unsafe_allow_html=True,
)

with st.expander("🎯 Define Investment Criteria", expanded=True):
    c1, c2, c3 = st.columns(3)
    industries = c1.multiselect(
        "Industries",
        ["Technology", "Healthcare", "Finance", "Energy", "Retail", "Manufacturing"],
        ["Technology", "Healthcare"],
    )
    regions = c2.multiselect(
        "Regions",
        ["MENA", "Europe", "North America", "Asia Pacific"],
        ["MENA"],
    )
    stage = c3.selectbox(
        "Funding Stage",
        ["Pre‑Seed", "Seed", "Series A", "Series B", "Growth"],
        index=1,
    )
    c4, c5 = st.columns([2, 1])
    sectors = c4.multiselect(
        "Sectors",
        ["Fintech", "AI/ML", "ClimateTech", "HealthTech", "SaaS"],
        ["Fintech"],
    )
    deal_count = c5.slider("Deals per run", 5, 50, 15, 5)

sources = st.multiselect(
    "Active Data Sources",
    ["Crunchbase", "AngelList", "Magnitt", "Wamda", "PitchBook"],
    ["Crunchbase", "AngelList", "Magnitt"],
)
qdb_section_end()

# ==== CALL‑TO‑ACTION BUTTON (TEAL) ====
st.markdown("<br>", unsafe_allow_html=True)
colA, colB, colC = st.columns([1, 0.8, 1])
with colB:
    discover = st.button("🚀 Discover Live Deals", use_container_width=True)
st.markdown(
    """
<style>
div.stButton > button:first-child {
    background: linear-gradient(135deg, #16A085 0%, #138074 50%, #0E5F55 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 40px !important;
    padding: 14px 40px !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    letter-spacing: 0.3px !important;
    box-shadow: 0 5px 18px rgba(19,128,116,0.35) !important;
    transition: all 0.3s ease !important;
}
div.stButton > button:first-child:hover {
    background: linear-gradient(135deg, #0E5F55 0%, #138074 50%, #16A085 100%) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 22px rgba(19,128,116,0.45) !important;
}
</style>
""",
    unsafe_allow_html=True,
)

# ==== CORE FUNCTIONALITY ====
if discover:
    st.info("🔍 Fetching real‑time startup data …")
    results = []
    for src in sources:
        st.write(f"Scraping {src} …")
        results += scraper.search_startups(
            src, industries, sectors, [stage], regions, limit=int(deal_count / len(sources))
        )
    if not results:
        st.warning("No results found for the current criteria.")
    else:
        df = pd.DataFrame(results)
        st.success(f"✅ {len(df)} qualified deals retrieved.")
        st.dataframe(df, use_container_width=True)
        st.markdown("#### Regulus AI Summary")
        summary = llm.generate_text(
            f"Summarize {len(df)} deals covering {', '.join(industries)} in {', '.join(regions)}."
        )
        st.info(summary)

# ==== FOOTER ====
st.markdown(
    f"""
<div style="background:{QDB_DARK_BLUE};color:#E2E8F0;padding:26px 36px;margin:80px -3rem -2rem;
display:flex;justify-content:space-between;align-items:center;">
  <p style="margin:0;font-size:0.9rem;">© 2025 Regulus AI | All Rights Reserved</p>
  <p style="margin:0;color:#A0AEC0;font-size:0.9rem;">Powered by Regulus AI</p>
</div>
""",
    unsafe_allow_html=True,
)
