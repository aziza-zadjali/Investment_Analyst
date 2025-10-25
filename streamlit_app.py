"""Investment Analyst AI – Regulus Edition | Original Layout Restored"""
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

def encode_image(path):
    """Safely embed logos"""
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f"data:image/png;base64,{base64.b64encode(f.read()).decode()}"
    return None

# --- Load logos
qdb_logo = encode_image("QDB_Logo.png")
regulus_logo = encode_image("regulus_logo.png")

# ===== HERO SECTION (unchanged) =====
st.markdown(
    f"""
    <div style="background: linear-gradient(135deg, #1B2B4D 0, #2C3E5E 100);
                color: white; text-align: center; margin: 0 -3rem;
                padding: 110px 20px 100px 20px; position: relative;
                overflow: hidden;">
        <div style="position:absolute; top:25px; left:35px;">
            <img src="{qdb_logo}" style="max-height:70px;" alt="QDB Logo" />
        </div>
        <div style="max-width:950px; margin:0 auto;">
            <h1 style="font-size:2.5rem;font-weight:700;letter-spacing:-0.3px;">
                Investment Analyst AI
            </h1>
            <p style="color:#E2E8F0;font-size:1.05rem;margin-bottom:8px;">
                Supporting Qatar's Economic Vision with Data‑Driven Investment Insights
            </p>
            <p style="color:#CBD5E0;font-size:0.95rem;line-height:1.6;
                      max-width:720px;margin:0 auto 30px;">
                End‑to‑End AI Platform for Deal Sourcing, Due Diligence, Market Analysis
                & Investment Memoranda
            </p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ===== BUTTON BAR (exact original gray/teal style) =====
st.markdown(
    """
    <style>
    .nav-btns {
        display:flex;
        flex-wrap:wrap;
        justify-content:center;
        gap:18px;
        margin:60px 0 40px 0;
    }
    .btn {
        border:none;
        border-radius:40px;
        padding:12px 30px;
        font-weight:600;
        font-size:0.95rem;
        color:white;
        cursor:pointer;
        transition: background-color 0.3s ease;
        text-decoration:none;
    }
    .btn.teal {background-color:#319795;}
    .btn.teal:hover {background-color:#2C7A7B;}
    .btn.gray {background-color:#2D3748;}
    .btn.gray:hover {background-color:#4A5568;}
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Preserves layout: alternating teal / gray
st.markdown(
    """
    <div class="nav-btns">
        <a class="btn teal" href="/pages/1_Deal_Sourcing">Deal Sourcing</a>
        <a class="btn gray" href="/pages/2_Due_Diligence">Due Diligence</a>
        <a class="btn teal" href="/pages/3_Market_Analysis">Market Analysis</a>
        <a class="btn gray" href="/pages/4_Financial_Modeling">Financial Modeling</a>
        <a class="btn teal" href="/pages/5_Investment_Memo">Investment Memo</a>
    </div>
    """,
    unsafe_allow_html=True,
)

# ===== LIGHT SECTION (same spacing, unchanged) =====
qdb_section_start("light")
st.markdown(
    """
    <div style="text-align:center; max-width:950px; margin:0 auto 35px auto;">
        <h2 style="color:#1B2B4D; font-size:2rem; font-weight:700; margin-bottom:10px;">
            Choose Your Analysis Path
        </h2>
        <p style="color:#555; font-size:1.05rem;">
            Start your workflow below or use the navigation above.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- Two-column section preserved
col1, col2 = st.columns(2, gap="large")

def section_card(title, bullets, color_theme, page):
    bg = "#FFF" if color_theme == "light" else "#1B2B4D"
    text = "#1B2B4D" if color_theme == "light" else "#E2E8F0"
    button = "#319795" if color_theme == "light" else "#2D3748"
    hover = "#2C7A7B" if color_theme == "light" else "#4A5568"
    st.markdown(
        f"""
        <div style="background:{bg};color:{text};
                    border-radius:16px;padding:35px;height:390px;
                    box-shadow:0 5px 20px rgba(0,0,0,0.08);
                    border-top:4px solid #2C3E5E;
                    display:flex;flex-direction:column;justify-content:space-between;">
            <div>
                <h3 style="font-size:1.6rem;font-weight:600;margin-bottom:16px;">
                    {title}
                </h3>
                <ul style="margin-top:10px;line-height:1.9;color:{text};">
                    {''.join(f'<li>{point}</li>' for point in bullets)}
                </ul>
            </div>
            <div style="text-align:center;margin-top:10px;">
                <a href='/{page}' style='text-decoration:none;
                    background-color:{button};
                    color:white;padding:10px 28px;border-radius:30px;
                    font-weight:600;transition:background-color 0.3s ease;'>
                    Start →
                </a>
                <style>a[href='/{page}']:hover{{background-color:{hover}!important;}}</style>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col1:
    section_card(
        "Deal Sourcing Path",
        ["AI‑powered deal sourcing", "Market data hand‑off", "Prepare next stage"],
        "light",
        "pages/1_Deal_Sourcing",
    )

with col2:
    section_card(
        "Due Diligence Path",
        ["Upload and analyze reports", "Benchmark company data", "Generate memo"],
        "dark",
        "pages/2_Due_Diligence",
    )

qdb_section_end()

# ===== FOOTER SECTION (untouched) =====
st.markdown(
    f"""
    <div style="background-color:#1B2B4D;color:#E2E8F0;
                padding:25px 20px;margin:0 auto;width:85%;
                border-radius:15px 15px 0 0;font-size:0.94rem;">
        <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;">
            <div style="flex:3;">
                <ul style="list-style:none;display:flex;gap:25px;flex-wrap:wrap;padding:0;margin:0;">
                    <li><a href="#" style="text-decoration:none;color:#E2E8F0;">About Regulus</a></li>
                    <li><a href="#" style="text-decoration:none;color:#E2E8F0;">Careers</a></li>
                    <li><a href="#" style="text-decoration:none;color:#E2E8F0;">Contact Us</a></li>
                    <li><a href="#" style="text-decoration:none;color:#E2E8F0;">Privacy Policy</a></li>
                    <li><a href="#" style="text-decoration:none;color:#E2E8F0;">Terms</a></li>
                </ul>
            </div>
            <div style="flex:1;text-align:right;">
                <p style="margin:0;color:#A0AEC0;font-size:0.9rem;">Powered by Regulus AI</p>
                {"<img src='"+regulus_logo+"' style='max-height:55px;margin-top:6px;opacity:0.95;' alt='Regulus Logo'>" if regulus_logo else "<b>Regulus</b>"}
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
