"""
Investment Memo Generation - Final Workflow Step
Auto-filled from complete analysis workflow
"""

import streamlit as st
from datetime import datetime
from io import BytesIO
from utils.template_generator import TemplateGenerator
from utils.llm_handler import LLMHandler

st.set_page_config(page_title="Investment Memo", layout="wide", initial_sidebar_state="collapsed")

# Hide sidebar
st.markdown("""
<style>
    [data-testid="stSidebar"] {display: none;}
    .main > div {padding-top: 2rem;}
</style>
""", unsafe_allow_html=True)

def gradient_box(text, gradient="linear-gradient(90deg, #A6D8FF, #D5B8FF)"):
    return f"""<div style="background: {gradient}; padding: 15px 20px; border-radius: 12px; color: white; font-weight: 600; font-size: 1.5rem; text-align: center; margin-bottom: 20px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);">{text}</div>"""

@st.cache_resource
def init_handlers():
    return TemplateGenerator(), LLMHandler()

template_gen, llm = init_handlers()

if 'memo_complete' not in st.session_state:
    st.session_state.memo_complete = False
if 'memo_content' not in st.session_state:
    st.session_state.memo_content = ""

# Top Navigation
col_nav1, col_nav2, col_nav3 = st.columns([1, 2, 1])
with col_nav1:
    if st.button("← Back to Financial"):
        st.switch_page("pages/4_Financial_Modeling.py")
with col_nav2:
    st.markdown("<p style='text-align: center; color: #666; font-weight: 600;'>Step 5 of 5: Investment Memo</p>", unsafe_allow_html=True)
with col_nav3:
    st.markdown("<p style='text-align: right; color: #999;'>QDB Analyst</p>", unsafe_allow_html=True)

st.markdown("<div style='background: linear-gradient(90deg, #A6D8FF, #D5B8FF); height: 4px; border-radius: 2px; margin-bottom: 30px;'></div>", unsafe_allow_html=True)

# HEADER
st.markdown(gradient_box("Investment Memorandum Generator"), unsafe_allow_html=True)

# Auto-fill from workflow
selected_deal = st.session_state.get('selected_deal')
dd_report = st.session_state.get('dd_report')
market_report = st.session_state.get('market_report')
financial_model = st.session_state.get('financial_model')

if selected_deal:
    st.success(f"📝 Generating Investment Memo for: **{selected_deal['company']}**")
    company_name_default = selected_deal['company']
    industry_default = selected_deal['industry']
    sector_default = selected_deal['sector']
    stage_default = selected_deal['stage']
else:
    st.info("💡 Complete previous workflow steps for auto-fill, or enter manually")
    company_name_default = ""
    industry_default = ""
    sector_default = ""
    stage_default = "Seed"

st.markdown("<div style='background: linear-gradient(90deg, #A6D8FF, #D5B8FF); height: 4px; border-radius: 2px; margin: 30px 0;'></div>", unsafe_allow_html=True)

# Company & Deal Information
st.markdown(gradient_box("Company & Deal Information", "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"), unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    company_name = st.text_input("Company Name *", value=company_name_default)
    founded_year = st.text_input("Founded", placeholder="e.g., 2020")

with col2:
    industry = st.text_input("Industry *", value=industry_default)
    location = st.text_input("Location", placeholder="e.g., Doha, Qatar")

with col3:
    stage = st.selectbox("Stage *", ["Seed", "Series A", "Series B", "Series C", "Growth", "Pre-IPO"], index=["Seed", "Series A", "Series B"].index(stage_default) if stage_default in ["Seed", "Series A", "Series B"] else 0)
    deal_size = st.text_input("Investment *", placeholder="e.g., $5M")

col4, col5, col6 = st.columns(3)
with col4:
    valuation = st.text_input("Valuation *", placeholder="e.g., $50M")
with col5:
    ownership = st.text_input("Ownership %", placeholder="e.g., 10%")
with col6:
    recommendation = st.selectbox("Recommendation *", ["STRONG BUY", "BUY", "HOLD", "PASS"])

st.markdown("<div style='background: linear-gradient(90deg, #A6D8FF, #D5B8FF); height: 4px; border-radius: 2px; margin: 30px 0;'></div>", unsafe_allow_html=True)

# Business Overview
st.markdown(gradient_box("Business Overview", "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)"), unsafe_allow_html=True)

col_bus1, col_bus2 = st.columns(2)
with col_bus1:
    business_model = st.text_area("Business Model", height=100, placeholder="Describe business model...")
    products_services = st.text_area("Products/Services", height=100)
with col_bus2:
    investment_thesis = st.text_area("Investment Thesis", height=100)
    key_highlights = st.text_area("Key Highlights", height=100)

st.markdown("<div style='background: linear-gradient(90deg, #A6D8FF, #D5B8FF); height: 4px; border-radius: 2px; margin: 30px 0;'></div>", unsafe_allow_html=True)

# Market & Financials (Condensed)
col_mkt1, col_mkt2, col_mkt3 = st.columns(3)
with col_mkt1:
    tam = st.text_input("TAM", placeholder="$50B")
with col_mkt2:
    current_revenue = st.text_input("ARR", placeholder="$10M")
with col_mkt3:
    growth_rate = st.text_input("Growth", placeholder="150% YoY")

# Scoring Framework (Optional)
with st.expander("📊 Optional: Gulf Resonance Scoring", expanded=False):
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        strategic_clarity = st.slider("Strategic Clarity", 1, 10, 7)
        symbolic_fluency = st.slider("Symbolic Fluency", 1, 10, 6)
        execution_discipline = st.slider("Execution Discipline", 1, 10, 6)
    with col_s2:
        archetypal_fit = st.slider("Archetypal Fit", 1, 10, 7)
        gulf_resonance = st.slider("Gulf Resonance", 1, 10, 6)
    
    composite_score = (strategic_clarity + symbolic_fluency + execution_discipline + archetypal_fit + gulf_resonance) / 5
    st.metric("Composite Score", f"{composite_score:.1f}/10")
    enable_scoring = st.checkbox("Include scoring in memo", value=False)

st.markdown("<div style='background: linear-gradient(90deg, #A6D8FF, #D5B8FF); height: 4px; border-radius: 2px; margin: 30px 0;'></div>", unsafe_allow_html=True)

# Generate Button
if st.button("🚀 Generate Investment Memo", type="primary", use_container_width=True):
    
    if not company_name or not industry or not stage or not deal_size or not valuation:
        st.error("⚠️ Please fill required fields (*)")
    else:
        with st.spinner("Generating professional investment memo..."):
            
            memo_data = {
                'company_name': company_name,
                'analyst_name': 'Regulus AI - Qatar Development Bank',
                'analysis_date': datetime.now().strftime('%B %d, %Y'),
                'stage': stage,
                'investment_size': deal_size,
                'valuation': valuation,
                'ownership': ownership or 'TBD',
                'recommendation': recommendation,
                'founded': founded_year or 'N/A',
                'location': location or 'N/A',
                'industry': industry,
                'business_model': business_model or 'To be documented',
                'products_services': products_services or 'To be documented',
                'investment_thesis': investment_thesis or 'To be developed',
                'key_highlights': key_highlights or 'To be documented',
                'tam': tam or 'N/A',
                'current_revenue': current_revenue or 'N/A',
                'revenue_growth': growth_rate or 'N/A'
            }
            
            if enable_scoring:
                memo_data['scoring'] = {
                    'strategic_clarity': strategic_clarity,
                    'symbolic_fluency': symbolic_fluency,
                    'execution_discipline': execution_discipline,
                    'archetypal_fit': archetypal_fit,
                    'gulf_resonance': gulf_resonance,
                    'composite_score': composite_score
                }
            
            memo_content = generate_memo(memo_data)
            st.session_state.memo_complete = True
            st.session_state.memo_content = memo_content
            st.session_state.memo_data = memo_data
            st.success("✅ Investment Memo Generated!")
            st.rerun()

# Display Results
if st.session_state.memo_complete:
    st.markdown("<div style='background: linear-gradient(90deg, #A6D8FF, #D5B8FF); height: 4px; border-radius: 2px; margin: 30px 0;'></div>", unsafe_allow_html=True)
    st.markdown(gradient_box("Investment Memo Ready"), unsafe_allow_html=True)
    
    col_dl1, col_dl2 = st.columns(2)
    
    with col_dl1:
        st.download_button(
            "📥 Download Markdown",
            st.session_state.memo_content,
            f"{st.session_state.memo_data['company_name'].replace(' ', '_')}_Memo_{datetime.now().strftime('%Y%m%d')}.md",
            "text/markdown",
            use_container_width=True
        )
    
    with col_dl2:
        try:
            doc = template_gen.markdown_to_docx(st.session_state.memo_content)
            bio = BytesIO()
            doc.save(bio)
            st.download_button(
                "📥 Download DOCX",
                bio.getvalue(),
                f"{st.session_state.memo_data['company_name'].replace(' ', '_')}_Memo_{datetime.now().strftime('%Y%m%d')}.docx",
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )
        except:
            pass
    
    with st.expander("📄 Preview Memo", expanded=True):
        st.markdown(st.session_state.memo_content[:2000] + "...")
    
    # WORKFLOW COMPLETE
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style='
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 12px;
            padding: 30px;
            color: white;
            text-align: center;
        '>
            <h2 style='margin: 0 0 15px 0;'>🎉 Analysis Complete!</h2>
            <p style='margin: 0; font-size: 1.2rem;'>Full investment workflow completed successfully</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_final1, col_final2 = st.columns(2)
    
    with col_final1:
        if st.button("← Back to Financial", use_container_width=True):
            st.switch_page("pages/4_Financial_Modeling.py")
    
    with col_final2:
        if st.button("🏠 Return to Home", type="primary", use_container_width=True):
            st.switch_page("Main_Page.py")

def generate_memo(data):
    memo = f"""# INVESTMENT MEMORANDUM
## {data['company_name']}

**Prepared by:** {data['analyst_name']}  
**Date:** {data['analysis_date']}

---

## EXECUTIVE SUMMARY

**Recommendation:** **{data['recommendation']}**

**Investment Highlights:**
{data['key_highlights']}

## COMPANY OVERVIEW
- **Industry:** {data['industry']}
- **Stage:** {data['stage']}
- **Location:** {data['location']}

## INVESTMENT TERMS
- **Amount:** {data['investment_size']}
- **Valuation:** {data['valuation']}
- **Ownership:** {data['ownership']}

## MARKET & FINANCIALS
- **TAM:** {data['tam']}
- **Revenue:** {data['current_revenue']}
- **Growth:** {data['revenue_growth']}

"""
    
    if data.get('scoring'):
        s = data['scoring']
        memo += f"""## STRATEGIC ASSESSMENT

| Dimension | Score |
|-----------|-------|
| Strategic Clarity | {s['strategic_clarity']}/10 |
| Symbolic Fluency | {s['symbolic_fluency']}/10 |
| Execution Discipline | {s['execution_discipline']}/10 |
| Archetypal Fit | {s['archetypal_fit']}/10 |
| Gulf Resonance | {s['gulf_resonance']}/10 |

**Composite Score: {s['composite_score']:.1f}/10**

"""
    
    memo += f"""---
**CONFIDENTIAL - Qatar Development Bank**
"""
    return memo

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center; color: #999; font-size: 0.9rem;'>Investment Memo | Powered by Regulus AI</div>", unsafe_allow_html=True)
