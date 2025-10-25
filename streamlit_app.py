"""Investment Analyst AI – Regulus Edition | Enhanced Page Navigation"""
import streamlit as st
import base64
import os
from utils.qdb_styling import (
    apply_qdb_styling,
    qdb_section_start,
    qdb_section_end,
)

# --- Page configuration
st.set_page_config(
    page_title="Investment Analyst AI - Regulus",
    layout="wide",
    initial_sidebar_state="collapsed",
)

apply_qdb_styling()

# === Helper: Encode image for logos ===
def encode_image(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f"data:image/png;base64,{base64.b64encode(f.read()).decode()}"
    return None


# === Logos
qdb_logo = encode_image("QDB_Logo.png")
regulus_logo = encode_image("regulus_logo.png")

# ===== HERO =====
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
            <p style='color:#CBD5E0;font-size:1.05rem;max-width:700px;margin:auto;'>Supporting Qatar’s economic vision with data‑driven investment insights.</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ===== TOP NAVIGATION =====
st.markdown(
    """
    <style>
    .nav-row {
        display:flex;
        justify-content:center;
        gap:40px;
        padding:22px 0;
        background-color:#F6F6F6;
        margin:-10px -3rem 0 -3rem;
    }
    .nav-btn {
        background:none;
        border:none;
        color:#1B2B4D;
        font-weight:600;
        font-size:1.05rem;
        cursor:pointer;
        transition: all 0.3s ease;
        padding-bottom:4px;
        border-bottom:2px solid transparent;
    }
    .nav-btn:hover {
        color:#319795;
        border-color:#319795;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

nav_cols = st.columns(5)
nav_links = [
    ("Deal Sourcing", "pages/1_Deal_Sourcing.py"),
    ("Due Diligence", "pages/2_Due_Diligence.py"),
    ("Market Analysis", "pages/3_Market_Analysis.py"),
    ("Financial Modeling", "pages/4_Financial_Modeling.py"),
    ("Investment Memo", "pages/5_Investment_Memo.py"),
]

for idx, (title, path) in enumerate(nav_links):
    with nav_cols[idx]:
        st.page_link(path, label=title, icon="🌐")

# ===== LIGHT SECTION =====
qdb_section_start("light")
st.markdown(
    """
    <div style='text-align:center; max-width:900px; margin:0 auto 35px auto;'>
        <h2 style='color:#1B2B4D; font-weight:700;'>Choose Your Analysis Path</h2>
        <p style='color:#555; font-size:1.05rem;'>Start your workflow below or use the menu above.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

col1, col2, col3 = st.columns([1, 1, 1])

# === Path Cards ===
def nav_card(title, desc, features, page, color):
    st.markdown(
        f"""
        <div style="background:{'#ffffff' if color=='teal' else '#1B2B4D'};
                    color:{'#1B2B4D' if color=='teal' else '#E2E8F0'};
                    border-radius:14px;
                    padding:28px 25px;
                    box-shadow:0 5px 14px rgba(0,0,0,0.08);
                    text-align:left;
                    transition:transform 0.25s ease; height:100%;">
            <h3 style="margin-bottom:12px;">{title}</h3>
            <ul style="padding-left:18px; line-height:1.7;">
                {''.join(f'<li>{f}</li>' for f in features)}
            </ul>
            <br>
            <a href='/{page}' target='_self'
               style='text-decoration:none; background-color:{'#319795' if color=='teal' else '#2D3748'};
                      color:white; padding:10px 25px; border-radius:30px;
                      font-weight:600; font-size:0.95rem;
                      transition:background-color 0.3s ease;'>
               Start {title.split()[0]} →
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col1:
    nav_card(
        "Deal Sourcing",
        "AI‑driven lead generation and intelligence.",
        ["Identify high‑potential startups", "Filter by sector and stage", "Export to Due Diligence"],
        "pages/1_Deal_Sourcing.py",
        "teal",
    )

with col2:
    nav_card(
        "Due Diligence",
        "Systematic evaluation of company readiness.",
        ["Upload reports", "Score financial health", "Identify red flags"],
        "pages/2_Due_Diligence.py",
        "gray",
    )

with col3:
    nav_card(
        "Market Analysis",
        "Assess trends and competitive dynamics.",
        ["Review industry data", "Map competitors", "Generate insights for memo"],
        "pages/3_Market_Analysis.py",
        "teal",
    )

qdb_section_end()

# ===== FOOTER =====
st.markdown(
    f"""
    <div style='background:#1B2B4D; color:#A0AEC0; padding:25px 30px; margin-top:50px;
                border-radius:10px 10px 0 0; text-align:center;'>
        Powered by Regulus AI
        {'<img src="'+regulus_logo+'" style="max-height:40px; vertical-align:middle; margin-left:10px;">' if regulus_logo else ''}
    </div>
    """,
    unsafe_allow_html=True,
)
