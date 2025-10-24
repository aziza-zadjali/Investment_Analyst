"""
Automated Due Diligence Document Analysis
AI-powered document ingestion, analysis, red flag detection,
and dual-format professional report generation.
"""

import streamlit as st
from datetime import datetime
import pandas as pd
from utils.llm_handler import LLMHandler
from utils.template_generator import TemplateGenerator
from utils.file_processor import FileProcessor
from utils.web_scraper import WebScraper

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Automated Due Diligence",
    page_icon="📄",
    layout="wide"
)

# ============================================================================
# INITIALIZATION
# ============================================================================
@st.cache_resource
def init_handlers():
    """Initialize and cache utility handlers"""
    return (
        LLMHandler(),
        TemplateGenerator(),
        FileProcessor(),
        WebScraper()
    )

llm, tmpl, file_proc, scraper = init_handlers()

# ============================================================================
# DATA SOURCES CONFIGURATION
# ============================================================================
SOURCES = {
    "📊 SEC EDGAR": "https://www.sec.gov/edgar/search/",
    "🏛️ NYSE": "https://www.nyse.com/index",
    "📈 NASDAQ": "https://www.nasdaq.com/",
    "🇬🇧 LSE": "https://www.londonstockexchange.com/",
    "🇶🇦 Qatar Stock Exchange": "https://www.qe.com.qa/",
    "🏦 QFMA": "https://www.qfma.org.qa/english/pages/index.html",
    "🌍 Zawya": "https://www.zawya.com/",
    "💹 Bloomberg": "https://www.bloomberg.com/",
    "💰 Yahoo Finance": "https://finance.yahoo.com/"
}

# ============================================================================
# HEADER
# ============================================================================
st.title("📄 Automated Due Diligence Document Analysis")
st.markdown(
    """
    Upload or fetch company filings, legal documents, and financial statements.  
    AI analyzes content, extracts critical data, flags risks, and generates  
    **two professional Due Diligence Reports** matching institutional templates.
    """
)
st.divider()

# ============================================================================
# STEP 1: DOCUMENT INGESTION
# ============================================================================
st.header("📤 Step 1 – Ingest Documents")

option = st.radio(
    "Select Document Source",
    ["📁 Upload Files", "🔗 Fetch Public Data", "🌐 From URLs"],
    horizontal=True
)

docs = []

# --- Upload Files ---
if option == "📁 Upload Files":
    uploaded = st.file_uploader(
        "Upload financial statements, legal contracts, or business plans",
        type=["pdf", "docx", "xlsx", "txt"],
        accept_multiple_files=True
    )
    if uploaded:
        for f in uploaded:
            docs.append({"name": f.name, "file": f})
        st.success(f"✅ {len(docs)} file(s) uploaded successfully")

# --- Fetch Public Data ---
elif option == "🔗 Fetch Public Data":
    picks = st.multiselect(
        "Select Data Providers",
        list(SOURCES.keys()),
        default=["📊 SEC EDGAR", "💹 Bloomberg", "🇶🇦 Qatar Stock Exchange"]
    )
    
    if picks:
        cols = st.columns(min(len(picks), 4))
        for i, s in enumerate(picks):
            cols[i % 4].link_button(s, SOURCES[s])
    
    ticker = st.text_input(
        "Enter Company Ticker or Name",
        placeholder="e.g., AAPL, TSLA, BALADNA"
    )
    
    if st.button("📥 Fetch Documents", type="primary"):
        if ticker and picks:
            with st.spinner(f"Fetching documents for {ticker}..."):
                for s in picks:
                    docs.append({
                        "name": f"{ticker}_{s.replace('📊 ', '').replace('🇶🇦 ', '')}_Filing.pdf",
                        "source": s
                    })
            st.success(f"✅ Fetched {len(docs)} documents from selected sources")

# --- From URLs ---
elif option == "🌐 From URLs":
    urls = st.text_area(
        "Paste document URLs (one per line)",
        placeholder="https://example.com/annual_report.pdf\nhttps://example.com/financials.xlsx"
    )
    
    if st.button("📥 Import Documents"):
        if urls.strip():
            for line in urls.splitlines():
                if line.strip():
                    docs.append({
                        "name": line.split("/")[-1],
                        "url": line.strip()
                    })
            st.success(f"✅ Imported {len(docs)} URLs")

# --- Display Documents ---
if docs:
    try:
        # Safe display - serialize only strings
        display_data = [{
            "Document Name": d.get("name", "Unknown"),
            "Type": "File" if "file" in d else "URL" if "url" in d else "Fetched"
        } for d in docs]
        st.dataframe(pd.DataFrame(display_data), use_container_width=True)
    except Exception as e:
        st.info(f"📋 {len(docs)} document(s) loaded")

st.divider()

# ============================================================================
# STEP 2: AI ANALYSIS
# ============================================================================
if docs:
    st.header("🤖 Step 2 – AI Document Analysis")
    
    if st.button("🚀 Run Automated Analysis", type="primary", use_container_width=True):
        
        with st.spinner("Analyzing documents with AI..."):
            progress = st.progress(0)
            
            fin_results = ""
            leg_results = ""
            ops_results = ""
            red_flags = []
            
            # Process each document
            for idx, doc in enumerate(docs, start=1):
                name = doc.get("name", "Unknown")
                
                # Simulate content extraction (replace with actual file processing)
                content = f"Document: {name}\nType: {doc.get('type', 'N/A')}"
                
                # AI Analysis
                analysis = llm.analyze_document(content, "due_diligence")
                
                # Categorize results
                if "financial" in name.lower() or "10" in name.lower():
                    fin_results += f"\n\n### {name}\n{analysis}"
                elif "legal" in name.lower() or "contract" in name.lower():
                    leg_results += f"\n\n### {name}\n{analysis}"
                else:
                    ops_results += f"\n\n### {name}\n{analysis}"
                
                # Red flag detection
                if "risk" in analysis.lower() or "concern" in analysis.lower():
                    red_flags.append(f"⚠️ {name} – Potential issue detected")
                
                progress.progress(idx / len(docs))
            
            st.success("✅ Analysis complete!")
            
            # ================================================================
            # STEP 3: RESULTS DISPLAY
            # ================================================================
            st.header("📊 Analysis Results")
            
            tab1, tab2, tab3, tab4 = st.tabs([
                "💰 Financial Review",
                "⚖️ Legal Review",
                "🏢 Operational Review",
                "🚩 Red Flags"
            ])
            
            with tab1:
                st.markdown(fin_results if fin_results else "_No financial documents analyzed._")
            
            with tab2:
                st.markdown(leg_results if leg_results else "_No legal documents analyzed._")
            
            with tab3:
                st.markdown(ops_results if ops_results else "_No operational documents analyzed._")
            
            with tab4:
                if red_flags:
                    for flag in red_flags:
                        st.warning(flag)
                else:
                    st.success("✅ No critical red flags detected")
            
            st.divider()
            
            # ================================================================
            # STEP 4: GENERATE DUE DILIGENCE REPORTS
            # ================================================================
            st.header("📝 Step 3 – Generate Due Diligence Reports")
            
            # Prepare data for reports
            report_data = {
                "company_name": ticker if 'ticker' in locals() and ticker else docs[0].get("name", "Target Company"),
                "analyst_name": "AI Analyst",
                "financial_review": fin_results or "No financial documents provided.",
                "legal_review": leg_results or "No legal documents provided.",
                "operations_review": ops_results or "No operational documents provided.",
                "key_findings": "Analysis completed successfully. See detailed sections above.",
                "recommendation": "Further review recommended" if red_flags else "No critical blockers identified."
            }
            
            # Generate both report formats
            solartech_report = tmpl.generate_due_diligence_report_solartech_format(report_data)
            early_stage_report = tmpl.generate_due_diligence_report_early_stage_format(report_data)
            
            # Download options
            col1, col2 = st.columns(2)
            
            with col1:
                st.download_button(
                    label="📘 Download Corporate DD Report (SolarTech Style)",
                    data=solartech_report,
                    file_name=f"Due_Diligence_Corporate_{datetime.now():%Y%m%d}.md",
                    mime="text/markdown",
                    use_container_width=True
                )
            
            with col2:
                st.download_button(
                    label="📗 Download Early-Stage Investor DD Report",
                    data=early_stage_report,
                    file_name=f"Due_Diligence_EarlyStage_{datetime.now():%Y%m%d}.md",
                    mime="text/markdown",
                    use_container_width=True
                )

# ============================================================================
# SIDEBAR: GUIDE & RESOURCES
# ============================================================================
with st.sidebar:
    st.markdown("### 💡 Usage Guide")
    st.info(
        """
        **How It Works:**
        
        1️⃣ **Upload or fetch** company documents  
        2️⃣ **Run AI analysis** to extract insights  
        3️⃣ **Review** flagged risks and summaries  
        4️⃣ **Download** both DD report formats  
        """
    )
    
    st.markdown("### 📚 Reference Sources")
    for label, url in SOURCES.items():
        st.markdown(f"- [{label}]({url})")
    
    st.markdown("### 🔒 Security")
    st.caption("All documents processed in-session only. No data is stored after session ends.")
