"""
QDB Global Styling Module
Import this in every page to apply consistent branding and full-width layout
"""

import streamlit as st

# QDB Official Brand Colors
QDB_PURPLE = "#5E2A84"
QDB_GOLD = "#C69C6D"
QDB_DARK_BLUE = "#1B2B4D"
QDB_LIGHT_GRAY = "#F5F5F5"
QDB_WHITE = "#FFFFFF"


def apply_qdb_styling():
    """Apply QDB branding and full-width layout to any page"""
    st.markdown(f"""
    <style>
    /* ========================================
       QDB GLOBAL STYLING - FULL WIDTH LAYOUT
       ======================================== */
    
    /* COMPLETELY HIDE SIDEBAR */
    [data-testid="stSidebar"] {{
        display: none !important;
    }}
    
    /* REMOVE ALL SIDEBAR SPACING */
    .main {{
        margin-left: 0 !important;
        padding-left: 0 !important;
    }}
    
    /* FULL WIDTH CONTAINER */
    .main > div {{
        max-width: 100% !important;
        padding: 1.5rem 3rem !important;
    }}
    
    /* CONTENT WRAPPER (for centered content) */
    .content-wrapper {{
        max-width: 1400px;
        margin: 0 auto;
    }}
    
    /* ========================================
       QDB BUTTON STYLING
       ======================================== */
    
    /* Primary Buttons */
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
        cursor: pointer;
    }}
    
    .stButton > button:hover {{
        background: linear-gradient(135deg, {QDB_DARK_BLUE} 0%, {QDB_PURPLE} 100%);
        box-shadow: 0 6px 16px rgba(94, 42, 132, 0.45);
        transform: translateY(-2px);
    }}
    
    .stButton > button:active {{
        transform: translateY(0px);
        box-shadow: 0 2px 8px rgba(94, 42, 132, 0.4);
    }}
    
    /* ========================================
       QDB TEXT & HEADERS
       ======================================== */
    
    h1 {{
        color: {QDB_DARK_BLUE};
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }}
    
    h2 {{
        color: {QDB_PURPLE};
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }}
    
    h3 {{
        color: {QDB_DARK_BLUE};
    }}
    
    /* ========================================
       QDB INPUT FIELDS
       ======================================== */
    
    .stTextInput > div > div > input {{
        border: 2px solid {QDB_LIGHT_GRAY};
        border-radius: 6px;
        padding: 10px;
    }}
    
    .stTextInput > div > div > input:focus {{
        border-color: {QDB_PURPLE};
        box-shadow: 0 0 0 1px {QDB_PURPLE};
    }}
    
    /* ========================================
       QDB CARDS & CONTAINERS
       ======================================== */
    
    .qdb-card {{
        background: white;
        border-radius: 12px;
        padding: 30px;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
        border-left: 5px solid {QDB_PURPLE};
        transition: all 0.3s ease;
    }}
    
    .qdb-card:hover {{
        box-shadow: 0 8px 30px rgba(94, 42, 132, 0.2);
        transform: translateY(-5px);
    }}
    
    /* ========================================
       QDB FOOTER & DIVIDERS
       ======================================== */
    
    .qdb-divider {{
        height: 3px;
        background: linear-gradient(90deg, {QDB_PURPLE}, {QDB_GOLD});
        border-radius: 2px;
        margin: 30px 0;
    }}
    
    /* ========================================
       EXPANDER STYLING
       ======================================== */
    
    .streamlit-expanderHeader {{
        background-color: {QDB_LIGHT_GRAY};
        border-radius: 6px;
        color: {QDB_DARK_BLUE};
        font-weight: 600;
    }}
    
    </style>
    """, unsafe_allow_html=True)


def qdb_divider():
    """Insert a QDB-branded gradient divider"""
    st.markdown(f"<div style='height:3px;background:linear-gradient(90deg,{QDB_PURPLE},{QDB_GOLD});border-radius:2px;margin:30px 0;'></div>", unsafe_allow_html=True)


def qdb_header(title, subtitle=""):
    """Create a QDB-branded page header"""
    st.markdown(f"""
    <div style='text-align:center;margin:30px 0;'>
        <h1 style='color:{QDB_DARK_BLUE};margin-bottom:10px;'>{title}</h1>
        <p style='color:#666;font-size:1.15rem;'>{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)
