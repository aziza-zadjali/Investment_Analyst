""" Investment Analyst AI – Regulus Edition | Updated Navigation Integration """
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
    """Safely embed logos in base64"""
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f"data:image/png;base64,{base64.b64encode(f.read()).decode()}"
    return None


# --- Logos
qdb_logo = encode_image("QDB_Logo.png")
regulus_logo = encode_image("regulus_logo.png")

# ===== HERO SECTION =====
st.markdown(
    f"""
    <div style="
        background: linear-gradient(135deg, #1B2B4D 0%, #2C3E5E 100%);
        color: white;
        text-align: center;
        margin: 0 -3rem;
        padding: 110px 20px 100px 20px;
        position: relative;
        overflow: hidden;">
        
        <!-- QDB Logo -->
        <div style="position:absolute; top:25px; left:35px;">
            <img src="{qdb_logo}" style="max-height:70px;" alt="QDB Logo">
        </div>
        
        <!-- Central Content -->
        <div style="max-width:950px; margin:0 auto;">
            <h1 style="font-size:2.5rem; font-weight:700; letter-spacing:-0.3px;">Investment Analyst AI</h1>
            <p style="color:#E2E8F0; font-size:1.05rem; margin-bottom:8px;">
                Supporting Qatar's Economic Vision with Data‑Driven Investment Insights
            </p>
            <p style="color:#CBD5E0; font-size:0.95rem; line-height:1.6; max-width:720px; margin:0 auto 30px;">
                End‑to‑End AI Platform for Deal Sourcing, Due Diligence, Market Analysis & Investment Memoranda
            </p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ===== NAVIGATION MENU =====
nav_items = {
    "Deal Sourcing": "pages/1_Deal_Sourcing.py",
    "Due Diligence": "pages/2_Due_Diligence.py",
    "Market Analysis": "pages/3_Market_Analysis.py",
    "Financial Modeling": "pages/4_Financial_Modeling.py",
    "Investment Memo": "pages/5_Investment_Memo.py",
}

with st.container():
    st.markdown(
        """
        <style>
        .navbar {
            background-color:#F6F5F2;
            display:flex;
            justify-content:center;
            gap:40px;
            padding:18px 10px;
            margin:-10px -3rem 4px -3rem;
            font-size:1.07rem;
        }
        .nav-item {
            font-weight:600;
            color:#1B2B4D;
            cursor:pointer;
            border-bottom:2.5px solid transparent;
            transition:color 0.3s, border-color 0.3s;
        }
        .nav-item:hover {
            color:#319795;
            border-color:#319795;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    cols = st.columns(len(nav_items))
    for i, (name, page_path) in enumerate(nav_items.items()):
        with cols[i]:
            if st.button(name, key=f"btn_{i}", use_container_width=True):
                st.switch_page(page_path)

# ===== CHOOSE PATH SECTION =====
qdb_section_start("light")
st.markdown(
    """
    <div style="text-align:center; max-width:950px; margin:0 auto 35px auto;">
        <h2 style="color:#1B2B4D; font-size:2rem; font-weight:700; margin-bottom:10px;">Choose Your Analysis Path</h2>
        <p style="color:#555; font-size:1.05rem;">Start your workflow below or use the navigation above.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

col1, col2 = st.columns(2, gap="large")

# --- Helper: Hover style for buttons ---
def custom_button(label, page_path, bg_color="#319795", hover_color="#2C7A7B"):
    btn_placeholder = st.empty()
    btn_html = f"""
        <style>
        .btn-custom {{
            background-color:{bg_color};
            color:white;
            border:none;
            border-radius:40px;
            padding:12px 30px;
            font-size:0.95rem;
            font-weight:600;
            box-shadow:0 3px 12px rgba(49,151,149,0.3);
            text-decoration:none;
            display:inline-block;
            transition: all 0.25s ease;
        }}
        .btn-custom:hover {{
            background-color:{hover_color};
        }}
        </style>
        <a href="#" class="btn-custom">{label}</a>
    """
    if btn_placeholder.button(label):
        st.switch_page(page_path)
    st.markdown(btn_html, unsafe_allow_html=True)

# --- Deal Sourcing block ---
with col1:
    st.markdown(
        """
        <div style="background:white; border-radius:16px; padding:35px; height:390px;
                    box-shadow:0 5px 20px rgba(0,0,0,0.08); border-top:4px solid #2C3E5E;
                    display:flex; flex-direction:column; justify-content:space-between;">
            <div>
                <h3 style="color:#1B2B4D; font-size:1.6rem; font-weight:600; margin-bottom:16px;">Deal Sourcing Path</h3>
                <ul style="margin-top:10px; line-height:1.9; color:#333;">
                    <li>AI‑powered deal identification</li>
                    <li>Market analysis hand‑off</li>
                    <li>Proceed to due diligence</li>
                </ul>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    custom_button("Start Deal Sourcing", "pages/1_Deal_Sourcing.py")

# --- Due Diligence block ---
with col2:
    st.markdown(
        """
        <div style="background:white; border-radius:16px; padding:35px; height:390px;
                    box-shadow:0 5px 20px rgba(0,0,0,0.08); border-top:4px solid #2C3E5E;
                    display:flex; flex-direction:column; justify-content:space-between;">
            <div>
                <h3 style="color:#1B2B4D; font-size:1.6rem; font-weight:600; margin-bottom:16px;">Due Diligence Path</h3>
                <ul style="margin-top:10px; line-height:1.9; color:#333;">
                    <li>Upload and analyze company data</li>
                    <li>Market fit comparatives</li>
                    <li>Create investment memo</li>
                </ul>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    custom_button("Start Due Diligence", "pages/2_Due_Diligence.py")

qdb_section_end()

# ===== FOOTER =====
st.markdown(
    f"""
    <div style="
        background-color:#1B2B4D;
        color:#E2E8F0;
        padding:25px 20px;
        margin:0 auto;
        width:85%;
        border-radius:15px 15px 0 0;
        font-size:0.94rem;">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap;">
            <div style="flex:3;">
                <ul style="list-style:none; display:flex; gap:25px; flex-wrap:wrap; padding:0; margin:0;">
                    <li><a href="#" style="text-decoration:none; color:#E2E8F0;">About Regulus</a></li>
                    <li><a href="#" style="text-decoration:none; color:#E2E8F0;">Careers</a></li>
                    <li><a href="#" style="text-decoration:none; color:#E2E8F0;">Contact Us</a></li>
                    <li><a href="#" style="text-decoration:none; color:#E2E8F0;">Privacy Policy</a></li>
                    <li><a href="#" style="text-decoration:none; color:#E2E8F0;">Terms & Conditions</a></li>
                </ul>
            </div>
            <div style="flex:1; text-align:right;">
                <p style="margin:0; color:#A0AEC0; font-size:0.9rem;">Powered by Regulus AI</p>
                {"<img src='"+regulus_logo+"' style='max-height:55px; margin-top:6px; opacity:0.95;' alt='Regulus Logo'>" if regulus_logo else "<b>Regulus</b>"}
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
