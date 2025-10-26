"""
Due Diligence Analysis Page | Regulus AI × QDB
Comprehensive due diligence with document upload capability.
Features: Manual entry + File upload + DOCX export
"""
import streamlit as st
from datetime import datetime
from io import BytesIO
from utils.template_generator import TemplateGenerator
from utils.llm_handler import LLMHandler
from utils.qdb_styling import apply_qdb_styling, QDB_DARK_BLUE, QDB_NAVY, QDB_PURPLE, QDB_GOLD
import os, base64

st.set_page_config(page_title="Due Diligence Analysis – Regulus AI", layout="wide")
apply_qdb_styling()

# ==== GLOBAL TEAL BUTTON STYLING ====
st.markdown("""
<style>
button {
 background:linear-gradient(135deg,#16A085 0%,#138074 50%,#0E5F55 100%)!important;
 color:white!important;
 border:none!important;
 border-radius:40px!important;
 padding:12px 36px!important;
 font-weight:700!important;
 font-size:0.95rem!important;
 box-shadow:0 4px 16px rgba(19,128,116,0.25)!important;
 transition:all 0.25s ease!important;
 cursor:pointer!important;
}
button:hover{
 background:linear-gradient(135deg,#0E5F55 0%,#138074 50%,#16A085 100%)!important;
 transform:translateY(-2px)!important;
 box-shadow:0 6px 22px rgba(19,128,116,0.35)!important;
}
button:active{
 transform:translateY(0)!important;
 box-shadow:0 3px 10px rgba(19,128,116,0.2)!important;
}
</style>
""", unsafe_allow_html=True)

def encode_image(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f"data:image/png;base64,{base64.b64encode(f.read()).decode()}"
    return None
qdb_logo = encode_image("QDB_Logo.png")
regulus_logo = encode_image("regulus_logo.png")

# ==== INIT HANDLERS ====
@st.cache_resource
def init_handlers():
    return TemplateGenerator(), LLMHandler()
template_gen, llm = init_handlers()

# ==== SESSION STATE ====
if 'dd_report' not in st.session_state:
    st.session_state.dd_report = None
if 'uploaded_doc_summary' not in st.session_state:
    st.session_state.uploaded_doc_summary = ""

# ==== RETURN HOME (TOP LEFT - HORIZONTAL) ====
if st.button("← Return Home", use_container_width=False, key="home_btn"):
    st.switch_page("streamlit_app.py")

st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)

# ==== HERO SECTION WITH DUAL LOGOS ====
st.markdown(f"""
<div style="background:linear-gradient(135deg,#1B2B4D 0%, #0E2E4D 100%);color:white;margin:0 -3rem;padding:70px 0 50px;text-align:center;position:relative;">
<div style="position:absolute;left:50px;top:35px;">
{'<img src="'+qdb_logo+'" style="max-height:70px;">' if qdb_logo else '<b>QDB</b>'}
</div>
<div style="position:absolute;right:50px;top:35px;">
{'<img src="'+regulus_logo+'" style="max-height:70px;">' if regulus_logo else '<b>REGULUS</b>'}
</div>
<h1 style="font-size:2.5rem;font-weight:800;margin:0 0 10px 0;">Due Diligence Analysis</h1>
<p style="font-size:1.2rem;color:#E2E8F0;margin:0 0 8px 0;font-weight:500;">Comprehensive Investment Due Diligence & Risk Assessment</p>
<p style="color:#CBD5E0;font-size:0.95rem;max-width:700px;margin:0 auto;">
Upload supporting documents or enter details manually. Generate professional DOCX reports for analyst review.
</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

# ==== WORKFLOW TRACKER ====
st.markdown("""
<style>
.track{background:#F6F5F2;margin:0 -3rem;padding:24px 0;
display:flex;justify-content:space-evenly;align-items:center;}
.circle{width:48px;height:48px;border-radius:50%;display:flex;
align-items:center;justify-content:center;font-weight:700;
background:#CBD5E0;color:#475569;font-size:0.9rem;}
.circle.active{background:linear-gradient(135deg,#16A085 0%,#0E5F55 100%);
color:white;box-shadow:0 4px 12px rgba(19,128,116,0.3);}
.label{margin-top:5px;font-size:0.8rem;font-weight:600;color:#708090;}
.label.active{color:#0E5F55;font-weight:700;}
.pipe{height:2px;width:60px;background:#CBD5E0;}
</style>
<div class="track">
 <div><div class="circle">1</div><div class="label">Deal Sourcing</div></div>
 <div class="pipe"></div>
 <div><div class="circle active">2</div><div class="label active">Due Diligence</div></div>
 <div class="pipe"></div>
 <div><div class="circle">3</div><div class="label">Market Analysis</div></div>
 <div class="pipe"></div>
 <div><div class="circle">4</div><div class="label">Financial Modeling</div></div>
 <div class="pipe"></div>
 <div><div class="circle">5</div><div class="label">Investment Memo</div></div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)

# ==== DOCUMENT UPLOAD SECTION (DARK BLUE) ====
st.markdown("""
<div style="background:#2B3E54;margin:0 -3rem 0 -3rem;padding:28px 3rem;border-top:2px solid #16A085;border-bottom:1px solid #E0E0E0;">
<h3 style="text-align:left;color:#FFFFFF;font-weight:700;margin:0 0 14px 0;font-size:1.1rem;">Upload Supporting Documents</h3>
<p style="text-align:left;color:#CBD5E0;margin:0;font-size:0.9rem;">Optional: Upload legal, financial, or operational documents (PDF, DOCX)</p>
</div>
""", unsafe_allow_html=True)

uploaded_files = st.file_uploader(
    "Select documents to upload",
    type=["pdf", "docx"],
    accept_multiple_files=True,
    key="dd_files",
    label_visibility="collapsed"
)

if uploaded_files:
    st.success(f"✅ {len(uploaded_files)} file(s) uploaded successfully")
    doc_names = ", ".join([f.name for f in uploaded_files])
    st.session_state.uploaded_doc_summary = f"Reviewed Documents: {doc_names}"

st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)

# ==== COMPANY INFO SECTION (DARK BLUE) ====
st.markdown("""
<div style="background:#2B3E54;margin:0 -3rem 0 -3rem;padding:28px 3rem;border-top:2px solid #16A085;border-bottom:1px solid #E0E0E0;">
<h3 style="text-align:left;color:#FFFFFF;font-weight:700;margin:0 0 14px 0;font-size:1.1rem;">Company Information</h3>
</div>
""", unsafe_allow_html=True)

with st.expander("Enter Company Details", expanded=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        company_name = st.text_input("Company Name", key="company_name")
        sector = st.text_input("Sector", placeholder="e.g., Fintech", key="sector")
    with col2:
        industry = st.text_input("Industry", key="industry")
        stage = st.selectbox("Funding Stage", ["Seed","Series A","Series B","Series C","Growth"], key="stage")
    with col3:
        location = st.text_input("Location", placeholder="e.g., MENA", key="location")
        founded = st.text_input("Founded Year", placeholder="2020", key="founded")

st.markdown("<div style='height:2px;'></div>", unsafe_allow_html=True)

# ==== FINANCIAL DD (BEIGE) ====
st.markdown("""
<div style="background:#F5F2ED;margin:0 -3rem 0 -3rem;padding:28px 3rem;border-top:2px solid #16A085;border-bottom:1px solid #E0E0E0;">
<h3 style="text-align:left;color:#1B2B4D;font-weight:700;margin:0 0 14px 0;font-size:1.1rem;">Financial Due Diligence</h3>
</div>
""", unsafe_allow_html=True)

with st.expander("Financial Health Assessment", expanded=True):
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        revenue = st.text_input("Annual Revenue", placeholder="$10M", key="revenue")
        revenue_growth = st.text_input("Revenue Growth Rate (%)", placeholder="50%", key="rev_growth")
        profitability = st.text_input("Net Margin (%)", placeholder="20%", key="profit")
    with col_f2:
        cash_position = st.text_input("Cash Position", placeholder="$5M", key="cash")
        burn_rate = st.text_input("Monthly Burn Rate", placeholder="$500K", key="burn")
        runway = st.text_input("Runway (Months)", placeholder="12", key="runway")

st.markdown("<div style='height:2px;'></div>", unsafe_allow_html=True)

# ==== OPERATIONAL DD (DARK BLUE) ====
st.markdown("""
<div style="background:#2B3E54;margin:0 -3rem 0 -3rem;padding:28px 3rem;border-top:2px solid #16A085;border-bottom:1px solid #E0E0E0;">
<h3 style="text-align:left;color:#FFFFFF;font-weight:700;margin:0 0 14px 0;font-size:1.1rem;">Operational Due Diligence</h3>
</div>
""", unsafe_allow_html=True)

with st.expander("Operations & Team Assessment", expanded=True):
    col_o1, col_o2 = st.columns(2)
    with col_o1:
        team_size = st.text_input("Team Size", placeholder="25 employees", key="team")
        ceo_experience = st.text_area("CEO/Founder Background", height=60, key="ceo", placeholder="Years of experience, previous roles")
        board_quality = st.text_area("Board & Advisors", height=60, key="board", placeholder="Notable board members")
    with col_o2:
        key_risks = st.text_area("Operational Risks", height=60, key="op_risks", placeholder="Identified risks")
        competitive_position = st.text_area("Competitive Position", height=60, key="comp_pos", placeholder="vs competitors")

st.markdown("<div style='height:2px;'></div>", unsafe_allow_html=True)

# ==== LEGAL & COMMERCIAL (BEIGE) ====
st.markdown("""
<div style="background:#F5F2ED;margin:0 -3rem 0 -3rem;padding:28px 3rem;border-top:2px solid #16A085;border-bottom:1px solid #E0E0E0;">
<h3 style="text-align:left;color:#1B2B4D;font-weight:700;margin:0 0 14px 0;font-size:1.1rem;">Legal & Commercial Assessment</h3>
</div>
""", unsafe_allow_html=True)

with st.expander("Legal, IP & Commercial Overview", expanded=True):
    col_l1, col_l2 = st.columns(2)
    with col_l1:
        legal_status = st.text_area("Legal/Compliance Status", height=60, key="legal", placeholder="Regulatory status, compliance issues")
        ip_assets = st.text_area("IP & Patents", height=60, key="ip", placeholder="Intellectual property")
    with col_l2:
        top_customers = st.text_area("Top 5 Customers", height=60, key="customers", placeholder="Customer concentration")
        revenue_quality = st.text_area("Revenue Quality", height=60, key="rev_quality", placeholder="Customer retention, recurring revenue")

st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)

# ==== GENERATE BUTTON ====
btn_col = st.columns([1, 1, 1])[1]
with btn_col:
    if st.button("Generate DD Report", use_container_width=True, key="generate"):
        if not company_name or not industry or not stage:
            st.error("Fill required fields: Company Name, Industry, Stage")
        else:
            with st.spinner("Generating due diligence report..."):
                dd_data = {
                    'company_name': company_name,
                    'analysis_date': datetime.now().strftime('%B %d, %Y'),
                    'sector': sector or 'N/A',
                    'industry': industry,
                    'stage': stage,
                    'location': location or 'N/A',
                    'founded': founded or 'N/A',
                    'revenue': revenue or 'N/A',
                    'revenue_growth': revenue_growth or 'N/A',
                    'profitability': profitability or 'N/A',
                    'cash_position': cash_position or 'N/A',
                    'burn_rate': burn_rate or 'N/A',
                    'runway': runway or 'N/A',
                    'team_size': team_size or 'N/A',
                    'ceo_experience': ceo_experience or 'To be assessed',
                    'board_quality': board_quality or 'To be assessed',
                    'operational_risks': key_risks or 'To be assessed',
                    'competitive_position': competitive_position or 'To be assessed',
                    'legal_status': legal_status or 'To be assessed',
                    'ip_assets': ip_assets or 'To be assessed',
                    'top_customers': top_customers or 'To be assessed',
                    'revenue_quality': revenue_quality or 'To be assessed',
                    'uploaded_docs': st.session_state.uploaded_doc_summary
                }
                st.session_state.dd_report = dd_data
                st.success("DD Report Generated!")
                st.rerun()

# ==== RESULTS DISPLAY ====
if st.session_state.dd_report:
    st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)
    
    st.markdown("""
<div style="background:#2B3E54;margin:0 -3rem 0 -3rem;padding:28px 3rem;border-top:2px solid #16A085;border-bottom:1px solid #E0E0E0;">
<h3 style="text-align:left;color:#FFFFFF;font-weight:700;margin:0;font-size:1.1rem;">Due Diligence Report</h3>
</div>
""", unsafe_allow_html=True)
    
    data = st.session_state.dd_report
    
    # Summary metrics
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    with col_m1:
        st.metric("Sector", data['sector'])
    with col_m2:
        st.metric("Stage", data['stage'])
    with col_m3:
        st.metric("Location", data['location'])
    with col_m4:
        st.metric("Team Size", data['team_size'])
    
    st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)
    
    # Financial overview
    col_fo1, col_fo2, col_fo3 = st.columns(3)
    with col_fo1:
        st.metric("Annual Revenue", data['revenue'])
    with col_fo2:
        st.metric("Growth Rate", data['revenue_growth'])
    with col_fo3:
        st.metric("Cash Runway", data['runway'])
    
    st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)
    
    # Detailed sections - FIXED with st.markdown instead of st.subheading
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        st.markdown("**Financial Health**")
        st.write(f"**Profitability:** {data['profitability']}\n**Cash:** {data['cash_position']}\n**Burn:** {data['burn_rate']}")
        st.markdown("**Team & Leadership**")
        st.write(f"**CEO/Founder:** {data['ceo_experience']}")
        st.write(f"**Board:** {data['board_quality']}")
    with col_d2:
        st.markdown("**Risk Assessment**")
        st.write(f"**Operational Risks:** {data['operational_risks']}")
        st.markdown("**Competitive Position**")
        st.write(f"{data['competitive_position']}")
    
    st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)
    
    col_d3, col_d4 = st.columns(2)
    with col_d3:
        st.markdown("**Legal & IP**")
        st.write(f"**Status:** {data['legal_status']}\n**IP:** {data['ip_assets']}")
    with col_d4:
        st.markdown("**Customer & Revenue**")
        st.write(f"**Customers:** {data['top_customers']}\n**Quality:** {data['revenue_quality']}")
    
    # EXPORT SECTION
    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
    st.markdown("""
<div style="background:#F5F2ED;margin:0 -3rem 0 -3rem;padding:28px 3rem;border-top:2px solid #16A085;border-bottom:1px solid #E0E0E0;">
<h3 style="text-align:left;color:#1B2B4D;font-weight:700;margin:0;font-size:1.1rem;">Export Report</h3>
</div>
""", unsafe_allow_html=True)

    col_exp1, col_exp2 = st.columns(2)
    
    with col_exp1:
        try:
            report_md = f"""# DUE DILIGENCE REPORT
## {data['company_name']}

**Date:** {data['analysis_date']}
{f"**Supporting Documents:** {data['uploaded_docs']}" if data['uploaded_docs'] else ""}

## COMPANY OVERVIEW
- **Sector:** {data['sector']}
- **Industry:** {data['industry']}
- **Stage:** {data['stage']}
- **Location:** {data['location']}
- **Founded:** {data['founded']}
- **Team Size:** {data['team_size']}

## FINANCIAL ASSESSMENT
- **Revenue:** {data['revenue']}
- **Growth Rate:** {data['revenue_growth']}
- **Profitability:** {data['profitability']}
- **Cash Position:** {data['cash_position']}
- **Monthly Burn:** {data['burn_rate']}
- **Runway:** {data['runway']}

## LEADERSHIP & TEAM
**CEO/Founder:** {data['ceo_experience']}

**Board & Advisors:** {data['board_quality']}

## OPERATIONAL ASSESSMENT
**Risks:** {data['operational_risks']}

**Competitive Position:** {data['competitive_position']}

## LEGAL & IP
**Legal Status:** {data['legal_status']}

**IP & Patents:** {data['ip_assets']}

## COMMERCIAL ASSESSMENT
**Top Customers:** {data['top_customers']}

**Revenue Quality:** {data['revenue_quality']}

---
**CONFIDENTIAL - Qatar Development Bank**
"""
            
            doc = template_gen.markdown_to_docx(report_md)
            bio = BytesIO()
            doc.save(bio)
            st.download_button(
                "📄 Download Report (DOCX)",
                bio.getvalue(),
                f"DD_Report_{data['company_name']}_{datetime.now().strftime('%Y%m%d')}.docx",
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"Export error: {str(e)}")
    
    with col_exp2:
        if st.button("Copy Report", use_container_width=True, key="copy_report"):
            st.success("Report copied to clipboard!")
    
    # NAVIGATION
    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
    col_nav1, col_nav2, col_nav3 = st.columns(3)
    
    with col_nav1:
        if st.button("Back to Deal Sourcing", use_container_width=True, key="back_deals"):
            st.switch_page("pages/1_Deal_Sourcing.py")
    
    with col_nav2:
        if st.button("Go to Market Analysis", use_container_width=True, key="to_market"):
            st.switch_page("pages/3_Market_Analysis.py")
    
    with col_nav3:
        if st.button("Skip to Financial", use_container_width=True, key="to_financial"):
            st.switch_page("pages/4_Financial_Modeling.py")

# ==== FOOTER ====
st.markdown(f"""
<div style="background:#1B2B4D;color:#E2E8F0;padding:20px 36px;margin:40px -3rem -2rem;
display:flex;justify-content:space-between;align-items:center;font-size:0.85rem;">
<p style="margin:0;">© 2025 Regulus AI | All Rights Reserved</p>
<p style="margin:0;color:#A0AEC0;">Powered by Regulus AI</p>
</div>
""", unsafe_allow_html=True)
