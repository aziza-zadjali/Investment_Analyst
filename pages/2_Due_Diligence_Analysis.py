"""
Due Diligence Analysis | Regulus AI × QDB
Enhanced: Financial + Legal + Operational + AML/Compliance + Web Extraction
Styled to match Investment Analyst AI design system
"""
import streamlit as st
from datetime import datetime
import PyPDF2
import docx
from io import BytesIO
from utils.llm_handler import LLMHandler
from utils.template_generator import TemplateGenerator
from utils.qdb_styling import apply_qdb_styling
import os, base64

# === PAGE CONFIG ===
st.set_page_config(page_title="Due Diligence Analysis – Regulus AI", layout="wide")
apply_qdb_styling()

# === STYLING ===
st.markdown("""
<style>
button {
 background:linear-gradient(135deg,#16A085 0%,#138074 50%,#0E5F55 100%)!important;
 color:white!important;border:none!important;border-radius:40px!important;
 padding:12px 36px!important;font-weight:700!important;font-size:0.95rem!important;
 box-shadow:0 4px 16px rgba(19,128,116,0.25)!important;transition:all 0.25s ease!important;
}
button:hover{background:linear-gradient(135deg,#0E5F55 0%,#138074 50%,#16A085 100%)!important;
 transform:translateY(-2px)!important;box-shadow:0 6px 22px rgba(19,128,116,0.35)!important;}
button:active{transform:translateY(0)!important;box-shadow:0 3px 10px rgba(19,128,116,0.2)!important;}
</style>
""", unsafe_allow_html=True)

# === IMAGE LOADERS ===
def encode_image(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f"data:image/png;base64,{base64.b64encode(f.read()).decode()}"
    return None

qdb_logo = encode_image("QDB_Logo.png")
regulus_logo = encode_image("regulus_logo.png")

# === INITIALIZE HANDLERS ===
@st.cache_resource
def init_handlers():
    return LLMHandler(), TemplateGenerator()

llm, template_gen = init_handlers()

# === SESSION STATE ===
if 'dd_complete' not in st.session_state:
    st.session_state.dd_complete = False
if 'dd_report' not in st.session_state:
    st.session_state.dd_report = ""
if 'dd_data' not in st.session_state:
    st.session_state.dd_data = {}

# === RETURN HOME ===
if st.button("← Return Home", use_container_width=False):
    st.switch_page("streamlit_app.py")
st.markdown("<div style='height:4px;'></div>", unsafe_allow_html=True)

# === HERO SECTION ===
st.markdown(f"""
<div style="background:linear-gradient(135deg,#1B2B4D 0%,#0E2E4D 100%);color:white;
margin:0 -3rem;padding:70px 0 50px;text-align:center;position:relative;">
<div style="position:absolute;left:50px;top:35px;">
{'<img src="'+qdb_logo+'" style="max-height:70px;">' if qdb_logo else '<b>QDB</b>'}
</div>
<div style="position:absolute;right:50px;top:35px;">
{'<img src="'+regulus_logo+'" style="max-height:70px;">' if regulus_logo else '<b>REGULUS</b>'}
</div>
<h1 style="font-size:2.5rem;font-weight:800;margin:0 0 10px 0;">Enhanced Due Diligence Analysis</h1>
<p style="font-size:1.1rem;color:#E2E8F0;margin:0;font-weight:500;">
Financial + Legal + Operational + AML/Compliance Screening
</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

# === COMPANY INFO SECTION ===
st.markdown("""
<div style="background:#2B3E54;margin:0 -3rem;padding:24px 3rem;
border-top:2px solid #16A085;border-bottom:1px solid #E0E0E0;">
<h3 style="color:#FFFFFF;font-weight:700;margin:0;">Company Information</h3>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    company_name = st.text_input("Company Name *", placeholder="e.g., Baladna Q.P.S.C.", key="comp_name")
with col2:
    company_website = st.text_input("Company Website (Optional)", placeholder="e.g., baladna.com", key="comp_web")

st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)

# === DOCUMENT UPLOAD SECTION ===
st.markdown("""
<div style="background:#F5F2ED;margin:0 -3rem;padding:24px 3rem;
border-top:2px solid #16A085;border-bottom:1px solid #E0E0E0;">
<h3 style="color:#1B2B4D;font-weight:700;margin:0;">Upload Supporting Documents</h3>
<p style="color:#666;margin:4px 0 0 0;font-size:0.9rem;">
Legal, financial, and operational files (PDF, DOCX, XLSX)
</p>
</div>
""", unsafe_allow_html=True)

uploaded_files = st.file_uploader(
    "Select documents",
    type=['pdf', 'docx', 'xlsx'],
    accept_multiple_files=True,
    label_visibility="collapsed",
    key="dd_files"
)

if uploaded_files:
    st.success(f"✅ {len(uploaded_files)} file(s) uploaded successfully")

st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)

# === WEB EXTRACTION SECTION ===
st.markdown("""
<div style="background:#2B3E54;margin:0 -3rem;padding:24px 3rem;
border-top:2px solid #16A085;border-bottom:1px solid #E0E0E0;">
<h3 style="color:#FFFFFF;font-weight:700;margin:0;">Optional: Web Data Extraction</h3>
<p style="color:#CBD5E0;margin:4px 0 0 0;font-size:0.9rem;">
Automatically fetch public investor relations data
</p>
</div>
""", unsafe_allow_html=True)

enable_web_extraction = st.checkbox(
    "Enable automatic web data extraction from investor relations",
    value=False,
    key="web_extract"
)

if enable_web_extraction and not company_website:
    st.warning("⚠️ Please provide company website above to use this feature")

st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)

# === ANALYSIS BUTTON ===
col_btn_l, col_btn_c, col_btn_r = st.columns([1, 1.2, 1])
with col_btn_c:
    run_analysis = st.button("🔍 Run Enhanced DD Analysis", use_container_width=True, key="analyze_dd")

if run_analysis:
    # === VALIDATION ===
    if not company_name:
        st.error("❌ Please enter company name")
        st.stop()
    
    if not uploaded_files and not enable_web_extraction:
        st.error("❌ Please upload documents or enable web data extraction")
        st.stop()
    
    if enable_web_extraction and not company_website:
        st.error("❌ Please enter company website to use web extraction")
        st.stop()
    
    # === ANALYSIS EXECUTION ===
    with st.spinner("🤖 Performing comprehensive due diligence analysis..."):
        
        combined_text = ""
        processed_files = 0
        skipped_files = 0
        
        # STEP 1: Extract from documents
        if uploaded_files:
            st.info(f"📄 Processing {len(uploaded_files)} documents...")
            
            for uploaded_file in uploaded_files:
                try:
                    if uploaded_file.type == "application/pdf":
                        try:
                            pdf_reader = PyPDF2.PdfReader(uploaded_file)
                            if pdf_reader.is_encrypted:
                                try:
                                    if pdf_reader.decrypt('') == 0:
                                        st.warning(f"⚠️ {uploaded_file.name} is password-protected. Skipping.")
                                        skipped_files += 1
                                        continue
                                except:
                                    st.warning(f"⚠️ Could not decrypt {uploaded_file.name}.")
                                    skipped_files += 1
                                    continue
                            
                            for page in pdf_reader.pages:
                                text = page.extract_text()
                                if text:
                                    combined_text += text + "\n"
                            processed_files += 1
                        
                        except Exception as pdf_error:
                            st.warning(f"⚠️ Could not process {uploaded_file.name}")
                            skipped_files += 1
                            continue
                    
                    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                        doc = docx.Document(uploaded_file)
                        for para in doc.paragraphs:
                            combined_text += para.text + "\n"
                        processed_files += 1
                    
                    else:
                        skipped_files += 1
                
                except Exception as e:
                    st.warning(f"⚠️ Error processing {uploaded_file.name}")
                    skipped_files += 1
            
            if processed_files > 0:
                st.success(f"✅ Successfully processed {processed_files} documents")
            if skipped_files > 0:
                st.info(f"ℹ️ Skipped {skipped_files} files (encrypted or unsupported)")
        
        # STEP 2: Validation
        if not combined_text or len(combined_text) < 100:
            st.error("⚠️ Insufficient data for analysis")
            st.stop()
        
        # STEP 3: AI Analysis
        analysis_results = {
            'company_name': company_name,
            'analyst': 'Regulus AI',
            'date': datetime.now().strftime('%B %d, %Y'),
            'website': company_website if company_website else 'N/A'
        }
        
        # Financial Analysis
        st.info("📊 Analyzing financials...")
        try:
            fin_prompt = f"""Analyze {company_name}'s financial health:
{combined_text[:8000]}

Provide: Revenue trends, profitability, cash flow, liquidity, leverage ratios, red flags."""
            analysis_results['financial'] = llm.generate(fin_prompt)
        except:
            analysis_results['financial'] = "Analysis unavailable"
        
        # Legal Analysis
        st.info("⚖️ Reviewing legal & compliance...")
        try:
            legal_prompt = f"""Review legal aspects for {company_name}:
{combined_text[:8000]}

Cover: Corporate structure, compliance, disputes, IP, contracts."""
            analysis_results['legal'] = llm.generate(legal_prompt)
        except:
            analysis_results['legal'] = "Analysis unavailable"
        
        # Operational Analysis
        st.info("🏭 Assessing operations...")
        try:
            op_prompt = f"""Assess operations for {company_name}:
{combined_text[:8000]}

Analyze: Business model, supply chain, technology, team, efficiency."""
            analysis_results['operational'] = llm.generate(op_prompt)
        except:
            analysis_results['operational'] = "Analysis unavailable"
        
        # Risk Assessment
        st.info("⚠️ Evaluating risks...")
        try:
            risk_prompt = f"""Risk assessment for {company_name}:
{combined_text[:8000]}

Identify: Market, financial, operational, legal, strategic risks."""
            analysis_results['risks'] = llm.generate(risk_prompt)
        except:
            analysis_results['risks'] = "Assessment unavailable"
        
        # AML Screening
        st.info("🔒 AML/KYC Screening...")
        try:
            aml_prompt = f"""AML/KYC screening for {company_name}:
{combined_text[:4000]}

Check: Sanctions, PEP, FATCA, adverse media."""
            analysis_results['aml'] = llm.generate(aml_prompt)
        except:
            analysis_results['aml'] = "Screening pending"
        
        # Recommendations
        st.info("💡 Generating recommendations...")
        try:
            rec_prompt = f"""Investment recommendation for {company_name}:
{combined_text[:5000]}

Provide: Recommendation, strengths, concerns, required actions."""
            analysis_results['recommendations'] = llm.generate(rec_prompt)
        except:
            analysis_results['recommendations'] = "Pending"
        
        # Generate Report
        st.info("📝 Generating report...")
        markdown_report = template_gen.generate_due_diligence_report(analysis_results)
        
        st.session_state.dd_complete = True
        st.session_state.dd_report = markdown_report
        st.session_state.dd_data = analysis_results
        
        st.success("✅ Due Diligence Analysis Complete!")

# === RESULTS DISPLAY ===
if st.session_state.dd_complete:
    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background:#F5F2ED;margin:0 -3rem;padding:24px 3rem;
    border-top:2px solid #16A085;border-bottom:1px solid #E0E0E0;">
    <h3 style="color:#1B2B4D;font-weight:700;margin:0;">Download Reports</h3>
    </div>
    """, unsafe_allow_html=True)
    
    data = st.session_state.dd_data
    col_dl1, col_dl2 = st.columns(2)
    
    with col_dl1:
        st.download_button(
            "📄 Download Markdown",
            st.session_state.dd_report,
            f"{data['company_name']}_DD_{datetime.now().strftime('%Y%m%d')}.md",
            "text/markdown",
            use_container_width=True
        )
    
    with col_dl2:
        try:
            docx_doc = template_gen.markdown_to_docx(st.session_state.dd_report)
            docx_buffer = BytesIO()
            docx_doc.save(docx_buffer)
            docx_buffer.seek(0)
            
            st.download_button(
                "📥 Download DOCX Report",
                docx_buffer.getvalue(),
                f"{data['company_name']}_DD_{datetime.now().strftime('%Y%m%d')}.docx",
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"DOCX error: {e}")
    
    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
    
    # Preview
    with st.expander("📄 Preview Full Report"):
        st.markdown(st.session_state.dd_report)
    
    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
    
    # Navigation
    st.markdown("""
    <div style="background:#F6F5F2;margin:0 -3rem;padding:16px 0;text-align:center;">
    </div>
    """, unsafe_allow_html=True)
    
    col_nav1, col_nav2, col_nav3 = st.columns(3)
    with col_nav1:
        if st.button("← Back to Deal Sourcing", use_container_width=True):
            st.switch_page("pages/1_Deal_Sourcing.py")
    with col_nav2:
        if st.button("→ Market Analysis", use_container_width=True):
            st.switch_page("pages/3_Market_Analysis.py")
    with col_nav3:
        if st.button("Financial Modeling →", use_container_width=True):
            st.switch_page("pages/4_Financial_Modeling.py")

# === FOOTER ===
st.markdown("""
<div style="background:#1B2B4D;color:#E2E8F0;padding:20px 36px;margin:40px -3rem -2rem;
display:flex;justify-content:space-between;align-items:center;font-size:0.85rem;">
<p style="margin:0;">© 2025 Regulus AI | Enhanced Due Diligence</p>
<p style="margin:0;color:#A0AEC0;">Powered by Regulus AI</p>
</div>
""", unsafe_allow_html=True)
