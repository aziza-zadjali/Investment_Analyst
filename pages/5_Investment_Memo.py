"""
Investment Memo Generation | Regulus AI × QDB
Final workflow step with comprehensive investment recommendation.
"""
import streamlit as st
from datetime import datetime
from io import BytesIO
from docx import Document
from utils.template_generator import TemplateGenerator
from utils.llm_handler import LLMHandler
from utils.qdb_styling import apply_qdb_styling, QDB_DARK_BLUE, QDB_NAVY, QDB_PURPLE, QDB_GOLD
import os, base64

st.set_page_config(page_title="Investment Memo – Regulus AI", layout="wide")
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

# ==== INIT HANDLERS ====
@st.cache_resource
def init_handlers():
    return TemplateGenerator(), LLMHandler()
template_gen, llm = init_handlers()

# ==== SESSION STATE ====
if 'memo_complete' not in st.session_state:
    st.session_state.memo_complete = False
if 'memo_content' not in st.session_state:
    st.session_state.memo_content = ""
if 'memo_data' not in st.session_state:
    st.session_state.memo_data = {}

# ==== GENERATE MEMO FUNCTION ====
def generate_memo(data):
    """Generate professional investment memo"""
    memo = f"""# INVESTMENT MEMORANDUM

**Company:** {data['company_name']}  
**Prepared by:** Regulus AI - Qatar Development Bank  
**Date:** {data['analysis_date']}  
**Recommendation:** **{data['recommendation']}**

---

## EXECUTIVE SUMMARY

This memorandum provides a comprehensive investment analysis and recommendation for {data['company_name']}, a {data['stage']} stage company in the {data['industry']} sector.

### Key Highlights
{data['key_highlights'] or 'To be documented'}

---

## COMPANY OVERVIEW

| Field | Value |
|-------|-------|
| **Company Name** | {data['company_name']} |
| **Industry** | {data['industry']} |
| **Founded** | {data['founded']} |
| **Location** | {data['location']} |
| **Funding Stage** | {data['stage']} |

### Business Model
{data['business_model'] or 'To be documented'}

### Products & Services
{data['products_services'] or 'To be documented'}

---

## INVESTMENT OPPORTUNITY

### Investment Thesis
{data['investment_thesis'] or 'To be developed'}

### Investment Terms
| Term | Value |
|------|-------|
| **Investment Amount** | {data['deal_size']} |
| **Pre-Money Valuation** | {data['valuation']} |
| **Ownership Stake** | {data['ownership']}% |

### Market Opportunity
| Metric | Value |
|--------|-------|
| **Total Addressable Market (TAM)** | {data['tam']} |
| **Current Revenue** | {data['current_revenue']} |
| **Revenue Growth Rate** | {data['growth_rate']} |

---

## STRATEGIC ASSESSMENT
"""
    
    if data.get('include_scoring'):
        s = data.get('scores', {})
        memo += f"""
### Gulf Resonance Scoring Framework

| Dimension | Score | Assessment |
|-----------|-------|------------|
| **Strategic Clarity** | {s.get('strategic_clarity', 'N/A')}/10 | Clear vision and roadmap |
| **Symbolic Fluency** | {s.get('symbolic_fluency', 'N/A')}/10 | Brand positioning and narrative |
| **Execution Discipline** | {s.get('execution_discipline', 'N/A')}/10 | Track record of delivery |
| **Archetypal Fit** | {s.get('archetypal_fit', 'N/A')}/10 | Portfolio alignment |
| **Gulf Resonance** | {s.get('gulf_resonance', 'N/A')}/10 | Regional market fit |

**Composite Score: {s.get('composite_score', 'N/A')}/10**

---
"""
    
    memo += f"""
## RECOMMENDATION

Based on comprehensive analysis across financial, operational, strategic, and market dimensions, we recommend **{data['recommendation']}** for this investment.

### Rationale
The opportunity presents significant strategic alignment with QDB's investment mandate, strong market fundamentals, and attractive financial returns potential.

---

**CONFIDENTIAL - Qatar Development Bank**  
**For Internal Use Only**
"""
    return memo

# ==== HERO SECTION ====
st.markdown(f"""
<div style="
background:linear-gradient(135deg,{QDB_DARK_BLUE} 0%, {QDB_NAVY} 100%);
color:white;margin:0 -3rem;padding:100px 0 80px;text-align:center;">
<div style="position:absolute;left:50px;top:48px;">
{'<img src="'+qdb_logo+'" style="max-height:80px;">' if qdb_logo else '<b>QDB</b>'}
</div>
<h1 style="font-size:2.8rem;font-weight:800;">Investment Memorandum</h1>
<p style="font-size:1.35rem;color:#E2E8F0;">Comprehensive Investment Recommendation</p>
<p style="color:#CBD5E0;font-size:1.1rem;max-width:750px;margin:auto;">
Final workflow step: Generate professional investment memos with strategic scoring and actionable recommendations for Qatar Development Bank.
</p>
</div>
""", unsafe_allow_html=True)

# ==== RETURN HOME ====
col1, col2, col3 = st.columns([1, 0.6, 1])
with col2:
    if st.button("Return Home", use_container_width=True, key="home_btn"):
        st.switch_page("streamlit_app.py")

# ==== WORKFLOW TRACKER ====
st.markdown("""
<style>
.track{background:#F6F5F2;margin:-2px -3rem;padding:34px 0;
display:flex;justify-content:space-evenly;align-items:center;}
.circle{width:54px;height:54px;border-radius:50%;display:flex;
align-items:center;justify-content:center;font-weight:700;
background:#CBD5E0;color:#475569;font-size:0.95rem;}
.circle.active{background:linear-gradient(135deg,#138074 0%,#0E5F55 100%);
color:white;box-shadow:0 5px 15px rgba(19,128,116,0.4);}
.label{margin-top:7px;font-size:0.9rem;font-weight:600;color:#708090;}
.label.active{color:#138074;}
.pipe{height:3px;width:70px;background:#CBD5E0;}
</style>
<div class="track">
 <div><div class="circle">1</div><div class="label">Deal Sourcing</div></div>
 <div class="pipe"></div>
 <div><div class="circle">2</div><div class="label">Due Diligence</div></div>
 <div class="pipe"></div>
 <div><div class="circle">3</div><div class="label">Market Analysis</div></div>
 <div class="pipe"></div>
 <div><div class="circle">4</div><div class="label">Financial Modeling</div></div>
 <div class="pipe"></div>
 <div><div class="circle active">5</div><div class="label active">Investment Memo</div></div>
</div>
""", unsafe_allow_html=True)

# ==== COMPANY INFO SECTION (LIGHT BLUE) ====
st.markdown("""
<div style="background:#EBF3F8;margin:50px -3rem 0 -3rem;padding:45px 3rem;
border-top:3px solid #138074;box-shadow:0 0 12px rgba(0,0,0,0.05);">
<h2 style="text-align:center;color:#1B2B4D;font-weight:700;">Company & Deal Information</h2>
</div>
""", unsafe_allow_html=True)

with st.expander("Enter Company and Investment Details", expanded=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        company_name = st.text_input("Company Name *", key="memo_company")
        founded = st.text_input("Founded", placeholder="2020", key="memo_founded")
    with col2:
        industry = st.text_input("Industry *", key="memo_industry")
        location = st.text_input("Location", placeholder="Doha, Qatar", key="memo_location")
    with col3:
        stage = st.selectbox("Funding Stage *", ["Seed","Series A","Series B","Series C","Growth"], key="memo_stage")
        recommendation = st.selectbox("Recommendation *", ["STRONG BUY","BUY","HOLD","PASS"], key="memo_rec")
    
    col4, col5, col6 = st.columns(3)
    with col4:
        deal_size = st.text_input("Investment Size *", placeholder="$5M", key="memo_deal")
    with col5:
        valuation = st.text_input("Pre-Money Valuation *", placeholder="$50M", key="memo_val")
    with col6:
        ownership = st.text_input("Ownership %", placeholder="10", key="memo_own")

# ==== BUSINESS DETAILS (LIGHT BEIGE) ====
st.markdown("""
<div style="background:#FAF7F2;margin:50px -3rem 0 -3rem;padding:45px 3rem;
border-top:3px solid #138074;box-shadow:0 0 12px rgba(0,0,0,0.05);">
<h2 style="text-align:center;color:#1B2B4D;font-weight:700;">Business & Strategic Details</h2>
</div>
""", unsafe_allow_html=True)

with st.expander("Business Model, Thesis & Market Data", expanded=True):
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        business_model = st.text_area("Business Model", height=70, key="memo_biz")
        investment_thesis = st.text_area("Investment Thesis", height=70, key="memo_thesis")
    with col_b2:
        products = st.text_area("Products & Services", height=70, key="memo_products")
        highlights = st.text_area("Key Highlights", height=70, key="memo_highlights")
    
    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        tam = st.text_input("TAM", placeholder="$50B", key="memo_tam")
    with col_m2:
        revenue = st.text_input("Current Revenue", placeholder="$10M", key="memo_rev")
    with col_m3:
        growth = st.text_input("Growth Rate", placeholder="150%", key="memo_growth")

# ==== SCORING (LIGHT BLUE) ====
st.markdown("""
<div style="background:#EBF3F8;margin:50px -3rem 0 -3rem;padding:45px 3rem;
border-top:3px solid #138074;box-shadow:0 0 12px rgba(0,0,0,0.05);">
<h2 style="text-align:center;color:#1B2B4D;font-weight:700;">Strategic Assessment Scoring (Optional)</h2>
</div>
""", unsafe_allow_html=True)

include_scoring = st.checkbox("Include Scoring Framework in Memo", key="memo_include_score")

strategic_clarity = 7
symbolic_fluency = 6
execution = 6
archetypal = 7
gulf_res = 6
composite = 6.4

if include_scoring:
    with st.expander("Gulf Resonance Scoring", expanded=True):
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            strategic_clarity = st.slider("Strategic Clarity", 1, 10, 7, key="memo_clarity")
            symbolic_fluency = st.slider("Symbolic Fluency", 1, 10, 6, key="memo_fluency")
            execution = st.slider("Execution Discipline", 1, 10, 6, key="memo_exec")
        with col_s2:
            archetypal = st.slider("Archetypal Fit", 1, 10, 7, key="memo_arch")
            gulf_res = st.slider("Gulf Resonance", 1, 10, 6, key="memo_gulf")
        
        composite = (strategic_clarity + symbolic_fluency + execution + archetypal + gulf_res) / 5
        st.metric("Composite Score", f"{composite:.1f}/10")

# ==== GENERATE BUTTON ====
st.markdown("<br>", unsafe_allow_html=True)
btn_col = st.columns([1, 1, 1])[1]
with btn_col:
    if st.button("Generate Investment Memo", use_container_width=True, key="gen_memo"):
        if not company_name or not industry or not deal_size or not valuation:
            st.error("Please fill all required fields (*)")
        else:
            with st.spinner("Generating investment memo..."):
                memo_data = {
                    'company_name': company_name,
                    'analysis_date': datetime.now().strftime('%B %d, %Y'),
                    'stage': stage,
                    'industry': industry,
                    'founded': founded or 'N/A',
                    'location': location or 'N/A',
                    'deal_size': deal_size,
                    'valuation': valuation,
                    'ownership': ownership or 'TBD',
                    'recommendation': recommendation,
                    'business_model': business_model or 'To be documented',
                    'products_services': products or 'To be documented',
                    'investment_thesis': investment_thesis or 'To be developed',
                    'key_highlights': highlights or 'To be documented',
                    'tam': tam or 'N/A',
                    'current_revenue': revenue or 'N/A',
                    'growth_rate': growth or 'N/A',
                    'include_scoring': include_scoring
                }
                
                if include_scoring:
                    memo_data['scores'] = {
                        'strategic_clarity': strategic_clarity,
                        'symbolic_fluency': symbolic_fluency,
                        'execution_discipline': execution,
                        'archetypal_fit': archetypal,
                        'gulf_resonance': gulf_res,
                        'composite_score': composite
                    }
                
                memo_content = generate_memo(memo_data)
                st.session_state.memo_complete = True
                st.session_state.memo_content = memo_content
                st.session_state.memo_data = memo_data
                st.success("Investment memo generated!")
                st.rerun()

# ==== RESULTS DISPLAY (LIGHT BEIGE) ====
if st.session_state.memo_complete and st.session_state.get('memo_data'):
    st.markdown("---")
    st.markdown("""
<div style="background:#FAF7F2;margin:30px -3rem 0 -3rem;padding:45px 3rem;
border-top:3px solid #138074;box-shadow:0 0 12px rgba(0,0,0,0.05);">
<h2 style="text-align:center;color:#1B2B4D;font-weight:700;">Investment Memo Generated</h2>
</div>
""", unsafe_allow_html=True)
    
    # Download DOCX Only
    try:
        doc = template_gen.markdown_to_docx(st.session_state.memo_content)
        bio = BytesIO()
        doc.save(bio)
        col_center = st.columns([1, 1, 1])[1]
        with col_center:
            st.download_button(
                "Download Investment Memo (DOCX)",
                bio.getvalue(),
                f"Investment_Memo_{st.session_state.memo_data['company_name'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.docx",
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )
    except Exception as e:
        st.error(f"DOCX generation error: {str(e)}")
    
    # Preview
    with st.expander("View Full Memo", expanded=True):
        st.markdown(st.session_state.memo_content)
    
    # Completion Message
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(f"""
<div style='background:linear-gradient(135deg,{QDB_PURPLE} 0%,{QDB_DARK_BLUE} 100%);
border-radius:12px;padding:40px;color:white;text-align:center;'>
<h2 style='margin:0 0 10px 0;'>Workflow Complete!</h2>
<p style='margin:0;font-size:1.1rem;'>Investment analysis and memo generation finished successfully.</p>
</div>
""", unsafe_allow_html=True)
    
    # Navigation
    st.markdown("<br>", unsafe_allow_html=True)
    col_nav1, col_nav2, col_nav3 = st.columns(3)
    
    with col_nav1:
        if st.button("Back to Financial Modeling", use_container_width=True, key="back_fin"):
            st.switch_page("pages/4_Financial_Modeling.py")
    
    with col_nav2:
        if st.button("Return Home", use_container_width=True, key="home_final"):
            st.switch_page("streamlit_app.py")
    
    with col_nav3:
        if st.button("Start New Analysis", use_container_width=True, key="restart"):
            st.switch_page("pages/1_Deal_Sourcing.py")

# ==== FOOTER ====
st.markdown(f"""
<div style="background:{QDB_DARK_BLUE};color:#E2E8F0;padding:26px 36px;margin:80px -3rem -2rem;
display:flex;justify-content:space-between;align-items:center;">
<p style="margin:0;font-size:0.9rem;">© 2025 Regulus AI | All Rights Reserved</p>
<p style="margin:0;color:#A0AEC0;font-size:0.9rem;">Powered by Regulus AI</p>
</div>
""", unsafe_allow_html=True)
