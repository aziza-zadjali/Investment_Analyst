""" Investment Analyst AI – Regulus Edition Footer refined | Powered by Regulus AI only """

import streamlit as st
import base64
import os
from utils.qdb_styling import (
    apply_qdb_styling,
    QDB_PURPLE,
    QDB_DARK_BLUE,
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


qdb_logo = encode_image("QDB_Logo.png")
regulus_logo = encode_image("regulus_logo.png")

# ===== HERO SECTION =====
st.markdown(
    f"""<div style="background: linear-gradient(135deg, #1B2B4D 0, #2C3E5E 100%);
             color: white; text-align: center; margin: 0 -3rem;
             padding: 110px 20px 100px 20px; position: relative;
             overflow: hidden;">

        <!-- QDB Logo -->
        <div style="position:absolute; top:25px; left:35px;">
            <img src="{qdb_logo}" style="max-height:70px;" alt="QDB Logo" />
        </div>

        <!-- Central Content -->
        <div style="max-width:950px; margin:0 auto;">
            <h1 style="font-size:2.5rem; font-weight:700; letter-spacing:-0.3px;">
                Investment Analyst AI
            </h1>
            <p style="color:#E2E8F0; font-size:1.05rem; margin-bottom:8px;">
                Supporting Qatar's Economic Vision with Data‑Driven Investment Insights
            </p>
            <p style="color:#CBD5E0; font-size:0.95rem; line-height:1.6;
                      max-width:720px; margin:0 auto 30px;">
                End‑to‑End AI Platform for Deal Sourcing, Due Diligence, Market Analysis & Investment Memos
            </p>
        </div>
    </div>""",
    unsafe_allow_html=True,
)

# ===== TOP NAVIGATION =====
st.markdown(
    f"""<style>
        .topnav {{
            display:flex;
            flex-wrap:wrap;
            justify-content:center;
            gap:20px;
            margin:60px 0 40px 0;
        }}
        .topbtn {{
            border:none;
            border-radius:40px;
            padding:12px 32px;
            font-weight:600;
            font-size:0.95rem;
            cursor:pointer;
            transition:all 0.3s ease;
            text-decoration:none;
            color:white;
        }}
        .teal{{background-color:#319795;}}
        .teal:hover{{background-color:#2C7A7B;}}
        .gray{{background-color:#2D3748;}}
        .gray:hover{{background-color:#4A5568;}}
    </style>

    <div class="topnav">
        <a href="/pages/1_Deal_Sourcing" class="topbtn teal">Deal Sourcing</a>
        <a href="/pages/2_Due_Diligence" class="topbtn gray">Due Diligence</a>
        <a href="/pages/3_Market_Analysis" class="topbtn teal">Market Analysis</a>
        <a href="/pages/4_Financial_Modeling" class="topbtn gray">Financial Modeling</a>
        <a href="/pages/5_Investment_Memo" class="topbtn teal">Investment Memo</a>
    </div>""",
    unsafe_allow_html=True,
)

# ===== CHOOSE PATH SECTION =====
st.markdown("", unsafe_allow_html=True)

qdb_section_start("light")

st.markdown(
    f"""
    <div style='text-align:center; max-width:950px; margin:0 auto 35px auto;'>
        <h2 style='color:#1B2B4D; font-size:2rem; font-weight:700; margin-bottom:10px;'>
            Choose Your Analysis Path
        </h2>
        <p style='color:#555; font-size:1.05rem;'>Start your workflow below or use the navigation above.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

col1, col2 = st.columns(2, gap="large")

# ===== LIGHT SECTION CARDS =====
with col1:
    st.markdown(
        f"""
        <div style="background:white; border-radius:16px; padding:35px;
                    height:390px; box-shadow:0 5px 20px rgba(0,0,0,0.08);
                    border-top:4px solid #2C3E5E;
                    display:flex; flex-direction:column; justify-content:space-between;">
            <div>
                <h3 style="color:#1B2B4D; font-size:1.6rem; font-weight:600; margin-bottom:16px;">
                    Deal Sourcing Path
                </h3>
                <ul style="margin-top:10px; line-height:1.9; color:#333;">
                    <li>AI‑powered deal identification</li>
                    <li>Market analysis hand‑off</li>
                    <li>Proceed to due diligence</li>
                </ul>
            </div>
            <div style="text-align:center;">
                <a href='/pages/1_Deal_Sourcing' style='text-decoration:none;
                    background:#319795; color:white; padding:10px 25px;
                    border-radius:30px; font-weight:600; transition:background-color 0.3s ease;'>
                    Start →
                </a>
            </div>
        </div>""",
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        f"""
        <div style="background:#1B2B4D; border-radius:16px; padding:35px; height:390px;
                    box-shadow:0 5px 20px rgba(0,0,0,0.08); border-top:4px solid #2C3E5E;
                    display:flex; flex-direction:column; justify-content:space-between;">
            <div>
                <h3 style="color:#E2E8F0; font-size:1.6rem; font-weight:600; margin-bottom:16px;">
                    Due Diligence Path
                </h3>
                <ul style="margin-top:10px; line-height:1.9; color:#CBD5E0;">
                    <li>Upload and analyze data</li>
                    <li>Market fit comparatives</li>
                    <li>Create investment memo</li>
                </ul>
            </div>
            <div style="text-align:center;">
                <a href='/pages/2_Due_Diligence' style='text-decoration:none;
                    background:#2D3748; color:white; padding:10px 25px;
                    border-radius:30px; font-weight:600; transition:background-color 0.3s ease;'>
                    Start →
                </a>
            </div>
        </div>""",
        unsafe_allow_html=True,
    )

qdb_section_end()

# ===== FOOTER =====
st.markdown(
    f"""
    <div style='background-color:#1B2B4D; color:#E2E8F0; padding:25px 20px;
                margin:0 auto; width:85%; border-radius:15px 15px 0 0;
                font-size:0.94rem;'>
        <div style='display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap;'>
            <div style='flex:3;'>
                <ul style='list-style:none; display:flex; gap:25px; flex-wrap:wrap; padding:0; margin:0;'>
                    <li><a href='#' style='text-decoration:none; color:#E2E8F0;'>About Regulus</a></li>
                    <li><a href='#' style='text-decoration:none; color:#E2E8F0;'>Careers</a></li>
                    <li><a href='#' style='text-decoration:none; color:#E2E8F0;'>Contact Us</a></li>
                    <li><a href='#' style='text-decoration:none; color:#E2E8F0;'>Privacy Policy</a></li>
                    <li><a href='#' style='text-decoration:none; color:#E2E8F0;'>Terms & Conditions</a></li>
                </ul>
            </div>
            <div style='flex:1; text-align:right;'>
                <p style='margin:0; color:#A0AEC0; font-size:0.9rem;'>
                    Powered by Regulus AI
                </p>
                {"<img src='"+regulus_logo+"' style='max-height:55px; margin-top:6px; opacity:0.95;' alt='Regulus Logo'>" if regulus_logo else "<b>Regulus</b>"}
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
