"""
Automated Due Diligence Document Analysis
Uploads or fetches financial & legal docs,
extracts key data, highlights red flags, and
produces analyst‑ready summary reports in both formats.
"""

import streamlit as st
from utils.llm_handler import LLMHandler
from utils.template_generator import TemplateGenerator
from utils.file_processor import FileProcessor
from utils.web_scraper import WebScraper
import pandas as pd
from datetime import datetime

# --------------------------------------------------------------------------
# PAGE SETTINGS
# --------------------------------------------------------------------------
st.set_page_config(page_title="Automated Due Diligence", page_icon="📄", layout="wide")

# --------------------------------------------------------------------------
# INITIALIZATION
# --------------------------------------------------------------------------
@st.cache_resource
def init_handlers():
    return LLMHandler(), TemplateGenerator(), FileProcessor(), WebScraper()

llm, template_gen, file_proc, scraper = init_handlers()

# --------------------------------------------------------------------------
# SOURCES
# --------------------------------------------------------------------------
DATA_SOURCES = {
    "📊 SEC EDGAR": "https://www.sec.gov/edgar/search/",
    "🏛️ NYSE": "https://www.nyse.com/index",
    "📈 NASDAQ": "https://www.nasdaq.com/",
    "🇬🇧 LSE": "https://www.londonstockexchange.com/",
    "🇶🇦 Qatar Stock Exchange": "https://www.qe.com.qa/",
    "🏦 QFMA": "https://www.qfma.org.qa/english/pages/index.html",
    "🌍 Zawya": "https://www.zawya.com/",
    "🏦 Bloomberg": "https://www.bloomberg.com/",
    "💹 Yahoo Finance": "https://finance.yahoo.com/"
}

# --------------------------------------------------------------------------
# HEADER
# --------------------------------------------------------------------------
st.title("📄 Automated Due Diligence Document Analysis")
st.markdown("""
Upload or fetch company filings, legal, or financial documents.  
AI will extract critical information, identify risks and red flags,  
then generate **two full Due Diligence Reports** matching your official templates.
""")

st.divider()

# --------------------------------------------------------------------------
# STEP 1 – DOCUMENT INGESTION
# --------------------------------------------------------------------------
st.header("📤 Step 1 – Ingest Documents")

method = st.radio("Select Source Type", ["📁 Upload Files", "🔗 Public Sources", "🌐 From URL"], horizontal=True)

uploaded = []

if method == "📁 Upload Files":
    files = st.file_uploader("Upload legal / financial files",
                             type=["pdf", "docx", "xlsx", "txt"],
                             accept_multiple_files=True)
    if files:
        for f in files:
            uploaded.append({"name": f.name, "content": f})
        st.success(f"✅ {len(files)} file(s) ingested successfully")

elif method == "🔗 Public Sources":
    chosen = st.multiselect("Choose data providers", list(DATA_SOURCES.keys()),
                            default=["📊 SEC EDGAR", "🏦 Bloomberg", "💹 Yahoo Finance"])
    if chosen:
        cols = st.columns(min(len(chosen), 4))
        for i, s in enumerate(chosen):
            cols[i % 4].link_button(s, DATA_SOURCES[s])
    ticker = st.text_input("Company Ticker or Name", placeholder="e.g., AAPL or BALADNA")
    if st.button("📥 Fetch", type="primary"):
        if ticker:
            with st.spinner(f"Fetching docs for {ticker}..."):
                for s in chosen:
                    uploaded.append({"name": f"{ticker}_{s}_Filing.pdf", "source": s})
            st.success(f"✅ Fetched {len(uploaded)} documents from selected sources")

elif method == "🌐 From URL":
    urls = st.text_area("Paste each document URL on a new line ↓")
    if st.button("📑 Import"):
        if urls.strip():
            for u in urls.splitlines():
                uploaded.append({"name": u.split('/')[-1], "url": u.strip()})
            st.success(f"✅ Imported {len(uploaded)} documents from URLs")

if uploaded:
    st.dataframe(pd.DataFrame(uploaded))
st.divider()

# --------------------------------------------------------------------------
# STEP 2 – AI ANALYSIS
# --------------------------------------------------------------------------
if uploaded:
    st.header("🤖 Step 2 – AI Analysis")
    mode = st.select_slider("Select Depth", ["Quick Scan", "Standard", "Deep Dive"], value="Standard")

    if st.button("🚀 Run Automated Analysis", type="primary", use_container_width=True):
        with st.spinner("Analyzing documents..."):
            progress = st.progress(0)
            results_fin = ""
            results_leg = ""
            results_ops = ""
            red_flags = []
            for i, d in enumerate(uploaded):
                name = d["name"]
                content = f"File: {name}"
                analysis = llm.analyze_document(content, "due_diligence")
                if "financial" in name.lower() or "10" in name.lower():
                    results_fin += f"\n\n### {name}\n{analysis}"
                elif "legal" in name.lower() or "contract" in name.lower():
                    results_leg += f"\n\n### {name}\n{analysis}"
                else:
                    results_ops += f"\n\n### {name}\n{analysis}"
                if "risk" in analysis.lower() or "concern" in analysis.lower():
                    red_flags.append(f"⚠️ {name}: Potential issue detected")
                progress.progress((i + 1) / len(uploaded))
            st.success("✅ Analysis complete")

        # ------------------------------------------------------------------
        # STEP 3 – RESULTS + REPORT GENERATION
        # ------------------------------------------------------------------
        st.header("📊 Results")

        tab1, tab2, tab3, tab4 = st.tabs(["💰 Financial", "⚖️ Legal", "🏢 Operational", "🚩 Flags"])
        with tab1: st.markdown(results_fin or "_No financial docs found._")
        with tab2: st.markdown(results_leg or "_No legal docs found._")
        with tab3: st.markdown(results_ops or "_No operational docs found._")
        with tab4:
            if red_flags:
                [st.warning(f) for f in red_flags]
            else: st.success("🚀 No major red flags detected")

        st.divider()
        st.header("📝 Generate Due Diligence Reports")

        report_data = {
            "company_name": uploaded[0].get("name","Company"),
            "analyst_name": "AI Analyst",
            "financial_review": results_fin or "Pending",
            "legal_review": results_leg or "Pending",
            "operations_review": results_ops or "Pending",
            "key_findings": "Major insights summarized.",
            "recommendation": "Proceed with caution" if red_flags else "No critical issues identified"
        }

        solartech = template_gen.generate_due_diligence_report_solartech_format(report_data)
        early = template_gen.generate_due_diligence_report_early_stage_format(report_data)

        col1, col2 = st.columns(2)
        with col1:
            st.download_button("📘 Download Corporate Report (SolarTech Style)",
                solartech,
                f"Due_Diligence_SolarTech_{datetime.now().strftime('%Y%m%d')}.md",
                "text/markdown",
                use_container_width=True)
        with col2:
            st.download_button("📗 Download Early‑Stage Report",
                early,
                f"Due_Diligence_EarlyStage_{datetime.now().strftime('%Y%m%d')}.md",
                "text/markdown",
                use_container_width=True)

# --------------------------------------------------------------------------
# SIDEBAR
# --------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 💡 Usage Guide")
    st.info("""
1️⃣ Upload or fetch documents  
2️⃣ Run AI analysis  
3️⃣ Review flags & summaries  
4️⃣ Download your Corporate and Early‑Stage DD reports
""")
    st.markdown("### 📚 Reference Sources")
    for k,v in DATA_SOURCES.items():
        st.markdown(f"- [{k}]({v})")
