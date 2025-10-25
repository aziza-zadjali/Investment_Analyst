"""
Enhanced Investment Memo Generation with Scoring Framework
"""

import streamlit as st
from datetime import datetime
from io import BytesIO
from utils.template_generator import TemplateGenerator
from utils.llm_handler import LLMHandler

st.set_page_config(page_title="Investment Memo", page_icon="📝", layout="wide")

# Initialize handlers
@st.cache_resource
def init_handlers():
    return TemplateGenerator(), LLMHandler()

template_gen, llm = init_handlers()

# Session state
if 'memo_complete' not in st.session_state:
    st.session_state.memo_complete = False
if 'memo_content' not in st.session_state:
    st.session_state.memo_content = ""

st.markdown("""
<div style="padding: 1.5rem 0; border-bottom: 2px solid #f0f0f0;">
    <h1 style="margin: 0; font-size: 2.5rem;">📝 Investment Memo Generator</h1>
    <p style="margin: 0.5rem 0 0 0; color: #666; font-size: 1.1rem;">
        AI-powered professional investment memos with scoring framework
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Company & Deal Information
st.subheader("🏢 Company & Deal Information")

col1, col2, col3 = st.columns(3)

with col1:
    company_name = st.text_input("Company Name *", placeholder="e.g., GreenTech Solutions")
    founded_year = st.text_input("Founded", placeholder="e.g., 2020")

with col2:
    industry = st.text_input("Industry/Sector *", placeholder="e.g., Renewable Energy")
    location = st.text_input("Location", placeholder="e.g., San Francisco, CA")

with col3:
    stage = st.selectbox("Investment Stage *", ["Seed", "Series A", "Series B", "Series C", "Growth", "Pre-IPO"])
    deal_size = st.text_input("Investment Amount *", placeholder="e.g., $5M")

col4, col5, col6 = st.columns(3)

with col4:
    valuation = st.text_input("Pre-Money Valuation *", placeholder="e.g., $50M")

with col5:
    ownership = st.text_input("Ownership %", placeholder="e.g., 10%")

with col6:
    recommendation = st.selectbox("Recommendation *", ["STRONG BUY", "BUY", "HOLD", "PASS"])

st.divider()

# Business Overview
st.subheader("📊 Business Overview")

col_bus1, col_bus2 = st.columns(2)

with col_bus1:
    business_model = st.text_area("Business Model", height=100, placeholder="Describe the company's business model...")
    products_services = st.text_area("Products/Services", height=100, placeholder="Describe key products and services...")

with col_bus2:
    investment_thesis = st.text_area("Investment Thesis", height=100, placeholder="Why is this a compelling investment?")
    key_highlights = st.text_area("Key Highlights", height=100, placeholder="List key achievements and strengths...")

st.divider()

# Market Analysis
st.subheader("🌐 Market Analysis")

col_mkt1, col_mkt2, col_mkt3 = st.columns(3)

with col_mkt1:
    tam = st.text_input("TAM (Total Addressable Market)", placeholder="e.g., $50B")

with col_mkt2:
    sam = st.text_input("SAM (Serviceable Addressable Market)", placeholder="e.g., $5B")

with col_mkt3:
    som = st.text_input("SOM (Serviceable Obtainable Market)", placeholder="e.g., $500M")

market_trends = st.text_area("Market Trends & Drivers", height=80, placeholder="Describe market dynamics, growth drivers, and trends...")
competitive_landscape = st.text_area("Competitive Landscape", height=80, placeholder="Describe competitors and competitive positioning...")

st.divider()

# Financial Performance
st.subheader("💰 Financial Performance")

col_fin1, col_fin2, col_fin3 = st.columns(3)

with col_fin1:
    current_revenue = st.text_input("Current Revenue (ARR)", placeholder="e.g., $10M")

with col_fin2:
    revenue_growth = st.text_input("Revenue Growth Rate", placeholder="e.g., 150% YoY")

with col_fin3:
    gross_margin = st.text_input("Gross Margin", placeholder="e.g., 75%")

col_fin4, col_fin5, col_fin6 = st.columns(3)

with col_fin4:
    burn_rate = st.text_input("Monthly Burn Rate", placeholder="e.g., $500K")

with col_fin5:
    runway = st.text_input("Runway (Months)", placeholder="e.g., 18 months")

with col_fin6:
    unit_economics = st.text_input("LTV/CAC Ratio", placeholder="e.g., 3.5x")

st.divider()

# Initialize scoring variables with defaults
strategic_clarity = 7
symbolic_fluency = 6
execution_discipline = 6
archetypal_fit = 7
gulf_resonance = 6
composite_score = 6.4
enable_scoring = False

# Gulf Resonance Scoring Framework (Optional)
with st.expander("📊 **Optional:** Gulf Resonance Scoring Framework", expanded=False):
    st.info("**Strategic Investment Scoring Framework:** Rate each dimension from 1-10 based on comprehensive analysis.")
    
    col_s1, col_s2 = st.columns(2)
    
    with col_s1:
        strategic_clarity = st.slider("Strategic Clarity", min_value=1, max_value=10, value=7, help="Clear vision, mission, and strategic roadmap")
        symbolic_fluency = st.slider("Symbolic Fluency", min_value=1, max_value=10, value=6, help="Brand positioning and market narrative")
        execution_discipline = st.slider("Execution Discipline", min_value=1, max_value=10, value=6, help="Track record of delivering on commitments")
    
    with col_s2:
        archetypal_fit = st.slider("Archetypal Fit", min_value=1, max_value=10, value=7, help="Alignment with portfolio strategy and thesis")
        gulf_resonance = st.slider("Gulf Resonance", min_value=1, max_value=10, value=6, help="Regional market fit and cultural alignment")
    
    composite_score = (strategic_clarity + symbolic_fluency + execution_discipline + archetypal_fit + gulf_resonance) / 5
    st.metric("Composite Score", f"{composite_score:.1f}/10")
    enable_scoring = st.checkbox("Include scoring framework in memo", value=False)

st.divider()

# Team Information
st.subheader("👥 Team & Leadership")
team_info = st.text_area("Management Team", height=100, placeholder="Describe key team members, their backgrounds, and relevant experience...")

st.divider()

# Risks & Mitigation
st.subheader("⚠️ Risks & Mitigation")

col_risk1, col_risk2 = st.columns(2)

with col_risk1:
    risks = st.text_area("Key Risks", height=150, placeholder="Identify market, execution, financial, and regulatory risks...")

with col_risk2:
    mitigation = st.text_area("Mitigation Strategies", height=150, placeholder="Describe strategies to address identified risks...")

st.divider()

# Generate Button
if st.button("🚀 Generate Investment Memo", type="primary", use_container_width=True):
    
    if not company_name or not industry or not stage or not deal_size or not valuation:
        st.error("⚠️ Please fill in all required fields (*)")
        st.stop()
    
    with st.spinner("🤖 Generating professional investment memo..."):
        
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
            'risk_mitigation': mitigation if mitigation else 'To be developed'
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
        else:
            memo_data['scoring'] = None
        
        if not investment_thesis or investment_thesis == "":
            st.info("💡 Generating investment thesis with AI...")
            try:
                thesis_prompt = f"Generate a compelling investment thesis for {company_name}, a {stage} stage company in the {industry} industry. Context: Business Model: {business_model[:500] if business_model else 'Not provided'}, Market: TAM {tam}, SAM {sam}, Current Revenue: {current_revenue}, Growth: {revenue_growth}. Provide a concise 2-3 paragraph investment thesis highlighting why this is an attractive investment opportunity."
                memo_data['investment_thesis'] = llm.generate(thesis_prompt)
            except Exception as e:
                st.warning(f"Could not generate thesis: {e}")
        
        st.info("📝 Generating comprehensive investment memo...")
        memo_content = generate_investment_memo(memo_data)
        
        st.session_state.memo_complete = True
        st.session_state.memo_content = memo_content
        st.session_state.memo_data = memo_data
        
        st.success("✅ Investment Memo Generated!")
        st.rerun()

# Display Results
if st.session_state.memo_complete:
    
    st.divider()
    st.subheader("📥 Download Investment Memo")
    
    col_dl1, col_dl2 = st.columns(2)
    
    with col_dl1:
        st.download_button(
            label="⬇️ Download Markdown (.md)",
            data=st.session_state.memo_content,
            file_name=f"{st.session_state.memo_data['company_name'].replace(' ', '_')}_Investment_Memo_{datetime.now().strftime('%Y%m%d')}.md",
            mime="text/markdown"
        )
    
    with col_dl2:
        try:
            docx_doc = template_gen.markdown_to_docx(st.session_state.memo_content)
            docx_buffer = BytesIO()
            docx_doc.save(docx_buffer)
            docx_buffer.seek(0)
            
            st.download_button(
                label="⬇️ Download DOCX (.docx)",
                data=docx_buffer.getvalue(),
                file_name=f"{st.session_state.memo_data['company_name'].replace(' ', '_')}_Investment_Memo_{datetime.now().strftime('%Y%m%d')}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
        except Exception as e:
            st.error(f"Error generating DOCX: {e}")
    
    st.divider()
    
    with st.expander("📄 Preview Investment Memo", expanded=True):
        st.markdown(st.session_state.memo_content)


def generate_investment_memo(data):
    """Generate comprehensive investment memo"""
    
    memo = f"""# INVESTMENT MEMORANDUM
## {data['company_name']}

**{data['stage']} Stage Investment Opportunity**

---

**Prepared by:** {data['analyst_name']}  
**Date:** {data['analysis_date']}  
**Investment Amount:** {data['investment_size']}  
**Valuation:** {data['valuation']} (Pre-Money)  
**Ownership:** {data['ownership']}

---

## EXECUTIVE SUMMARY

### Investment Recommendation: **{data['recommendation']}**

{data['investment_thesis']}

### Key Investment Highlights

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

- **Current Revenue (ARR):** {data['current_revenue']}
- **Revenue Growth:** {data['revenue_growth']}
- **Gross Margin:** {data['gross_margin']}
- **Monthly Burn Rate:** {data['burn_rate']}
- **Runway:** {data['runway']}
- **Unit Economics (LTV/CAC):** {data['unit_economics']}

---

## 4. MANAGEMENT TEAM

{data['team_info']}

---

## 5. INVESTMENT TERMS

### Proposed Structure

- **Investment Amount:** {data['investment_size']}
- **Pre-Money Valuation:** {data['valuation']}
- **Ownership:** {data['ownership']}

---

## 6. RISK ANALYSIS

### Key Risks

{data['business_risks']}

### Risk Mitigation Strategies

{data['risk_mitigation']}

---
"""

    if data.get('scoring'):
        scores = data['scoring']
        memo += f"""
## 7. STRATEGIC ASSESSMENT FRAMEWORK

### Gulf Resonance Scoring

| Dimension | Score | Description |
|-----------|-------|-------------|
| **Strategic Clarity** | {scores['strategic_clarity']}/10 | Clear vision, mission, and strategic roadmap |
| **Symbolic Fluency** | {scores['symbolic_fluency']}/10 | Brand positioning and market narrative |
| **Execution Discipline** | {scores['execution_discipline']}/10 | Track record of delivering on commitments |
| **Archetypal Fit** | {scores['archetypal_fit']}/10 | Alignment with portfolio strategy |
| **Gulf Resonance** | {scores['gulf_resonance']}/10 | Regional market fit and cultural alignment |

**Composite Score: {scores['composite_score']:.1f}/10**

---
"""

    memo += f"""
## 8. RECOMMENDATION & NEXT STEPS

### Investment Recommendation: **{data['recommendation']}**

Based on comprehensive analysis, we recommend **{data['recommendation']}** for this investment opportunity.

---

**CONFIDENTIAL - For Internal Use Only**

**Prepared by:** {data['analyst_name']}  
**Date:** {data['analysis_date']}
"""
    
    return memo


# Sidebar
with st.sidebar:
    st.markdown("### 💡 Investment Memo Features")
    st.markdown("""
✓ **Comprehensive Analysis**
✓ **Professional Format**
✓ **Scoring Framework**
✓ **AI-Enhanced Content**
✓ **Market Assessment**
✓ **Financial Metrics**
✓ **Risk Analysis**
✓ **Download MD & DOCX**
""")
    
    if st.session_state.memo_complete:
        st.divider()
        st.markdown("### 📋 Memo Summary")
        data = st.session_state.memo_data
        st.caption(f"**Company:** {data.get('company_name', 'N/A')}")
        st.caption(f"**Stage:** {data.get('stage', 'N/A')}")
        st.caption(f"**Investment:** {data.get('investment_size', 'N/A')}")
        st.caption(f"**Recommendation:** {data.get('recommendation', 'N/A')}")
        
        if data.get('scoring'):
            st.caption(f"**Composite Score:** {data['scoring']['composite_score']:.1f}/10")
