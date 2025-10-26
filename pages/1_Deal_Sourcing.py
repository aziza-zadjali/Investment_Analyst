"""
Deal Discovery & Sourcing | Regulus AI × QDB
Teal on light sections | Grey‑blue on dark header (section aware buttons)
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

# ============ PAGE CONFIG ============
st.set_page_config(page_title="Deal Sourcing – Regulus AI", layout="wide")
apply_qdb_styling()

@st.cache_resource
def init():
    return WebScraper(), LLMHandler(), TemplateGenerator()
scraper, llm, templater = init()

# ============ DARK BLUE HEADER ============
st.markdown(
    f"""
<div class="qdb-section-dark" style="
background:linear-gradient(135deg,{QDB_DARK_BLUE} 0%,{QDB_NAVY} 100%);
text-align:center;margin:0 -3rem;padding:100px 20px 70px;position:relative;">
  <h1 style="font-family:'Segoe UI',sans-serif;font-weight:700;font-size:2.6rem;margin-bottom:10px;">
      AI‑Powered Deal Discovery & Sourcing
  </h1>
  <p style="color:#E2E8F0;font-size:1.05rem;">
      Discover and qualify startup investment opportunities using Regulus AI sourcing engine.
  </p>
  <svg viewBox="0 0 1440 120" xmlns="http://www.w3.org/2000/svg"
       style="position:absolute;bottom:-1px;left:0;width:100%;">
       <path fill="#F6F5F2"
        d="M0,32L80,42.7C160,53,320,75,480,80C640,85,800,75,960,69.3C1120,64,1280,75,1360,80L1440,85L1440,120L0,120Z"></path>
  </svg>
</div>
""",
    unsafe_allow_html=True,
)

# ============ LIGHT BG SECTION ============
qdb_section_start("light")

st.markdown(
    """
<div style="text-align:center;margin-bottom:35px;">
<h2 style="color:#1B2B4D;font-weight:700;">Daily Deal Discovery Dashboard</h2>
<p style="color:#555;font-size:1.02rem;">
Use the filters below to source verified startups from QDB aligned sectors and ticket sizes.
</p>
</div>
""",
    unsafe_allow_html=True,
)

with st.expander("🎯 Define Investment Criteria", expanded=True):
    col1, col2, col3 = st.columns(3)
    industries = col1.multiselect(
        "Industries",
        ["Technology", "Healthcare", "Finance", "Energy", "Retail", "Manufacturing"],
        ["Technology", "Healthcare"],
    )
    regions = col2.multiselect(
        "Regions",
        ["MENA", "Europe", "North America", "Asia Pacific"],
        ["MENA"],
    )
    stage = col3.selectbox(
        "Funding Stage", ["Pre‑Seed", "Seed", "Series A", "Series B", "Growth"], index=1
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

# ============ BUTTON STYLES (dynamic by section type) ============
st.markdown(
    """
<style>
/* --- teal for light   --- */
.light-btn button{
 background:linear-gradient(135deg,#138074 0%,#107563 100%)!important;
 color:white!important;font-weight:700!important;
 border:none!important;border-radius:38px!important;
 padding:13px 34px!important;font-size:0.96rem!important;
 box-shadow:0 4px 14px rgba(19,128,116,0.35)!important;
 transition:all 0.25s ease;}
.light-btn button:hover{
 background:linear-gradient(135deg,#107563 0%,#0E5F55 100%)!important;
 transform:translateY(-2px)!important;
 box-shadow:0 6px 18px rgba(19,128,116,0.45)!important;}
/* --- grey-blue buttons for dark backgrounds --- */
.dark-btn button{
 background:linear-gradient(135deg,#94A3B8 0%,#64748B 100%)!important;
 color:#F0F5FF!important;font-weight:700!important;
 border:none!important;border-radius:38px!important;
 padding:13px 34px!important;font-size:0.96rem!important;
 box-shadow:0 4px 14px rgba(100,116,139,0.35)!important;
 transition:all 0.25s ease;}
.dark-btn button:hover{
 background:linear-gradient(135deg,#64748B 0%,#475569 100%)!important;
 transform:translateY(-2px)!important;
 box-shadow:0 6px 18px rgba(71,85,105,0.45)!important;}
</style>
""",
    unsafe_allow_html=True,
)

# ============ CTA BUTTONS ============
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 0.8, 1])
with col2:
    discover = st.button("🚀 Discover Live Deals", key="discover", use_container_width=True)
st.markdown(
    """
<script>
let btn=document.querySelector('button[key="discover"]');
if(btn){
 btn.parentElement.classList.add('light-btn');
}
</script>
""",
    unsafe_allow_html=True,
)

# ============ EXECUTION ============
if discover:
    st.info("🔍 Retrieving real‑time startup data…")
    results = []
    for src in sources:
        st.write(f"Scraping {src} …")
        results += scraper.search_startups(
            src, industries, sectors, [stage], regions, limit=int(deal_count / len(sources))
        )

    if not results:
        st.warning("No deals found for selected filters.")
    else:
        df = pd.DataFrame(results)
        st.success(f"✅ {len(df)} qualified deals sourced successfully.")
        st.dataframe(df, use_container_width=True)
        st.markdown("#### Regulus AI Summary")
        summary = llm.generate_text(
            f"Summarize {len(df)} startup deals for {', '.join(industries)} sectors in {', '.join(regions)}."
        )
        st.info(summary)

# ============ FOOTER ============
st.markdown(
    f"""
<div style="background:{QDB_DARK_BLUE};color:#E2E8F0;padding:28px 36px;margin:80px -3rem -2rem;
display:flex;justify-content:space-between;align-items:center;">
  <p style="margin:0;font-size:0.9rem;">© 2025 Regulus AI | All Rights Reserved</p>
  <p style="margin:0;color:#A0AEC0;font-size:0.9rem;">Powered by Regulus AI</p>
</div>
""",
    unsafe_allow_html=True,
)
