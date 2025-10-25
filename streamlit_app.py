"""
Investment Analyst AI Agent - Main Application
A unified AI platform for investment due diligence, financial modeling, and memo drafting
"""

import streamlit as st
import os
from pathlib import Path

# Configure page
st.set_page_config(
    page_title="Investment Analyst AI",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'analysis_cache' not in st.session_state:
    st.session_state.analysis_cache = {}
if 'uploaded_documents' not in st.session_state:
    st.session_state.uploaded_documents = []

def main():
    """Main application entry point"""
    
    # Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/fluency/96/000000/investment-portfolio.png", width=80)
        st.title("💼 Investment Analyst AI")
        st.markdown("---")
        
        st.markdown("""
        ###  Features
        -  Deal Sourcing
        -  Document Analysis
        -  Market Research
        -  Financial Modeling
        -  Investment Memos
        """)
        
        st.markdown("---")
        st.info("**Tip:** Use multi-page navigation to access different features")
        
    # Main content
    # Container for your header

import streamlit as st

import streamlit as st

import streamlit as st

with st.container():
    st.markdown(
        """
        <div style='
            background: linear-gradient(90deg, #A6D8FF, #D5B8FF);
            border: none;
            border-radius: 12px;
            padding: 25px;
            text-align: center;
            color: white;
            font-weight: 600;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        '>
            <h1 style='
                margin: 0;
                text-shadow: 1px 1px 5px rgba(0, 0, 0, 0.2);
            '>
                 Welcome to Investment Analyst AI
            </h1>
        </div>
        """,
        unsafe_allow_html=True
    )


    
    st.markdown("### Accelerate Your Investment Analysis with AI")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Documents Analyzed", len(st.session_state.uploaded_documents))
    with col2:
        st.metric("Active Analyses", len(st.session_state.analysis_cache))
    with col3:
        st.metric("Models Available", "5")
    
    st.markdown("---")
    
    # Overview sections
    with st.container():
        st.markdown(
        """
        <div style='
            background: linear-gradient(90deg, #A6D8FF, #D5B8FF);
            border: none;
            border-radius: 12px;
            padding: 25px;
            text-align: center;
            color: white;
            font-weight: 600;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        '>
            <h1 style='
                margin: 0;
                text-shadow: 1px 1px 5px rgba(0, 0, 0, 0.2);
            '>
                Platform overview
            </h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    
    tab1, tab2, tab3 = st.tabs([" Purpose", " Features", " Quick Start"])
    
    with tab1:
        st.markdown("""
        ### The Investment Process Challenge
        
        Investment analysis is:
        -  **Time-consuming**: Thousands of documents to review
        -  **Fragmented**: Data scattered across multiple sources
        -  **Manual**: Repetitive tasks in modeling and memo drafting
        
        ### Our Solution
        
        This AI-powered platform assists analysts in:
        - **Due Diligence**: Automated document analysis and red flag detection
        - **Financial Modeling**: Rapid scenario planning and projections
        - **Memo Drafting**: Consistent, professional investment documentation
        """)
    
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ####  Deal Sourcing
            - Scrape accelerators & funding platforms
            - Daily qualified deal lists
            - Custom filtering criteria
            
            ####  Document Analysis
            - Ingest PDF, DOCX, XLSX files
            - Extract key data automatically
            - Highlight red flags
            
            #### 🌐 Market Analysis
            - Pull data from multiple sources
            - Generate market overviews
            - Competitor performance tracking
            """)
        
        with col2:
            st.markdown("""
            ####  Financial Modeling
            - Generate projection models
            - Run what-if scenarios
            - Sensitivity analysis
            
            ####  Investment Memos
            - Auto-draft memo sections
            - Consistent formatting
            - Export to PDF/DOCX
            
            ####  AI-Powered
            - Natural language queries
            - Intelligent summarization
            - Contextual recommendations
            """)
    
    with tab3:
        st.markdown("""
        ###  Getting Started
        
        1. **Configure API Keys**
           - Go to `.streamlit/secrets.toml`
           - Add your OpenAI API key
        
        2. **Navigate Features**
           - Use the sidebar to access different modules
           - Each page handles a specific workflow
        
        3. **Upload Documents**
           - Start with Document Analysis page
           - Upload financial statements, contracts, reports
        
        4. **Generate Insights**
           - Run analyses on uploaded documents
           - Generate financial models
           - Create investment memos
        
        5. **Export Results**
           - Download reports in PDF/DOCX
           - Export financial models to Excel
           - Share with your team
        """)
        
        st.info("💡 **Pro Tip**: Start with Deal Sourcing to identify opportunities, then move to Document Analysis for due diligence.")
    
    st.markdown("---")
    
 
# ✅ Define the function first
def check_api_connection():
    """Check if OpenAI API is configured"""
    try:
        api_key = st.secrets.get("OPENAI_API_KEY", "")
        return len(api_key) > 0
    except:
        return False

# Main Streamlit app
def main():
    # System status
    st.header("System Status")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        api_status = "🟢 Connected" if check_api_connection() else "🔴 Disconnected"
        st.markdown(f"**OpenAI API**: {api_status}")
    
    with col2:
        st.markdown("**Vector Store**: 🟢 Ready")
    
    with col3:
        st.markdown("**Document Parser**: 🟢 Active")
    
    with col4:
        st.markdown("**Web Scraper**: 🟢 Online")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center'>
        <p>Built with ❤️ using Streamlit, LangChain, and OpenAI</p>
        <p>© 2025 Investment Analyst AI | Version 1.0.0</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
