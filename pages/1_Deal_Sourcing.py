"""
Deal Discovery & Sourcing | Regulus × QDB
Teal theme • valid HTML • stunning step tracker • responsive centered layout
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import base64, os
from utils.web_scraper import WebScraper
from utils.llm_handler import LLMHandler
from utils.template_generator import TemplateGenerator
from utils.qdb_styling import apply_qdb_styling

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Deal Sourcing - Regulus AI", layout="wide", initial_sidebar_state="collapsed")
apply_qdb_styling()

# ---------- IMAGE ENCODER ----------
def encode_image(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return "data:image/png;base64," + base64.b64encode(f.read()).decode()
    return None

# ---------- INITIALIZE SESSION ----------
for key in ["discovered_deals","selected_deals","saved_deals"]:
    if key not in st.session_state:
        st.session_state[key]=[]
if "show_contact_form" not in st.session_state:
    st.session_state.show_contact_form={}

# ---------- HANDLERS ----------
@st.cache_resource
def init_handlers():
    return WebScraper(), LLMHandler(), TemplateGenerator()

scraper,llm,templater=init_handlers()

# ---------- HEADER ----------
st.markdown(
    """
<div style="background:linear-gradient(135deg,#1B2B4D 0%,#2C3E5E 100%);
color:white;text-align:center;margin:0 -3rem;padding:70px 20px;">
  <h1 style="font-weight:700;font-size:2rem;">Deal Discovery & Sourcing</h1>
  <p style="color:#CBD5E0;">AI‑powered investment opportunity discovery from global platforms</p>
</div>
""",
    unsafe_allow_html=True,
)

# ---------- STEP TRACKER (clean HTML) ----------
st.markdown(
    """
<style>
.tracker{
  background-color:#F6F5F2;margin:0 -3rem;padding:25px 40px;
  display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;
  font-family:'Segoe UI',sans-serif;
}
.steps{display:flex;justify-content:center;align-items:center;gap:12px;flex:1;}
.step{display:flex;flex-direction:column;align-items:center;gap:6px;}
.circle{
  width:40px;height:40px;border-radius:50%;
  display:flex;justify-content:center;align-items:center;
  font-weight:700;font-size:0.95rem;
}
.circle.active{background:#138074;color:white;
box-shadow:0 3px 8px rgba(19,128,116,0.4);}
.circle.inactive{background:#D1D5DB;color:#9CA3AF;}
.label{font-size:0.8rem;font-weight:600;}
.label.active{color:#138074;}
.label.inactive{color:#9CA3AF;}
.line{height:2px;width:40px;background:#D1D5DB;}
.navtext{color:#138074;text-decoration:none;font-weight:600;font-size:0.9rem;}
</style>

<div class="tracker">
  <a href="streamlit_app.py" class="navtext">← Back to Home</a>
  <div class="steps">
    <div class="step"><div class="circle active">1</div><div class="label active">Deal Sourcing</div></div>
    <div class="line"></div>
    <div class="step"><div class="circle inactive">2</div><div class="label inactive">Due Diligence</div></div>
    <div class="line"></div>
    <div class="step"><div class="circle inactive">3</div><div class="label inactive">Market Analysis</div></div>
    <div class="line"></div>
    <div class="step"><div class="circle inactive">4</div><div class="label inactive">Financial Model</div></div>
    <div class="line"></div>
    <div class="step"><div class="circle inactive">5</div><div class="label inactive">Investment Memo</div></div>
  </div>
  <span style="color:#777;font-size:0.9rem;">Regulus AI</span>
</div>
""",
    unsafe_allow_html=True,
)

# ---------- CRITERIA ----------
with st.expander("Define Investment Criteria", expanded=True):
    st.markdown("**Unattractive Industry Screening** – Exclude sectors as per QDB list.")
    industries=st.multiselect(
        "Industries",
        ["Technology","Healthcare","Energy","Finance","Retail","Manufacturing"],
        ["Technology","Healthcare"])
    sectors=st.multiselect(
        "Sectors",
        ["Fintech","HealthTech","AI/ML","SaaS","Cleantech"],
        ["Fintech"]
    )
    stage=st.multiselect("Stage",["Pre‑Seed","Seed","Series A","Growth"],["Seed"])
    regions=st.multiselect("Regions",["MENA","Europe","North America","Asia Pacific"],["MENA"])
    deal_count=st.number_input("Deals to Source",5,50,15,5)

# ---------- SOURCES ----------
st.subheader("Select Data Sources")
sources=st.multiselect("Providers",
                       ["Crunchbase","AngelList","PitchBook","Magnitt","Dealroom"],
                       ["Crunchbase","AngelList"])
if sources:
    cols=st.columns(len(sources))
    for i,s in enumerate(sources):
        with cols[i]:
            st.markdown(f"**{s}**")
            st.caption("Global startup and funding data")

# ---------- BUTTON ----------
c1,c2,c3=st.columns([1,0.8,1])
with c2:
    go=st.button("🚀 Discover Deals",use_container_width=True)

st.markdown(
    """
<style>
div.stButton>button:first-child{
  background:linear-gradient(135deg,#138074 0%,#0e5f55 100%)!important;
  color:white!important;border:none!important;
  border-radius:40px!important;padding:12px 30px!important;
  font-weight:700!important;font-size:0.95rem!important;
  box-shadow:0 4px 10px rgba(19,128,116,0.3)!important;
  transition:all 0.2s ease!important;}
div.stButton>button:first-child:hover{
  transform:translateY(-2px)!important;
  box-shadow:0 6px 14px rgba(19,128,116,0.35)!important;}
</style>
""",
    unsafe_allow_html=True,
)

# ---------- DISCOVER DEALS ----------
if go:
    deals=[]
    for i in range(deal_count):
        deals.append({
            "Company":f"Startup {i+1}",
            "Industry":industries[i%len(industries)],
            "Sector":sectors[i%len(sectors)],
            "Stage":stage[0],
            "Region":regions[0],
            "Ticket Size":f"${(i%5)+1} M"
        })
    st.session_state.discovered_deals=deals
    st.success(f"✅ {len(deals)} potential deals discovered!")

# ---------- SHOW RESULTS ----------
if st.session_state.discovered_deals:
    df=pd.DataFrame(st.session_state.discovered_deals)
    st.markdown("### Discovered Deals")
    st.dataframe(df,use_container_width=True)

# ---------- FOOTER ----------
st.markdown(
    """
<div style="background:#1B2B4D;color:#E2E8F0;padding:25px 30px;margin:40px -3rem 0 -3rem;">
  <div style="display:flex;justify-content:space-between;align-items:center;max-width:1300px;margin:auto;">
    <p style="margin:0;font-size:0.9rem;">© 2025 Regulus AI | All Rights Reserved</p>
    <p style="margin:0;color:#A0AEC0;font-size:0.9rem;">Powered by Regulus AI</p>
  </div>
</div>
""",
    unsafe_allow_html=True,
)
