"""Investment Analyst AI – Regulus Edition | Final Fixed Navigation"""
import streamlit as st
import base64
import os
from utils.qdb_styling import (
    apply_qdb_styling,
    qdb_section_start,
    qdb_section_end,
)

# ---------- PAGE CONFIGURATION ----------
st.set_page_config(
    page_title="Investment Analyst AI - Regulus",
    layout="wide",
    initial_sidebar_state="collapsed",
)
apply_qdb_styling()

# ---------- UTILITIES ----------
def encode_image(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f"data:image/png;base64,{base64.b64encode(f.read()).decode()}"
    return None

qdb_logo = encode_image("QDB_Logo.png")
regulus_logo = encode_image("regulus_logo.png")

# ---------- HERO SECTION ----------
st.markdown(
    f"""
    <div style="
        background: linear-gradient(135deg,#1B2B4D 0%,#2C3E5E 100%);
        color: white;
        text-align: center;
        margin: 0 -3rem;
        padding: 110px 20px 90px 20px;
        position: relative;
        overflow: hidden;">
        <div style='position:absolute; top:25px; left:35px;'>
            <img src='{qdb_logo}' style='max-height:70px;' alt='QDB Logo'>
        </div>
        <div style='max-width:950px; margin:0 auto;'>
            <h1 style='font-size:2.6rem;font-weight:700;margin-bottom:0.3rem;'>Investment Analyst AI</h1>
            <p style='color:#CBD5E0;font-size:1.05rem;max-width:700px;margin:auto;'>Empowering investment decisions with data‑driven intelligence.</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------- TOP NAVIGATION ----------
st.markdown(
    """
    <style>
    .nav-bar {
        display:flex;
        justify-content:center;
        gap:40px;
        padding:22px 0;
        background-color:#F6F6F6;
        margin:-10px -3rem 0 -3rem;
    }
    .nav-button {
        color:#1B2B4D;
        font-weight:600;
        font-size:1.05rem;
        border:none;
        background:none;
        cursor:pointer;
        transition:all 0.3s ease;
        border-bottom:2px solid transparent;
        padding-bottom:3px;
    }
    .nav-button:hover {
        color:#319795;
        border-color:#319795;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Streamlit must know these pages exist in /pages folder
nav_links = [
    ("Deal Sourcing", "pages/1_Deal_Sourcing.py"),
    ("Due Diligence", "pages/2_Due_Diligence.py"),
    ("Market Analysis", "pages/3_Market_Analysis.py"),
    ("Financial Modeling", "pages/4_Financial_Modeling.py"),
    ("Investment Memo", "pages/5_Investment_Memo.py"),
]

cols = st.columns(len(nav_links))
for i, (label, path) in enumerate(nav_links):
    with cols[i]:
        if st.button(label, key=f"topnav_{i}"):
            # st.switch_page works reliably with exact file structure
            st.switch_page(path)

# ---------- CHOOSE PATH SECTION ----------
qdb_section_start("light")

st.markdown(
    """
    <div style='text-align:center; max-width:900px; margin:0 auto 35px auto;'>
        <h2 style='color:#1B2B4D; font-weight:700;'>Choose Your Analysis Path</h2>
        <p style='color:#555; font-size:1.05rem;'>Start your workflow below or use the navigation above.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

col1, col2, col3 = st.columns([1,1,1])

# Helper layout for consistent cards
def nav_card(title, bullets, page, theme):
    bg = "#FFF" if theme == "light" else "#1B2B4D"
    text = "#1B2B4D" if theme == "light" else "#E2E8F0"
    btn = "#319795" if theme == "light" else "#2D3748"
    hover = "#2C7A7B" if theme == "light" else "#4A5568"

    st.markdown(
        f"""
        <div style="background:{bg};
                    color:{text};
                    border-radius:15px;
                    padding:30px;
                    box-shadow:0 5px 15px rgba(0,0,0,0.08);
                    display:flex;
                    flex-direction:column;
                    justify-content:space-between;
                    height:380px;">
            <div>
                <h3 style="margin-bottom:10px;">{title}</h3>
                <ul style="padding-left:18px; line-height:1.8;">
                    {''.join(f'<li>{b}</li>' for b in bullets)}
                </ul>
            </div>
            <div style="text-align:center; margin-top:10px;">
                <a href='/{page}' target='_self'
                   style='text-decoration:none;
                          background:{btn};
                          color:white;
                          padding:10px 25px;
                          border-radius:30px;
                          font-weight:600;
                          font-size:0.95rem;
                          transition:background-color 0.3s ease;'>
                   Start →
                </a>
            </div>
        </div>
        <style>
        a[href='/{page}']:hover {{
            background-color:{hover} !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

with col1:
    nav_card(
        "Deal Sourcing",
        ["Find and rank promising startups", "Filter by sector & region", "Export to Due Diligence"],
        "pages/1_Deal_Sourcing.py",
        "light",
    )

with col2:
    nav_card(
        "Due Diligence",
        ["Upload files for review", "Automated risk highlights", "Collaborate on findings"],
        "pages/2_Due_Diligence.py",
        "dark",
    )

with col3:
    nav_card(
        "Market Analysis",
        ["Gather sector reports", "Compare trends and players", "Feed results to Memo prep"],
        "pages/3_Market_Analysis.py",
        "light",
    )

qdb_section_end()

# ---------- FOOTER ----------
st.markdown(
    f"""
    <div style='background:#1B2B4D; color:#A0AEC0; padding:25px 30px; margin-top:60px;
                border-radius:10px 10px 0 0; text-align:center; font-size:0.9rem;'>
        Powered by Regulus AI
        {'<img src="'+regulus_logo+'" style="max-height:40px; vertical-align:middle; margin-left:10px;">' if regulus_logo else ''}
    </div>
    """,
    unsafe_allow_html=True,
)
