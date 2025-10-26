"""
Deal Discovery & Sourcing Page
Teal theme, fixed code with visual step tracker and centered design
"""

import streamlit as st
from utils.web_scraper import WebScraper
from utils.llm_handler import LLMHandler
from utils.template_generator import TemplateGenerator
import pandas as pd
from datetime import datetime
from utils.qdb_styling import apply_qdb_styling
import base64
import os

# --- Page setup ---
st.set_page_config(page_title="Deal Sourcing - Regulus", layout="wide")
apply_qdb_styling()

# --- Helper to safely embed logos ---
def encode_image(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f"data:image/png;base64,{base64.b64encode(f.read()).decode()}"
    return None

# --- Initialize Session Data ---
if "discovered_deals" not in st.session_state:
    st.session_state.discovered_deals = []
if "selected_deals" not in st.session_state:
    st.session_state.selected_deals = []
if "saved_deals" not in st.session_state:
    st.session_state.saved_deals = []
if "show_contact_form" not in st.session_state:
    st.session_state.show_contact_form = {}

# --- Handlers ---
@st.cache_resource
def init_handlers():
    return WebScraper(), LLMHandler(), TemplateGenerator()

scraper, llm, template_gen = init_handlers()

# --- HEADER ---
st.markdown(
    """
<div style="
    background: linear-gradient(135deg, #1B2B4D 0%, #2C3E5E 100%);
    color: white; text-align: center;
    margin: 0 -3rem; padding: 70px 20px;
">
  <h1 style="font-weight:700; font-size:2rem;">Deal Discovery & Sourcing</h1>
  <p style="color:#CBD5E0;">AI-powered investment opportunity discovery from global platforms</p>
</div>
""",
    unsafe_allow_html=True,
)

# --- STEP TRACKER ---
st.markdown(
    """
<style>
.step-container {
    background-color: #F6F5F2;
    margin: 0 -3rem;
    padding: 20px 40px;
    display: flex; justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
}

.steps {
    display: flex; justify-content: center; align-items: center; gap: 12px; flex: 1;
}

.step {
    display: flex; flex-direction: column; align-items: center; gap: 8px;
}

.circle {
    width: 40px; height: 40px; border-radius: 50%;
    display: flex; justify-content: center; align-items: center;
    font-weight: 600; font-size: 0.95rem;
}

.circle.active { background-color: #138074; color: white; box-shadow: 0 3px 10px rgba(19,128,116,0.4);}
.circle.inactive { background-color: #D1D5DB; color: #9CA3AF;}

.label { font-size: 0.8rem; font-weight: 600;}
.label.active { color: #138074;}
.label.inactive { color: #9CA3AF;}

.line {
    height: 2px; width: 40px; background: #D1D5DB; align-self: center;
}

.link {
    text-decoration: none; color: #138074; font-weight: 600; font-size: 0.9rem;
}
</style>

<div class="step-container">
  <a href="streamlit_app.py" class="link">Back to Home</a>
  <div class="steps">
    <div class="step">
      <div class="circle active">1</div><div class="label active">Deal Sourcing</div>
    </div>
    <div class="line"></div>
    <div class="step">
      <div class="circle inactive">2</div><div class="label inactive">Due Diligence</div>
    </div>
    <div class="line"></div>
    <div class="step">
      <div class="circle inactive">3</div><div class="label inactive">Market</div>
    </div>
    <div class="line"></div>
    <div class="step">
      <div class="circle inactive">4</div><div class="label inactive">Financials</div>
    </div>
    <div class="line"></div>
    <div class="step">
      <div class="circle inactive">5</div><div class="label inactive">Memo</div>
    </div>
  </div>
  <div style="color:#999;font-size:0.9rem;">Regulus AI</div>
</div>
""",
    unsafe_allow_html=True,
)

# ========================
# DEFINE INVESTMENT CRITERIA
# ========================
with st.expander("Define Investment Criteria", expanded=True):
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("**Unattractive Industry Screening** - Exclude sectors per QDB list")
    with col2:
        enable_filter = st.checkbox("Enable Filter", True)

    industries = st.multiselect(
        "Target Industries",
        ["Technology", "Healthcare", "Energy", "Finance", "Retail", "Manufacturing"],
        default=["Technology", "Healthcare"],
    )
    sectors = st.multiselect(
        "Sectors",
        ["Fintech", "ClimateTech", "HealthTech", "AI/ML", "SaaS"],
        default=["Fintech"],
    )

    stage = st.multiselect("Stage", ["Pre-Seed", "Seed", "Series A", "Growth"], ["Seed"])
    geography = st.multiselect("Geography", ["MENA", "Europe", "North America"], ["MENA"])
    deal_count = st.number_input("Deals to source", 5, 50, 15, 5)

# ========================
# DATA SOURCE SELECTION
# ========================
st.subheader("Select Data Sources")

sources = st.multiselect(
    "Active Providers",
    ["Crunchbase", "AngelList", "PitchBook", "Magnitt", "Wamda", "Dealroom"],
    ["Crunchbase", "AngelList", "Magnitt"],
)

if sources:
    st.markdown("#### Selected:")
    cols = st.columns(len(sources))
    for i, src in enumerate(sources):
        with cols[i]:
            st.markdown(f"**{src}**")
            st.caption("Global funding and startup data")

# ========================
# CENTERED TEAL BUTTON
# ========================
colA, colB, colC = st.columns([1, 0.8, 1])
with colB:
    discover_clicked = st.button("Discover Deals", type="primary", use_container_width=True)

st.markdown(
    """
<style>
div.stButton > button:first-child {
    background: linear-gradient(135deg, #138074 0%, #0e5f55 100%) !important;
    color: white !important; border: none !important; border-radius: 40px !important;
    padding: 12px 30px !important; font-weight:700 !important; font-size:0.95rem !important;
    box-shadow: 0 4px 10px rgba(19,128,116,0.3); transition:all 0.2s ease;
}
div.stButton > button:first-child:hover {
    background: linear-gradient(135deg,#0e5f55 0%,#138074 100%) !important;
    transform: translateY(-2px);
}
</style>
""",
    unsafe_allow_html=True,
)

# ========================
# DISCOVER DEALS
# ========================
if discover_clicked:
    all_deals = []
    st.info("Fetching deals...")
    for i in range(deal_count):
        all_deals.append(
            {
                "Company": f"Startup {i+1}",
                "Industry": industries[i % len(industries)],
                "Sector": sectors[i % len(sectors)],
                "Stage": stage[0],
                "Region": geography[0],
                "Ticket": f"${(i % 5) + 1}M",
            }
        )
    st.session_state.discovered_deals = all_deals
    st.success(f"Discovered {len(all_deals)} potential deals!")

# ========================
# DISPLAY RESULTS
# ========================
if st.session_state.discovered_deals:
    st.markdown("### Discovered Deals")
    df = pd.DataFrame(st.session_state.discovered_deals)
    st.dataframe(df, use_container_width=True)

# ========================
# FOOTER
# ========================
st.markdown(
    """
<div style="background-color:#1B2B4D;color:#E2E8F0;padding:25px 20px;margin:40px -3rem 0 -3rem;">
  <div style="display:flex;justify-content:space-between;align-items:center;max-width:1400px;margin:0 auto;">
    <p>© 2025 Regulus AI. All rights reserved.</p>
    <p>Powered by Regulus AI</p>
  </div>
</div>
""",
    unsafe_allow_html=True,
)
