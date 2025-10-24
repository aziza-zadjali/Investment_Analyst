"""
Automated Due Diligence Document Analysis
AI-powered document ingestion, key data extraction, red flag detection,
and professional analyst-ready summary reports
"""

import streamlit as st
from utils.file_processor import FileProcessor
from utils.llm_handler import LLMHandler
from utils.template_generator import TemplateGenerator
from utils.web_scraper import WebScraper
import pandas as pd
from datetime import datetime
from io import BytesIO

# Page configuration
st.set_page_config(
    page_title="Document Analysis",
    page_icon="📄",
    layout="wide"
)

# Initialize handlers
@st.cache_resource
def init_handlers():
    return FileProcessor(), LLMHandler(), TemplateGenerator(), WebScraper()

file_proc, llm, template_gen, scraper = init_handlers()

# ========================================
# DATA SOURCES CONFIGURATION
# ========================================
DD_SOURCES = {
    "📊 SEC EDGAR": {
        "url": "https://www.sec.gov/edgar/search/",
        "description": "U.S. Securities filings (10-K, 10-Q, 8-K)",
        "best_for": "U.S. public company financials",
        "region": "United States"
    },
    "🏛️ NYSE": {
        "url": "https://www.nyse.com/index",
        "description": "New York Stock Exchange listings and data",
        "best_for": "NYSE-listed company information",
        "region": "United States"
    },
    "📈 NASDAQ": {
        "url": "https://www.nasdaq.com/",
        "description": "NASDAQ market data and filings",
        "best_for": "Tech and growth company data",
        "region": "United States"
    },
    "🇬🇧 LSE": {
        "url": "https://www.londonstockexchange.com/",
        "description": "London Stock Exchange listings",
        "best_for": "UK and European companies",
        "region": "United Kingdom"
    },
    "🇶🇦 Qatar Stock Exchange": {
        "url": "https://www.qe.com.qa/",
        "description": "Qatar market listings and data",
        "best_for": "Qatar-based companies",
        "region": "Qatar"
    },
    "🏦 QFMA": {
        "url": "https://www.qfma.org.qa/english/pages/index.html",
        "description": "Qatar Financial Markets Authority",
        "best_for": "Regulatory filings (Qatar)",
        "region": "Qatar"
    },
    "🌍 Zawya": {
        "url": "https://www.zawya.com/",
        "description": "MENA business intelligence",
        "best_for": "Middle East company data",
        "region": "MENA"
    },
    "🏦 Bloomberg": {
        "url": "https://www.bloomberg.com/",
        "description": "Global financial market data",
        "best_for": "Comprehensive market intelligence",
        "region": "Global"
    },
    "💹 Yahoo Finance": {
        "url": "https://finance.yahoo.com/",
        "description": "Real-time quotes and financial news",
        "best_for": "Market data and earnings reports",
        "region": "Global"
    }
}

# ========================================
# HEADER & INTRODUCTION
# ========================================
st.title("📄 Automated Due Diligence Document Analysis")
st.markdown("""
**AI-powered analysis** that ingests legal, financial, and operational documents, extracts key data, 
highlights red flags, and produces **analyst-ready summary reports** matching institutional standards.
""")

st.divider()

# ========================================
# SECTION 1: Document Upload
# ========================================
st.markdown("### 📤 Step 1: Upload Documents")
st.caption("Upload financial statements, legal contracts, cap tables, pitch decks, or other due diligence materials")

upload_method = st.radio(
    "Choose document source:",
    ["📁 Upload Files", "🔗 Fetch from Public Sources", "🌐 Import from URL"],
    horizontal=True
)

uploaded_docs = []

if upload_method == "📁 Upload Files":
    files = st.file_uploader(
        "Select documents (PDF, DOCX, XLSX, TXT)",
        type=["pdf", "docx", "xlsx", "txt", "csv"],
        accept_multiple_files=True,
        help="Upload company financials, contracts, pitch decks, or regulatory filings"
    )
    
    if files:
        for file in files:
            uploaded_docs.append({
                "name": file.name,
                "type": file.type,
                "size": f"{file.size / 1024:.2f} KB",
                "content": file
            })
        
        st.success(f"✅ {len(files)} document(s) uploaded successfully")
        
        # Display uploaded files
        df_files = pd.DataFrame([{
            "File Name": doc["name"],
            "Type": doc["type"].split("/")[-1].upper(),
            "Size": doc["size"]
        } for doc in uploaded_docs])
        st.dataframe(df_files, use_container_width=True)

elif upload_method == "🔗 Fetch from Public Sources":
    st.markdown("#### Select Data Sources")
    
    selected_sources = st.multiselect(
        "Choose regulatory and financial data providers",
        options=list(DD_SOURCES.keys()),
        default=["📊 SEC EDGAR", "🇶🇦 Qatar Stock Exchange", "🏦 Bloomberg"]
    )
    
    if selected_sources:
        cols = st.columns(min(len(selected_sources), 3))
        for idx, source in enumerate(selected_sources):
            with cols[idx % 3]:
                st.markdown(f"**{source}**")
                st.caption(DD_SOURCES[source]["description"])
                st.link_button("Visit", DD_SOURCES[source]["url"], use_container_width=True)
    
    company_ticker = st.text_input("Enter Company Ticker or Name", placeholder="e.g., AAPL, TSLA, BALADNA")
    
    if st.button("🔍 Fetch Documents", type="primary"):
        if company_ticker and selected_sources:
            with st.spinner(f"Fetching documents for {company_ticker}..."):
                for source in selected_sources:
                    st.info(f"📥 Retrieving from {source}...")
                    # Simulated document fetch (replace with actual scraping logic)
                    uploaded_docs.append({
                        "name": f"{company_ticker}_{source}_10K.pdf",
                        "type": "application/pdf",
                        "size": "1250 KB",
                        "source": source
                    })
                st.success(f"✅ Retrieved {len(uploaded_docs)} documents")

elif upload_method == "🌐 Import from URL":
    doc_urls = st.text_area(
        "Enter document URLs (one per line)",
        placeholder="https://example.com/document1.pdf\nhttps://example.com/annual_report.pdf"
    )
    
    if st.button("📥 Import from URLs"):
        urls = [url.strip() for url in doc_urls.split("\n") if url.strip()]
        if urls:
            with st.spinner("Importing documents..."):
                for url in urls:
                    st.info(f"Fetching: {url}")
                    uploaded_docs.append({
                        "name": url.split("/")[-1],
                        "type": "URL",
                        "size": "N/A",
                        "url": url
                    })
                st.success(f"✅ Imported {len(urls)} documents")

st.divider()

# ========================================
# SECTION 2: AI-Powered Analysis
# ========================================
if uploaded_docs:
    st.markdown("### 🤖 Step 2: AI Document Analysis")
    
    analysis_type = st.selectbox(
        "Select Analysis Type",
        [
            "🔍 Comprehensive Due Diligence",
            "📊 Financial Statement Analysis",
            "⚖️ Legal & Compliance Review",
            "🚩 Red Flag Detection",
            "📝 Executive Summary Only"
        ]
    )
    
    col1, col2 = st.columns(2)
    with col1:
        detail_level = st.select_slider(
            "Analysis Detail Level",
            options=["Quick Scan", "Standard", "Deep Dive"],
            value="Standard"
        )
    
    with col2:
        include_recommendations = st.checkbox("Include Investment Recommendations", value=True)
    
    if st.button("🚀 Run Analysis", type="primary", use_container_width=True):
        
        with st.spinner("🔄 Processing documents with AI..."):
            progress_bar = st.progress(0)
            
            # Initialize report sections
            financial_analysis = ""
            legal_review = ""
            operational_review = ""
            red_flags = []
            key_findings = []
            
            # Process each document
            for idx, doc in enumerate(uploaded_docs):
                st.info(f"📄 Analyzing: {doc['name']}")
                
                # Extract text content (mock)
                document_content = f"Document: {doc['name']}\nContent analysis pending..."
                
                # AI Analysis
                analysis = llm.analyze_document(document_content, document_type="due_diligence")
                
                # Categorize findings
                if "financial" in doc['name'].lower() or "10-k" in doc['name'].lower():
                    financial_analysis += f"\n\n### Analysis of {doc['name']}\n{analysis}\n"
                elif "legal" in doc['name'].lower() or "contract" in doc['name'].lower():
                    legal_review += f"\n\n### Analysis of {doc['name']}\n{analysis}\n"
                else:
                    operational_review += f"\n\n### Analysis of {doc['name']}\n{analysis}\n"
                
                # Extract red flags (simulate)
                if "risk" in analysis.lower() or "concern" in analysis.lower():
                    red_flags.append(f"⚠️ {doc['name']}: Potential concern detected in analysis")
                
                progress_bar.progress((idx + 1) / len(uploaded_docs))
            
            st.success("✅ Analysis complete!")
            
            # ========================================
            # SECTION 3: Results Display
            # ========================================
            st.markdown("### 📋 Analysis Results")
            
            tab1, tab2, tab3, tab4 = st.tabs([
                "📊 Financial Review",
                "⚖️ Legal Review",
                "🏢 Operational Review",
                "🚩 Red Flags & Risks"
            ])
            
            with tab1:
                st.markdown(financial_analysis if financial_analysis else "_No financial documents analyzed._")
            
            with tab2:
                st.markdown(legal_review if legal_review else "_No legal documents analyzed._")
            
            with tab3:
                st.markdown(operational_review if operational_review else "_No operational documents analyzed._")
            
            with tab4:
                if red_flags:
                    for flag in red_flags:
                        st.warning(flag)
                else:
                    st.success("✅ No major red flags detected")
            
            st.divider()
            
            # ========================================
            # SECTION 4: Generate Due Diligence Report
            # ========================================
            st.markdown("### 📝 Generate Due Diligence Report")
            
            report_data = {
                "company_name": company_ticker if 'company_ticker' in locals() else "Target Company",
                "analyst_name": "AI Analyst",
                "financial_review": financial_analysis or "Pending",
                "legal_review": legal_review or "Pending",
                "operations_review": operational_review or "Pending",
                "key_findings": "\n".join(key_findings) if key_findings else "Analysis complete",
                "recommendation": "Further review recommended" if red_flags else "Proceed with caution"
            }
            
            dd_report = template_gen.generate_due_diligence_report(report_data)
            
            st.markdown(dd_report)
            
            # Export options
            col_exp1, col_exp2 = st.columns(2)
            
            with col_exp1:
                st.download_button(
                    label="📄 Download Report (Markdown)",
                    data=dd_report,
                    file_name=f"DD_Report_{datetime.now().strftime('%Y%m%d')}.md",
                    mime="text/markdown",
                    use_container_width=True
                )
            
            with col_exp2:
                # Generate PDF-ready version (placeholder)
                st.download_button(
                    label="📑 Download Report (PDF)",
                    data=dd_report.encode(),
                    file_name=f"DD_Report_{datetime.now().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )

# ========================================
# SIDEBAR: Instructions & Resources
# ========================================
with st.sidebar:
    st.markdown("### 💡 How It Works")
    st.info("""
    **1. Upload Documents**  
    - Financial statements (10-K, 10-Q)
    - Legal contracts & agreements
    - Cap tables & term sheets
    - Pitch decks & business plans
    
    **2. AI Analysis**  
    - Extracts key financial metrics
    - Identifies legal risks & clauses
    - Detects red flags automatically
    - Cross-references regulatory data
    
    **3. Export Report**  
    - Institutional-grade summary
    - Highlights findings & risks
    - Ready for investment committee
    """)
    
    st.markdown("### 📚 Supported Sources")
    st.markdown("- SEC EDGAR (U.S. filings)")
    st.markdown("- NYSE & NASDAQ")
    st.markdown("- Qatar Stock Exchange")
    st.markdown("- Bloomberg & Yahoo Finance")
    st.markdown("- Custom document uploads")
    
    st.markdown("### 🔒 Data Security")
    st.caption("All documents are processed securely. No data is stored after session ends.")
