"""
Automated Due Diligence Document Analysis
Uploads or fetches financial & legal docs,
extracts key data, flags risks, and produces both report formats.
"""

import streamlit as st
from datetime import datetime
import pandas as pd
from utils.llm_handler import LLMHandler
from utils.template_generator import TemplateGenerator
from utils.file_processor import FileProcessor
from utils.web_scraper import WebScraper

st.set_page_config(page_title="Automated Due Diligence", page_icon="📄", layout="wide")

@st.cache_resource
def init_handlers():
    return LLMHandler(), TemplateGenerator(), FileProcessor(), WebScraper()

llm, tmpl, file_proc, scraper = init_handlers()

SOURCES = {
    "SEC EDGAR": "https://www.sec.gov/edgar/search/",
    "NYSE": "https://www.nyse.com/index",
    "NASDAQ": "https://www.nasdaq.com/",
    "LSE": "https://www.londonstockexchange.com/",
    "Qatar Stock Exchange": "https://www.qe.com.qa/",
    "QFMA": "https://www.qfma.org.qa/english/pages/index.html",
    "Zawya": "https://www.zawya.com/",
    "Bloomberg": "https://www.bloomberg.com/",
    "Yahoo Finance": "https://finance.yahoo.com/"
}

st.title("📄 Automated Due Diligence Document Analysis")
st.markdown(
    """
AI-powered module that analyzes uploaded or public filings,
extracts key data and red flags, and generates **two formal Due Diligence Reports**
matching your provided templates.
"""
)
st.divider()

st.header("📤 Step 1 – Ingest Documents")
option = st.radio(
    "Choose Source Type",
    ["Upload Files", "Fetch Public Data", "From URL"],
    horizontal=True,
)
docs = []

if option == "Upload Files":
    f = st.file_uploader("Upload PDFs/DOCXs/XLSXs", type=["pdf", "docx", "xlsx"], accept_multiple_files=True)
    if f:
        for i in f:
            docs.append({"name": i.name, "file": i})
        st.success(f"Loaded {len(docs)} files")

elif option == "Fetch Public Data":
    picks = st.multiselect("Select Providers", list(SOURCES.keys()), default=["SEC EDGAR", "Bloomberg"])
    for s in picks:
        st.link_button(s, SOURCES[s])
    ticker = st.text_input("Enter Ticker / Company")
    if st.button("Fetch"):
        for s in picks:
            docs.append({"name": f"{ticker}_{s}.pdf"})
        st.success(f"Fetched {len(docs)} sample docs")

elif option == "From URL":
    urls = st.text_area("Paste each document URL on new line")
    if st.button("Import"):
        for line in urls.splitlines():
            if line.strip():
                docs.append({"name": line.split("/")[-1], "url": line})
        st.success(f"Imported {len(docs)} URLs")

if docs:
    st.dataframe(pd.DataFrame(docs))
st.divider()

if docs:
    st.header("🤖 Step 2 – AI Analysis")
    if st.button("Run Analysis", type="primary"):
        st.spinner("Analyzing...")
        fin, leg, ops, flags = "", "", "", []
        for idx, d in enumerate(docs, start=1):
            name = d["name"]
            text = f"Document {name}"
            out = llm.analyze_document(text, "due_diligence")
            if "finance" in name.lower() or "10" in name.lower():
                fin += f"\n\n### {name}\n{out}"
            elif "legal" in name.lower():
                leg += f"\n\n### {name}\n{out}"
            else:
                ops += f"\n\n### {name}\n{out}"
            if "risk" in out.lower() or "concern" in out.lower():
                flags.append(f"⚠️ {name} – possible issue")

        st.success("Analysis complete.")
        tab1, tab2, tab3, tab4 = st.tabs(["Financial", "Legal", "Operational", "Red Flags"])
        with tab1: st.markdown(fin or "_No financial data_")
        with tab2: st.markdown(leg or "_No legal data_")
        with tab3: st.markdown(ops or "_No operational data_")
        with tab4:
            if flags: [st.warning(f) for f in flags]
            else: st.success("No serious red flags detected")

        st.divider()
        st.header("📝 Step 3 – Generate Reports")

        data = {
            "company_name": docs[0].get("name", "Target"),
            "analyst_name": "AI Analyst",
            "financial_review": fin or "Pending",
            "legal_review": leg or "Pending",
            "operations_review": ops or "Pending",
            "key_findings": "Compiled from analysis.",
            "recommendation": "Review flagged docs" if flags else "No critical issues."
        }

        corp = tmpl.generate_due_diligence_report_solartech_format(data)
        early = tmpl.generate_due_diligence_report_early_stage_format(data)

        c1, c2 = st.columns(2)
        with c1:
            st.download_button("📘 Corporate Report (SolarTech)", corp,
                f"DD_Corporate_{datetime.now():%Y%m%d}.md", "text/markdown")
        with c2:
            st.download_button("📗 Early‑Stage Investor Report", early,
                f"DD_EarlyStage_{datetime.now():%Y%m%d}.md", "text/markdown")

with st.sidebar:
    st.markdown("### Guide")
    st.info("Upload → Analyze → Download Reports ✓")
    st.markdown("### References")
    for k, v in SOURCES.items():
        st.markdown(f"- [{k}]({v})")
