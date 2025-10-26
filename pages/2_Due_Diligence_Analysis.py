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
        AI-powered comprehensive analysis with AML/Compliance screening
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
        "Company Website (Optional)",
        placeholder="e.g., baladna.com",
        help="Optionally provide company website for enhanced data extraction"
    )

st.divider()

# Document Upload
st.subheader("📤 Upload Documents")

uploaded_files = st.file_uploader(
    "Upload financial documents, legal files, contracts (PDF, DOCX, XLSX)",
    type=['pdf', 'docx', 'xlsx'],
    accept_multiple_files=True,
    help="Upload company documents for analysis"
)

if uploaded_files:
    st.success(f"✅ {len(uploaded_files)} file(s) uploaded")

st.divider()

# Optional: Web Data Extraction
with st.expander("🌐 **Optional:** Fetch Public Company Data from Website", expanded=False):
    st.info("""
**Enhance your analysis by automatically extracting:**
- Financial statements and annual reports
- Investor relations documents
- ESG/Sustainability reports
- Corporate governance information
- Company fact sheets

This feature works best with publicly listed companies that have dedicated investor relations pages.
    """)
    
    enable_web_extraction = st.checkbox(
        "Enable automatic web data extraction",
        value=False,
        help="System will attempt to discover and extract relevant company documents from the provided website"
    )
    
    if enable_web_extraction and not company_website:
        st.warning("⚠️ Please provide company website above to use this feature")

st.divider()

# Analysis Button
if st.button("🔍 Run Enhanced Due Diligence Analysis", type="primary", use_container_width=True):
    
    # Validation
    if not company_name:
        st.error("⚠️ Please enter company name")
        st.stop()
    
    if not uploaded_files and not enable_web_extraction:
        st.error("⚠️ Please upload documents or enable web data extraction")
        st.stop()
    
    if enable_web_extraction and not company_website:
        st.error("⚠️ Please enter company website to use web extraction feature")
        st.stop()
    
    with st.spinner("🤖 Performing comprehensive due diligence analysis..."):
        
        combined_text = ""
        processed_files = 0
        skipped_files = 0
        
        # STEP 1: Extract from uploaded documents
        if uploaded_files:
            st.info(f"📄 Processing {len(uploaded_files)} uploaded documents...")
            
            for uploaded_file in uploaded_files:
                try:
                    if uploaded_file.type == "application/pdf":
                        # Enhanced PDF handling with encryption support
                        try:
                            pdf_reader = PyPDF2.PdfReader(uploaded_file)
                            
                            # Check if PDF is encrypted
                            if pdf_reader.is_encrypted:
                                try:
                                    # Try to decrypt with empty password (some PDFs allow this)
                                    decrypt_result = pdf_reader.decrypt('')
                                    if decrypt_result == 0:
                                        # Decryption failed
                                        st.warning(f"⚠️ {uploaded_file.name} is password-protected. Skipping this file.")
                                        st.caption("💡 Tip: Please upload an unencrypted version or add pycryptodome to requirements.txt")
                                        skipped_files += 1
                                        continue
                                except Exception as decrypt_error:
                                    st.warning(f"⚠️ Could not decrypt {uploaded_file.name}. Skipping.")
                                    skipped_files += 1
                                    continue
                            
                            # Extract text from PDF
                            for page in pdf_reader.pages:
                                text = page.extract_text()
                                if text:
                                    combined_text += text + "\n"
                            
                            processed_files += 1
                            
                        except Exception as pdf_error:
                            if "PyCryptodome" in str(pdf_error) or "AES" in str(pdf_error):
                                st.warning(f"⚠️ {uploaded_file.name} requires PyCryptodome library for decryption. Skipping.")
                                st.caption("💡 Add `pycryptodome>=3.19.0` to requirements.txt to process encrypted PDFs")
                            else:
                                st.warning(f"⚠️ Could not process {uploaded_file.name}: {str(pdf_error)}")
                            skipped_files += 1
                            continue
                    
                    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                        doc = docx.Document(uploaded_file)
                        for para in doc.paragraphs:
                            combined_text += para.text + "\n"
                        processed_files += 1
                    
                    else:
                        # Other file types
                        st.caption(f"ℹ️ {uploaded_file.name} - Unsupported file type, skipping")
                        skipped_files += 1
                    
                except Exception as e:
                    st.warning(f"⚠️ Error processing {uploaded_file.name}: {str(e)}")
                    skipped_files += 1
            
            if processed_files > 0:
                st.success(f"✅ Successfully processed {processed_files} documents ({len(combined_text)} characters)")
            if skipped_files > 0:
                st.info(f"ℹ️ Skipped {skipped_files} files (encrypted or unsupported)")
        
        # STEP 2: Extract from company website (if enabled)
        web_data = {}
        web_extraction_success = False
        
        if enable_web_extraction and company_website:
            st.info(f"🌐 Extracting public data from {company_website}...")
            
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
                    st.warning("⚠️ No data found on website. Analysis will proceed with uploaded documents only.")
                
            except Exception as e:
                progress_bar.empty()
                status_text.empty()
                st.warning(f"⚠️ Web extraction encountered issues: {str(e)}")
                st.info("💡 Analysis will proceed with uploaded documents")
        
        # STEP 3: Validation
        if not combined_text or len(combined_text) < 100:
            st.error("⚠️ Insufficient data for analysis.")
            st.info("""
**Please ensure:**
- Documents are uploaded and readable, OR
- Company website is accessible with investor relations content
- If uploading encrypted PDFs, add pycryptodome to requirements.txt
            """)
            st.stop()
        
        # STEP 4: AI Analysis
        st.info("🤖 Analyzing with AI...")
        
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
        except Exception as e:
            analysis_results['operational_analysis'] = "Analysis unavailable"
        
        # Risk Assessment
        st.info("⚠️ Evaluating risks...")
        risk_prompt = f"""
        Comprehensive risk assessment for {company_name}:
        
        {combined_text[:8000]}
        
        Identify and assess:
        1. Market and competitive risks
        2. Financial risks
        3. Operational risks
        4. Regulatory and legal risks
        5. Strategic risks
        6. Overall risk rating (Low/Medium/High)
        """
        
        try:
            analysis_results['risk_assessment'] = llm.generate(risk_prompt)
        except Exception as e:
            analysis_results['risk_assessment'] = "Assessment unavailable"
        
        # AML/Compliance Screening
        st.info("🔒 Performing AML/KYC screening...")
        
        # Sanctions
        sanctions_prompt = f"""
        Conduct sanctions screening for {company_name}:
        
        {combined_text[:4000]}
        
        Check for:
        - OFAC SDN list concerns
        - EU/UN sanctions exposure
        - High-risk jurisdiction connections
        - Sanctioned activities or parties
        
        Provide screening status.
        """
        
        try:
            analysis_results['sanctions_screening'] = llm.generate(sanctions_prompt)
        except:
            analysis_results['sanctions_screening'] = "Screening pending"
        
        # PEP
        pep_prompt = f"""
        PEP (Politically Exposed Persons) screening for {company_name}:
        
        {combined_text[:4000]}
        
        Identify:
        - Key individuals and roles
        - PEP connections
        - Enhanced due diligence requirements
        - Risk classification
        """
        
        try:
            analysis_results['pep_screening'] = llm.generate(pep_prompt)
        except:
            analysis_results['pep_screening'] = "Screening pending"
        
        # FATCA
        fatca_prompt = f"""
        FATCA compliance assessment for {company_name}:
        
        {combined_text[:4000]}
        
        Review:
        - Entity classification
        - GIIN status
        - US person indicators
        - Compliance requirements
        """
        
        try:
            analysis_results['fatca_compliance'] = llm.generate(fatca_prompt)
        except:
            analysis_results['fatca_compliance'] = "Review pending"
        
        # Adverse Media
        adverse_prompt = f"""
        Adverse media screening for {company_name}:
        
        {combined_text[:4000]}
        
        Check for:
        - Financial crime indicators
        - Regulatory actions
        - Negative press
        - Reputational risks
        """
        
        try:
            analysis_results['adverse_media'] = llm.generate(adverse_prompt)
        except:
            analysis_results['adverse_media'] = "Screening pending"
        
        # Recommendations
        st.info("💡 Generating recommendations...")
        rec_prompt = f"""
        Based on all analysis for {company_name}, provide:
        
        1. Investment recommendation (Proceed/Caution/Decline)
        2. Key strengths
        3. Major concerns
        4. Required actions before proceeding
        5. Overall assessment
        
        Context: {combined_text[:5000]}
        """
        
        try:
            analysis_results['recommendations'] = llm.generate(rec_prompt)
        except:
            analysis_results['recommendations'] = "Recommendations pending"
        
        # Generate Report
        st.info("📝 Generating comprehensive report...")
        markdown_report = template_gen.generate_due_diligence_report(analysis_results)
        
        # Store in session state
        st.session_state.dd_complete = True
        st.session_state.dd_report = markdown_report
        st.session_state.dd_data = analysis_results
        
        st.success("✅ Due Diligence Analysis Complete!")

# Display Results
if st.session_state.dd_complete:
    
    st.divider()
    st.subheader("📥 Download Reports")
    
    data = st.session_state.dd_data
    
    col_dl1, col_dl2 = st.columns(2)
    
    with col_dl1:
        st.download_button(
            label="⬇️ Download Markdown Report",
            data=st.session_state.dd_report,
            file_name=f"{data['company_name']}_DD_Report_{datetime.now().strftime('%Y%m%d')}.md",
            mime="text/markdown"
        )
    
    with col_dl2:
        # Generate DOCX from markdown
        try:
            docx_doc = template_gen.markdown_to_docx(st.session_state.dd_report)
            
            # Save to BytesIO
            docx_buffer = BytesIO()
            docx_doc.save(docx_buffer)
            docx_buffer.seek(0)
            
            st.download_button(
                label="⬇️ Download DOCX Report",
                data=docx_buffer.getvalue(),
                file_name=f"{data['company_name']}_DD_Report_{datetime.now().strftime('%Y%m%d')}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
        except Exception as e:
            st.error(f"Error generating DOCX: {e}")
    
    st.divider()
    
    # Preview
    with st.expander("📄 Preview Report", expanded=False):
        st.markdown(st.session_state.dd_report)

# Sidebar
with st.sidebar:
    st.markdown("### 💡 DD Analysis Features")
    st.markdown("""
✓ **Financial Analysis**
✓ **Legal & Compliance Review**
✓ **Operational Assessment**
✓ **Risk Evaluation**
✓ **AML/KYC Screening**
  - Sanctions Lists
  - PEP Screening
  - FATCA Compliance
  - Adverse Media
✓ **Optional Web Data Extraction**
✓ **Professional Reports (MD & DOCX)**
✓ **Encrypted PDF Handling**
""")
    
    if st.session_state.dd_complete:
        st.divider()
        st.markdown("### 📋 Analysis Summary")
        st.caption(f"**Company:** {st.session_state.dd_data.get('company_name', 'N/A')}")
        st.caption(f"**Date:** {st.session_state.dd_data.get('analysis_date', 'N/A')}")
        sources = st.session_state.dd_data.get('data_sources', [])
        if sources:
            st.caption(f"**Sources:** {', '.join(sources)}")
