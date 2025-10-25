"""
Investment Analyst AI Agent - Main Application
A unified AI platform for investment due diligence, financial modeling, and memo drafting
Optimized for QDB Analysts
"""

import streamlit as st

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
if 'workflow_path' not in st.session_state:
    st.session_state.workflow_path = None
if 'current_deal' not in st.session_state:
    st.session_state.current_deal = None

def check_api_connection():
    """Check if OpenAI API is configured"""
    try:
        api_key = st.secrets.get("OPENAI_API_KEY", "")
        return len(api_key) > 0
    except:
        return False

def main():
    """Main application entry point"""
    
    # Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/fluency/96/000000/investment-portfolio.png", width=80)
        st.title("💼 Investment Analyst AI")
        st.caption("*Powered by Regulus AI*")
        st.markdown("---")
        
        # Workflow Indicators
        if st.session_state.workflow_path:
            st.markdown("### 📍 Current Workflow")
            st.info(f"**Path:** {st.session_state.workflow_path}")
            
            if st.session_state.current_deal:
                st.success(f"**Deal:** {st.session_state.current_deal}")
        
        st.markdown("---")
        
        st.markdown("""
        ### 🎯 Quick Navigation
        - 🔍 Deal Sourcing
        - 📄 Due Diligence
        - 🌐 Market Analysis
        - 📊 Financial Modeling
        - 📝 Investment Memo
        """)
        
        st.markdown("---")
        
        # System Status
        st.markdown("### ⚙️ System Status")
        api_status = "🟢 Connected" if check_api_connection() else "🔴 Disconnected"
        st.caption(f"**API:** {api_status}")
        st.caption("**Parser:** 🟢 Active")
        st.caption("**Scraper:** 🟢 Online")
    
    # Main Header
    st.markdown(
        """
        <div style='
            background: linear-gradient(90deg, #A6D8FF, #D5B8FF);
            border-radius: 12px;
            padding: 25px;
            text-align: center;
            color: white;
            font-weight: 600;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            margin-bottom: 30px;
        '>
            <h1 style='margin: 0; text-shadow: 1px 1px 5px rgba(0, 0, 0, 0.2);'>
                🎯 Investment Analyst AI - QDB Edition
            </h1>
            <p style='margin: 10px 0 0 0; font-size: 1.1rem;'>Streamlined Investment Analysis Workflow</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Dashboard Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📄 Documents", len(st.session_state.uploaded_documents))
    with col2:
        st.metric("🔍 Active Analyses", len(st.session_state.analysis_cache))
    with col3:
        st.metric("📊 Models", "5")
    with col4:
        st.metric("✅ Deals Sourced", st.session_state.get('total_deals', 0))
    
    st.markdown("---")
    
    # WORKFLOW PATHS
    st.markdown(
        """
        <div style='
            background: linear-gradient(90deg, #A6D8FF, #D5B8FF);
            border-radius: 12px;
            padding: 15px;
            color: white;
            font-weight: 600;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            margin-bottom: 20px;
        '>
            <h2 style='margin: 0; text-shadow: 1px 1px 5px rgba(0, 0, 0, 0.2);'>
                📋 Choose Your Workflow
            </h2>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("### Select how you'd like to proceed:")
    
    # Workflow Option 1: Deal Sourcing Path
    with st.container():
        st.markdown(
            """
            <div style='
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 10px;
                padding: 20px;
                color: white;
                margin-bottom: 20px;
            '>
                <h3 style='margin: 0;'>🔍 Path 1: Deal Sourcing → Full Analysis</h3>
                <p style='margin: 10px 0 0 0;'>Start by discovering new investment opportunities</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        col_path1_1, col_path1_2 = st.columns([3, 1])
        
        with col_path1_1:
            st.markdown("""
**Workflow Steps:**
1. 🔍 **Deal Sourcing** - Discover and filter potential deals
2. 📄 **Due Diligence** - Analyze selected deal in depth
3. 🌐 **Market Analysis** - Research market & competitors
4. 📊 **Financial Modeling** - Build projections & scenarios
5. 📝 **Investment Memo** - Generate final recommendation

**Best for:** Proactive deal discovery and pipeline building
            """)
        
        with col_path1_2:
            if st.button("🚀 Start Deal Sourcing", type="primary", use_container_width=True):
                st.session_state.workflow_path = "Deal Sourcing Path"
                st.switch_page("pages/1_🔍_Deal_Sourcing.py")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Workflow Option 2: Document Analysis Path
    with st.container():
        st.markdown(
            """
            <div style='
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                border-radius: 10px;
                padding: 20px;
                color: white;
                margin-bottom: 20px;
            '>
                <h3 style='margin: 0;'>📄 Path 2: Due Diligence → Full Analysis</h3>
                <p style='margin: 10px 0 0 0;'>Start with documents you already have</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        col_path2_1, col_path2_2 = st.columns([3, 1])
        
        with col_path2_1:
            st.markdown("""
**Workflow Steps:**
1. 📄 **Due Diligence** - Upload & analyze company documents
2. 🌐 **Market Analysis** - Research market context
3. 📊 **Financial Modeling** - Build financial projections
4. 📝 **Investment Memo** - Create investment recommendation

**Best for:** Reactive analysis when you receive investment proposals
            """)
        
        with col_path2_2:
            if st.button("📁 Start Due Diligence", type="primary", use_container_width=True):
                st.session_state.workflow_path = "Due Diligence Path"
                st.switch_page("pages/2_📄_Due_Diligence_Analysis.py")
    
    st.markdown("---")
    
    # Platform Overview
    st.markdown(
        """
        <div style='
            background: linear-gradient(90deg, #A6D8FF, #D5B8FF);
            border-radius: 12px;
            padding: 15px;
            color: white;
            font-weight: 600;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            margin-bottom: 20px;
        '>
            <h3 style='margin: 0; text-shadow: 1px 1px 5px rgba(0, 0, 0, 0.2);'>
                📚 Platform Overview
            </h3>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    tab1, tab2, tab3 = st.tabs(["🎯 Purpose", "✨ Features", "🚀 Quick Start"])
    
    with tab1:
        col_purpose1, col_purpose2 = st.columns(2)
        
        with col_purpose1:
            st.markdown("""
### The Challenge

Investment analysis at QDB involves:
- ⏰ **Time-consuming** document review
- 🔍 **Manual** screening of opportunities
- 📊 **Complex** financial modeling
- 📝 **Repetitive** memo drafting

### The Solution

This AI platform streamlines:
- **Deal Discovery** with automated filtering
- **Document Analysis** with AI extraction
- **Market Research** with web scraping
- **Financial Modeling** with templates
- **Memo Generation** with consistent formatting
            """)
        
        with col_purpose2:
            st.image("https://img.icons8.com/clouds/400/000000/workflow.png", width=300)
            st.info("""
**💡 Key Benefits:**
- ⚡ 80% faster analysis
- 🎯 Consistent quality
- 📊 Data-driven insights
- 🤖 AI-powered automation
            """)
    
    with tab2:
        col_feat1, col_feat2 = st.columns(2)
        
        with col_feat1:
            st.markdown("""
#### 🔍 Deal Sourcing
- Multi-source aggregation
- Industry filter (QDB unattractive list)
- Custom criteria matching
- Export deal pipeline

#### 📄 Due Diligence
- PDF/DOCX document ingestion
- AML/PEP/FATCA screening
- Web data extraction
- Red flag detection

#### 🌐 Market Analysis
- Market size & trends
- Competitive landscape
- SWOT & Porter's Five Forces
- Regulatory environment
            """)
        
        with col_feat2:
            st.markdown("""
#### 📊 Financial Modeling
- Projection templates
- Scenario planning
- Formula-embedded Excel
- What-if analysis

#### 📝 Investment Memo
- Auto-draft sections
- Gulf Resonance scoring
- Professional formatting
- Export MD/DOCX

#### 🤖 AI Capabilities
- Natural language processing
- Intelligent summarization
- Contextual insights
            """)
    
    with tab3:
        st.markdown("""
### 🚀 Getting Started - QDB Analyst Guide

#### **Choose Your Starting Point:**

**Option A: New Deal Discovery**
1. Click "🚀 Start Deal Sourcing" above
2. Define your investment criteria
3. Review discovered deals
4. Select interesting opportunity
5. Click "Proceed to Due Diligence" button
6. Follow guided workflow

**Option B: Existing Documents**
1. Click "📁 Start Due Diligence" above
2. Upload company documents (PDF, DOCX)
3. Optionally fetch web data
4. Review AI analysis
5. Click "Proceed to Market Analysis"
6. Continue through workflow

#### **📋 Workflow Navigation:**
Each page has a **"Next Step"** button to guide you through the complete analysis process.

#### **💾 Data Persistence:**
Your work is saved in session state - you can navigate back to previous steps without losing data.

#### **📥 Export Options:**
Download reports at each stage in multiple formats (MD, DOCX, XLSX).
        """)
        
        st.success("💡 **Pro Tip:** The platform guides you through each step - just follow the workflow buttons!")
    
    st.markdown("---")
    
    # Recent Activity (if any)
    if st.session_state.analysis_cache or st.session_state.uploaded_documents:
        st.markdown(
            """
            <div style='
                background: linear-gradient(90deg, #A6D8FF, #D5B8FF);
                border-radius: 12px;
                padding: 15px;
                color: white;
                font-weight: 600;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
                margin-bottom: 20px;
            '>
                <h3 style='margin: 0; text-shadow: 1px 1px 5px rgba(0, 0, 0, 0.2);'>
                    📊 Recent Activity
                </h3>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        if st.session_state.uploaded_documents:
            st.markdown("**📄 Uploaded Documents:**")
            for doc in st.session_state.uploaded_documents[:5]:
                st.caption(f"• {doc}")
        
        if st.session_state.analysis_cache:
            st.markdown("**🔍 Recent Analyses:**")
            for analysis in list(st.session_state.analysis_cache.keys())[:5]:
                st.caption(f"• {analysis}")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>Built with ❤️ for Qatar Development Bank</p>
        <p><strong>Investment Analyst AI</strong> | Powered by Regulus AI | Version 1.0.0</p>
        <p>© 2025 All Rights Reserved</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
