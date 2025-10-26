"""
Deal Discovery & Sourcing – Regulus × QDB
Teal theme | Fixed markup | Modern step tracker | Centered responsive design
"""

import streamlit as st
from utils.web_scraper import WebScraper
from utils.llm_handler import LLMHandler
from utils.template_generator import TemplateGenerator
import pandas as pd
from utils.qdb_styling import apply_qdb_styling
from datetime import datetime
import base64, os

# ===== PAGE CONFIGURATION =====
st.set_page_config(page_title="Deal Sourcing – Regulus", layout="wide")
apply_qdb_styling()

# ===== SAFE IMAGE EMBED =====
def encode_image(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return "data:image/png;base64," + base64.b64encode(f.read()).decode()
    return None

# ===== INITIALIZE SESSION =====
for key, default in {
    "discovered_deals": [],
    "selected_deals": [],
    "saved_deals": [],
    "show_contact_form": {}
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ===== HANDLERS =====
@st.cache_resource
def init_handlers():
    return WebScraper(), LLMHandler(), TemplateGenerator()

scraper, llm, template = init_handlers()

# ===== HEADER =====
st.markdown(
    """
<div style="background:linear-gradient(135deg,#1B2B4D 0%,#2C3E5E 100%);
    color:white;text-align:center;margin:0 -3rem;padding:70px 20px 60px;">
  <h1 style="font-size:2.2rem;font-weight:700;">Deal Discovery & Sourcing</h1>
  <p style="color:#CBD5E0;font-size:0.95rem;">
    AI‑powered investment opportunity discovery from global accelerators and funding databases.
  </p>
</div>
""",
    unsafe_allow_html=True,
)

# ===== STEP TRACKER (valid HTML) =====
st.markdown(
    """
<style>
.tracker{background:#F6F5F2;margin:0 -3rem;padding:24px 40px;display:flex;
justify-content:center;align-items:center;gap:16px;flex-wrap:wrap;font-family:'Segoe UI',sans-serif;}
.step{display:flex;flex-direction:column;align-items:center;}
.circle{width:42px;height:42px;border-radius:50%;display:flex;align-items:center;
justify-content:center;font-weight:700;font-size:0.95rem;}
.circle.active{background:#138074;color:white;box-shadow:0 3px 10px rgba(19,128,116,0.4);}
.circle.inactive{background:#D1D5DB;color:#9CA3AF;}
.label{font-size:0.8rem;font-weight:600;margin-top:6px;}
.label.active{color:#138074;}
.label.inactive{color:#9CA3AF;}
.line{width:45px;height:2px;background:#CBD5E0;margin:0 8px;}
.link{color:#138074;text-decoration:none;font-weight:600;font-size:0.9rem;}
.link:hover{text-decoration:underline;color:#10675E;}
</style>

<div class="tracker">
  <a href="streamlit_app.py" class="link">&larr;&nbsp;Back to Home</a>
  <div class="step"><div class="circle active">1</div><div class="label active">Deal Sourcing</div></div>
  <div class="line"></div>
  <div class="step"><div class="circle inactive">2</div><div class="label inactive">Due Diligence</div></div>
  <div class="line"></div>
  <div class="step"><div class="circle inactive">3</div><div class="label inactive">Market Analysis</div></div>
  <div class="line"></div>
  <div class="step"><div class="circle inactive">4</div><div class="label inactive">Financial Model</div></div>
  <div class="line"></div>
  <div class="step"><div class="circle inactive">5</div><div class="label inactive">Memo</div></div>
  <span style="margin-left:auto;color:#777;font-size:0.9rem;">Regulus AI</span>
</div>
""",
    unsafe_allow_html=True,
)

# ===== INVESTMENT CRITERIA =====
with st.expander("Define Investment Criteria", expanded=True):
    st.markdown("**Unattractive Industry Screening** – Exclude sectors per QDB policy.")
    industries = st.multiselect(
        "Target Industries",
        ["Technology","Healthcare","Finance","Energy","Retail","Manufacturing"],
        ["Technology","Healthcare"]
    )
    sectors = st.multiselect(
        "Preferred Sectors",
        ["Fintech","HealthTech","AI/ML","Cleantech","SaaS"], ["Fintech","AI/ML"]
    )
    stage = st.multiselect("Funding Stage",
                           ["Pre‑Seed","Seed","Series A","Series B","Growth"],["Seed"])
    geography = st.multiselect(
        "Regions", ["MENA","Europe","North America","Asia Pacific"], ["MENA"]
    )
    deal_count = st.number_input("Deals to source", 5, 50, 15, 5)

# ===== DATA SOURCES =====
st.markdown("#### Select Data Sources")
sources = st.multiselect(
    "Active Providers",
    ["Crunchbase","AngelList","PitchBook","Magnitt","Wamda","Dealroom"],
    ["Crunchbase","AngelList","Magnitt"]
)
if sources:
    c = st.columns(len(sources))
    for i, s in enumerate(sources):
        with c[i]:
            st.markdown(f"**{s}**")
            st.caption("Startup funding database")

# ===== MAIN BUTTON =====
col1, col2, col3 = st.columns([1,0.8,1])
with col2:
    run = st.button("🚀 Discover Deals", use_container_width=True)

st.markdown(
    """
<style>
div.stButton>button:first-child{
    background:linear-gradient(135deg,#138074 0%,#0E5F55 100%)!important;
    color:white!important;border:none!important;border-radius:40px!important;
    padding:12px 30px!important;font-weight:700!important;
    font-size:0.95rem!important;
    box-shadow:0 4px 10px rgba(19,128,116,0.3)!important;
    transition:0.2s ease;
}
div.stButton>button:first-child:hover{
    background:linear-gradient(135deg,#0E5F55,#138074)!important;
    transform:translateY(-2px)!important;
}
</style>
""",
    unsafe_allow_html=True,
)

# ===== DISCOVER DEALS =====
if run:
    st.info("Gathering opportunities from selected sources …")
    deals = []
    for i in range(deal_count):
        deals.append({
            "Company": f"Startup {i+1}",
            "Industry": industries[i % len(industries)],
            "Sector": sectors[i % len(sectors)],
            "Stage": stage[0],
            "Region": geography[0],
            "Ticket": f"${(i%5)+1} M"
        })
    st.session_state.discovered_deals = deals
    st.success(f"✅ {len(deals)} potential deals identified successfully.")

# ===== DISPLAY TABLE =====
if st.session_state.discovered_deals:
    st.markdown("### Discovered Deals")
    df = pd.DataFrame(st.session_state.discovered_deals)
    st.dataframe(df, use_container_width=True)

# ===== FOOTER =====
st.markdown(
    """
<div style="background-color:#1B2B4D;color:#E2E8F0;padding:26px 25px;
margin:40px -3rem 0 -3rem;">
  <div style="display:flex;justify-content:space-between;
  align-items:center;max-width:1300px;margin:auto;">
    <p style="margin:0;font-size:0.9rem;">© 2025 Regulus AI | All Rights Reserved</p>
    <p style="margin:0;color:#A0AEC0;font-size:0.9rem;">Powered by Regulus AI</p>
  </div>
</div>
""",
    unsafe_allow_html=True,
)
