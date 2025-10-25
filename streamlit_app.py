"""Investment Analyst AI – Regulus Edition | Fixed & Enhanced Navigation"""
import streamlit as st
import base64
import os
from utils.qdb_styling import (
    apply_qdb_styling,
    qdb_section_start,
    qdb_section_end,
)

# ---------------- PAGE CONFIGURATION ----------------
st.set_page_config(
    page_title="Investment Analyst AI - Regulus",
    layout="wide",
    initial_sidebar_state="collapsed",
)
apply_qdb_styling()

# ---------------- UTILITIES ----------------
def encode_image(path):
    """Safely embed logos into HTML"""
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f"data:image/png;base64,{base64.b64encode(f.read()).decode()}"
    return None

# ---------------- LOGOS ----------------
qdb_logo = encode_image("QDB_Logo.png")
regulus_logo = encode_image("regulus_logo.png")

# ---------------- HERO SECTION ----------------
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
            <p style='color:#CBD5E0;font-size:1.05rem;max-width:700px;margin:auto;'>
                Supporting Qatar’s economic vision with data‑driven investment insights.
            </p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------- TOP NAVIGATION ----------------
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

nav_links = [
    ("Deal Sourcing", "1_Deal_Sourcing"),
    ("Due Diligence", "2_Due_Diligence"),
    ("Market Analysis", "3_Market_Analysis"),
    ("Financial Modeling", "4_Financial_Modeling"),
    ("Investment Memo", "5_Investment_Memo"),
]

cols = st.columns(len(nav_links))
for i, (label, page) in enumerate(nav_links):
    with cols[i]:
        # No icon used
        st.page_link(page=page, label=label)

# ---------------- MAIN SECTION ----------------
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

# ---------------- CARD TEMPLATE ----------------
def nav_card(title, features, page, color):
    card_bg = "#ffffff" if color == "light" else "#1B2B4D"
    text_color = "#1B2B4D" if color == "light" else "#E2E8F0"
    btn_bg = "#319795" if color == "light" else "#2D3748"
    btn_hover = "#2C7A7B" if color == "light" else "#4A5568"

    st.markdown(
        f"""
        <div style="background:{card_bg};
                    color:{text_color};
                    border-radius:15px;
                    padding:30px;
                    box-shadow:0 5px 15px rgba(0,0,0,0.08);
                    transition:transform 0.25s ease; height:100%;">
            <h3 style="margin-bottom:10px;">{title}</h3>
            <ul style="padding-left:18px; line-height:1.7; margin-bottom:25px;">
                {''.join(f'<li>{item}</li>' for item in features)}
            </ul>
            <a href='/{page}' target='_self'
               style='text-decoration:none;
                      background-color:{btn_bg};
                      color:white;
                      padding:10px 25px;
                      border-radius:30px;
                      font-weight:600;
                      font-size:0.95rem;
                      transition:background-color 0.3s ease;'>
               Start →
            </a>
        </div>
        <style>
        a[href='/{page}']:hover {{
            background-color:{btn_hover} !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

# ---------------- PATH CARDS ----------------
with col1:
    nav_card(
        "Deal Sourcing",
        ["Identify potential startups", "Filter by stage/sector", "Export prospects to Due Diligence"],
        "1_Deal_Sourcing",
        "light",
    )

with col2:
    nav_card(
        "Due Diligence",
        ["Upload or analyze reports", "Review key risk metrics", "Generate summaries"],
        "2_Due_Diligence",
        "dark",
    )

with col3:
    nav_card(
        "Market Analysis",
        ["Analyze market trends", "Compare competitors", "Integrate results in memo"],
        "3_Market_Analysis",
        "light",
    )

qdb_section_end()

# ---------------- FOOTER ----------------
st.markdown(
    f"""
    <div style='background:#1B2B4D; color:#A0AEC0; padding:25px 30px; margin-top:50px;
                border-radius:10px 10px 0 0; text-align:center; font-size:0.9rem;'>
        Powered by Regulus AI
        {'<img src="'+regulus_logo+'" style="max-height:40px; vertical-align:middle; margin-left:10px;">' if regulus_logo else ''}
    </div>
    """,
    unsafe_allow_html=True,
)
