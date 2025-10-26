"""
Deal Discovery & Sourcing | Regulus AI | QDB
Premium teal‑themed UI aligned with main page. All HTML validated.
"""

import streamlit as st
import pandas as pd
from utils.web_scraper import WebScraper
from utils.llm_handler import LLMHandler
from utils.template_generator import TemplateGenerator
from utils.qdb_styling import apply_qdb_styling

# -------- PAGE SETTINGS --------
st.set_page_config(page_title="Deal Sourcing – Regulus AI", layout="wide")
apply_qdb_styling()

# -------- HANDLERS --------
@st.cache_resource
def _init():
    return WebScraper(), LLMHandler(), TemplateGenerator()
scraper, llm, template = _init()

# -------- HEADER + WAVE --------
st.markdown("""
<div style="
background:linear-gradient(135deg,#0E5F55 0%,#138074 60%,#1B2B4D 100%);
color:white;text-align:center;margin:0 -3rem;padding:88px 20px 67px;">
  <h1 style="font-family:'Segoe UI',sans-serif;font-weight:700;font-size:2.5rem;">
     AI‑Powered Deal Discovery & Sourcing
  </h1>
  <p style="color:#E2E8F0;font-size:1.05rem;margin-top:8px;">
     Identify qualified investment opportunities from global startup sources with Regulus AI‑driven analysis.
  </p>
</div>
<svg style="display:block;margin:0 -3rem -1px;" viewBox="0 0 1440 100"
xmlns="http://www.w3.org/2000/svg">
  <path fill="#F6F5F2"
  d="M0,64 L60,53.3 C120,43 240,21 360,26.7 C480,32 600,64 720,80 C840,96 960,96 1080,80 C1200,64 1320,32 1380,16 L1440,0 L1440,0 L0,0Z"></path>
</svg>
""", unsafe_allow_html=True)

# -------- STEP TRACKER --------
st.markdown("""
<style>
.bar{background:#F6F5F2;margin:-2px -3rem;padding:32px 20px;
display:flex;justify-content:space-evenly;align-items:center;}
.step{text-align:center;font-family:'Segoe UI',sans-serif;}
.circle{width:54px;height:54px;border-radius:50%;display:flex;
align-items:center;justify-content:center;font-weight:700;
background:#CBD5E0;color:#475569;font-size:0.95rem;}
.circle.active{background:linear-gradient(135deg,#138074 0%,#0E5F55 100%);
color:white;box-shadow:0 5px 15px rgba(19,128,116,0.4);}
.label{margin-top:7px;font-size:0.9rem;font-weight:600;color:#708090;}
.label.active{color:#138074;}
.line{height:3px;width:70px;background:#CBD5E0;}
</style>

<div class="bar">
 <div class="step"><div class="circle active">1</div><div class="label active">Deal Sourcing</div></div>
 <div class="line"></div>
 <div class="step"><div class="circle">2</div><div class="label">Due Diligence</div></div>
 <div class="line"></div>
 <div class="step"><div class="circle">3</div><div class="label">Market Analysis</div></div>
 <div class="line"></div>
 <div class="step"><div class="circle">4</div><div class="label">Financial Modeling</div></div>
 <div class="line"></div>
 <div class="step"><div class="circle">5</div><div class="label">Investment Memo</div></div>
</div>
""", unsafe_allow_html=True)

# -------- FILTERS --------
st.markdown("""
<div style="background:white;margin:50px -3rem 0 -3rem;padding:45px 3rem;
border-top:3px solid #138074;border-radius:10px 10px 0 0;
box-shadow:0 0 12px rgba(0,0,0,0.05);">
<h2 style="text-align:center;color:#1B2B4D;font-weight:700;">
Daily Deal Discovery Dashboard
</h2>
<p style="text-align:center;color:#555;font-size:1.02rem;margin-top:5px;">
Customize your search to source verified startups that match QDB investment criteria.
</p>
</div>
""", unsafe_allow_html=True)

with st.expander("🎯 Define Investment Criteria", expanded=True):
    col1,col2,col3=st.columns(3)
    industries=col1.multiselect("Industries",
       ["Technology","Healthcare","Finance","Energy","Retail","Manufacturing"],
       ["Technology","Healthcare"])
    regions=col2.multiselect("Regions",
       ["MENA","Europe","North America","Asia Pacific"],["MENA"])
    stage=col3.selectbox("Funding Stage",
       ["Pre‑Seed","Seed","Series A","Series B","Growth"],index=1)
    c4,c5=st.columns([2,1])
    sectors=c4.multiselect("Sectors",
       ["Fintech","AI/ML","ClimateTech","HealthTech","SaaS"],["Fintech"])
    deal_count=c5.slider("Deals per run",5,50,15,5)

sources=st.multiselect("Active Data Sources",
   ["Crunchbase","AngelList","Magnitt","Wamda","PitchBook"],
   ["Crunchbase","AngelList","Magnitt"])

# -------- BUTTON (Teal) --------
st.markdown("<br>", unsafe_allow_html=True)
_,center,_ = st.columns([1,0.8,1])
with center:
    discover = st.button("🚀 Discover Live Deals", use_container_width=True)

st.markdown("""
<style>
div.stButton>button:first-child{
background:linear-gradient(135deg,#138074 0%,#0E5F55 100%)!important;
color:white!important;border:none!important;border-radius:40px!important;
padding:13px 30px!important;font-weight:700!important;font-size:0.95rem!important;
box-shadow:0 5px 12px rgba(19,128,116,0.3)!important;transition:all 0.3s ease;}
div.stButton>button:first-child:hover{
transform:translateY(-2px)!important;
box-shadow:0 8px 20px rgba(19,128,116,0.45)!important;}
</style>
""", unsafe_allow_html=True)

# -------- EXECUTION --------
if discover:
    st.info("🔍 Retrieving real‑time startup data…")
    results=[]
    for src in sources:
        st.write(f"Scraping {src}...")
        results += scraper.search_startups(src,industries,sectors,[stage],regions,
                                           limit=int(deal_count/len(sources)))
    if not results:
        st.warning("No deals found for the chosen filters.")
    else:
        df=pd.DataFrame(results)
        st.success(f"✅ {len(df)} qualified deals sourced successfully.")
        st.dataframe(df,use_container_width=True)
        st.markdown("#### Regulus AI Summary")
        prompt=f"Summarize {len(df)} deals across {', '.join(industries)} in {', '.join(regions)}."
        summary=llm.generate_text(prompt)
        st.info(summary)

# -------- FOOTER --------
st.markdown("""
<div style="background:#1B2B4D;color:#E2E8F0;padding:26px 36px;margin:80px -3rem -2rem;
display:flex;justify-content:space-between;align-items:center;">
  <p style="margin:0;font-size:0.9rem;">© 2025 Regulus AI | All Rights Reserved</p>
  <p style="margin:0;color:#A0AEC0;font-size:0.9rem;">Powered by Regulus AI</p>
</div>
""", unsafe_allow_html=True)
