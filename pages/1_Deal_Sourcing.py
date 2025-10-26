"""
Deal Sourcing | Investment Analyst AI – Regulus Edition
Full QDB / Regulus‑aligned visual style and teal UI theme.
"""

import streamlit as st
import os, base64, pandas as pd
from utils.qdb_styling import apply_qdb_styling, QDB_DARK_BLUE
from utils.web_scraper import WebScraper
from utils.llm_handler import LLMHandler

# ---- CONFIGURATION ----
st.set_page_config(
    page_title="Deal Sourcing – Regulus AI",
    layout="wide",
    initial_sidebar_state="collapsed"
)
apply_qdb_styling()

def encode_image(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f"data:image/png;base64,{base64.b64encode(f.read()).decode()}"
    return None

qdb_logo = encode_image("QDB_Logo.png")
regulus_logo = encode_image("regulus_logo.png")

# ---- HERO HEADER ----
st.markdown(f"""
<div style="
background:linear-gradient(135deg,#1B2B4D 0%,#2C3E5E 100%);
color:white;text-align:center;margin:0 -3rem;
padding:100px 20px 90px;position:relative;">
  
  <div style="position:absolute;top:25px;left:35px;">
    {'<img src="'+qdb_logo+'" style="max-height:70px;">' if qdb_logo else '<b>QDB</b>'}
  </div>

  <div style="max-width:950px;margin:0 auto;">
    <h1 style="font-size:2.4rem;font-weight:700;letter-spacing:-0.3px;">
       Deal Sourcing – Regulus AI Module
    </h1>
    <p style="color:#E2E8F0;font-size:1.05rem;margin-top:8px;">
       AI‑powered discovery of qualified startup investment opportunities for QDB’s innovation portfolio.
    </p>
  </div>

  <svg viewBox="0 0 1440 100" xmlns="http://www.w3.org/2000/svg" 
       style="position:absolute;bottom:-1px;left:0;width:100%;">
    <path fill="#F6F5F2"
     d="M0,64 L60,53.3 C120,43,240,21,360,26.7 C480,32,600,64,720,80 C840,96,960,96,1080,80 C1200,64,1320,32,1380,16 L1440,0 L1440,0 L0,0Z"></path>
  </svg>
</div>
""", unsafe_allow_html=True)

# ---- STYLE (TEAL BUTTONS etc.) ----
st.markdown("""
<style>
div.stButton>button:first-child{
background:linear-gradient(135deg,#138074 0%,#16967F 100%)!important;
border:none!important;border-radius:32px!important;
color:white!important;font-weight:700!important;
padding:12px 34px!important;font-size:0.95rem!important;
min-width:160px!important;box-shadow:0 4px 14px rgba(19,128,116,0.35)!important;
transition:all 0.3s ease!important;}
div.stButton>button:first-child:hover{
background:linear-gradient(135deg,#0E5F55 0%,#107563 100%)!important;
box-shadow:0 6px 18px rgba(19,128,116,0.5)!important;
transform:translateY(-2px)!important;}
</style>
""", unsafe_allow_html=True)

# ---- SESSION + LLM ----
@st.cache_resource
def init_resources():
    return WebScraper(), LLMHandler()
scraper,llm = init_resources()

# ---- FILTERS ----
st.markdown("""
<div style="background:#F6F5F2;margin:0 -3rem;padding:55px 3rem 35px;
border-top:4px solid #138074;">
<h2 style="color:#1B2B4D;text-align:center;font-weight:700;">
Daily Deal Discovery Dashboard
</h2>
<p style="text-align:center;color:#555;font-size:1.02rem;">
Customize filters for AI‑based deal sourcing across global accelerators and investment feeds.
</p>
</div>
""", unsafe_allow_html=True)

with st.expander("🎯 Define Investment Criteria", expanded=True):
    c1,c2,c3=st.columns(3)
    industries=c1.multiselect("Industries",
       ["Technology","Healthcare","Finance","Energy","Retail","Manufacturing"],
       ["Technology","Finance"])
    regions=c2.multiselect("Regions",
       ["MENA","Europe","North America","Asia Pacific"],["MENA"])
    stage=c3.selectbox("Funding Stage",
       ["Pre‑Seed","Seed","Series A","Series B","Growth"],index=1)
    c4,c5=st.columns([2,1])
    sectors=c4.multiselect("Sectors",
       ["Fintech","AI/ML","ClimateTech","HealthTech","SaaS"],["Fintech"])
    limit=c5.slider("Deals per run",5,50,15,5)

# ---- DISCOVER BUTTON ----
center_col = st.columns([1,0.8,1])[1]
with center_col:
    run = st.button("🚀 Discover Startup Deals",use_container_width=True)

# ---- EXECUTION ----
if run:
    st.info("Searching selected platforms…")
    deals=[]
    for src in ["Crunchbase","AngelList","Magnitt"]:
        st.write(f"→ Fetching from {src}…")
        deals+=scraper.search_startups(src,industries,sectors,[stage],regions,limit)
    if not deals:
        st.warning("No matches found for chosen filters.")
    else:
        df=pd.DataFrame(deals)
        st.success(f"✅ {len(df)} deals retrieved.")
        st.dataframe(df,use_container_width=True)
        st.markdown("#### Regulus AI Insights Summary")
        prompt=f"Summarize {len(df)} deals within {', '.join(industries)} across {', '.join(regions)} regions."
        st.info(llm.generate_text(prompt))

# ---- FOOTER (QDB STYLE) ----
st.markdown(f"""
<div style="
background-color:#1B2B4D;color:#E2E8F0;padding:28px 40px;
margin:70px -3rem -2rem;font-size:0.94rem;">
  <div style="display:flex;justify-content:space-between;align-items:center;
        flex-wrap:wrap;max-width:1400px;margin:0 auto;">
    <div style="flex:2;">
      <ul style="list-style:none;display:flex;gap:30px;flex-wrap:wrap;padding:0;margin:0;">
        <li><a href="#" style="text-decoration:none;color:#E2E8F0;">About Regulus</a></li>
        <li><a href="#" style="text-decoration:none;color:#E2E8F0;">Contact Us</a></li>
        <li><a href="#" style="text-decoration:none;color:#E2E8F0;">Privacy Policy</a></li>
        <li><a href="#" style="text-decoration:none;color:#E2E8F0;">Terms & Conditions</a></li>
      </ul>
    </div>
    <div style="flex:1;text-align:right;display:flex;align-items:center;justify-content:flex-end;gap:12px;">
       <p style="margin:0;color:#A0AEC0;font-size:0.9rem;">Powered by Regulus AI</p>
       {'<img src="'+regulus_logo+'" style="max-height:42px;opacity:0.95;">' if regulus_logo else ''}
    </div>
  </div>
</div>
""", unsafe_allow_html=True)
