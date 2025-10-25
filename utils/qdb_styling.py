"""
QDB Global Styling Module
Import this in every page to apply consistent branding
"""

import streamlit as st

def apply_qdb_styling():
    """Apply QDB branding and full-width layout to any page"""
    st.markdown("""
    <style>
    /* HIDE SIDEBAR COMPLETELY */
    [data-testid="stSidebar"] {
        display: none !important;
    }
    
    /* REMOVE SIDEBAR SPACING */
    .main {
        margin-left: 0 !important;
        padding-left: 0 !important;
    }
    
    /* FULL WIDTH */
    .main > div {
        max-width: 100% !important;
        padding: 1.5rem 3rem !important;
    }
    
    /* QDB BUTTONS */
    .stButton > button {
        background: linear-gradient(135deg, #5E2A84 0%, #1B2B4D 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 14px 32px;
        font-size: 1.05rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        box-shadow: 0 4px 12px rgba(94, 42, 132, 0.3);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #1B2B4D 0%, #5E2A84 100%);
        box-shadow: 0 6px 16px rgba(94, 42, 132, 0.45);
        transform: translateY(-2px);
    }
    
    /* CONTENT WRAPPER */
    .content-wrapper {
        max-width: 1400px;
        margin: 0 auto;
    }
    </style>
    """, unsafe_allow_html=True)
