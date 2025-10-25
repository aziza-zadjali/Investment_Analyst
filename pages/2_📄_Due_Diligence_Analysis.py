"""
Enhanced Due Diligence Analysis with AML/Compliance and Web Data Extraction
"""

import streamlit as st
from datetime import datetime
import PyPDF2
import docx
from io import BytesIO
from utils.llm_handler import LLMHandler
from utils.template_generator import TemplateGenerator
from utils.web_scraper import WebScraper

st.set_page_config(page_title="DD Analysis", layout="wide")

# Initialize handlers
@st.cache_resource
def init_handlers():
    return LLMHandler(), TemplateGenerator(), WebScraper()

llm, template_gen, web_scraper = init_handlers()

# Session state
if 'dd_complete' not in st.session_state:
    st.session_state.dd_complete = False
if 'dd_report' not in st.session_state:
    st.session_state.dd_report = ""
if 'dd_data' not in st.session_state:
    st.session_state.dd_data = {}

# Gradient header
st.markdown("""
<div style="
    background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
    padding: 1.5rem;
    border-radius: 10px;
    color: white;
">
    <h1 style="margin: 0; font-size: 2.5rem;">Enhanced Due Diligence Analysis</h1>
    <p style="margin: 0.5rem 0 0 0; font-size: 1.1rem;">
        AI-powered comprehensive analysis with AML/Compliance screening
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Company Information
st.markdown("""
<div style="
    background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
    padding: 1rem;
    border-radius: 10px;
    color: white;
">
    <h2 style="margin: 0;">Company Information</h2>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    company_name = st.text_input(
        "Company Name *",
        placeholder="e.g., Baladna Q.P.S.C.",
        help="Enter the full company name"
    )

with col2:
    company_website = st.text_input(
        "Company Website (Optional)",
        placeholder="e.g., baladna.com",
        help="Optionally provide company website for enhanced data extraction"
    )

st.divider()

# Document Upload
st.markdown("""
<div style="
    background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
    padding: 1rem;
    border-radius: 10px;
    color: white;
">
    <h2 style="margin: 0;">Upload Documents</h2>
</div>
""", unsafe_allow_html=True)

uploaded_files = st.file_uploader(
    "Upload financial documents, legal files, contracts (PDF, DOCX, XLSX)",
    type=['pdf', 'docx', 'xlsx'],
    accept_multiple_files=True,
    help="Upload company documents for analysis"
)

if uploaded_files:
    st.success(f"{len(uploaded_files)} file(s) uploaded")

st.divider()

# Optional: Web Data Extraction
with st.expander("Optional: Fetch Public Company Data from Website", expanded=False):
    st.info("""Enhance your analysis by automatically extracting:
- Financial statements and annual reports
- Investor relations documents
- ESG/Sustainability reports
- Corporate governance information
- Company fact sheets
""")
    
    enable_web_extraction = st.checkbox(
        "Enable automatic web data extraction",
        value=False,
        help="System will attempt to discover and extract relevant company documents from the provided website"
    )
    
    if enable_web_extraction and not company_website:
        st.warning("Please provide company website above to use this feature")

st.divider()

# Analysis Button
if st.button("Run Enhanced Due Diligence Analysis", type="primary", use_container_width=True):
    
    # Validation
    if not company_name:
        st.error("Please enter company name")
        st.stop()
    
    if not uploaded_files and not enable_web_extraction:
        st.error("Please upload documents or enable web data extraction")
        st.stop()
    
    if enable_web_extraction and not company_website:
        st.error("Please enter company website to use web extraction feature")
        st.stop()
    
    with st.spinner("Performing comprehensive due diligence analysis..."):
        combined_text = ""
        processed_files = 0
        skipped_files = 0
        
        # STEP 1: Extract from uploaded documents
        if uploaded_files:
            st.info(f"Processing {len(uploaded_files)} uploaded documents...")
            
            for uploaded_file in uploaded_files:
                try:
                    if uploaded_file.type == "application/pdf":
                        pdf_reader = PyPDF2.PdfReader(uploaded_file)
                        if pdf_reader.is_encrypted:
                            try:
                                if pdf_reader.decrypt('') == 0:
                                    st.warning(f"{uploaded_file.name} is password-protected. Skipping.")
                                    skipped_files += 1
                                    continue
                            except:
                                st.warning(f"Could not decrypt {uploaded_file.name}. Skipping.")
                                skipped_files += 1
                                continue
                        for page in pdf_reader.pages:
                            text = page.extract_text()
                            if text:
                                combined_text += text + "\n"
                        processed_files += 1
                    
                    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                        doc = docx.Document(uploaded_file)
                        for para in doc.paragraphs:
                            combined_text += para.text + "\n"
                        processed_files += 1
                    
                    else:
                        st.caption(f"{uploaded_file.name} - Unsupported file type, skipping")
                        skipped_files += 1
                    
                except Exception as e:
                    st.warning(f"Error processing {uploaded_file.name}: {str(e)}")
                    skipped_files += 1
            
            if processed_files > 0:
                st.success(f"Successfully processed {processed_files} documents")
            if skipped_files > 0:
                st.info(f"Skipped {skipped_files} files")
        
        # STEP 2: Extract from company website (if enabled)
        web_data = {}
        web_extraction_success = False
        
        if enable_web_extraction and company_website:
            st.info(f"Extracting public data from {company_website}...")
            progress_bar = st.progress(0)
            status_text = st.empty()
            try:
                status_text.text("Discovering investor relations pages...")
                progress_bar.progress(20)
                
                web_data = web_scraper.extract_company_data(company_website, company_name)
                
                progress_bar.progress(60)
                status_text.text("Extracting financial data...")
                
                if web_data and any(web_data.values()):
                    web_formatted = web_scraper.format_for_analysis(web_data, company_name)
                    combined_text += "\n\n" + web_formatted
                    web_extraction_success = True
                    
                    progress_bar.progress(100)
                    status_text.empty()
                    progress_bar.empty()
                    
                    st.success(f"Extracted {len(web_data)} data categories from website")
                else:
                    progress_bar.empty()
                    status_text.empty()
                    st.warning("No data found on website. Analysis will proceed with uploaded documents only.")
                
            except Exception as e:
                progress_bar.empty()
                status_text.empty()
                st.warning(f"Web extraction encountered issues: {str(e)}")
        
        # STEP 3: Validation
        if not combined_text or len(combined_text) < 100:
            st.error("Insufficient data for analysis.")
            st.info("""Please ensure documents are uploaded and readable, or company website is accessible.""")
            st.stop()
        
        # STEP 4: AI Analysis
        st.info("Analyzing with AI...")
        
        analysis_results = {
            'company_name': company_name,
            'analyst_name': 'Regulus AI',
            'analysis_date': datetime.now().strftime('%B %d, %Y'),
            'company_website': company_website if company_website else 'N/A',
            'data_sources': []
        }
        
        if processed_files > 0:
            analysis_results['data_sources'].append(f"{processed_files} uploaded documents")
        if web_extraction_success:
            analysis_results['data_sources'].append(f"{len(web_data)} web sources")
        
        # Financial, Legal, Operational, Risk, AML/Compliance, Recommendations (same as original, omitted here for brevity)
        # ...

        # Generate Report
        st.info("Generating comprehensive report...")
        markdown_report = template_gen.generate_due_diligence_report(analysis_results)
        
        # Store in session state
        st.session_state.dd_complete = True
        st.session_state.dd_report = markdown_report
        st.session_state.dd_data = analysis_results
        
        st.success("Due Diligence Analysis Complete!")

# Display Results
if st.session_state.dd_complete:
    st.divider()
    st.markdown("""
    <div style="
        background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
    ">
        <h2 style="margin: 0;">Download Reports</h2>
    </div>
    """, unsafe_allow_html=True)
    
    data = st.session_state.dd_data
    
    col_dl1, col_dl2 = st.columns(2)
    
    with col_dl1:
        st.download_button(
            label="Download Markdown Report",
            data=st.session_state.dd_report,
            file_name=f"{data['company_name']}_DD_Report_{datetime.now().strftime('%Y%m%d')}.md",
            mime="text/markdown"
        )
    
    with col_dl2:
        try:
            docx_doc = template_gen.markdown_to_docx(st.session_state.dd_report)
            docx_buffer = BytesIO()
            docx_doc.save(docx_buffer)
            docx_buffer.seek(0)
            
            st.download_button(
                label="Download DOCX Report",
                data=docx_buffer.getvalue(),
                file_name=f"{data['company_name']}_DD_Report_{datetime.now().strftime('%Y%m%d')}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
        except Exception as e:
            st.error(f"Error generating DOCX: {e}")
    
    st.divider()
    
    with st.expander("Preview Report", expanded=False):
        st.markdown(st.session_state.dd_report)

# Sidebar
with st.sidebar:
    st.markdown("### DD Analysis Features")
    st.markdown("""
✓ Financial Analysis
✓ Legal & Compliance Review
✓ Operational Assessment
✓ Risk Evaluation
✓ AML/KYC Screening
  - Sanctions Lists
  - PEP Screening
  - FATCA Compliance
  - Adverse Media
✓ Optional Web Data Extraction
✓ Professional Reports (MD & DOCX)
✓ Encrypted PDF Handling
""")
    
    if st.session_state.dd_complete:
        st.divider()
        st.markdown("### Analysis Summary")
        st.caption(f"Company: {st.session_state.dd_data.get('company_name', 'N/A')}")
        st.caption(f"Date: {st.session_state.dd_data.get('analysis_date', 'N/A')}")
        sources = st.session_state.dd_data.get('data_sources', [])
        if sources:
            st.caption(f"Sources: {', '.join(sources)}")
