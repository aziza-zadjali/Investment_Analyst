"""
Investment Analyst AI - QDB Official Branding
Styled to match Qatar Development Bank corporate website (qdb.qa)
"""

import streamlit as st
import base64
import os

st.set_page_config(
    page_title="Investment Analyst AI - QDB",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# QDB Official Brand Colors
QDB_PURPLE = "#5E2A84"
QDB_GOLD = "#C69C6D"
QDB_DARK_BLUE = "#1B2B4D"
QDB_LIGHT_GRAY = "#F5F5F5"


# Helper function
def encode_image(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f"data:image/png;base64,{base64.b64encode(f.read()).decode()}"
    return None


qdb_logo = encode_image("QDB_Logo.png")
regulus_logo = encode_image("regulus_logo.png")


# --- QDB OFFICIAL STYLING ---
st.markdown(f"""
<style>
/* Hide Streamlit defaults */
[data-testid="stSidebar"] {{visibility: hidden;}}
.main > div {{padding-top: 1.5rem;}}

/* QDB Brand Buttons */
.stButton > button {{
    background: linear-gradient(135deg, {QDB_PURPLE} 0%, {QDB_DARK_BLUE} 100%);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 14px 32px;
    font-size: 1.05rem;
    font-weight: 600;
    letter-spacing: 0.5px;
    box-shadow: 0 4px 12px rgba(94, 42, 132, 0.3);
    transition: all 0.3s ease;
}}
.stButton > button:hover {{
    background: linear-gradient(135deg, {QDB_DARK_BLUE} 0%, {QDB_PURPLE} 100%);
    box-shadow: 0 6px 16px rgba(94, 42, 132, 0.45);
    transform: translateY(-2px);
}}

/* Header Container */
.qdb-header {{
    display: grid;
    grid-template-columns: 1fr 2fr 1fr;
    align-items: center;
    padding: 25px 0 35px 0;
    max-width: 1200px;
    margin: 0 auto;
    border-bottom: 3px solid {QDB_PURPLE};
}}
.qdb-logo {{
    text-align: center;
}}
.qdb-logo img {{
    max-height: 90px;
    object-fit: contain;
}}
.qdb-title {{
    text-align: center;
}}
.qdb-title h1 {{
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-size: 2.8rem;
    font-weight: 700;
    color: {QDB_DARK_BLUE};
    margin-bottom: 8px;
    letter-spacing: -0.5px;
}}
.qdb-title p {{
    color: #666;
    font-size: 1.15rem;
    font-weight: 400;
    margin: 0;
}}

/* Pathway Cards (QDB Style) */
.qdb-card {{
    background: white;
    border-radius: 12px;
    padding: 35px;
    height: 420px;
    box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
    border-left: 5px solid {QDB_PURPLE};
    transition: all 0.3s ease;
    display: flex;
    flex-direction: column;
}}
.qdb-card:hover {{
    box-shadow: 0 8px 30px rgba(94, 42, 132, 0.2);
    transform: translateY(-5px);
}}
.qdb-card h2 {{
    color: {QDB_PURPLE};
    font-size: 1.9rem;
    font-weight: 700;
    margin-bottom: 18px;
}}
.qdb-card p {{
    font-size: 1.05rem;
    line-height: 1.7;
    color: #555;
}}
.qdb-card-footer {{
    margin-top: auto;
    padding-top: 20px;
    border-top: 2px solid {QDB_LIGHT_GRAY};
    font-size: 0.95rem;
    color: {QDB_GOLD};
    font-weight: 600;
}}

@media (max-width: 900px) {{
    .qdb-header {{grid-template-columns: 1fr;}}
}}
</style>
""", unsafe_allow_html=True)


# --- HEADER SECTION ---
st.markdown("<div class='qdb-header'>", unsafe_allow_html=True)

# Left logo
if qdb_logo:
    st.markdown(f"<div class='qdb-logo'><img src='{qdb_logo}'></div>", unsafe_allow_html=True)
else:
    st.markdown("<div class='qdb-logo'><strong>Qatar Development Bank</strong></div>", unsafe_allow_html=True)

# Center title
st.markdown("""
<div class='qdb-title'>
    <h1>Investment Analyst AI</h1>
    <p>Intelligent Investment Analysis Platform</p>
</div>
""", unsafe_allow_html=True)

# Right logo
if regulus_logo:
    st.markdown(f"<div class='qdb-logo'><img src='{regulus_logo}'></div>", unsafe_allow_html=True)
else:
    st.markdown("<div class='qdb-logo'><strong>Regulus</strong></div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)


# --- INTRO SECTION ---
st.markdown(f"""
<div style='text-align:center;margin:40px 0 35px 0;'>
    <h2 style='color:{QDB_DARK_BLUE};font-size:2.2rem;margin-bottom:12px;font-weight:600;'>Choose Your Analysis Path</h2>
    <p style='color:#777;font-size:1.15rem;'>Select your investment workflow to begin comprehensive analysis</p>
</div>
""", unsafe_allow_html=True)


# --- PATH CARDS ---
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("""
    <div class='qdb-card'>
        <h2>Deal Sourcing Path</h2>
        <p><strong>Start here if you are:</strong></p>
        <ul style='margin-top:12px;line-height:2;'>
            <li>Looking for new investment opportunities</li>
            <li>Building your deal pipeline</li>
            <li>Discovering and filtering potential deals</li>
        </ul>
        <div class='qdb-card-footer'>
            <strong>Workflow:</strong> Deal Discovery → Due Diligence → Market → Financial → Memo
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚀 Start Deal Sourcing", use_container_width=True, key="btn_deal"):
        st.switch_page("pages/1_Deal_Sourcing.py")

with col2:
    st.markdown("""
    <div class='qdb-card'>
        <h2>Due Diligence Path</h2>
        <p><strong>Start here if you have:</strong></p>
        <ul style='margin-top:12px;line-height:2;'>
            <li>Received investment proposals</li>
            <li>Company documents to analyze</li>
            <li>Need deep-dive due diligence</li>
        </ul>
        <div class='qdb-card-footer'>
            <strong>Workflow:</strong> Due Diligence → Market → Financial → Memo
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("📋 Start Due Diligence", use_container_width=True, key="btn_dd"):
        st.switch_page("pages/2_Due_Diligence_Analysis.py")


# --- QUICK TOOLS ---
st.markdown("<br><br>", unsafe_allow_html=True)
with st.expander("🔧 Direct Access to Specific Tools"):
    col_t1, col_t2, col_t3 = st.columns(3)
    with col_t1:
        if st.button("📊 Market Analysis", use_container_width=True):
            st.switch_page("pages/3_Market_Analysis.py")
    with col_t2:
        if st.button("💰 Financial Modeling", use_container_width=True):
            st.switch_page("pages/4_Financial_Modeling.py")
    with col_t3:
        if st.button("📝 Investment Memo", use_container_width=True):
            st.switch_page("pages/5_Investment_Memo.py")


# --- FOOTER ---
st.markdown(f"<div style='height:3px;background:{QDB_PURPLE};margin:50px 0 25px 0;border-radius:2px;'></div>", unsafe_allow_html=True)
col_f1, col_f2, col_f3 = st.columns([1, 2, 1])
with col_f1:
    st.markdown(f"<p style='text-align:left;color:{QDB_DARK_BLUE};font-weight:500;'>© 2025 Qatar Development Bank</p>", unsafe_allow_html=True)
with col_f2:
    st.markdown("<p style='text-align:center;color:#999;'><strong>Investment Analyst AI</strong> | Version 1.0.0</p>", unsafe_allow_html=True)
with col_f3:
    st.markdown(f"<p style='text-align:right;color:{QDB_GOLD};font-weight:500;'>Powered by Regulus</p>", unsafe_allow_html=True)
