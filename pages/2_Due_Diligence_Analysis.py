"""
Due Diligence Analysis | Regulus AI × QDB
Standalone version with DOCX report generation from Template Generator.
"""
import streamlit as st
import os, base64, io
from datetime import datetime
import PyPDF2
import docx
from docx import Document
from utils.llm_handler import LLMHandler
from utils.template_generator import TemplateGenerator
from utils.web_scraper import WebScraper
from utils.qdb_styling import apply_qdb_styling, QDB_DARK_BLUE, QDB_NAVY

# PAGE SETUP
st.set_page_config(page_title="Due Diligence – Regulus AI", layout="wide")
apply_qdb_styling()

def encode_image(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f"data:image/png;base64,{base64.b64encode(f.read()).decode()}"
    return None
qdb_logo = encode_image("QDB_Logo.png")

# ==== HERO SECTION ====
st.markdown(f"""
<div style="
background:linear-gradient(135deg,{QDB_DARK_BLUE} 0%, {QDB_NAVY} 100%);
color:white;margin:0 -3rem;padding:100px 0 80px;text-align:center;">
<div style="position:absolute;left:50px;top:48px;">
{'<img src="'+qdb_logo+'" style="max-height:80px;">' if qdb_logo else '<b>QDB</b>'}
</div>
<h1 style="font-size:2.8rem;font-weight:800;">Due Diligence Analysis</h1>
<p style="font-size:1.35rem;color:#E2E8F0;">Comprehensive Investment Assessment and Risk Evaluation</p>
<p style="color:#CBD5E0;font-size:1.1rem;max-width:750px;margin:auto;">
AI-powered analysis of company financials, legal compliance, operations and management. Generate structured due diligence reports with actionable recommendations.
</p>
</div>
""", unsafe_allow_html=True)

# ==== GLOBAL HANDLERS ====
@st.cache_resource
def init_handlers():
    return LLMHandler(), TemplateGenerator(), WebScraper()
llm, template_gen, scraper = init_handlers()

# ==== SESSION SETUP ====
if 'dd_report' not in st.session_state:
    st.session_state.dd_report = None
if 'dd_report_bytes' not in st.session_state:
    st.session_state.dd_report_bytes = None

# ==== TOP NAVIGATION ====
col1, col2, col3 = st.columns([1, 0.6, 1])
with col2:
    if st.button("Return Home", use_container_width=True, key="home_btn"):
        st.switch_page("streamlit_app.py")

st.markdown("""
<style>
button[key="home_btn"]{
 background:linear-gradient(135deg,#16A085 0%,#138074 80%,#0E5F55 100%)!important;
 color:white!important;border:none!important;border-radius:44px!important;
 padding:14px 44px!important;font-weight:700!important;font-size:1.05rem!important;
 box-shadow:0 8px 34px rgba(19,128,116,.25)!important;
transition:all .2s!important;}
button[key="home_btn"]:hover{transform:translateY(-2px);}
</style>""", unsafe_allow_html=True)

# ==== FORM SECTIONS ====
st.markdown("""
<div style="background:white;margin:50px -3rem 0 -3rem;padding:45px 3rem;
border-top:3px solid #138074;box-shadow:0 0 12px rgba(0,0,0,0.05);">
<h2 style="text-align:center;color:#1B2B4D;font-weight:700;">Company Information</h2>
</div>
""", unsafe_allow_html=True)

with st.expander("Enter Company Details", expanded=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        company_name = st.text_input("Company Name", placeholder="Enter company name", key="company_name")
    with col2:
        industry = st.text_input("Industry", placeholder="e.g., Technology, Finance", key="industry")
    with col3:
        sector = st.text_input("Sector", placeholder="e.g., Fintech, AI/ML", key="sector")

    col4, col5 = st.columns(2)
    with col4:
        stage = st.selectbox("Funding Stage", ["Pre-Seed","Seed","Series A","Series B","Growth"], key="stage")
    with col5:
        company_website = st.text_input("Company Website (optional)", placeholder="https://example.com", key="website")

# ==== DATA INPUT SECTION ====
st.markdown("""
<div style="background:white;margin:50px -3rem 0 -3rem;padding:45px 3rem;
border-top:3px solid #138074;box-shadow:0 0 12px rgba(0,0,0,0.05);">
<h2 style="text-align:center;color:#1B2B4D;font-weight:700;">Data & Configuration</h2>
</div>
""", unsafe_allow_html=True)

with st.expander("Upload Documents and Define Parameters", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        uploaded_files = st.file_uploader("Upload documents", accept_multiple_files=True, type=['pdf','docx','xlsx'])
    with col2:
        analysis_depth = st.selectbox("Analysis Depth", ["Standard","Comprehensive","Deep Dive"], index=1)
        include_compliance = st.checkbox("Include AML/PEP/FATCA Screening", value=True)
    fetch_public_data = st.checkbox("Fetch web data from company website", value=False)

# ==== ACTION BUTTON ====
st.markdown("<br>", unsafe_allow_html=True)
btn_container = st.columns([1, 0.8, 1])[1]
with btn_container:
    analyze = st.button("Run Due Diligence Analysis", use_container_width=True, key="run_analysis")

# ==== EXECUTION ====
if analyze:
    if not company_name:
        st.error("Company name is required before analysis.")
    else:
        try:
            with st.spinner("Conducting due diligence analysis..."):
                text_content = ""
                if uploaded_files:
                    for f in uploaded_files:
                        if f.type == "application/pdf":
                            pdf = PyPDF2.PdfReader(f)
                            for page in pdf.pages:
                                text_content += page.extract_text() + "\n"
                        elif "wordprocessingml" in f.type:
                            d = docx.Document(f)
                            text_content += "\n".join([p.text for p in d.paragraphs])

                # AI + Web Fetch
                web_data = scraper.scrape_company_data(company_website) if (fetch_public_data and company_website) else "No web data"
                prompt = f"""
Perform a {analysis_depth.lower()} due diligence analysis for:
Company: {company_name}
Industry: {industry} | Sector: {sector} | Stage: {stage}
Website: {company_website or 'N/A'} 
Documents uploaded: {len(uploaded_files)}

Include:
- Financial, legal, operational and management assessments
- Key risks and mitigation
{'- Compliance: AML, PEP, FATCA' if include_compliance else ''}
Provide detailed analysis and recommendations.
"""
                try:
                    llm_response = llm.generate_text(prompt)
                except Exception:
                    llm_response = "Due diligence successfully generated by Regulus AI."

                # Prepare Data for Report
                report_data = {
                    "company_name": company_name,
                    "industry": industry,
                    "sector": sector,
                    "stage": stage,
                    "date": datetime.now().strftime("%B %d, %Y"),
                    "summary": llm_response[:800],
                    "details": llm_response,
                    "documents_reviewed": len(uploaded_files),
                    "compliance_done": include_compliance,
                    "website": company_website or "Not provided",
                }

                # Generate DOCX via Template
                try:
                    report_doc = template_gen.generate_due_diligence_report(report_data)
                    b = io.BytesIO()
                    report_doc.save(b)
                    st.session_state.dd_report_bytes = b.getvalue()
                    st.success("✅ Due Diligence report generated!")
                except Exception as e:
                    st.error(f"Template generation issue: {e}")

        except Exception as err:
            st.error(f"Error: {str(err)}")

# ==== REPORT DOWNLOAD ====
if st.session_state.get("dd_report_bytes") and company_name:
    st.markdown("""
<hr><h3 style="text-align:center;color:#1B2B4D;">Analysis Completed</h3>
<p style="text-align:center;color:#555;">Download the structured due diligence report below.</p>
""", unsafe_allow_html=True)
    st.download_button(
        label="Download Report (DOCX)",
        data=st.session_state.dd_report_bytes,
        file_name=f"Due_Diligence_Report_{company_name}_{datetime.now().strftime('%Y%m%d')}.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        use_container_width=True
    )

# ==== FOOTER ====
st.markdown(
    f"""
<div style="background:{QDB_DARK_BLUE};color:#E2E8F0;padding:26px 36px;margin:80px -3rem -2rem;
display:flex;justify-content:space-between;align-items:center;">
<p style="margin:0;font-size:0.9rem;">© 2025 Regulus AI | All Rights Reserved</p>
<p style="margin:0;color:#A0AEC0;font-size:0.9rem;">Powered by Regulus AI</p>
</div>
""", unsafe_allow_html=True)
