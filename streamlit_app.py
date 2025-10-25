"""Investment Analyst AI – Regulus Edition | Original Design Restored + Page Navigation"""
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


def encode_image(path):
    """Safely embed logos"""
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f"data:image/png;base64,{base64.b64encode(f.read()).decode()}"
    return None


qdb_logo = encode_image("QDB_Logo.png")
regulus_logo = encode_image("regulus_logo.png")

# ---------- HERO SECTION ----------
st.markdown(
    f"""
    <div style="background: linear-gradient(135deg,#1B2B4D 0%,#2C3E5E 100%);
                color:white;text-align:center;margin:0 -3rem;padding:110px 20px 90px 20px;
                position:relative;overflow:hidden;">
        <div style='position:absolute; top:25px; left:35px;'>
            <img src='{qdb_logo}' style='max-height:70px;' alt='QDB Logo'>
        </div>
        <div style='max-width:950px;margin:0 auto;'>
            <h1 style='font-size:2.5rem;font-weight:700;margin-bottom:0.4rem;'>Investment Analyst AI</h1>
            <p style='color:#E2E8F0;font-size:1.05rem;max-width:720px;margin:0 auto 30px;'>
                Supporting Qatar's Economic Vision with Data‑Driven Investment Insights
            </p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------- MAIN PAGE NAVIGATION BUTTONS ----------
st.markdown(
    """
    <style>
    .mainbuttons {
        display:flex;
        flex-wrap:wrap;
        justify-content:center;
        gap:20px;
        margin:50px 0 40px 0;
    }
    .qbtn {
        border:none;
        cursor:pointer;
        font-weight:600;
        border-radius:40px;
        padding:12px 32px;
        transition:all 0.3s ease;
        font-size:0.95rem;
        text-decoration:none;
    }
    .graybtn {
        background-color:#2D3748;
        color:white;
    }
    .graybtn:hover {
        background-color:#4A5568;
    }
    .tealbtn {
        background-color:#319795;
        color:#fff;
    }
    .tealbtn:hover {
        background-color:#2C7A7B;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="mainbuttons">
        <a href="/pages/1_Deal_Sourcing" class="qbtn tealbtn">Deal Sourcing</a>
        <a href="/pages/2_Due_Diligence" class="qbtn graybtn">Due Diligence</a>
        <a href="/pages/3_Market_Analysis" class="qbtn tealbtn">Market Analysis</a>
        <a href="/pages/4_Financial_Modeling" class="qbtn graybtn">Financial Modeling</a>
        <a href="/pages/5_Investment_Memo" class="qbtn tealbtn">Investment Memo</a>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------- LIGHT SECTION ----------
qdb_section_start("light")

st.markdown(
    """
    <div style='text-align:center;max-width:950px;margin:0 auto 35px auto;'>
        <h2 style='color:#1B2B4D;font-weight:700;'>Your Pathways</h2>
        <p style='color:#555;font-size:1.05rem;'>Start your workflow below or use the buttons above.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

col1, col2 = st.columns(2, gap="large")

# ---------- Custom Card ----------
def workflow_card(title, color, bullets, page):
    bg = "#FFF" if color == "light" else "#1B2B4D"
    text = "#1B2B4D" if color == "light" else "#E2E8F0"
    btn = "#319795" if color == "light" else "#2D3748"
    btn_hover = "#2C7A7B" if color == "light" else "#4A5568"

    st.markdown(
        f"""
        <div style="background:{bg};color:{text};
                    border-radius:16px;padding:35px;
                    box-shadow:0 4px 15px rgba(0,0,0,0.08);
                    border-top:4px solid #2C3E5E;
                    display:flex;flex-direction:column;
                    justify-content:space-between;height:380px;">
            <div>
                <h3 style="font-size:1.5rem;margin-bottom:15px;">{title}</h3>
                <ul style="padding-left:18px;line-height:1.8;">
                    {''.join(f'<li>{b}</li>' for b in bullets)}
                </ul>
            </div>
            <div style="text-align:center;margin-top:10px;">
                <a href='/{page}' target='_self' style='text-decoration:none;
                    background-color:{btn};color:white;
                    padding:10px 28px;border-radius:30px;
                    font-weight:600;transition:background-color 0.3s ease;'>Start →</a>
                <style>a[href='/{page}']:hover{{background:{btn_hover}!important;}}</style>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---------- LIGHT / DARK Sections Cards ----------
with col1:
    workflow_card(
        "Deal Sourcing",
        "light",
        ["AI‑powered identification", "Ranking by growth potential", "Export results to Due Diligence"],
        "pages/1_Deal_Sourcing",
    )

with col2:
    workflow_card(
        "Due Diligence",
        "dark",
        ["Upload company files", "Risk factor detection", "Generate summary report"],
        "pages/2_Due_Diligence",
    )

qdb_section_end()

# ---------- FOOTER ----------
st.markdown(
    f"""
    <div style='background:#1B2B4D;color:#A0AEC0;padding:25px 30px;
                margin-top:50px;border-radius:10px 10px 0 0;
                text-align:center;font-size:0.9rem;'>
        Powered by Regulus AI
        {'<img src="'+regulus_logo+'" style="max-height:40px;vertical-align:middle;margin-left:10px;">' if regulus_logo else ''}
    </div>
    """,
    unsafe_allow_html=True,
)
