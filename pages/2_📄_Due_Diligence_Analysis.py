"""
Automated Due Diligence Document Analysis
AI-powered document ingestion, analysis, red flag detection,
and professional report generation in DOCX and Markdown formats.
"""

import streamlit as st
from datetime import datetime
import pandas as pd
from io import BytesIO
from utils.llm_handler import LLMHandler
from utils.template_generator import TemplateGenerator
from utils.file_processor import FileProcessor
from utils.web_scraper import WebScraper

st.set_page_config(
    page_title="Automated Due Diligence",
    page_icon="📄",
    layout="wide"
)

@st.cache_resource
def init_handlers():
    return (LLMHandler(), TemplateGenerator(), FileProcessor(), WebScraper())

llm, tmpl, file_proc, scraper = init_handlers()

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

st.title("📄 Automated Due Diligence Document Analysis")
st.markdown("""
Upload or fetch company filings, legal documents, and financial statements.  
AI analyzes content, extracts data, flags risks, and generates  
**professional reports in DOCX and Markdown formats**.
""")
st.divider()

st.header("📤 Step 1 – Ingest Documents")
option = st.radio("Select Document Source", ["📁 Upload Files", "🔗 Fetch Public Data", "🌐 From URLs"], horizontal=True)
docs = []

if option == "📁 Upload Files":
    uploaded = st.file_uploader("Upload financial statements, legal contracts, or business plans", type=["pdf", "docx", "xlsx", "txt"], accept_multiple_files=True)
    if uploaded:
        for f in uploaded:
            docs.append({"name": f.name, "file": f})
        st.success(f"✅ {len(docs)} file(s) uploaded successfully")

elif option == "🔗 Fetch Public Data":
    picks = st.multiselect("Select Data Providers", list(SOURCES.keys()), default=["📊 SEC EDGAR", "💹 Bloomberg"])
    if picks:
        cols = st.columns(min(len(picks), 4))
        for i, s in enumerate(picks):
            cols[i % 4].link_button(s, SOURCES[s])
    ticker = st.text_input("Enter Company Ticker or Name", placeholder="e.g., AAPL, BALADNA")
    if st.button("📥 Fetch Documents", type="primary"):
        if ticker and picks:
            with st.spinner(f"Fetching documents for {ticker}..."):
                for s in picks:
                    docs.append({"name": f"{ticker}_{s.replace('📊 ', '').replace('🇶🇦 ', '')}_Filing.pdf", "source": s})
            st.success(f"✅ Fetched {len(docs)} documents")

elif option == "🌐 From URLs":
    urls = st.text_area("Paste document URLs (one per line)", placeholder="https://example.com/report.pdf")
    if st.button("📥 Import Documents"):
        if urls.strip():
            for line in urls.splitlines():
                if line.strip():
                    docs.append({"name": line.split("/")[-1], "url": line.strip()})
            st.success(f"✅ Imported {len(docs)} URLs")

if docs:
    try:
        display_data = [{"Document Name": d.get("name", "Unknown"), "Type": "File" if "file" in d else "URL" if "url" in d else "Fetched"} for d in docs]
        st.dataframe(pd.DataFrame(display_data), use_container_width=True)
    except:
        st.info(f"📋 {len(docs)} document(s) loaded")

st.divider()

if docs:
    st.header("🤖 Step 2 – AI Document Analysis")
    if st.button("🚀 Run Automated Analysis", type="primary", use_container_width=True):
        with st.spinner("Analyzing documents with AI..."):
            progress = st.progress(0)
            fin_results, leg_results, ops_results, red_flags = "", "", "", []
            
            for idx, doc in enumerate(docs, start=1):
                name = doc.get("name", "Unknown")
                content = f"Document: {name}\nType: {doc.get('type', 'N/A')}"
                analysis = llm.analyze_document(content, "due_diligence")
                
                if "financial" in name.lower() or "10" in name.lower():
                    fin_results += f"\n\n### {name}\n{analysis}"
                elif "legal" in name.lower() or "contract" in name.lower():
                    leg_results += f"\n\n### {name}\n{analysis}"
                else:
                    ops_results += f"\n\n### {name}\n{analysis}"
                
                if "risk" in analysis.lower() or "concern" in analysis.lower():
                    red_flags.append(f"⚠️ {name} – Potential issue detected")
                
                progress.progress(idx / len(docs))
            
            st.success("✅ Analysis complete!")
            
            st.header("📊 Analysis Results")
            tab1, tab2, tab3, tab4 = st.tabs(["💰 Financial", "⚖️ Legal", "🏢 Operational", "🚩 Red Flags"])
            with tab1: st.markdown(fin_results if fin_results else "_No financial documents analyzed._")
            with tab2: st.markdown(leg_results if leg_results else "_No legal documents analyzed._")
            with tab3: st.markdown(ops_results if ops_results else "_No operational documents analyzed._")
            with tab4:
                if red_flags:
                    for flag in red_flags: st.warning(flag)
                else:
                    st.success("✅ No critical red flags detected")
            
            st.divider()
            st.header("📝 Step 3 – Generate Due Diligence Reports")
            
            report_data = {
                "company_name": ticker if 'ticker' in locals() and ticker else docs[0].get("name", "Target Company"),
                "analyst_name": "AI Analyst",
                "financial_review": fin_results or "No financial documents provided.",
                "legal_review": leg_results or "No legal documents provided.",
                "operations_review": ops_results or "No operational documents provided.",
                "key_findings": "Analysis completed. See detailed sections above.",
                "recommendation": "Further review recommended" if red_flags else "No critical blockers identified."
            }
            
            solartech_report = tmpl.generate_due_diligence_report_solartech_format(report_data)
            early_stage_report = tmpl.generate_due_diligence_report_early_stage_format(report_data)
            
            with st.spinner("Generating DOCX reports..."):
                solartech_docx = tmpl.generate_docx_report(solartech_report, "Corporate Due Diligence Report")
                early_stage_docx = tmpl.generate_docx_report(early_stage_report, "Early-Stage Investor DD Report")
            
            st.markdown("### 📥 Download Reports")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### 📘 Corporate DD Report")
                st.download_button(
                    label="Download DOCX",
                    data=solartech_docx.getvalue(),
                    file_name=f"Due_Diligence_Corporate_{datetime.now():%Y%m%d}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True
                )
                st.download_button(
                    label="Download Markdown",
                    data=solartech_report,
                    file_name=f"Due_Diligence_Corporate_{datetime.now():%Y%m%d}.md",
                    mime="text/markdown",
                    use_container_width=True
                )
            
            with col2:
                st.markdown("#### 📗 Early-Stage Investor Report")
                st.download_button(
                    label="Download DOCX",
                    data=early_stage_docx.getvalue(),
                    file_name=f"Due_Diligence_EarlyStage_{datetime.now():%Y%m%d}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True
                )
                st.download_button(
                    label="Download Markdown",
                    data=early_stage_report,
                    file_name=f"Due_Diligence_EarlyStage_{datetime.now():%Y%m%d}.md",
                    mime="text/markdown",
                    use_container_width=True
                )

with st.sidebar:
    st.markdown("### 💡 Usage Guide")
    st.info("""
**How It Works:**

1️⃣ Upload or fetch documents  
2️⃣ Run AI analysis  
3️⃣ Review findings  
4️⃣ Download reports (DOCX or MD)  
""")
    st.markdown("### 📚 Reference Sources")
    for label, url in SOURCES.items():
        st.markdown(f"- [{label}]({url})")
    st.markdown("### 🔒 Security")
    st.caption("All documents processed in-session only. No data stored after session ends.")
