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
    """Main application - Professional branded interface"""
    
    # --- FIXED HEADER ALIGNMENT ---
    # Adjusted column width ratios and vertical centering CSS
    st.markdown(
        """
        <style>
        .logo-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            width: 100%;
            margin-bottom: 20px;
        }
        .logo-left, .logo-right {
            width: 200px;
        }
        .logo-center {
            flex-grow: 1;
            text-align: center;
        }
        .logo-center h1 {
            margin: 0;
            color: #333;
            font-size: 2.5rem;
            font-weight: 700;
        }
        .logo-center p {
            color: #666;
            margin: 5px 0 0 0;
            font-size: 1.1rem;
        }
        </style>
        """, unsafe_allow_html=True
    )

    st.markdown("<div class='logo-container'>", unsafe_allow_html=True)
    
    # Left Logo (QDB)
    st.markdown("<div class='logo-left'>", unsafe_allow_html=True)
    if os.path.exists("QDB_Logo.png"):
        st.image("QDB_Logo.png", width=190)
    else:
        st.markdown("**Qatar Development Bank**")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Center Title
    st.markdown(
        """
        <div class='logo-center'>
            <h1>Investment Analyst AI</h1>
            <p>Intelligent Investment Analysis Platform</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Right Logo (Regulus)
    st.markdown("<div class='logo-right'>", unsafe_allow_html=True)
    if os.path.exists("regulus_logo.png"):
        st.image("regulus_logo.png", width=190)
    else:
        st.markdown("<div style='text-align: right;'><strong>Powered by Regulus</strong></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    # --- END FIXED HEADER ALIGNMENT ---
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Gradient Divider
    st.markdown(
        """
        <div style='
            background: linear-gradient(90deg, #A6D8FF, #D5B8FF);
            height: 4px;
            border-radius: 2px;
            margin-bottom: 40px;
        '></div>
        """,
        unsafe_allow_html=True
    )
    
    # Workflow Selection
    st.markdown(
        """
        <div style='text-align: center; margin-bottom: 30px;'>
            <h2 style='color: #333; margin-bottom: 10px;'>Choose Your Analysis Path</h2>
            <p style='color: #666; font-size: 1.1rem;'>Select one option to begin your workflow</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    col1, col2 = st.columns(2, gap="large")
    
    # PATH 1: Deal Sourcing
    with col1:
        st.markdown(
            """
            <div style='
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 15px;
                padding: 40px;
                color: white;
                height: 420px;
                display: flex;
                flex-direction: column;
                box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
            '>
                <h2 style='margin: 0 0 15px 0; font-size: 2rem;'>Deal Sourcing Path</h2>
                <p style='font-size: 1.15rem; line-height: 1.7; margin-bottom: 25px;'>
                    <strong>Start here if you are:</strong><br/><br/>
                    • Looking for new investment opportunities<br/>
                    • Building your deal pipeline<br/>
                    • Discovering and filtering potential deals
                </p>
                <div style='margin-top: auto; padding-top: 20px; border-top: 1px solid rgba(255,255,255,0.3);'>
                    <strong style='font-size: 1.1rem;'>Complete Workflow:</strong><br/>
                    <span style='font-size: 1rem;'>Deal Discovery → Due Diligence → Market → Financial → Memo</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("Start Deal Sourcing", type="primary", use_container_width=True, key="btn_deal"):
            st.session_state.workflow_path = "Deal Sourcing"
            st.switch_page("pages/1_Deal_Sourcing.py")
    
    # PATH 2: Due Diligence
    with col2:
        st.markdown(
            """
            <div style='
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                border-radius: 15px;
                padding: 40px;
                color: white;
                height: 420px;
                display: flex;
                flex-direction: column;
                box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
            '>
                <h2 style='margin: 0 0 15px 0; font-size: 2rem;'>Due Diligence Path</h2>
                <p style='font-size: 1.15rem; line-height: 1.7; margin-bottom: 25px;'>
                    <strong>Start here if you have:</strong><br/><br/>
                    • Received investment proposals<br/>
                    • Company documents to analyze<br/>
                    • Need to conduct deep-dive analysis
                </p>
                <div style='margin-top: auto; padding-top: 20px; border-top: 1px solid rgba(255,255,255,0.3);'>
                    <strong style='font-size: 1.1rem;'>Complete Workflow:</strong><br/>
                    <span style='font-size: 1rem;'>Due Diligence → Market → Financial → Memo</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("Start Due Diligence", type="primary", use_container_width=True, key="btn_dd"):
            st.session_state.workflow_path = "Due Diligence"
            st.switch_page("pages/2_Due_Diligence_Analysis.py")
    
    # --- Everything below remains unchanged ---
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    with st.expander("Direct Access to Specific Tools", expanded=False):
        st.markdown("### Jump directly to any analysis module")
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
    
    st.markdown("---")
    
    with st.expander("About This Platform", expanded=False):
        col_info1, col_info2 = st.columns(2)
        with col_info1:
            st.markdown("""
### Features
Automated AI-driven investment research and modeling:
- Deal discovery  
- Due diligence  
- Market research  
- Financial modeling  
- Memo generation  
""")
        with col_info2:
            st.markdown("""
### Benefits
- ⚡ Faster analysis  
- 📊 Consistent outputs  
- 📈 AI-enhanced insights  
- 🧠 Standardized frameworks  
""")

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<div style='background: linear-gradient(90deg, #A6D8FF, #D5B8FF); height: 4px; border-radius: 2px; margin-bottom: 20px;'></div>", unsafe_allow_html=True)
    
    col_foot1, col_foot2, col_foot3 = st.columns([1, 2, 1])
    with col_foot1:
        st.markdown("<p style='text-align: left; color: #666;'>© 2025 Qatar Development Bank</p>", unsafe_allow_html=True)
    with col_foot2:
        st.markdown("<p style='text-align: center; color: #999; font-size: 0.9rem;'><strong>Investment Analyst AI</strong> | Version 1.0.0</p>", unsafe_allow_html=True)
    with col_foot3:
        st.markdown("<p style='text-align: right; color: #666;'>Powered by Regulus</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
