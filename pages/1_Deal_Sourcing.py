"""
Deal Discovery & Sourcing | Regulus AI × QDB
Aligned with QDB brand and Investment Analyst AI main page theme.
"""
import streamlit as st
import pandas as pd
from utils.web_scraper import WebScraper
from utils.llm_handler import LLMHandler
from utils.template_generator import TemplateGenerator
from utils.qdb_styling import apply_qdb_styling, qdb_section_start, qdb_section_end, QDB_DARK_BLUE, QDB_NAVY

# ---- PAGE CONFIG ----
st.set_page_config(page_title="Deal Sourcing – Regulus AI", layout="wide")
apply_qdb_styling()

# ---- LOAD RESOURCES ----
@st.cache_resource
def init():
    return WebScraper(), LLMHandler(), TemplateGenerator()
scraper, llm, template = init()

# ---- HERO HEADER ----
st.markdown(f"""
<div class="qdb-section-dark" style="background:linear-gradient(135deg,{QDB_DARK_BLUE} 0%,{QDB_NAVY} 100%);
text-align:center;margin:0 -3rem;padding:100px 20px 70px 20px;position:relative;">
  <h1 style="font-family:'Segoe UI',sans-serif;font-weight:700;font-size:2.5rem;margin-bottom:10px;">
      AI‑Powered Deal Discovery & Sourcing
  </h1>
  <p style="color:#E2E8F0;font-size:1.05rem;">
      Identify qualified investment opportunities from accelerators, funding platforms and Regulus AI feeds.
  </p>

  <!-- WAVE DIVIDER -->
  <svg viewBox="0 0 1440 120" xmlns="http://www.w3.org/2000/svg" style="position:absolute;bottom:-1px;left:0;width:100%;">
     <path fill="#F6F5F2" d="M0,32 L80,42.7 C160,53,320,75,480,80 C640,85,800,75,960,69.3 C1120,64,1280,75,1360,80 L1440,85 L1440,120 L0,120Z"></path>
  </svg>
</div>
""", unsafe_allow_html=True)

# ---- STEP TRACKER – UNIFIED STYLE ----
st.markdown("""
<style>
.track{background:#F6F5F2;margin:-2px -3rem 0 -3rem;padding:35px 20px;
display:flex;justify-content:space-evenly;align-items:center;}
.step{flex:1;text-align:center;font-family:'Segoe UI';}
.circle{width:52px;height:52px;border-radius:50%;display:flex;
align-items:center;justify-content:center;font-weight:700;
background:#CBD5E0;color:#475569;font-size:0.95rem;}
.circle.active{background:linear-gradient(135deg,#138074 0%,#0E5F55 100%);
color:white;box-shadow:0 4px 15px rgba(19,128,116,0.4);}
.label{margin-top:7px;font-size:0.9rem;color:#708090;font-weight:600;}
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
""", unsafe_allow_html=True)

# ---- FILTER SECTION IN LIGHT THEME ----
qdb_section_start("light")
st.markdown("""
<div style="text-align:center;margin-bottom:30px;">
    <h2 style="color:#1B2B4D;font-weight:700;">Daily Deal Discovery Dashboard</h2>
    <p style="color:#555;font-size:1.02rem;">
        Customize filters to source verified startups aligned with QDB investment criteria.
    </p>
</div>
""", unsafe_allow_html=True)

with st.expander("🎯 Define Investment Criteria", expanded=True):
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
    deals=c5.slider("Deals per fetch",5,50,15,5)

sources=st.multiselect("Active Sources",
    ["Crunchbase","AngelList","Magnitt","Wamda","PitchBook"],
    ["Crunchbase","AngelList","Magnitt"])

qdb_section_end()

# ---- CTA BUTTON — BRAND TEAL COLOR ----
st.markdown("<br>", unsafe_allow_html=True)
_,mid,_=st.columns([1,0.8,1])
with mid:
    start=st.button("🚀 Discover Live Deals",use_container_width=True)

st.markdown("""
<style>
div.stButton>button:first-child{
background:linear-gradient(135deg,#138074 0%,#0E5F55 100%)!important;
border:none!important;border-radius:40px!important;color:white!important;
padding:13px 34px!important;font-weight:700!important;font-size:0.96rem!important;
box-shadow:0 4px 14px rgba(19,128,116,0.35)!important;transition:all 0.25s ease;}
div.stButton>button:first-child:hover{
background:linear-gradient(135deg,#0E5F55 0%,#138074 100%)!important;
transform:translateY(-2px)!important;box-shadow:0 6px 18px rgba(19,128,116,0.5)!important;}
</style>
""",unsafe_allow_html=True)

# ---- EXECUTION SECTION ----
if start:
    st.info("🔍 Fetching real‑time deal data from selected platforms …")
    results=[]
    for src in sources:
        st.write(f"Scraping {src} …")
        results+=scraper.search_startups(src,industries,sectors,[stage],regions,
                                         limit=int(deals/len(sources)))
    if not results:
        st.warning("No matching deals found.")
    else:
        df=pd.DataFrame(results)
        st.success(f"✅ {len(df)} deals retrieved successfully.")
        st.dataframe(df,use_container_width=True)
        summary_text=llm.generate_text(f"Summarize {len(df)} startups for {', '.join(industries)} in {', '.join(regions)} .")
        st.markdown("#### Regulus AI Summary Report")
        st.info(summary_text)

# ---- FOOTER ----
st.markdown(f"""
<div style="background:{QDB_DARK_BLUE};color:#E2E8F0;margin:80px -3rem -2rem;
padding:26px 36px;display:flex;justify-content:space-between;align-items:center;">
  <p style="margin:0;font-size:0.9rem;">© 2025 Regulus AI | All Rights Reserved</p>
  <p style="margin:0;color:#A0AEC0;font-size:0.9rem;">Powered by Regulus AI</p>
</div>
""",unsafe_allow_html=True)
