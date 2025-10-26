"""
Deal Discovery & Sourcing | Regulus × QDB
AI‑Powered Real‑Time Startup Sourcing from Accelerator and Funding Platforms
"""

import streamlit as st
import pandas as pd
from utils.web_scraper import WebScraper
from utils.llm_handler import LLMHandler
from utils.template_generator import TemplateGenerator
from utils.qdb_styling import apply_qdb_styling
from datetime import datetime
import base64, os

# ============ PAGE CONFIG ============
st.set_page_config(page_title="Deal Sourcing – Regulus AI", layout="wide")
apply_qdb_styling()

# ============ HEADER ============
st.markdown(
    """
<div style="background:linear-gradient(135deg,#1B2B4D 0%,#2C3E5E 100%);
color:white;text-align:center;margin:0 -3rem;padding:80px 20px 70px;position:relative;">
  <h1 style="font-weight:700;font-size:2.3rem;">AI‑Powered Deal Discovery & Sourcing</h1>
  <p style="color:#CBD5E0;font-size:1rem;max-width:750px;margin:auto;">
    Identify qualified investment opportunities from global startup platforms with Regulus AI‑driven insights.
  </p>
</div>

<!-- Curved SVG Section Separator -->
<svg style="display:block;margin:0 -3rem;" viewBox="0 0 1440 150" xmlns="http://www.w3.org/2000/svg">
  <path fill="#F6F5F2" d="M0,160L60,149.3C120,139,240,117,360,117.3C480,117,600,139,720,144C840,149,960,139,1080,128C1200,117,1320,107,1380,101.3L1440,96L1440,0L1380,0C1320,0,1200,0,1080,0C960,0,840,0,720,0C600,0,480,0,360,0C240,0,120,0,60,0L0,0Z"></path>
</svg>
""",
    unsafe_allow_html=True,
)

# ============ STEP TRACKER ============
st.markdown(
    """
<style>
.track{background:#F6F5F2;margin:-2px -3rem 0 -3rem;padding:32px 40px;
display:flex;justify-content:center;align-items:center;flex-wrap:wrap;gap:1rem;}
.step{display:flex;flex-direction:column;align-items:center;}
.circle{
  width:48px;height:48px;border-radius:50%;
  display:flex;align-items:center;justify-content:center;
  font-weight:700;background:#D1D5DB;color:#475569;transition:all 0.3s ease;
}
.circle.active{background:linear-gradient(135deg,#138074 0%,#0E5F55 100%);color:white;
box-shadow:0 3px 12px rgba(19,128,116,0.35);transform:scale(1.05);}
.label{font-size:0.85rem;font-weight:600;color:#94A3B8;margin-top:6px;}
.label.active{color:#138074;}
.connector{width:60px;height:2px;background:#CBD5E0;margin:0 12px;}
</style>

<div class="track">
  <div class="step"><div class="circle active">1</div><div class="label active">Deal Sourcing</div></div>
  <div class="connector"></div>
  <div class="step"><div class="circle">2</div><div class="label">Due Diligence</div></div>
  <div class="connector"></div>
  <div class="step"><div class="circle">3</div><div class="label">Market Analysis</div></div>
  <div class="connector"></div>
  <div class="step"><div class="circle">4</div><div class="label">Financial Modeling</div></div>
  <div class="connector"></div>
  <div class="step"><div class="circle">5</div><div class="label">Investment Memo</div></div>
</div>
""",
    unsafe_allow_html=True,
)

# ============ INITIALIZATION ============
@st.cache_resource
def init_handlers():
    return WebScraper(), LLMHandler(), TemplateGenerator()

scraper, llm, template = init_handlers()

# ============ INVESTMENT FILTERS ============
with st.expander("🎯 Define Investment Criteria", expanded=True):
    c1,c2,c3=st.columns(3)
    industries=c1.multiselect("Industries",
        ["Technology","Healthcare","Finance","Energy","Retail","Manufacturing"],
        ["Technology","Healthcare"])
    regions=c2.multiselect("Regions",
        ["MENA","Europe","North America","Asia Pacific"],
        ["MENA"])
    stage=c3.selectbox("Funding Stage",["Pre‑Seed","Seed","Series A","Series B","Growth"],index=1)
    c4,c5=st.columns([2,1])
    sectors=c4.multiselect("Sectors",["Fintech","AI/ML","ClimateTech","HealthTech","SaaS"],["Fintech"])
    deal_count=c5.slider("Deals per Search (Range)",5,50,15,5)

sources=st.multiselect(
    "Active Data Sources",
    ["Crunchbase","AngelList","Magnitt","Wamda","PitchBook"],
    ["Crunchbase","AngelList","Magnitt"]
)

# ============ DISCOVER BUTTON ============
st.markdown("<br>",unsafe_allow_html=True)
colA,colB,colC=st.columns([1,0.8,1])
with colB:
    discover_clicked=st.button("🚀 Discover Live Deals",use_container_width=True)

st.markdown(
    """
<style>
div.stButton>button:first-child{
  background:linear-gradient(135deg,#138074 0%,#0E5F55 100%)!important;color:white!important;
  border:none!important;border-radius:40px!important;
  padding:12px 30px!important;font-weight:700!important;font-size:0.95rem!important;
  box-shadow:0 4px 12px rgba(19,128,116,0.35)!important;transition:0.2s ease;}
div.stButton>button:first-child:hover{transform:translateY(-2px)!important;}
</style>
""",
    unsafe_allow_html=True,
)

# ============ LIVE WEB SCRAPE SOURCING ============
if discover_clicked:
    st.info("Initiating Regulus AI deal scraper…")
    results=[]
    try:
        for src in sources:
            with st.spinner(f"Fetching {', '.join(industries)} deals from {src}…"):
                data=scraper.search_startups(
                    platform=src,
                    industries=industries,
                    sectors=sectors,
                    stage=[stage],
                    regions=regions,
                    limit=int(deal_count/len(sources))
                )
                results.extend(data)
                st.success(f"✔ Got {len(data)} results from {src}")
        if not results:
            st.warning("No matches found for your parameters.")
        else:
            st.session_state.discovered_deals=results
            df=pd.DataFrame(results)
            st.markdown("### Discovered Deals 📊")
            st.dataframe(df,use_container_width=True)

            # AI summary
            question=f"Create a concise summary of {len(results)} recent startup deals discovered in {', '.join(industries)} across {', '.join(regions)}."
            response=llm.generate_text(question)
            st.markdown("#### Regulus AI Summary Report")
            st.info(response)
    except Exception as e:
        st.error(f"⚠️ Scraping failed – {e}")

# ============ FOOTER ============
st.markdown(
    """
<div style="background:#1B2B4D;color:#E2E8F0;padding:28px 30px;margin:60px -3rem 0;margin-bottom:-2rem;">
  <div style="display:flex;justify-content:space-between;align-items:center;max-width:1300px;margin:auto;">
    <p style="margin:0;font-size:0.9rem;">© 2025 Regulus AI | All Rights Reserved</p>
    <p style="margin:0;color:#A0AEC0;font-size:0.9rem;">Powered by Regulus AI</p>
  </div>
</div>
""",
    unsafe_allow_html=True,
)
