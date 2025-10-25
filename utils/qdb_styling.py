"""
QDB Global Styling Module - With QDB Website Button Styles
"""

import streamlit as st

# QDB Official Brand Colors
QDB_PURPLE = "#5E2A84"
QDB_GOLD = "#C69C6D"
QDB_DARK_BLUE = "#1B2B4D"
QDB_LIGHT_GRAY = "#F5F5F5"
QDB_WHITE = "#FFFFFF"
QDB_CREAM = "#F5EFE6"
QDB_NAVY = "#2C3E5E"  # Updated navy from QDB website


def apply_qdb_styling():
    """Apply QDB branding and full-width layout"""
    st.markdown(f"""
    <style>
    /* HIDE SIDEBAR */
    [data-testid="stSidebar"] {{display: none !important;}}
    .main {{margin-left: 0 !important; padding-left: 0 !important;}}
    .main > div {{max-width: 100% !important; padding: 1.5rem 3rem !important;}}
    .content-wrapper {{max-width: 1400px; margin: 0 auto;}}
    
    /* QDB PILL BUTTONS (from website) */
    .stButton > button {{
        background: linear-gradient(135deg, {QDB_PURPLE} 0%, #764BA2 100%);
        color: white;
        border: none;
        border-radius: 50px !important;  /* Pill shape */
        padding: 16px 40px;
        font-size: 1.05rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        box-shadow: 0 4px 15px rgba(94, 42, 132, 0.3);
        transition: all 0.3s ease;
        cursor: pointer;
        text-transform: none;
    }}
    
    .stButton > button:hover {{
        background: linear-gradient(135deg, #764BA2 0%, {QDB_PURPLE} 100%);
        box-shadow: 0 6px 20px rgba(94, 42, 132, 0.5);
        transform: translateY(-3px);
    }}
    
    .stButton > button:active {{
        transform: translateY(0px);
        box-shadow: 0 2px 10px rgba(94, 42, 132, 0.4);
    }}
    
    /* TEXT & HEADERS */
    h1 {{color: {QDB_DARK_BLUE}; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;}}
    h2 {{color: {QDB_PURPLE}; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;}}
    h3 {{color: {QDB_DARK_BLUE};}}
    
    /* INPUT FIELDS */
    .stTextInput > div > div > input {{
        border: 2px solid {QDB_LIGHT_GRAY};
        border-radius: 6px;
        padding: 10px;
    }}
    .stTextInput > div > div > input:focus {{
        border-color: {QDB_PURPLE};
        box-shadow: 0 0 0 1px {QDB_PURPLE};
    }}
    
    /* CARDS */
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
    
    /* SECTION BACKGROUNDS */
    .qdb-section-light {{
        background-color: {QDB_CREAM};
        padding: 60px 20px;
        margin: 0 -3rem;
        margin-bottom: 0;
    }}
    
    .qdb-section-dark {{
        background: linear-gradient(135deg, {QDB_NAVY} 0%, {QDB_DARK_BLUE} 100%);
        color: white;
        padding: 60px 20px;
        margin: 0 -3rem;
        margin-bottom: 0;
    }}
    
    .qdb-section-dark h1,
    .qdb-section-dark h2,
    .qdb-section-dark h3,
    .qdb-section-dark p,
    .qdb-section-dark span,
    .qdb-section-dark div {{
        color: white !important;
    }}
    
    /* DIVIDERS */
    .qdb-divider {{
        height: 3px;
        background: linear-gradient(90deg, {QDB_PURPLE}, {QDB_GOLD});
        border-radius: 2px;
        margin: 30px 0;
    }}
    
    /* EXPANDER */
    .streamlit-expanderHeader {{
        background-color: {QDB_LIGHT_GRAY};
        border-radius: 6px;
        color: {QDB_DARK_BLUE};
        font-weight: 600;
    }}
    </style>
    """, unsafe_allow_html=True)


def qdb_divider():
    """QDB gradient divider"""
    st.markdown(f"<div style='height:3px;background:linear-gradient(90deg,{QDB_PURPLE},{QDB_GOLD});border-radius:2px;margin:30px 0;'></div>", unsafe_allow_html=True)


def qdb_header(title, subtitle=""):
    """QDB page header"""
    st.markdown(f"""
    <div style='text-align:center;margin:30px 0;'>
        <h1 style='color:{QDB_DARK_BLUE};margin-bottom:10px;'>{title}</h1>
        <p style='color:#666;font-size:1.15rem;'>{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)


def qdb_section_start(background="light"):
    """Start QDB section with background"""
    section_class = "qdb-section-light" if background == "light" else "qdb-section-dark"
    st.markdown(f"<div class='{section_class}'><div style='max-width:1400px;margin:0 auto;'>", unsafe_allow_html=True)


def qdb_section_end():
    """End QDB section"""
    st.markdown("</div></div>", unsafe_allow_html=True)
