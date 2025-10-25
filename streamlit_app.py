"""
Investment Analyst AI - QDB Edition
Professional Branded Interface
"""

import streamlit as st
import os

# Configure page
st.set_page_config(
    page_title="Investment Analyst AI - QDB",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide sidebar
st.markdown("""
<style>
    [data-testid="stSidebar"] {display: none;}
    .main > div {padding-top: 2rem;}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'workflow_path' not in st.session_state:
    st.session_state.workflow_path = None
if 'current_deal' not in st.session_state:
    st.session_state.current_deal = None

def main():
    """Main application - aligned header"""
    
    # --- FIXED HEADER LAYOUT ---
    st.markdown("""
    <style>
    .header-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        width: 100%;
        max-width: 1100px;
        margin: 0 auto 25px auto;
    }
    .header-logo {
        flex: 1;
        text-align: center;
    }
    .logo-img {
        max-height: 100px;
        object-fit: contain;
        vertical-align: middle;
    }
    .header-center {
        flex: 2;
        text-align: center;
    }
    .header-center h1 {
        font-size: 2.6rem;
        font-weight: 700;
        margin-bottom: 8px;
        color: #333;
    }
    .header-center p {
        font-size: 1.15rem;
        color: #666;
        margin: 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='header-container'>", unsafe_allow_html=True)
    
    # QDB logo (left)
    st.markdown("<div class='header-logo'>", unsafe_allow_html=True)
    if os.path.exists("QDB_Logo.png"):
        st.markdown("<img src='QDB_Logo.png' class='logo-img'>", unsafe_allow_html=True)
    else:
        st.markdown("<p><strong>Qatar Development Bank</strong></p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Center title block
    st.markdown("""
    <div class='header-center'>
        <h1>Investment Analyst AI</h1>
        <p>Intelligent Investment Analysis Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Regulus logo (right)
    st.markdown("<div class='header-logo'>", unsafe_allow_html=True)
    if os.path.exists("regulus_logo.png"):
        st.markdown("<img src='regulus_logo.png' class='logo-img'>", unsafe_allow_html=True)
    else:
        st.markdown("<p style='text-align:right;'><strong>Regulus</strong></p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    # --- END FIXED HEADER ---
    
    # Gradient divider
    st.markdown("<div style='background:linear-gradient(90deg,#A6D8FF,#D5B8FF);height:4px;border-radius:2px;margin-bottom:40px;'></div>", unsafe_allow_html=True)
    
    # Workflow Selection Section
    st.markdown("""
    <div style='text-align:center;margin-bottom:30px;'>
        <h2 style='color:#333;margin-bottom:10px;'>Choose Your Analysis Path</h2>
        <p style='color:#666;font-size:1.1rem;'>Select one option to begin your workflow</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2, gap="large")

    # Path 1 — Deal Sourcing
    with col1:
        st.markdown("""
        <div style='background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);
                    border-radius:15px;
                    padding:40px;
                    color:white;
                    height:420px;
                    display:flex;
                    flex-direction:column;
                    box-shadow:0 6px 20px rgba(0,0,0,0.15);'>
            <h2 style='margin:0 0 15px 0;font-size:2rem;'>Deal Sourcing Path</h2>
            <p style='font-size:1.15rem;line-height:1.7;margin-bottom:25px;'>
                <strong>Start here if you are:</strong><br/><br/>
                • Looking for new investment opportunities<br/>
                • Building your deal pipeline<br/>
                • Discovering and filtering potential deals
            </p>
            <div style='margin-top:auto;padding-top:20px;border-top:1px solid rgba(255,255,255,0.3);'>
                <strong style='font-size:1.1rem;'>Complete Workflow:</strong><br/>
                <span style='font-size:1rem;'>Deal Discovery → Due Diligence → Market → Financial → Memo</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Start Deal Sourcing", type="primary", use_container_width=True):
            st.session_state.workflow_path = "Deal Sourcing"
            st.switch_page("pages/1_Deal_Sourcing.py")
    
    # Path 2 — Due Diligence
    with col2:
        st.markdown("""
        <div style='background:linear-gradient(135deg,#f093fb 0%,#f5576c 100%);
                    border-radius:15px;
                    padding:40px;
                    color:white;
                    height:420px;
                    display:flex;
                    flex-direction:column;
                    box-shadow:0 6px 20px rgba(0,0,0,0.15);'>
            <h2 style='margin:0 0 15px 0;font-size:2rem;'>Due Diligence Path</h2>
            <p style='font-size:1.15rem;line-height:1.7;margin-bottom:25px;'>
                <strong>Start here if you have:</strong><br/><br/>
                • Received investment proposals<br/>
                • Company documents to analyze<br/>
                • Need to conduct deep-dive analysis
            </p>
            <div style='margin-top:auto;padding-top:20px;border-top:1px solid rgba(255,255,255,0.3);'>
                <strong style='font-size:1.1rem;'>Complete Workflow:</strong><br/>
                <span style='font-size:1rem;'>Due Diligence → Market → Financial → Memo</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Start Due Diligence", type="primary", use_container_width=True):
            st.session_state.workflow_path = "Due Diligence"
            st.switch_page("pages/2_Due_Diligence_Analysis.py")
    
    # Tool shortcuts
    st.markdown("<br><br>", unsafe_allow_html=True)
    with st.expander("Direct Access to Specific Tools", expanded=False):
        st.markdown("### Jump directly to any module")
        col_tool1, col_tool2, col_tool3 = st.columns(3)
        with col_tool1:
            if st.button("Market Analysis", use_container_width=True):
                st.switch_page("pages/3_Market_Analysis.py")
        with col_tool2:
            if st.button("Financial Modeling", use_container_width=True):
                st.switch_page("pages/4_Financial_Modeling.py")
        with col_tool3:
            if st.button("Investment Memo", use_container_width=True):
                st.switch_page("pages/5_Investment_Memo.py")
    
    # Footer
    st.markdown("<br><br><div style='background:linear-gradient(90deg,#A6D8FF,#D5B8FF);height:4px;border-radius:2px;margin-bottom:20px;'></div>", unsafe_allow_html=True)
    col_f1, col_f2, col_f3 = st.columns([1, 2, 1])
    with col_f1:
        st.markdown("<p style='text-align:left;color:#666;'>© 2025 Qatar Development Bank</p>", unsafe_allow_html=True)
    with col_f2:
        st.markdown("<p style='text-align:center;color:#999;font-size:0.9rem;'><strong>Investment Analyst AI</strong> | Version 1.0.0</p>", unsafe_allow_html=True)
    with col_f3:
        st.markdown("<p style='text-align:right;color:#666;'>Powered by Regulus</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
