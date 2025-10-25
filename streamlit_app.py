"""
Investment Analyst AI - QDB Edition
Streamlined Single-Page Workflow
"""

import streamlit as st

# Configure page - COLLAPSED sidebar
st.set_page_config(
    page_title="Investment Analyst AI - QDB",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="collapsed"  # Hide sidebar
)

# Hide sidebar completely with CSS
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
    """Main application - Single page workflow"""
    
    # Header
    st.markdown(
        """
        <div style='
            background: linear-gradient(90deg, #A6D8FF, #D5B8FF);
            border-radius: 12px;
            padding: 30px;
            text-align: center;
            color: white;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            margin-bottom: 40px;
        '>
            <h1 style='margin: 0; font-size: 2.5rem; text-shadow: 1px 1px 5px rgba(0, 0, 0, 0.2);'>
                💼 Investment Analyst AI
            </h1>
            <p style='margin: 10px 0 0 0; font-size: 1.2rem; opacity: 0.95;'>
                Qatar Development Bank | Powered by Regulus AI
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Direct Workflow Selection - Large, Clear Buttons
    st.markdown(
        """
        <div style='text-align: center; margin-bottom: 30px;'>
            <h2 style='color: #333; margin-bottom: 10px;'>Choose Your Analysis Path</h2>
            <p style='color: #666; font-size: 1.1rem;'>Select one option to begin</p>
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
                padding: 30px;
                color: white;
                height: 400px;
                display: flex;
                flex-direction: column;
                box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
            '>
                <div style='font-size: 4rem; margin-bottom: 20px;'>🔍</div>
                <h2 style='margin: 0 0 15px 0;'>Deal Sourcing Path</h2>
                <p style='font-size: 1.1rem; line-height: 1.6; margin-bottom: 20px;'>
                    <strong>Start here if:</strong><br/>
                    • You're looking for new investment opportunities<br/>
                    • You want to build your deal pipeline<br/>
                    • You need to discover & filter deals
                </p>
                <div style='margin-top: auto;'>
                    <strong>Workflow:</strong><br/>
                    Deal Discovery → Due Diligence → Market → Financial → Memo
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("🚀 Start Deal Sourcing", type="primary", use_container_width=True, key="btn_deal"):
            st.session_state.workflow_path = "Deal Sourcing"
            st.switch_page("pages/1_🔍_Deal_Sourcing.py")
    
    # PATH 2: Document Analysis
    with col2:
        st.markdown(
            """
            <div style='
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                border-radius: 15px;
                padding: 30px;
                color: white;
                height: 400px;
                display: flex;
                flex-direction: column;
                box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
            '>
                <div style='font-size: 4rem; margin-bottom: 20px;'>📄</div>
                <h2 style='margin: 0 0 15px 0;'>Due Diligence Path</h2>
                <p style='font-size: 1.1rem; line-height: 1.6; margin-bottom: 20px;'>
                    <strong>Start here if:</strong><br/>
                    • You received investment proposals<br/>
                    • You have company documents to analyze<br/>
                    • You're conducting deep-dive analysis
                </p>
                <div style='margin-top: auto;'>
                    <strong>Workflow:</strong><br/>
                    Due Diligence → Market Analysis → Financial → Memo
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("📁 Start Due Diligence", type="primary", use_container_width=True, key="btn_dd"):
            st.session_state.workflow_path = "Due Diligence"
            st.switch_page("pages/2_📄_Due_Diligence_Analysis.py")
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Quick Access Tools (Optional - for advanced users)
    with st.expander("🎯 Direct Access to Specific Tools", expanded=False):
        st.markdown("### Jump directly to any analysis module")
        
        col_tool1, col_tool2, col_tool3 = st.columns(3)
        
        with col_tool1:
            if st.button("🌐 Market Analysis", use_container_width=True):
                st.switch_page("pages/3_🌐_Market_Analysis.py")
        
        with col_tool2:
            if st.button("📊 Financial Modeling", use_container_width=True):
                st.switch_page("pages/4_📊_Financial_Modeling.py")
        
        with col_tool3:
            if st.button("📝 Investment Memo", use_container_width=True):
                st.switch_page("pages/5_📝_Investment_Memo.py")
    
    st.markdown("---")
    
    # Minimal Info Section (Collapsible)
    with st.expander("ℹ️ About This Platform", expanded=False):
        col_info1, col_info2 = st.columns(2)
        
        with col_info1:
            st.markdown("""
### What This Platform Does

**Investment Analyst AI** automates and accelerates the complete investment analysis workflow for QDB analysts:

✅ **Deal Discovery** - Multi-source aggregation with QDB industry filters  
✅ **Due Diligence** - AI-powered document analysis with AML/PEP screening  
✅ **Market Research** - Automated competitive & market intelligence  
✅ **Financial Modeling** - Template-based projections with formulas  
✅ **Memo Generation** - Professional investment recommendations  
            """)
        
        with col_info2:
            st.markdown("""
### Key Benefits

⚡ **80% Faster** - Complete analysis in hours, not days  
🎯 **Consistent Quality** - Standardized frameworks & templates  
📊 **Data-Driven** - AI-powered insights from multiple sources  
🤖 **Automated Workflows** - Guided step-by-step process  
📥 **Export Ready** - Professional reports in MD, DOCX, XLSX  

**Designed specifically for Qatar Development Bank analysts.**
            """)
    
    # Footer
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align: center; color: #999; padding: 20px;'>
        <p style='font-size: 0.9rem;'>
            <strong>Investment Analyst AI</strong> | Qatar Development Bank<br/>
            Powered by <strong>Regulus AI</strong> | Version 1.0.0 | © 2025
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
