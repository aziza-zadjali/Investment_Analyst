"""
Deal Discovery & Sourcing | Regulus AI × QDB
Hero style visually identical to your main page, with center-aligned CTA and full brand setup.
"""
import streamlit as st
import os, base64, pandas as pd
from utils.web_scraper import WebScraper
from utils.llm_handler import LLMHandler
from utils.template_generator import TemplateGenerator
from utils.qdb_styling import (
    apply_qdb_styling,
    QDB_DARK_BLUE,
    QDB_NAVY,
)

st.set_page_config(page_title="Deal Sourcing – Regulus AI", layout="wide")
apply_qdb_styling()

def encode_image(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f"data:image/png;base64,{base64.b64encode(f.read()).decode()}"
    return None
qdb_logo = encode_image("QDB_Logo.png")

# ==== HERO SECTION (EXACT MAIN PAGE STYLE) ====
st.markdown(
    f"""
<div style="
    background:linear-gradient(135deg,{QDB_DARK_BLUE} 0%, {QDB_NAVY} 100%);
    color:white;
    position:relative;
    margin:0 -3rem; padding:100px 0 80px 0;
    min-height:390px; text-align:center; overflow:hidden;">
  <!-- QDB LOGO LEFT -->
  <div style="position:absolute;left:50px;top:48px;">
    {'<img src="'+qdb_logo+'" style="max-height:80px;">' if qdb_logo else '<b>QDB</b>'}
  </div>
  <div style="max-width:950px;margin:0 auto;">
    <h1 style="font-size:2.8rem;font-weight:800;letter-spacing:-0.5px;line-height:1.18; margin-bottom:16px;">
      Deal Discovery & Sourcing
    </h1>
    <p style="font-size:1.35rem;color:#E2E8F0; font-weight:500; margin-bottom:18px;">
      Supporting Qatar's Economic Vision with Data-Driven Startup Intelligence
    </p>
    <p style="color:#CBD5E0; font-size:1.07rem;line-height:1.6;max-width:760px;margin:0 auto 38px;">
      Daily AI-powered identification and curation of investment opportunities. <br>
      End-to-End Sourcing, Due Diligence, Market Analysis & Investment Memos.
    </p>
    <div style="margin-top:30px;">
      <button onclick="window.location.href='/'" style="
        background:linear-gradient(135deg,#16A085 0%,#138074 80%,#0E5F55 100%);
        color:white; border:none; border-radius:44px!important;
        padding:19px 54px; font-weight:700; font-size:1.08rem;
        letter-spacing:0.01em; box-shadow:0 8px 34px rgba(19,128,116,.20);
        transition:all .19s; cursor:pointer;">
        ⬅ Return Home
      </button>
    </div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

# ==== WORKFLOW TRACKER (no change needed) ====
st.markdown(
    """
<style>
.track{background:#F6F5F2;margin:-2px -3rem;padding:34px 0;
display:flex;justify-content:space-evenly;align-items:center;}
.circle{width:54px;height:54px;border-radius:50%;display:flex;
align-items:center;justify-content:center;font-weight:700;
background:#CBD5E0;color:#475569;font-size:0.95rem;}
.circle.active{background:linear-gradient(135deg,#138074 0%,#0E5F55 100%);
color:white;box-shadow:0 5px 15px rgba(19,128,116,0.4);}
.label{margin-top:7px;font-size:0.9rem;font-weight:600;color:#708090;}
.label.active{color:#138074;}
.pipe{height:3px;width:70px;background:#CBD5E0;}
</style>
<div class="track">
 <div><div class="circle active">1</div><div class="label active">Deal Sourcing</div></div>
 <div class="pipe"></div>
 <div><div class="circle">2</div><div class="label">Due Diligence</div></div>
 <div class="pipe"></div>
 <div><div class="circle">3</div><div class="label">Market Analysis</div></div>
 <div class="pipe"></div>
 <div><div class="circle">4</div><div class="label">Financial Modeling</div></div>
 <div class="pipe"></div>
 <div><div class="circle">5</div><div class="label">Investment Memo</div></div>
</div>
""",
    unsafe_allow_html=True,
)

# ==== MAIN CONTENT FILTERS & BUTTON ====
st.markdown(
    """
<div style="background:white;margin:50px -3rem 0 -3rem;padding:45px 3rem;
border-top:3px solid #138074;box-shadow:0 0 12px rgba(0,0,0,0.05);">
<h2 style="text-align:center;color:#1B2B4D;font-weight:700;">
Daily Deal Discovery Dashboard
</h2>
<p style="text-align:center;color:#555;margin-top:6px;">
Apply custom filters to identify pre-qualified, relevant startups fast.
</p>
</div>
""",
    unsafe_allow_html=True,
)
with st.expander("🎯 Define Investment Criteria", expanded=True):
    c1, c2, c3 = st.columns(3)
    industries = c1.multiselect(
        "Industries",
        ["Technology","Healthcare","Finance","Energy","Retail","Manufacturing"],
        ["Technology","Healthcare"],
    )
    regions = c2.multiselect(
        "Regions",["MENA","Europe","North America","Asia Pacific"],["MENA"]
    )
    stage = c3.selectbox("Funding Stage",["Pre‑Seed","Seed","Series A","Series B","Growth"],index=1)
    c4, c5 = st.columns([2,1])
    sectors = c4.multiselect("Sectors",["Fintech","AI/ML","ClimateTech","HealthTech","SaaS"],["Fintech"])
    deal_count = c5.slider("Deals per run",5,50,15,5)
sources = st.multiselect(
    "Active Sources",
    ["Crunchbase","AngelList","Magnitt","Wamda","PitchBook"],
    ["Crunchbase","AngelList","Magnitt"],
)

st.markdown("<br>", unsafe_allow_html=True)
col1,col2,col3 = st.columns([1,0.8,1])
with col2:
    discover = st.button("🚀 Discover Live Deals", use_container_width=True)
st.markdown(
    """
<style>
div.stButton>button:first-child{
 background:linear-gradient(135deg,#16A085 0%,#138074 50%,#0E5F55 100%)!important;
 color:white!important;border:none!important;border-radius:40px!important;
 padding:14px 42px!important;font-weight:700!important;font-size:1rem!important;
 box-shadow:0 5px 18px rgba(19,128,116,0.35)!important;transition:all 0.3s ease!important;}
div.stButton>button:first-child:hover{
 background:linear-gradient(135deg,#0E5F55 0%,#138074 50%,#16A085 100%)!important;
 transform:translateY(-2px)!important;
 box-shadow:0 8px 22px rgba(19,128,116,0.45)!important;}
</style>
""",
    unsafe_allow_html=True,
)

if discover:
    scraper, llm, template = WebScraper(), LLMHandler(), TemplateGenerator()
    st.info("🔍 Fetching startup deals…")
    data=[]
    for s in sources:
        st.write(f"Scraping {s} …")
        data+=scraper.search_startups(s,industries,sectors,[stage],regions,limit=int(deal_count/len(sources)))
    if not data:
        st.warning("No results found.")
    else:
        df=pd.DataFrame(data)
        st.success(f"✅ {len(df)} deals found.")
        st.dataframe(df,use_container_width=True)
        st.markdown("#### AI Summary")
        st.info(llm.generate_text(f"Summarize {len(df)} deals for {', '.join(industries)} in {', '.join(regions)}."))

st.markdown(
    f"""
<div style="background:{QDB_DARK_BLUE};color:#E2E8F0;padding:26px 36px;margin:80px -3rem -2rem;
display:flex;justify-content:space-between;align-items:center;">
  <p style="margin:0;font-size:0.9rem;">© 2025 Regulus AI | All Rights Reserved</p>
  <p style="margin:0;color:#A0AEC0;font-size:0.9rem;">Powered by Regulus AI</p>
</div>
""",
    unsafe_allow_html=True,
)
