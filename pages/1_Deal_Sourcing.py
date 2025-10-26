"""
Deal Discovery & Sourcing | Regulus AI | QDB
Teal‑themed premium UI/UX matching main page design.
"""

import streamlit as st
import pandas as pd
from utils.web_scraper import WebScraper
from utils.llm_handler import LLMHandler
from utils.template_generator import TemplateGenerator
from utils.qdb_styling import apply_qdb_styling
from datetime import datetime

# ==== PAGE CONFIG ====
st.set_page_config(page_title="AI Deal Sourcing – Regulus AI", layout="wide")
apply_qdb_styling()

# ==== HEADER WITH WAVE SEPARATOR ====
st.markdown("""
<div style="
background:linear-gradient(135deg,#0E5F55 0%,#138074 50%,#1B2B4D 100%);
color:white;text-align:center;margin:0 -3rem;padding:85px 20px 65px;">
  <h1 style="font-weight:700;font-size:2.6rem;font-family:'Segoe UI',sans-serif;">
     AI‑Powered Deal Discovery & Sourcing
  </h1>
  <p style="color:#E2E8F0;font-size:1.05rem;max-width:760px;margin:auto;">
     Identify qualified investment opportunities from global startup sources with Regulus AI‑driven analysis.
  </p>
</div>

<svg style="display:block;margin:0 -3rem -1px;" viewBox="0 0 1440 100"
xmlns="http://www.w3.org/2000/svg"><path fill="#F6F5F2"
d="M0,64 L60,53.3 C120,43,240,21,360,26.7 C480,32,600,64,720,80 C840,96,960,96,1080,80 C1200,64,1320,32,1380,16 L1440,0 L1440,0 L0,0Z"></path></svg>
""",unsafe_allow_html=True)

# ==== STEP TRACKER ====
st.markdown("""
<style>
.flowbar{background:#F6F5F2;margin:-2px -3rem;display:flex;justify-content:space-evenly;
align-items:center;padding:34px 20px;flex-wrap:wrap;}
.stepbox{text-align:center;flex:1;}
.circle{
width:56px;height:56px;border-radius:50%;display:flex;
align-items:center;justify-content:center;
background:#D1D5DB;color:#475569;font-weight:700;font-size:1rem;
transition:all 0.3s ease;}
.circle.active{
background:linear-gradient(135deg,#138074 0%,#0E5F55 100%);
color:white;box-shadow:0 5px 15px rgba(19,128,116,0.4);transform:scale(1.05);}
.label{margin-top:7px;font-size:0.9rem;font-weight:600;color:#94A3B8;}
.label.active{color:#138074;}
.pipe{width:70px;height:3px;background:#CBD5E0;}
</style>

<div class="flowbar">
  <div class="stepbox"><div class="circle active">1</div><div class="label active">Deal Sourcing</div></div>
  <div class="pipe"></div>
  <div class="stepbox"><div class="circle">2</div><div class="label">Due Diligence</div></div>
  <div class="pipe"></div>
  <div class="stepbox"><div class="circle">3</div><div class="label">Market Analysis</div></div>
  <div class="pipe"></div>
  <div class="stepbox"><div class="circle">4</div><div class="label">Financial Modeling</div></div>
  <div class="pipe"></div>
  <div class="stepbox"><div class="circle">5</div><div class="label">Investment Memo</div></div>
</div>
""",unsafe_allow_html=True)

# ==== HANDLERS ====
@st.cache_resource
def _init():
    return WebScraper(), LLMHandler(), TemplateGenerator()
scraper,llm,template=_init()

# ==== FILTERS SECTION ====
st.markdown("""
<div style="background:white;margin:50px -3rem 0 -3rem;padding:50px 3rem;
border-top:3px solid #138074;border-radius:10px 10px 0 0;
box-shadow:0 0 12px rgba(0,0,0,0.05);">
<h2 style="text-align:center;color:#1B2B4D;font-family:'Segoe UI',sans-serif;font-weight:700;">
Daily Deal Discovery Dashboard
</h2>
<p style="text-align:center;color:#555;font-size:1.02rem;margin-top:6px;">
Customize your search to source verified startups that match QDB criteria.
</p>
</div>
""",unsafe_allow_html=True)

with st.expander("🎯 Define Investment Criteria",expanded=True):
    c1,c2,c3=st.columns(3)
    industries=c1.multiselect("Industries",
      ["Technology","Healthcare","Finance","Energy","Retail","Manufacturing"],
      ["Technology","Healthcare"])
    regions=c2.multiselect("Regions",
      ["MENA","Europe","North America","Asia Pacific"],["MENA"])
    stage=c3.selectbox("Funding Stage",
      ["Pre‑Seed","Seed","Series A","Series B","Growth"],index=1)
    c4,c5=st.columns([2,1])
    sectors=c4.multiselect("Sectors",
      ["Fintech","AI/ML","ClimateTech","HealthTech","SaaS"],["Fintech"])
    deal_count=c5.slider("Deals per run",5,50,15,5)

sources=st.multiselect("Active Sources",
    ["Crunchbase","AngelList","Magnitt","PitchBook","Wamda"],
    ["Crunchbase","AngelList","Magnitt"])

# ==== DISCOVER BUTTON (TEAL) ====
st.markdown("<br>",unsafe_allow_html=True)
colA,colB,colC=st.columns([1,0.8,1])
with colB:
    run=st.button("🚀 Discover Live Deals",use_container_width=True)

st.markdown("""
<style>
div.stButton>button:first-child{
background:linear-gradient(135deg,#138074 0%,#0E5F55 100%)!important;
color:white!important;border:none!important;border-radius:40px!important;
padding:13px 30px!important;font-weight:700!important;font-size:0.96rem!important;
box-shadow:0 5px 15px rgba(19,128,116,0.35)!important;transition:all 0.25s ease;}
div.stButton>button:first-child:hover{
transform:translateY(-2px)!important;
box-shadow:0 8px 20px rgba(19,128,116,0.45)!important;}
</style>
""",unsafe_allow_html=True)

# ==== RESULTS ====
if run:
    st.info("🔍 Fetching real‑time startup deal data …")
    data=[]
    for src in sources:
        st.write(f"Scraping {src} …")
        data+=scraper.search_startups(src,industries,sectors,[stage],regions,limit=int(deal_count/len(sources)))
    if not data:
        st.warning("No deals found for the given criteria .")
    else:
        df=pd.DataFrame(data)
        st.success(f"✅ {len(df)} qualified deals retrieved successfully.")
        st.dataframe(df,use_container_width=True)
        st.markdown("#### Regulus AI Insights 🧠")
        context=f"Summarize {len(df)} deals across {', '.join(industries)} within {', '.join(regions)}."
        summary=llm.generate_text(context)
        st.info(summary)

# ==== FOOTER ====
st.markdown("""
<div style="background:#1B2B4D;color:#E2E8F0;
padding:25px 40px;margin:80px -3rem -2rem;
display:flex;justify-content:space-between;align-items:center;">
  <p style="margin:0;font-size:0.9rem;">
     © 2025 Regulus AI | All Rights Reserved
  </p>
  <p style="margin:0;color:#A0AEC0;font-size:0.9rem;">
     Powered by Regulus AI
  </p>
</div>
""",unsafe_allow_html=True)
