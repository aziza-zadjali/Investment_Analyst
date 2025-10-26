"""
Investment Memo & Pitch Deck Generator
CLEAN: No icons - clean professional interface
"""
import streamlit as st
import base64
import os
from datetime import datetime
from io import BytesIO
from utils.qdb_styling import apply_qdb_styling
from utils.llm_handler import LLMHandler
from utils.template_generator import TemplateGenerator

st.set_page_config(page_title="Investment Memo", page_icon="📋", layout="wide", initial_sidebar_state="collapsed")
apply_qdb_styling()

# ===== Initialize Handlers =====
@st.cache_resource
def init_handlers():
    try:
        llm = LLMHandler()
        template_gen = TemplateGenerator()
        return llm, template_gen
    except Exception as e:
        st.error(f"Error initializing handlers: {e}")
        return None, None

llm, template_gen = init_handlers()

if llm is None or template_gen is None:
    st.error("Failed to initialize handlers")
    st.stop()

# ===== Image Loader =====
def encode_image(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f"data:image/png;base64,{base64.b64encode(f.read()).decode()}"
    return None

qdb_logo = encode_image("QDB_Logo.png")
regulus_logo = encode_image("regulus_logo.png")

# ===== Session State =====
if 'memo_complete' not in st.session_state:
    st.session_state.memo_complete = False
if 'memo_content' not in st.session_state:
    st.session_state.memo_content = ""
if 'memo_data' not in st.session_state:
    st.session_state.memo_data = {}

# ===== CUSTOM STYLING =====
st.markdown("""
<style>
.stButton>button {
    background: linear-gradient(135deg,#16A085 0%,#138074 100%)!important;
    color:white!important;
    border:none!important;
    border-radius:8px!important;
    padding:12px 24px!important;
    font-weight:700!important;
    font-size:0.95rem!important;
    box-shadow:0 4px 12px rgba(22,160,133,0.3)!important;
    transition:all 0.25s ease!important;
}

.stButton>button:hover{
    background: linear-gradient(135deg,#0E5F55 0%,#107563 100%)!important;
    transform:translateY(-2px)!important;
    box-shadow:0 6px 18px rgba(22,160,133,0.4)!important;
}

.section-beige {
    background-color: #F6F5F2;
    border-radius: 10px;
    padding: 20px;
    margin: 12px 0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}

.required-asterisk {
    color: #E74C3C;
    font-weight: 700;
    margin-left: 2px;
}

.section-header {
    font-size: 1.2rem;
    font-weight: 700;
    color: #1B2B4D;
    margin-bottom: 12px;
}
</style>
""", unsafe_allow_html=True)

# ===== HERO HEADER =====
st.markdown(f"""
<div style="
    background: linear-gradient(135deg,#1B2B4D 0%,#2C3E5E 100%);
    color: white;
    text-align: center;
    margin: 0 -3rem;
    padding: 40px 20px 50px 20px;
    position: relative;
    overflow:visible;
    width: calc(100% + 6rem);
    border-bottom: 3px solid #16A085;">

  <div style="position:absolute; top:15px; left:35px;">
    {'<img src="'+qdb_logo+'" style="max-height:55px;">' if qdb_logo else ''}
  </div>

  <div style="position:absolute; top:15px; right:35px;">
    {'<img src="'+regulus_logo+'" style="max-height:55px;">' if regulus_logo else ''}
  </div>

  <div style="max-width:800px; margin:0 auto;">
    <h1 style="font-size:2rem; font-weight:800; margin-bottom:6px;">Investment Memorandum</h1>
    <p style="color:#E2E8F0; font-size:0.95rem; margin:0;">AI-powered professional investment memos with comprehensive scoring</p>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

# ===== HOME BUTTON =====
if st.button("Return Home", key="home_btn"):
    st.switch_page("streamlit_app.py")

st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

# ===== SECTION 1: COMPANY & DEAL INFORMATION =====
st.markdown('<div class="section-beige"><div class="section-header">Company & Deal Information</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("<div style='color:#1B2B4D; font-size:0.85rem; margin-bottom:4px; font-weight:600;'>Company Name <span class='required-asterisk'>*</span></div>", unsafe_allow_html=True)
    company_name = st.text_input("Company Name", placeholder="e.g., GreenTech Solutions", label_visibility="collapsed", key="company")

with col2:
    st.markdown("<div style='color:#1B2B4D; font-size:0.85rem; margin-bottom:4px; font-weight:600;'>Industry <span class='required-asterisk'>*</span></div>", unsafe_allow_html=True)
    industry = st.text_input("Industry", placeholder="e.g., Renewable Energy", label_visibility="collapsed", key="industry")

with col3:
    st.markdown("<div style='color:#1B2B4D; font-size:0.85rem; margin-bottom:4px; font-weight:600;'>Funding Stage <span class='required-asterisk'>*</span></div>", unsafe_allow_html=True)
    stage = st.selectbox("Funding Stage", ["Seed", "Series A", "Series B", "Series C", "Growth", "Pre-IPO"], label_visibility="collapsed", key="stage")

col4, col5, col6 = st.columns(3)

with col4:
    st.markdown("<div style='color:#1B2B4D; font-size:0.85rem; margin-bottom:4px; font-weight:600;'>Founded Year</div>", unsafe_allow_html=True)
    founded_year = st.text_input("Founded", placeholder="e.g., 2020", label_visibility="collapsed", key="founded")

with col5:
    st.markdown("<div style='color:#1B2B4D; font-size:0.85rem; margin-bottom:4px; font-weight:600;'>Location</div>", unsafe_allow_html=True)
    location = st.text_input("Location", placeholder="e.g., San Francisco, CA", label_visibility="collapsed", key="location")

with col6:
    st.markdown("<div style='color:#1B2B4D; font-size:0.85rem; margin-bottom:4px; font-weight:600;'>Recommendation <span class='required-asterisk'>*</span></div>", unsafe_allow_html=True)
    recommendation = st.selectbox("Recommendation", ["STRONG BUY", "BUY", "HOLD", "PASS"], label_visibility="collapsed", key="rec")

col7, col8, col9 = st.columns(3)

with col7:
    st.markdown("<div style='color:#1B2B4D; font-size:0.85rem; margin-bottom:4px; font-weight:600;'>Investment Amount <span class='required-asterisk'>*</span></div>", unsafe_allow_html=True)
    deal_size = st.text_input("Investment Ask", placeholder="e.g., $5M", label_visibility="collapsed", key="deal")

with col8:
    st.markdown("<div style='color:#1B2B4D; font-size:0.85rem; margin-bottom:4px; font-weight:600;'>Pre-Money Valuation <span class='required-asterisk'>*</span></div>", unsafe_allow_html=True)
    valuation = st.text_input("Valuation", placeholder="e.g., $50M", label_visibility="collapsed", key="val")

with col9:
    st.markdown("<div style='color:#1B2B4D; font-size:0.85rem; margin-bottom:4px; font-weight:600;'>Ownership %</div>", unsafe_allow_html=True)
    ownership = st.text_input("Ownership", placeholder="e.g., 10%", label_visibility="collapsed", key="own")

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

# ===== SECTION 2: BUSINESS OVERVIEW =====
st.markdown('<div class="section-beige"><div class="section-header">Business Overview</div>', unsafe_allow_html=True)

st.markdown("<div style='color:#1B2B4D; font-size:0.85rem; margin-bottom:4px; font-weight:600;'>Investment Thesis</div>", unsafe_allow_html=True)
investment_thesis = st.text_area("Investment Thesis", height=80, placeholder="Why is this a compelling investment opportunity?", label_visibility="collapsed", key="thesis")

col_bus1, col_bus2 = st.columns(2)

with col_bus1:
    st.markdown("<div style='color:#1B2B4D; font-size:0.85rem; margin-bottom:4px; font-weight:600;'>Business Model</div>", unsafe_allow_html=True)
    business_model = st.text_area("Business Model", height=100, placeholder="Describe the company's business model...", label_visibility="collapsed", key="bm")

with col_bus2:
    st.markdown("<div style='color:#1B2B4D; font-size:0.85rem; margin-bottom:4px; font-weight:600;'>Products & Services</div>", unsafe_allow_html=True)
    products_services = st.text_area("Products/Services", height=100, placeholder="Describe key products and services...", label_visibility="collapsed", key="prod")

st.markdown("<div style='color:#1B2B4D; font-size:0.85rem; margin-bottom:4px; font-weight:600;'>Key Highlights</div>", unsafe_allow_html=True)
key_highlights = st.text_area("Key Highlights", height=80, placeholder="List key achievements and strengths...", label_visibility="collapsed", key="highlight")

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

# ===== SECTION 3: MARKET ANALYSIS =====
st.markdown('<div class="section-beige"><div class="section-header">Market Analysis</div>', unsafe_allow_html=True)

col_mkt1, col_mkt2, col_mkt3 = st.columns(3)

with col_mkt1:
    st.markdown("<div style='color:#1B2B4D; font-size:0.85rem; margin-bottom:4px; font-weight:600;'>TAM</div>", unsafe_allow_html=True)
    tam = st.text_input("TAM", placeholder="e.g., $50B", label_visibility="collapsed", key="tam")

with col_mkt2:
    st.markdown("<div style='color:#1B2B4D; font-size:0.85rem; margin-bottom:4px; font-weight:600;'>SAM</div>", unsafe_allow_html=True)
    sam = st.text_input("SAM", placeholder="e.g., $5B", label_visibility="collapsed", key="sam")

with col_mkt3:
    st.markdown("<div style='color:#1B2B4D; font-size:0.85rem; margin-bottom:4px; font-weight:600;'>SOM</div>", unsafe_allow_html=True)
    som = st.text_input("SOM", placeholder="e.g., $500M", label_visibility="collapsed", key="som")

col_mkt4, col_mkt5 = st.columns(2)

with col_mkt4:
    st.markdown("<div style='color:#1B2B4D; font-size:0.85rem; margin-bottom:4px; font-weight:600;'>Market Trends</div>", unsafe_allow_html=True)
    market_trends = st.text_area("Market Trends", height=80, placeholder="Describe market dynamics and growth drivers...", label_visibility="collapsed", key="trends")

with col_mkt5:
    st.markdown("<div style='color:#1B2B4D; font-size:0.85rem; margin-bottom:4px; font-weight:600;'>Competitive Landscape</div>", unsafe_allow_html=True)
    competitive_landscape = st.text_area("Competition", height=80, placeholder="Describe competitors and positioning...", label_visibility="collapsed", key="comp")

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

# ===== SECTION 4: FINANCIAL PERFORMANCE =====
st.markdown('<div class="section-beige"><div class="section-header">Financial Performance</div>', unsafe_allow_html=True)

col_fin1, col_fin2, col_fin3 = st.columns(3)

with col_fin1:
    st.markdown("<div style='color:#1B2B4D; font-size:0.85rem; margin-bottom:4px; font-weight:600;'>Revenue (ARR)</div>", unsafe_allow_html=True)
    current_revenue = st.text_input("Revenue", placeholder="e.g., $10M", label_visibility="collapsed", key="rev")

with col_fin2:
    st.markdown("<div style='color:#1B2B4D; font-size:0.85rem; margin-bottom:4px; font-weight:600;'>Growth Rate</div>", unsafe_allow_html=True)
    revenue_growth = st.text_input("Growth", placeholder="e.g., 150% YoY", label_visibility="collapsed", key="growth")

with col_fin3:
    st.markdown("<div style='color:#1B2B4D; font-size:0.85rem; margin-bottom:4px; font-weight:600;'>Gross Margin</div>", unsafe_allow_html=True)
    gross_margin = st.text_input("Margin", placeholder="e.g., 75%", label_visibility="collapsed", key="margin")

col_fin4, col_fin5, col_fin6 = st.columns(3)

with col_fin4:
    st.markdown("<div style='color:#1B2B4D; font-size:0.85rem; margin-bottom:4px; font-weight:600;'>Burn Rate</div>", unsafe_allow_html=True)
    burn_rate = st.text_input("Burn", placeholder="e.g., $500K", label_visibility="collapsed", key="burn")

with col_fin5:
    st.markdown("<div style='color:#1B2B4D; font-size:0.85rem; margin-bottom:4px; font-weight:600;'>Runway</div>", unsafe_allow_html=True)
    runway = st.text_input("Runway", placeholder="e.g., 18 months", label_visibility="collapsed", key="run")

with col_fin6:
    st.markdown("<div style='color:#1B2B4D; font-size:0.85rem; margin-bottom:4px; font-weight:600;'>LTV/CAC</div>", unsafe_allow_html=True)
    unit_economics = st.text_input("Unit Economics", placeholder="e.g., 3.5x", label_visibility="collapsed", key="ltv")

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

# ===== SECTION 5: TEAM & RISKS =====
st.markdown('<div class="section-beige"><div class="section-header">Team & Risks</div>', unsafe_allow_html=True)

st.markdown("<div style='color:#1B2B4D; font-size:0.85rem; margin-bottom:4px; font-weight:600;'>Management Team</div>", unsafe_allow_html=True)
team_info = st.text_area("Team", height=100, placeholder="Describe key team members and experience...", label_visibility="collapsed", key="team")

col_risk1, col_risk2 = st.columns(2)

with col_risk1:
    st.markdown("<div style='color:#1B2B4D; font-size:0.85rem; margin-bottom:4px; font-weight:600;'>Key Risks</div>", unsafe_allow_html=True)
    risks = st.text_area("Risks", height=100, placeholder="Identify key risks...", label_visibility="collapsed", key="risks")

with col_risk2:
    st.markdown("<div style='color:#1B2B4D; font-size:0.85rem; margin-bottom:4px; font-weight:600;'>Risk Mitigation</div>", unsafe_allow_html=True)
    mitigation = st.text_area("Mitigation", height=100, placeholder="Describe mitigation strategies...", label_visibility="collapsed", key="miti")

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

# ===== OPTIONAL SCORING SECTION =====
with st.expander("Optional: Gulf Resonance Scoring Framework", expanded=False):
    st.markdown('<div class="section-beige">', unsafe_allow_html=True)
    
    st.info("Rate each dimension from 1-10 for comprehensive investment analysis")
    
    col_s1, col_s2 = st.columns(2)
    
    with col_s1:
        strategic_clarity = st.slider("Strategic Clarity", min_value=1, max_value=10, value=7, help="Clear vision and roadmap", key="s1")
        symbolic_fluency = st.slider("Symbolic Fluency", min_value=1, max_value=10, value=6, help="Brand positioning", key="s2")
        execution_discipline = st.slider("Execution Discipline", min_value=1, max_value=10, value=6, help="Delivery track record", key="s3")
    
    with col_s2:
        archetypal_fit = st.slider("Archetypal Fit", min_value=1, max_value=10, value=7, help="Portfolio alignment", key="s4")
        gulf_resonance = st.slider("Gulf Resonance", min_value=1, max_value=10, value=6, help="Market fit", key="s5")
    
    composite_score = (strategic_clarity + symbolic_fluency + execution_discipline + archetypal_fit + gulf_resonance) / 5
    
    col_score1, col_score2 = st.columns(2)
    with col_score1:
        st.metric("Composite Score", f"{composite_score:.1f}/10")
    with col_score2:
        enable_scoring = st.checkbox("Include scoring in memo", value=False, key="enable_score")
    
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

# ===== GENERATE BUTTON =====
if st.button("Generate Investment Memo", use_container_width=True, key="gen_button"):
    
    if not company_name or not industry or not stage or not deal_size or not valuation or not recommendation:
        st.error("Please fill in all required fields (*)")
        st.stop()
    
    with st.spinner("Generating professional investment memo..."):
        try:
            strategic_clarity = 7
            symbolic_fluency = 6
            execution_discipline = 6
            archetypal_fit = 7
            gulf_resonance = 6
            composite_score = 6.4
            enable_scoring = False
            
            memo_data = {
                'company_name': company_name,
                'analyst_name': 'Regulus AI Investment Team',
                'analysis_date': datetime.now().strftime('%B %d, %Y'),
                'stage': stage,
                'investment_size': deal_size,
                'valuation': valuation,
                'ownership': ownership if ownership else 'TBD',
                'recommendation': recommendation,
                'founded': founded_year if founded_year else 'N/A',
                'location': location if location else 'N/A',
                'industry': industry,
                'business_model': business_model if business_model else 'To be documented',
                'products_services': products_services if products_services else 'To be documented',
                'investment_thesis': investment_thesis if investment_thesis else 'To be developed',
                'key_highlights': key_highlights if key_highlights else 'To be documented',
                'tam': tam if tam else 'N/A',
                'sam': sam if sam else 'N/A',
                'som': som if som else 'N/A',
                'market_trends': market_trends if market_trends else 'To be analyzed',
                'competitive_landscape': competitive_landscape if competitive_landscape else 'To be researched',
                'current_revenue': current_revenue if current_revenue else 'N/A',
                'revenue_growth': revenue_growth if revenue_growth else 'N/A',
                'gross_margin': gross_margin if gross_margin else 'N/A',
                'burn_rate': burn_rate if burn_rate else 'N/A',
                'runway': runway if runway else 'N/A',
                'unit_economics': unit_economics if unit_economics else 'N/A',
                'team_info': team_info if team_info else 'To be documented',
                'business_risks': risks if risks else 'To be identified',
                'risk_mitigation': mitigation if mitigation else 'To be developed',
                'scoring': None
            }
            
            memo_content = generate_investment_memo(memo_data)
            
            st.session_state.memo_complete = True
            st.session_state.memo_content = memo_content
            st.session_state.memo_data = memo_data
            
            st.success("Investment Memo Generated!")
            st.rerun()
        
        except Exception as e:
            st.error(f"Error: {str(e)}")
            import traceback
            st.error(traceback.format_exc())

st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

# ===== DOWNLOAD SECTION =====
if st.session_state.memo_complete:
    st.markdown('<div class="section-beige"><div class="section-header">Download Investment Memo</div>', unsafe_allow_html=True)
    
    col_dl1, col_dl2 = st.columns(2)
    
    with col_dl1:
        try:
            docx_doc = template_gen.markdown_to_docx(st.session_state.memo_content)
            docx_buffer = BytesIO()
            docx_doc.save(docx_buffer)
            docx_bytes = docx_buffer.getvalue()
            
            st.download_button(
                label="Download Memo (DOCX)",
                data=docx_bytes,
                file_name=f"{st.session_state.memo_data.get('company_name', 'Memo').replace(' ', '_')}_Investment_Memo_{datetime.now().strftime('%Y%m%d')}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    with col_dl2:
        st.success("Ready to download")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
    
    # ===== MEMO PREVIEW =====
    st.markdown('<div class="section-beige"><div class="section-header">Memo Preview</div>', unsafe_allow_html=True)
    
    with st.expander("View Full Memo", expanded=True):
        st.markdown(st.session_state.memo_content)
    
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)

# ===== FOOTER =====
st.markdown(f"""
<div style="
    background-color:#1B2B4D;
    color:#E2E8F0;
    padding:28px 40px;
    margin:40px -3rem -2rem -3rem;
    font-size:0.92rem;
    width: calc(100% + 6rem);">
  <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; max-width:1400px; margin:auto;">
    <div style="flex:2;">
      <ul style="list-style:none; display:flex; gap:30px; flex-wrap:wrap; padding:0; margin:0;">
        <li><a href="#" style="text-decoration:none; color:#E2E8F0; font-weight:500;">About</a></li>
        <li><a href="#" style="text-decoration:none; color:#E2E8F0; font-weight:500;">Contact</a></li>
      </ul>
    </div>
    <div style="flex:1; text-align:right; display:flex; align-items:center; justify-content:flex-end; gap:12px;">
      <p style="margin:0; color:#A0AEC0; font-size:0.88rem; font-weight:600;">Powered by Regulus AI</p>
      {'<img src="'+regulus_logo+'" style="max-height:45px; opacity:0.92;">' if regulus_logo else ''}
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


# ===== HELPER FUNCTION =====
def generate_investment_memo(data):
    """Generate comprehensive investment memo"""
    
    memo = f"""# INVESTMENT MEMORANDUM
## {data['company_name']}

{data['stage']} Stage Investment Opportunity

---

**Prepared by:** {data['analyst_name']}  
**Date:** {data['analysis_date']}  
**Investment Amount:** {data['investment_size']}  
**Valuation:** {data['valuation']} (Pre-Money)  
**Ownership:** {data['ownership']}

---

## EXECUTIVE SUMMARY

### Investment Recommendation: {data['recommendation']}

{data['investment_thesis']}

### Key Highlights

{data['key_highlights']}

---

## 1. COMPANY OVERVIEW

### Background

- **Founded:** {data['founded']}
- **Location:** {data['location']}
- **Industry:** {data['industry']}
- **Stage:** {data['stage']}

### Products & Services

{data['products_services']}

### Business Model

{data['business_model']}

---

## 2. MARKET OPPORTUNITY

### Market Size

- **Total Addressable Market (TAM):** {data['tam']}
- **Serviceable Addressable Market (SAM):** {data['sam']}
- **Serviceable Obtainable Market (SOM):** {data['som']}

### Market Trends & Drivers

{data['market_trends']}

### Competitive Landscape

{data['competitive_landscape']}

---

## 3. FINANCIAL PERFORMANCE

### Current Metrics

- **Revenue (ARR):** {data['current_revenue']}
- **Growth Rate:** {data['revenue_growth']}
- **Gross Margin:** {data['gross_margin']}
- **Monthly Burn Rate:** {data['burn_rate']}
- **Runway:** {data['runway']}
- **Unit Economics (LTV/CAC):** {data['unit_economics']}

---

## 4. MANAGEMENT TEAM

{data['team_info']}

---

## 5. RISKS & MITIGATION

### Key Risks

{data['business_risks']}

### Risk Mitigation Strategies

{data['risk_mitigation']}

---

## 6. INVESTMENT TERMS

### Proposed Structure

- **Investment Amount:** {data['investment_size']}
- **Pre-Money Valuation:** {data['valuation']}
- **Ownership:** {data['ownership']}

---

## RECOMMENDATION

**Investment Recommendation: {data['recommendation']}**

---

**CONFIDENTIAL - For Internal Use Only**

**Prepared by:** {data['analyst_name']}  
**Date:** {data['analysis_date']}
"""
    
    return memo
