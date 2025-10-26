"""
Investment Memo & Pitch Deck Generator
FIXED: Proper session state management + method calls
"""
import streamlit as st
import base64
import os
from datetime import datetime
from io import BytesIO
from utils.qdb_styling import apply_qdb_styling
from utils.template_generator import TemplateGenerator

st.set_page_config(page_title="Investment Memo", page_icon="📋", layout="wide", initial_sidebar_state="collapsed")
apply_qdb_styling()

@st.cache_resource
def init_handlers():
    try:
        template_gen = TemplateGenerator()
        return template_gen
    except Exception as e:
        st.error(f"Init error: {e}")
        return None

template_gen = init_handlers()
if template_gen is None:
    st.stop()

def encode_image(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f"data:image/png;base64,{base64.b64encode(f.read()).decode()}"
    return None

qdb_logo = encode_image("QDB_Logo.png")
regulus_logo = encode_image("regulus_logo.png")

# Session state
if 'memo_complete' not in st.session_state:
    st.session_state.memo_complete = False
if 'memo_data' not in st.session_state:
    st.session_state.memo_data = {}

st.markdown("""
<style>
.stButton>button {
    background: linear-gradient(135deg,#16A085 0%,#138074 100%)!important;
    color:white!important;
    border-radius:8px!important;
    padding:12px 24px!important;
    font-weight:700!important;
}
.section-beige {
    background-color: #F6F5F2;
    border-radius: 10px;
    padding: 20px;
    margin: 12px 0;
}
.required-asterisk { color: #E74C3C; font-weight: 700; }
.section-header { font-size: 1.2rem; font-weight: 700; color: #1B2B4D; margin-bottom: 12px; }
</style>
""", unsafe_allow_html=True)

st.markdown(f"""
<div style="background: linear-gradient(135deg,#1B2B4D 0%,#2C3E5E 100%);color:white;text-align:center;margin:0 -3rem;padding:40px 20px 50px;width:calc(100% + 6rem);border-bottom:3px solid #16A085;">
  <div style="position:absolute;top:15px;left:35px;">{'<img src="'+qdb_logo+'" style="max-height:55px;">' if qdb_logo else ''}</div>
  <div style="position:absolute;top:15px;right:35px;">{'<img src="'+regulus_logo+'" style="max-height:55px;">' if regulus_logo else ''}</div>
  <h1 style="font-size:2rem;font-weight:800;margin-bottom:6px;">Investment Memorandum</h1>
  <p style="color:#E2E8F0;font-size:0.95rem;margin:0;">Generate professional memo & pitch deck</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

if st.button("Return Home"):
    st.switch_page("streamlit_app.py")

st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

# Input sections
st.markdown('<div class="section-beige"><div class="section-header">Company & Deal Information</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("<div style='color:#1B2B4D;font-size:0.85rem;margin-bottom:4px;font-weight:600;'>Company Name <span class='required-asterisk'>*</span></div>", unsafe_allow_html=True)
    company_name = st.text_input("Company", label_visibility="collapsed", key="company")

with col2:
    st.markdown("<div style='color:#1B2B4D;font-size:0.85rem;margin-bottom:4px;font-weight:600;'>Industry <span class='required-asterisk'>*</span></div>", unsafe_allow_html=True)
    industry = st.text_input("Industry", label_visibility="collapsed", key="industry")

with col3:
    st.markdown("<div style='color:#1B2B4D;font-size:0.85rem;margin-bottom:4px;font-weight:600;'>Funding Stage <span class='required-asterisk'>*</span></div>", unsafe_allow_html=True)
    stage = st.selectbox("Stage", ["Seed", "Series A", "Series B", "Series C", "Growth", "Pre-IPO"], label_visibility="collapsed", key="stage")

col4, col5, col6 = st.columns(3)
with col4:
    st.markdown("<div style='color:#1B2B4D;font-size:0.85rem;margin-bottom:4px;font-weight:600;'>Founded</div>", unsafe_allow_html=True)
    founded = st.text_input("Founded", label_visibility="collapsed", key="founded")

with col5:
    st.markdown("<div style='color:#1B2B4D;font-size:0.85rem;margin-bottom:4px;font-weight:600;'>Location</div>", unsafe_allow_html=True)
    location = st.text_input("Location", label_visibility="collapsed", key="location")

with col6:
    st.markdown("<div style='color:#1B2B4D;font-size:0.85rem;margin-bottom:4px;font-weight:600;'>Recommendation <span class='required-asterisk'>*</span></div>", unsafe_allow_html=True)
    recommendation = st.selectbox("Recommendation", ["STRONG BUY", "BUY", "HOLD", "PASS"], label_visibility="collapsed", key="rec")

col7, col8, col9 = st.columns(3)
with col7:
    st.markdown("<div style='color:#1B2B4D;font-size:0.85rem;margin-bottom:4px;font-weight:600;'>Investment Amount <span class='required-asterisk'>*</span></div>", unsafe_allow_html=True)
    deal_size = st.text_input("Amount", label_visibility="collapsed", key="deal")

with col8:
    st.markdown("<div style='color:#1B2B4D;font-size:0.85rem;margin-bottom:4px;font-weight:600;'>Pre-Money Valuation <span class='required-asterisk'>*</span></div>", unsafe_allow_html=True)
    valuation = st.text_input("Valuation", label_visibility="collapsed", key="val")

with col9:
    st.markdown("<div style='color:#1B2B4D;font-size:0.85rem;margin-bottom:4px;font-weight:600;'>Ownership %</div>", unsafe_allow_html=True)
    ownership = st.text_input("Ownership", label_visibility="collapsed", key="own")

st.markdown("</div>", unsafe_allow_html=True)
st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

# Business info
st.markdown('<div class="section-beige"><div class="section-header">Business Overview</div>', unsafe_allow_html=True)

st.markdown("<div style='color:#1B2B4D;font-size:0.85rem;margin-bottom:4px;font-weight:600;'>Investment Thesis</div>", unsafe_allow_html=True)
thesis = st.text_area("Thesis", height=80, label_visibility="collapsed", key="thesis")

col_b1, col_b2 = st.columns(2)
with col_b1:
    st.markdown("<div style='color:#1B2B4D;font-size:0.85rem;margin-bottom:4px;font-weight:600;'>Business Model</div>", unsafe_allow_html=True)
    business_model = st.text_area("Business", height=100, label_visibility="collapsed", key="bm")

with col_b2:
    st.markdown("<div style='color:#1B2B4D;font-size:0.85rem;margin-bottom:4px;font-weight:600;'>Products & Services</div>", unsafe_allow_html=True)
    products = st.text_area("Products", height=100, label_visibility="collapsed", key="prod")

st.markdown("</div>", unsafe_allow_html=True)
st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

# Market
st.markdown('<div class="section-beige"><div class="section-header">Market Analysis</div>', unsafe_allow_html=True)

col_m1, col_m2, col_m3 = st.columns(3)
with col_m1:
    st.markdown("<div style='color:#1B2B4D;font-size:0.85rem;margin-bottom:4px;font-weight:600;'>TAM</div>", unsafe_allow_html=True)
    tam = st.text_input("TAM", label_visibility="collapsed", key="tam")

with col_m2:
    st.markdown("<div style='color:#1B2B4D;font-size:0.85rem;margin-bottom:4px;font-weight:600;'>SAM</div>", unsafe_allow_html=True)
    sam = st.text_input("SAM", label_visibility="collapsed", key="sam")

with col_m3:
    st.markdown("<div style='color:#1B2B4D;font-size:0.85rem;margin-bottom:4px;font-weight:600;'>SOM</div>", unsafe_allow_html=True)
    som = st.text_input("SOM", label_visibility="collapsed", key="som")

col_m4, col_m5 = st.columns(2)
with col_m4:
    st.markdown("<div style='color:#1B2B4D;font-size:0.85rem;margin-bottom:4px;font-weight:600;'>Market Trends</div>", unsafe_allow_html=True)
    trends = st.text_area("Trends", height=80, label_visibility="collapsed", key="trends")

with col_m5:
    st.markdown("<div style='color:#1B2B4D;font-size:0.85rem;margin-bottom:4px;font-weight:600;'>Competitive Landscape</div>", unsafe_allow_html=True)
    comp = st.text_area("Competition", height=80, label_visibility="collapsed", key="comp")

st.markdown("</div>", unsafe_allow_html=True)
st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

# Financial
st.markdown('<div class="section-beige"><div class="section-header">Financial Performance</div>', unsafe_allow_html=True)

col_f1, col_f2, col_f3 = st.columns(3)
with col_f1:
    st.markdown("<div style='color:#1B2B4D;font-size:0.85rem;margin-bottom:4px;font-weight:600;'>Revenue (ARR)</div>", unsafe_allow_html=True)
    revenue = st.text_input("Revenue", label_visibility="collapsed", key="rev")

with col_f2:
    st.markdown("<div style='color:#1B2B4D;font-size:0.85rem;margin-bottom:4px;font-weight:600;'>Growth Rate</div>", unsafe_allow_html=True)
    growth = st.text_input("Growth", label_visibility="collapsed", key="growth")

with col_f3:
    st.markdown("<div style='color:#1B2B4D;font-size:0.85rem;margin-bottom:4px;font-weight:600;'>Gross Margin</div>", unsafe_allow_html=True)
    margin = st.text_input("Margin", label_visibility="collapsed", key="margin")

col_f4, col_f5, col_f6 = st.columns(3)
with col_f4:
    st.markdown("<div style='color:#1B2B4D;font-size:0.85rem;margin-bottom:4px;font-weight:600;'>Burn Rate</div>", unsafe_allow_html=True)
    burn = st.text_input("Burn", label_visibility="collapsed", key="burn")

with col_f5:
    st.markdown("<div style='color:#1B2B4D;font-size:0.85rem;margin-bottom:4px;font-weight:600;'>Runway</div>", unsafe_allow_html=True)
    runway = st.text_input("Runway", label_visibility="collapsed", key="run")

with col_f6:
    st.markdown("<div style='color:#1B2B4D;font-size:0.85rem;margin-bottom:4px;font-weight:600;'>LTV/CAC</div>", unsafe_allow_html=True)
    ltv = st.text_input("Unit Economics", label_visibility="collapsed", key="ltv")

st.markdown("</div>", unsafe_allow_html=True)
st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

# Team & Risks
st.markdown('<div class="section-beige"><div class="section-header">Team & Risks</div>', unsafe_allow_html=True)

st.markdown("<div style='color:#1B2B4D;font-size:0.85rem;margin-bottom:4px;font-weight:600;'>Management Team</div>", unsafe_allow_html=True)
team = st.text_area("Team", height=100, label_visibility="collapsed", key="team")

col_r1, col_r2 = st.columns(2)
with col_r1:
    st.markdown("<div style='color:#1B2B4D;font-size:0.85rem;margin-bottom:4px;font-weight:600;'>Key Risks</div>", unsafe_allow_html=True)
    risks = st.text_area("Risks", height=100, label_visibility="collapsed", key="risks")

with col_r2:
    st.markdown("<div style='color:#1B2B4D;font-size:0.85rem;margin-bottom:4px;font-weight:600;'>Risk Mitigation</div>", unsafe_allow_html=True)
    mitigation = st.text_area("Mitigation", height=100, label_visibility="collapsed", key="miti")

st.markdown("</div>", unsafe_allow_html=True)
st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

# Generate
if st.button("Generate Investment Memo & Pitch Deck", use_container_width=True):
    if not all([company_name, industry, stage, deal_size, valuation, recommendation]):
        st.error("Please fill all required fields (*)")
    else:
        with st.spinner("Generating documents..."):
            try:
                memo_data = {
                    'company_name': company_name,
                    'analyst_name': 'Qatar Development Bank - Investment Team',
                    'analysis_date': datetime.now().strftime('%B %d, %Y'),
                    'stage': stage,
                    'investment_size': deal_size,
                    'valuation': valuation,
                    'ownership': ownership or 'TBD',
                    'recommendation': recommendation,
                    'founded': founded or 'N/A',
                    'location': location or 'N/A',
                    'industry': industry,
                    'business_model': business_model or 'Pending',
                    'products_services': products or 'Pending',
                    'investment_thesis': thesis or 'Pending',
                    'tam': tam or 'N/A',
                    'sam': sam or 'N/A',
                    'som': som or 'N/A',
                    'market_trends': trends or 'Pending',
                    'competitive_landscape': comp or 'Pending',
                    'current_revenue': revenue or 'N/A',
                    'revenue_growth': growth or 'N/A',
                    'gross_margin': margin or 'N/A',
                    'burn_rate': burn or 'N/A',
                    'runway': runway or 'N/A',
                    'unit_economics': ltv or 'N/A',
                    'team_info': team or 'Pending',
                    'business_risks': risks or 'Pending',
                    'risk_mitigation': mitigation or 'Pending'
                }
                
                st.session_state.memo_data = memo_data
                st.session_state.memo_complete = True
                st.success("Documents generated!")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

# Downloads
if st.session_state.memo_complete:
    st.markdown('<div class="section-beige"><div class="section-header">Download Documents</div>', unsafe_allow_html=True)
    
    col_dl1, col_dl2 = st.columns(2)
    
    with col_dl1:
        try:
            docx_doc = template_gen.generate_investment_memo_docx(st.session_state.memo_data)
            docx_buf = BytesIO()
            docx_doc.save(docx_buf)
            
            st.download_button(
                label="Download Memo (DOCX)",
                data=docx_buf.getvalue(),
                file_name=f"{st.session_state.memo_data['company_name']}_Memo_{datetime.now().strftime('%Y%m%d')}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"Memo error: {e}")
    
    with col_dl2:
        try:
            pptx_pres = template_gen.generate_pitch_deck_pptx(st.session_state.memo_data)
            pptx_buf = BytesIO()
            pptx_pres.save(pptx_buf)
            
            st.download_button(
                label="Download Pitch Deck (PPTX)",
                data=pptx_buf.getvalue(),
                file_name=f"{st.session_state.memo_data['company_name']}_Deck_{datetime.now().strftime('%Y%m%d')}.pptx",
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"Deck error: {e}")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
    
    # Preview
    st.markdown('<div class="section-beige"><div class="section-header">Memo Summary</div>', unsafe_allow_html=True)
    
    with st.expander("View Summary", expanded=True):
        d = st.session_state.memo_data
        st.write(f"**{d['company_name']}** | {d['industry']} | {d['stage']}")
        st.write(f"**Investment:** {d['investment_size']} | **Valuation:** {d['valuation']}")
        st.write(f"**Recommendation:** {d['recommendation']}")
    
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)

st.markdown(f"""
<div style="background-color:#1B2B4D;color:#E2E8F0;padding:28px 40px;margin:40px -3rem -2rem;width:calc(100% + 6rem);">
  <p style="text-align:center;margin:0;">Powered by Regulus AI | Qatar Development Bank</p>
</div>
""", unsafe_allow_html=True)
