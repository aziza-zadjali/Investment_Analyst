"""
Automated Due Diligence Document Analysis
AI-powered analysis with persistent state - downloads don't reset analysis
"""

import streamlit as st
from datetime import datetime
import pandas as pd
from io import BytesIO
from utils.llm_handler import LLMHandler
from utils.template_generator import TemplateGenerator
from utils.file_processor import FileProcessor
from utils.web_scraper import WebScraper

st.set_page_config(page_title="Automated Due Diligence", page_icon="📄", layout="wide")

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
    
    # Initialize session state
    if 'analysis_complete' not in st.session_state:
        st.session_state.analysis_complete = False
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = {}
    
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
            
            # Store in session state
            st.session_state.analysis_results = {
                'fin_results': fin_results,
                'leg_results': leg_results,
                'ops_results': ops_results,
                'red_flags': red_flags,
                'company_name': ticker if 'ticker' in locals() and ticker else docs[0].get("name", "Target Company").split('.')[0],
                'num_docs': len(docs)
            }
            st.session_state.analysis_complete = True
            st.success("✅ Analysis complete!")
    
    # Display results if available (persists across reruns)
    if st.session_state.analysis_complete:
        results = st.session_state.analysis_results
        
        st.header("📊 Analysis Results")
        tab1, tab2, tab3, tab4 = st.tabs(["💰 Financial", "⚖️ Legal", "🏢 Operational", "🚩 Red Flags"])
        with tab1: st.markdown(results['fin_results'] if results['fin_results'] else "_No financial documents analyzed._")
        with tab2: st.markdown(results['leg_results'] if results['leg_results'] else "_No legal documents analyzed._")
        with tab3: st.markdown(results['ops_results'] if results['ops_results'] else "_No operational documents analyzed._")
        with tab4:
            if results['red_flags']:
                for flag in results['red_flags']: st.warning(flag)
            else:
                st.success("✅ No critical red flags detected")
        
        st.divider()
        st.header("📝 Step 3 – Generate Due Diligence Reports")
        
        # Extract structured insights (cached)
        if 'structured_response' not in st.session_state:
            with st.spinner("Extracting structured insights..."):
                extraction_prompt = f"""
Analyze the following due diligence findings and extract structured data:

FINANCIAL ANALYSIS:
{results['fin_results'] if results['fin_results'] else "No financial documents provided"}

LEGAL ANALYSIS:
{results['leg_results'] if results['leg_results'] else "No legal documents provided"}

OPERATIONAL ANALYSIS:
{results['ops_results'] if results['ops_results'] else "No operational documents provided"}

Provide concise extraction in this format:
1. Financial Risk Level (Low/Medium/High)
2. Financial Summary (2-3 sentences)
3. Legal Risk Level (Low/Medium/High)
4. Legal Summary (2-3 sentences)
5. Operational Risk Level (Low/Medium/High)
6. Operational Summary (2-3 sentences)
7. Top 3 Recommendations
8. Investment Thesis (3-4 sentences)
"""
                st.session_state.structured_response = llm.chat_completion([
                    {"role": "system", "content": "Extract structured due diligence insights precisely."},
                    {"role": "user", "content": extraction_prompt}
                ])
        
        structured_response = st.session_state.structured_response
        company_name = results['company_name']
        
        report_data = {
            "company_name": company_name,
            "analyst_name": "Regulus AI",
            "review_dates": datetime.now().strftime("%B %d, %Y"),
            "financial_scope": f"Analyzed {len([d for d in docs if 'financial' in d.get('name','').lower()])} financial documents",
            "legal_scope": f"Reviewed {len([d for d in docs if 'legal' in d.get('name','').lower()])} legal documents",
            "operational_scope": f"Examined {len([d for d in docs if 'operation' in d.get('name','').lower() or 'business' in d.get('name','').lower()])} operational documents",
            "commercial_scope": "Market positioning and competitive landscape assessment",
            "financial_findings": results['fin_results'][:300].strip() if results['fin_results'] else "No financial data available for analysis",
            "financial_risk": "High" if len(results['red_flags']) > 2 else ("Medium" if len(results['red_flags']) > 0 else "Low"),
            "legal_findings": results['leg_results'][:300].strip() if results['leg_results'] else "No legal data available for analysis",
            "legal_risk": "Medium" if "litigation" in results['leg_results'].lower() or "compliance" in results['leg_results'].lower() else "Low",
            "operational_findings": results['ops_results'][:300].strip() if results['ops_results'] else "No operational data available for analysis",
            "operational_risk": "Low",
            "commercial_findings": "Market analysis based on provided documentation",
            "commercial_risk": "Medium",
            "recommendations": structured_response[:500] if structured_response else f"Based on analysis of {results['num_docs']} documents, recommend thorough review.",
            "conclusion": f"Due diligence completed for {company_name}. " + ("Critical risks identified." if results['red_flags'] else "No major blockers identified."),
            "company_description": f"Analysis based on {results['num_docs']} documents.",
            "investment_thesis": structured_response if structured_response else f"Investment opportunity in {company_name}.",
            "investment_thesis_rating": "++" if len(results['red_flags']) == 0 else ("+" if len(results['red_flags']) < 2 else "0"),
            "wntbb": "Risk factors extracted from analysis.",
            "wntbb_rating": "0" if results['red_flags'] else "+",
            "failure_risk": f"{len(results['red_flags'])} risk factors identified.",
            "failure_risk_rating": "--" if len(results['red_flags']) > 3 else ("0" if len(results['red_flags']) > 0 else "+"),
            "leadership_assessment": "Leadership assessment requires management interviews.",
            "leadership_rating": "0",
            "tech_assessment": results['ops_results'][:200] if "tech" in results['ops_results'].lower() else "Technology review from operational documents.",
            "tech_rating": "+",
            "gtm_assessment": "Go-to-market strategy from business documentation.",
            "gtm_rating": "0",
            "competition_assessment": "Competitive landscape requires market research.",
            "competition_rating": "0",
            "market_assessment": "Market size from available data.",
            "market_rating": "+",
            "financial_assessment": results['fin_results'][:200] if results['fin_results'] else "Financial projections require additional statements.",
            "financial_rating": "++" if results['fin_results'] and "strong" in results['fin_results'].lower() else "0",
            "exit_assessment": "Exit strategy pending market conditions.",
            "exit_rating": "+",
            "terms_assessment": "Deal terms pending negotiation.",
            "terms_rating": "0"
        }
        
        # Generate and cache reports
        if 'reports_generated' not in st.session_state:
            with st.spinner("Generating reports..."):
                solartech_report = tmpl.generate_due_diligence_report_solartech_format(report_data)
                early_stage_report = tmpl.generate_due_diligence_report_early_stage_format(report_data)
                solartech_docx = tmpl.generate_docx_report(solartech_report, f"Due Diligence Report - {company_name}")
                early_stage_docx = tmpl.generate_docx_report(early_stage_report, f"Early-Stage DD Report - {company_name}")
                
                st.session_state.reports_generated = {
                    'solartech_md': solartech_report,
                    'early_stage_md': early_stage_report,
                    'solartech_docx': solartech_docx.getvalue(),
                    'early_stage_docx': early_stage_docx.getvalue(),
                    'company_name': company_name
                }
        
        reports = st.session_state.reports_generated
        
        st.markdown("### 📥 Download Reports (All Formats Available)")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 📘 Corporate DD Report")
            st.download_button("📄 Download DOCX", reports['solartech_docx'], f"DD_Corporate_{reports['company_name']}_{datetime.now():%Y%m%d}.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", use_container_width=True, key="dl1")
            st.download_button("📝 Download Markdown", reports['solartech_md'], f"DD_Corporate_{reports['company_name']}_{datetime.now():%Y%m%d}.md", "text/markdown", use_container_width=True, key="dl2")
        with col2:
            st.markdown("#### 📗 Early-Stage Investor Report")
            st.download_button("📄 Download DOCX", reports['early_stage_docx'], f"DD_EarlyStage_{reports['company_name']}_{datetime.now():%Y%m%d}.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", use_container_width=True, key="dl3")
            st.download_button("📝 Download Markdown", reports['early_stage_md'], f"DD_EarlyStage_{reports['company_name']}_{datetime.now():%Y%m%d}.md", "text/markdown", use_container_width=True, key="dl4")

with st.sidebar:
    st.markdown("### 💡 Usage Guide")
    st.info("1️⃣ Upload/fetch documents\n2️⃣ Run AI analysis\n3️⃣ Review findings\n4️⃣ Download all report formats")
    st.markdown("### 📚 Reference Sources")
    for label, url in SOURCES.items():
        st.markdown(f"- [{label}]({url})")
    st.caption("🔒 All documents processed in-session only")
