"""
Deal Discovery & Sourcing Page
Teal theme, visual workflow tracker, centered layout
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from utils.qdb_styling import apply_qdb_styling
import os
import base64

# --- Streamlit setup ---
st.set_page_config(page_title="Deal Discovery - Regulus", layout="wide", initial_sidebar_state="collapsed")
apply_qdb_styling()

# --- Helper for logo embedding (used only in header) ---
def encode_image(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f"data:image/png;base64," + base64.b64encode(f.read()).decode()
    return None

# --- Initialize Session ---
if "discovered_deals" not in st.session_state:
    st.session_state.discovered_deals = []
if "saved_deals" not in st.session_state:
    st.session_state.saved_deals = []
if "selected_deals" not in st.session_state:
    st.session_state.selected_deals = []
if "show_contact_form" not in st.session_state:
    st.session_state.show_contact_form = {}

# --- HERO HEADER (matches home page) ---
qdb_logo = encode_image("QDB_Logo.png")

st.markdown(
    f"""
<div style="
    background: linear-gradient(135deg,#1B2B4D 0%,#2C3E5E 100%);
    color:white; text-align:center;
    margin:0 -3rem; padding:60px 20px 50px 20px;
    position:relative; overflow:hidden;">
  <div style="position:absolute;top:20px;left:35px;">
    {"<img src='"+qdb_logo+"' style='max-height:60px;'>" if qdb_logo else "<b>QDB</b>"}
  </div>
  <div style="max-width:900px;margin:0 auto;">
    <h1 style="font-size:2.2rem;font-weight:700;">Deal Discovery & Sourcing</h1>
    <p style="color:#CBD5E0;font-size:0.95rem;">AI-powered investment opportunity discovery from verified sources.</p>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

# --- VISUAL 5-STEP WORKFLOW ---
st.markdown(
    """
<style>
.step-bar{background-color:#F6F5F2;margin:0 -3rem;padding:20px 40px;display:flex;justify-content:space-between;align-items:center;}
.step-track{display:flex;align-items:center;gap:14px;justify-content:center;flex:1;}
.step{display:flex;flex-direction:column;align-items:center;gap:6px;}
.circle{width:42px;height:42px;border-radius:50%;display:flex;justify-content:center;align-items:center;font-weight:600;}
.circle.active{background-color:#138074;color:#fff;box-shadow:0 3px 10px rgba(19,128,116,0.4);}
.circle.inactive{background-color:#D1D5DB;color:#9CA3AF;}
.label{font-size:0.8rem;font-weight:600;}
.label.active{color:#138074;}
.label.inactive{color:#9CA3AF;}
.line{width:50px;height:2px;background-color:#D1D5DB;}
.link{color:#138074;text-decoration:none;font-weight:600;}
.link:hover{color:#0e5f55;}
</style>

<div class="step-bar">
  <a href="streamlit_app.py" class="link">Back to Home</a>
  <div class="step-track">
    <div class="step"><div class="circle active">1</div><div class="label active">Deal Sourcing</div></div>
    <div class="line"></div>
    <div class="step"><div class="circle inactive">2</div><div class="label inactive">Due Diligence</div></div>
    <div class="line"></div>
    <div class="step"><div class="circle inactive">3</div><div class="label inactive">Market Analysis</div></div>
    <div class="line"></div>
    <div class="step"><div class="circle inactive">4</div><div class="label inactive">Financial Model</div></div>
    <div class="line"></div>
    <div class="step"><div class="circle inactive">5</div><div class="label inactive">Investment Memo</div></div>
  </div>
  <span style="color:#999;font-size:0.9rem;">Regulus AI</span>
</div>
""",
    unsafe_allow_html=True,
)

# --- DEFINE FILTERS ---
with st.expander("Define Investment Criteria", expanded=True):
    st.markdown("**Unattractive Industry Filter** – Exclude sectors tagged non-priority per QDB.")
    industries = st.multiselect(
        "Target Industries",
        ["Technology", "Healthcare", "Energy", "Finance", "Retail", "Manufacturing"],
        default=["Technology"],
    )
    sectors = st.multiselect(
        "Target Sectors",
        ["Fintech", "HealthTech", "AI/ML", "SaaS", "Cleantech"],
        default=["Fintech"],
    )
    stage = st.multiselect("Stage", ["Pre-Seed", "Seed", "Series A", "Growth"], ["Seed"])
    geography = st.multiselect("Regions", ["MENA", "Europe", "North America"], ["MENA"])
    deal_count = st.number_input("Deals to source", min_value=5, max_value=50, value=10, step=5)

# --- CENTERED TEAL BUTTON ---
st.markdown("<br>", unsafe_allow_html=True)
colA, colB, colC = st.columns([1, 0.8, 1])
with colB:
    discover_clicked = st.button("Discover Deals", type="primary", use_container_width=True)

st.markdown(
    """
<style>
div.stButton>button:first-child {
    background:linear-gradient(135deg,#138074,#0e5f55)!important;
    color:#fff!important;border:none!important;
    border-radius:40px!important;
    padding:12px 30px!important;
    font-weight:700!important;
    font-size:0.95rem!important;
    box-shadow:0 4px 10px rgba(19,128,116,0.3)!important;
    transition:all 0.2s ease!important;
}
div.stButton>button:first-child:hover {
    background:linear-gradient(135deg,#0e5f55,#138074)!important;
    transform:translateY(-2px)!important;
}
</style>
""",
    unsafe_allow_html=True,
)

# --- DISCOVER DEALS ACTION ---
if discover_clicked:
    st.session_state.discovered_deals = [
        {
            "Company": f"Startup {i+1}",
            "Industry": industries[i % len(industries)],
            "Sector": sectors[i % len(sectors)],
            "Stage": stage[0],
            "Region": geography[0],
            "Ticket Size": f"${(i%5)+1}M",
            "Contact": f"contact@startup{i+1}.com",
        }
        for i in range(deal_count)
    ]
    st.success(f"Discovered {len(st.session_state.discovered_deals)} potential deals!")

# --- DISPLAY DEALS TABLE ---
if st.session_state.discovered_deals:
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("Discovered Deals")
    df = pd.DataFrame(st.session_state.discovered_deals)
    st.dataframe(df, use_container_width=True)

# --- FOOTER (Full width, no logos) ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(
    """
<div style="background-color:#1B2B4D;color:#E2E8F0;padding:30px 40px;margin:40px -3rem 0 -3rem;font-size:0.94rem;">
  <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;max-width:1400px;margin:0 auto;">
    <div style="flex:2;">
      <ul style="list-style:none;display:flex;gap:30px;flex-wrap:wrap;padding:0;margin:0;">
        <li><a href="#" style="text-decoration:none;color:#E2E8F0;">About Regulus</a></li>
        <li><a href="#" style="text-decoration:none;color:#E2E8F0;">Careers</a></li>
        <li><a href="#" style="text-decoration:none;color:#E2E8F0;">Contact Us</a></li>
        <li><a href="#" style="text-decoration:none;color:#E2E8F0;">Privacy Policy</a></li>
      </ul>
    </div>
    <div style="flex:1;text-align:right;">
      <p style="margin:0;color:#A0AEC0;font-size:0.9rem;">Powered by Regulus AI</p>
    </div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)
