""" Investment Analyst AI – Regulus Edition Footer refined
 Powered by Regulus AI only """
import streamlit as st
import base64
import os
from utils.qdb_styling import (
    apply_qdb_styling, QDB_PURPLE, QDB_DARK_BLUE, qdb_section_start, qdb_section_end,
)

# --- Page configuration
st.set_page_config(
    page_title="Investment Analyst AI - Regulus",
    layout="wide",
    initial_sidebar_state="collapsed",
)
apply_qdb_styling()

def encode_image(path):
    """Safely embed logos"""
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f"data:image/png;base64,{base64.b64encode(f.read()).decode()}"
    return None

qdb_logo = encode_image("QDB_Logo.png")
regulus_logo = encode_image("regulus_logo.png")

# ===== HERO SECTION =====
st.markdown(
    f"""
    {'<img src="'+qdb_logo+'" height="48" style="margin-right:16px;" />' if qdb_logo else "<b>QDB</b>"}
    ## Investment Analyst AI

    Supporting Qatar’s Economic Vision with Data‑Driven Investment Insights  
    End‑to‑End AI Platform for Deal Sourcing, Due Diligence, Market Analysis & Investment Memoranda

     Explore Analysis Workflows 
    """,
    unsafe_allow_html=True,
)

# ===== TOP NAVIGATION =====
st.markdown(
    f"""
    <div style="display: flex; gap: 16px;">
        <div style="flex:1;">
            <b>Deal Sourcing</b>
            <br>
            <small>Discover and qualify investment opportunities using AI‑based ranking.</small>
        </div>
        <div style="flex:1;">
            <b>Due Diligence</b>
            <br>
            <small>Run comprehensive due diligence across financial, legal, and operational data.</small>
        </div>
        <div style="flex:1;">
            <b>Market Analysis</b>
            <br>
            <small>Extract actionable insights and competitive landscape summaries instantly.</small>
        </div>
        <div style="flex:1;">
            <b>Financial Modeling</b>
            <br>
            <small>Build predictive financial models with AI‑powered accuracy checks.</small>
        </div>
        <div style="flex:1;">
            <b>Investment Memo</b>
            <br>
            <small>Create professional‑grade summary memos ready for executive review.</small>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
nav_cols = st.columns(5)
with nav_cols[0]:
    if st.button("Go to Deal Sourcing", key="nav_deal"):
        st.switch_page("pages/1_Deal_Sourcing.py")
with nav_cols[1]:
    if st.button("Go to Due Diligence", key="nav_dd"):
        st.switch_page("pages/2_Due_Diligence.py")
with nav_cols[2]:
    if st.button("Go to Market Analysis", key="nav_market"):
        st.switch_page("pages/3_Market_Analysis.py")
with nav_cols[3]:
    if st.button("Go to Financial Modeling", key="nav_fin"):
        st.switch_page("pages/4_Financial_Modeling.py")
with nav_cols[4]:
    if st.button("Go to Investment Memo", key="nav_memo"):
        st.switch_page("pages/5_Investment_Memo.py")

# ===== CHOOSE PATH SECTION =====
st.markdown("\n", unsafe_allow_html=True)
qdb_section_start("light")
st.markdown(
    f"""
    ### Choose Your Analysis Path

    Start your workflow below or use the navigation above.
    """,
    unsafe_allow_html=True,
)

button_style = """
background-color:#319795; color:white; border:none; border-radius:40px; padding:12px 30px; font-size:0.95rem; font-weight:600; box-shadow:0 3px 12px rgba(49,151,149,0.3); text-decoration:none; transition:all 0.25s ease;
"""
hover_in = "this.style.backgroundColor='#2C7A7B'"
hover_out = "this.style.backgroundColor='#319795'"

col1, col2 = st.columns(2, gap="large")
with col1:
    st.markdown(
        f"""
        #### Deal Sourcing Path
        - AI‑powered deal identification
        - Market analysis handoff
        - Proceed to due diligence
        """,
        unsafe_allow_html=True,
    )
    if st.button("Start Deal Sourcing", key="start_deal"):
        st.switch_page("pages/1_Deal_Sourcing.py")
    st.markdown(
        f"""
        <br>
        <b>Market Analysis Handoff</b>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Go to Market Analysis", key="deal_market"):
        st.switch_page("pages/3_Market_Analysis.py")
    st.markdown(
        f"""
        <br>
        <b>Proceed to Due Diligence</b>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Go to Due Diligence", key="deal_dd"):
        st.switch_page("pages/2_Due_Diligence.py")

with col2:
    st.markdown(
        f"""
        #### Due Diligence Path
        - Upload and analyze company data
        - Market fit comparatives
        - Create Investment Memo
        """,
        unsafe_allow_html=True,
    )
    if st.button("Start Due Diligence", key="start_dd"):
        st.switch_page("pages/2_Due_Diligence.py")
    st.markdown(
        f"""
        <br>
        <b>Market Fit Comparatives</b>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Go to Market Analysis (from DD)", key="dd_market"):
        st.switch_page("pages/3_Market_Analysis.py")
    st.markdown(
        f"""
        <br>
        <b>Create Investment Memo</b>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Go to Investment Memo", key="dd_memo"):
        st.switch_page("pages/5_Investment_Memo.py")

qdb_section_end()

# ===== FOOTER (Minimal Width + Branding) =====
st.markdown(
    f"""
    - About Regulus
    - Careers
    - [Contact Us](# - Privacy Policy
    - [Terms & Conditions    <br>
    Powered by Regulus AI
    {'<img src="'+regulus_logo+'" height="32" style="margin-left:8px;" />' if regulus_logo else "<b>Regulus</b>"}
    """,
    unsafe_allow_html=True,
)
