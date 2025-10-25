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

st.set_page_config(page_title="DD Analysis", page_icon="📄", layout="wide")

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

st.markdown("""
<div style="padding: 1.5rem 0; border-bottom: 2px solid #f0f0f0;">
    <h1 style="margin: 0; font-size: 2.5rem;">📄 Enhanced Due Diligence Analysis</h1>
    <p style="margin: 0.5rem 0 0 0; color: #666; font-size: 1.1rem;">
        AI-powered comprehensive analysis with AML/Compliance screening and automatic web data extraction
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Company Information
st.subheader("🏢 Company Information")

col1, col2 = st.columns(2)

with col1:
    company_name = st.text_input(
        "Company Name *",
        placeholder="e.g., Baladna Q.P.S.C.",
        help="Enter the full company name"
    )

with col2:
    company_website = st.text_input(
        "Company Website",
        placeholder="e.g., baladna.com or https://www.baladna.com",
        help="Enter company website for automatic data extraction (optional)"
    )

st.divider()

# Web Data Extraction Options
st.subheader("🌐 Automatic Web Data Extraction")

st.info("""
**🚀 Smart Web Extraction:** The system will automatically:
- Discover investor relations pages
- Extract financial statements, annual reports, governance docs
- Pull sustainability/ESG reports
- Gather fact sheets and company profiles
- Extract share/stock information

This enriches your DD report with the latest public information!
""")

col_web1, col_web2 = st.columns(2)

with col_web1:
    enable_web_extraction = st.checkbox(
        "Enable Automatic Web Data Extraction",
        value=False,
        help="Automatically fetch public company data from website"
    )

with col_web2:
    if enable_web_extraction:
        st.info("✓ Web extraction enabled - will fetch data from company website")
    else:
        st.caption("Web extraction disabled - only uploaded documents will be analyzed")

st.divider()

# Document Upload
st.subheader("📤 Upload Documents")

uploaded_files = st.file_uploader(
    "Upload financial documents, legal files, contracts (PDF, DOCX, XLSX)",
    type=['pdf', 'docx', 'xlsx'],
    accept_multiple_files=True,
    help="Upload any existing documents you have for analysis (optional if web extraction is enabled)"
)

if uploaded_files:
    st.success(f"✅ {len(uploaded_files)} file(s) uploaded")

st.divider()

# Analysis Button
if st.button("🔍 Run Enhanced Due Diligence Analysis", type="primary", use_container_width=True):
    
    # Validation
    if not company_name:
        st.error("⚠️ Please enter company name")
        st.stop()
    
    if enable_web_extraction and not company_website:
        st.error("⚠️ Please enter company website for web extraction")
        st.stop()
    
    if not uploaded_files and not enable_web_extraction:
        st.error("⚠️ Please either upload documents OR enable web data extraction")
        st.stop()
    
    with st.spinner("🤖 Performing comprehensive due diligence analysis..."):
        
        combined_text = ""
        
        # STEP 1: Extract from uploaded documents
        if uploaded_files:
            st.info(f"📄 Processing {len(uploaded_files)} uploaded documents...")
            
            for uploaded_file in uploaded_files:
                try:
                    if uploaded_file.type == "application/pdf":
                        pdf_reader = PyPDF2.PdfReader(uploaded_file)
                        for page in pdf_reader.pages:
                            text = page.extract_text()
                            if text:
                                combined_text += text + "\n"
                    
                    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                        doc = docx.Document(uploaded_file)
                        for para in doc.paragraphs:
                            combined_text += para.text + "\n"
                    
                except Exception as e:
                    st.warning(f"⚠️ Could not process {uploaded_file.name}: {e}")
            
            if combined_text:
                st.success(f"✅ Processed {len(uploaded_files)} documents ({len(combined_text)} characters)")
        
        # STEP 2: Extract from company website
        web_data = {}
        web_extraction_success = False
        
        if enable_web_extraction and company_website:
            st.info(f"🌐 Extracting data from {company_website}...")
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                status_text.text("🔍 Discovering investor relations pages...")
                progress_bar.progress(20)
                
                web_data = web_scraper.extract_company_data(company_website, company_name)
                
                progress_bar.progress(60)
                status_text.text("📊 Extracting financial data...")
                
                if web_data and any(web_data.values()):
                    web_formatted = web_scraper.format_for_analysis(web_data, company_name)
                    combined_text += "\n\n" + web_formatted
                    web_extraction_success = True
                    
                    progress_bar.progress(100)
                    status_text.empty()
                    progress_bar.empty()
                    
                    st.success(f"✅ Extracted {len(web_data)} data categories from website:")
                    
                    cols = st.columns(min(4, len(web_data)))
                    for idx, category in enumerate(web_data.keys()):
                        with cols[idx % len(cols)]:
                            st.caption(f"✓ {category.replace('_', ' ').title()}")
                else:
                    progress_bar.empty()
                    status_text.empty()
                    st.warning("⚠️ No data found on website. Please check URL or upload documents.")
                
            except Exception as e:
                progress_bar.empty()
                status_text.empty()
                st.error(f"❌ Web extraction failed: {str(e)}")
                st.info("💡 Try uploading documents manually or check if the website is accessible")
        
        # STEP 3: Validation
        if not combined_text or len(combined_text) < 100:
            st.error("⚠️ Insufficient data for analysis.")
            st.info("""
**Please ensure:**
- Documents are uploaded and readable, OR
- Company website URL is correct and accessible
- Website has investor relations/corporate pages
            """)
            st.stop()
        
        # STEP 4: AI Analysis
        st.info("🤖 Analyzing with AI...")
        
        analysis_results = {
            'company_name': company_name,
            'analyst_name': 'Regulus AI',
            'analysis_date': datetime.now().strftime('%B %d, %Y'),
            'company_website': company_website,
            'data_sources': []
        }
        
        if uploaded_files:
            analysis_results['data_sources'].append(f"{len(uploaded_files)} uploaded documents")
        if web_extraction_success:
            analysis_results['data_sources'].append(f"{len(web_data)} website sections")
        
        # Financial Analysis
        st.info("📊 Analyzing financials...")
        financial_prompt = f"""
        Analyze the financial health and performance of {company_name}:
        
        {combined_text[:8000]}
        
        Provide detailed analysis covering:
        1. Revenue trends and growth
        2. Profitability metrics (margins, EBITDA)
        3. Cash flow and liquidity position
        4. Asset quality and leverage ratios
        5. Key financial ratios (ROE, ROA, debt-to-equity)
        6. Red flags or concerns
        
        Be specific with numbers and dates.
        """
        
        try:
            analysis_results['financial_analysis'] = llm.generate(financial_prompt)
        except Exception as e:
            st.warning(f"Financial analysis error: {e}")
            analysis_results['financial_analysis'] = "Analysis unavailable due to error"
        
        # Legal Analysis
        st.info("⚖️ Reviewing legal & compliance...")
        legal_prompt = f"""
        Review legal and compliance aspects for {company_name}:
        
        {combined_text[:8000]}
        
        Cover:
        1. Corporate structure and governance
        2. Regulatory compliance status
        3. Legal proceedings or disputes
        4. Intellectual property
        5. Contractual obligations
        6. Compliance risks
        """
        
        try:
            analysis_results['legal_analysis'] = llm.generate(legal_prompt)
        except Exception as e:
            analysis_results['legal_analysis'] = "Analysis unavailable"
        
        # Operational Analysis
        st.info("🏭 Assessing operations...")
        operational_prompt = f"""
        Assess operational capabilities of {company_name}:
        
        {combined_text[:8000]}
        
        Analyze:
        1. Business model and operations
        2. Supply chain and distribution
        3. Technology and systems
        4. Human resources and management
        5. Operational efficiency
        6. Scalability potential
        """
        
        try:
            analysis_results['operational_analysis'] = llm.generate(operational_prompt)
        except
