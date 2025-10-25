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

    [ Explore Analysis Workflows ](#choose-pathnsafe_allow_html=True,
)

# ===== TOP NAVIGATION =====
nav_cols = st.columns(5)
with nav_cols[0]:
    if st.button("Deal Sourcing"):
        st.switch_page("pages/1_Deal_Sourcing.py")
with nav_cols[1]:
    if st.button("Due Diligence"):
        st.switch_page("pages/2_Due_Diligence.py")
with nav_cols[2]:
    if st.button("Market Analysis"):
        st.switch_page("pages/3_Market_Analysis.py")
with nav_cols[3]:
    if st.button("Financial Modeling"):
        st.switch_page("pages/4_Financial_Modeling.py")
with nav_cols[4]:
    if st.button("Investment Memo"):
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

qdb_section_end()

# ===== FOOTER (Minimal Width + Branding) =====
st.markdown(
    f"""
    - [About Regulus](# - Careers
    - [ContactUs
    - Privacy Policy
    - Terms & Conditions
    <br>
    Powered by Regulus AI
    {'<img src="'+regulus_logo+'" height="32" style="margin-left:8px;" />' if regulus_logo else "<b>Regulus</b>"}
    """,
    unsafe_allow_html=True,
)
