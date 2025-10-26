"""
Deal Sourcing - AI-Powered Investment Pipeline
ENHANCED: Industry attractiveness, deal contacts, database stats, next-step selection
"""
import streamlit as st
import base64
import os
from datetime import datetime
from io import BytesIO
from utils.qdb_styling import apply_qdb_styling
from utils.llm_handler import LLMHandler
from utils.template_generator import TemplateGenerator
from utils.deal_sourcer import DealSourcer

st.set_page_config(page_title="Deal Sourcing", page_icon="🎯", layout="wide", initial_sidebar_state="collapsed")
apply_qdb_styling()

# ===== Initialize Handlers =====
@st.cache_resource
def init_handlers():
    try:
        llm = LLMHandler()
        template_gen = TemplateGenerator()
        deal_sourcer = DealSourcer()
        return llm, template_gen, deal_sourcer
    except Exception as e:
        st.error(f"Error initializing handlers: {e}")
        return None, None, None

llm, template_gen, deal_sourcer = init_handlers()

if any(x is None for x in [llm, template_gen, deal_sourcer]):
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
if 'deal_sourcing_complete' not in st.session_state:
    st.session_state.deal_sourcing_complete = False
if 'deal_sourcing_report' not in st.session_state:
    st.session_state.deal_sourcing_report = ""
if 'deal_sourcing_data' not in st.session_state:
    st.session_state.deal_sourcing_data = {}
if 'matched_deals' not in st.session_state:
    st.session_state.matched_deals = []
if 'selected_deals' not in st.session_state:
    st.session_state.selected_deals = []

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

.deal-card {
    background: linear-gradient(135deg, #E8F5F3 0%, #F6F5F2 100%);
    border-left: 4px solid #16A085;
    padding: 14px;
    border-radius: 8px;
    margin: 10px 0;
}

.deal-score {
    display: inline-block;
    background: #16A085;
    color: white;
    padding: 4px 10px;
    border-radius: 12px;
    font-weight: 700;
    font-size: 0.75rem;
}

.industry-badge-hot {
    background: linear-gradient(135deg, #E74C3C 0%, #C0392B 100%);
    color: white;
    padding: 6px 12px;
    border-radius: 6px;
    font-size: 0.75rem;
    font-weight: 700;
    display: inline-block;
    margin: 4px;
}

.industry-badge-warm {
    background: linear-gradient(135deg, #F39C12 0%, #E67E22 100%);
    color: white;
    padding: 6px 12px;
    border-radius: 6px;
    font-size: 0.75rem;
    font-weight: 700;
    display: inline-block;
    margin: 4px;
}

.industry-badge-cool {
    background: linear-gradient(135deg, #3498DB 0%, #2980B9 100%);
    color: white;
    padding: 6px 12px;
    border-radius: 6px;
    font-size: 0.75rem;
    font-weight: 700;
    display: inline-block;
    margin: 4px;
}

.contact-badge {
    background: linear-gradient(135deg, #9B59B6 0%, #8E44AD 100%);
    color: white;
    padding: 8px 14px;
    border-radius: 6px;
    font-size: 0.8rem;
    font-weight: 600;
    display: inline-block;
}

.db-stat {
    background: linear-gradient(135deg, #16A085 0%, #138074 100%);
    color: white;
    padding: 12px 18px;
    border-radius: 8px;
    text-align: center;
    font-weight: 700;
    margin: 8px;
    display: inline-block;
}

.next-step-action {
    background: linear-gradient(135deg, #2980B9 0%, #2471A3 100%);
    color: white;
    padding: 12px 20px;
    border-radius: 8px;
    font-weight: 600;
    text-align: center;
    margin: 10px 0;
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
    <h1 style="font-size:2rem; font-weight:800; margin-bottom:6px;">Deal Sourcing</h1>
    <p style="color:#E2E8F0; font-size:0.95rem; margin:0;">AI-powered investment pipeline with industry intelligence & deal management</p>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

# ===== HOME BUTTON =====
if st.button("← Return Home", key="home_btn"):
    st.switch_page("streamlit_app.py")

st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

# ===== DATABASE & MARKET INTELLIGENCE SECTION =====
st.markdown('<div class="section-beige"><div style="font-size:1.2rem; font-weight:700; color:#1B2B4D; margin-bottom:12px;">📊 Deal Database & Market Intelligence</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown('<div class="db-stat">20<br><span style="font-size:0.7rem;">Total Deals<br>in Database</span></div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="db-stat">$87.8M<br><span style="font-size:0.7rem;">Combined<br>Revenue</span></div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="db-stat">156%<br><span style="font-size:0.7rem;">Avg YoY<br>Growth Rate</span></div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="db-stat">4.5/5.0<br><span style="font-size:0.7rem;">Avg Team<br>Quality Score</span></div>', unsafe_allow_html=True)

# ===== INDUSTRY ATTRACTIVENESS SECTION =====
st.markdown("<div style='margin-top:16px;'><strong style='color:#1B2B4D; font-size:0.95rem;'>🎯 Industry Attractiveness Indicators:</strong></div>", unsafe_allow_html=True)

st.markdown("""
<div style="margin-top:8px;">
<span class="industry-badge-hot">🔥 HOT - Fintech</span>
<span class="industry-badge-warm">📈 WARM - ClimateTech</span>
<span class="industry-badge-warm">📈 WARM - Enterprise SaaS</span>
<span class="industry-badge-cool">❄️ EMERGING - HealthTech</span>
<span class="industry-badge-cool">❄️ EMERGING - EdTech</span>
</div>
""", unsafe_allow_html=True)

st.markdown("<small style='color:#666;'>🔥 HOT = 8+ deals, >200% avg growth | 📈 WARM = 5-7 deals, 100-200% growth | ❄️ EMERGING = <5 deals, <100% growth</small>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

# ===== SEARCH CRITERIA =====
st.markdown('<div class="section-beige"><div style="font-size:1.2rem; font-weight:700; color:#1B2B4D; margin-bottom:12px;">Search Criteria</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown("<div style='color:#1B2B4D; font-size:0.85rem; margin-bottom:4px; font-weight:600;'>Industry Focus <span class='required-asterisk'>*</span></div>", unsafe_allow_html=True)
    industry_focus = st.multiselect(
        "Industry Focus",
        [
            "Fintech",
            "ClimateTech",
            "Enterprise SaaS",
            "HealthTech",
            "EdTech",
            "D2C",
            "Logistics",
            "AgriTech",
            "Energy Tech",
            "AI/ML"
        ],
        default=["Fintech", "ClimateTech"],
        label_visibility="collapsed"
    )

with col2:
    st.markdown("<div style='color:#1B2B4D; font-size:0.85rem; margin-bottom:4px; font-weight:600;'>Funding Stage <span class='required-asterisk'>*</span></div>", unsafe_allow_html=True)
    funding_stage = st.multiselect(
        "Funding Stage",
        ["Seed", "Series A", "Series B", "Series C"],
        default=["Seed", "Series A", "Series B"],
        label_visibility="collapsed"
    )

col3, col4 = st.columns(2)
with col3:
    st.markdown("<div style='color:#1B2B4D; font-size:0.85rem; margin-bottom:4px; font-weight:600;'>Revenue Range (Million USD) <span class='required-asterisk'>*</span></div>", unsafe_allow_html=True)
    revenue_min, revenue_max = st.slider(
        "Revenue Range",
        0.0, 10.0, (0.0, 10.0),
        step=0.5,
        label_visibility="collapsed"
    )
    st.caption(f"${revenue_min}M - ${revenue_max}M")

with col4:
    st.markdown("<div style='color:#1B2B4D; font-size:0.85rem; margin-bottom:4px; font-weight:600;'>Geographic Focus</div>", unsafe_allow_html=True)
    geographic_focus = st.multiselect(
        "Geographic Focus",
        ["North America", "Europe", "MENA", "Asia Pacific", "Global"],
        default=["North America", "Europe"],
        label_visibility="collapsed"
    )

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

# ===== SCREENING CRITERIA =====
st.markdown('<div class="section-beige"><div style="font-size:1.2rem; font-weight:700; color:#1B2B4D; margin-bottom:12px;">Screening Criteria</div>', unsafe_allow_html=True)

criteria_options = st.multiselect(
    "Select Screening Factors",
    [
        "Unit Economics (LTV/CAC)",
        "Growth Rate (YoY)",
        "Market Traction",
        "Team Quality",
        "IP/Technology",
        "Strategic Fit with QDB",
        "Exit Potential",
        "ESG Alignment"
    ],
    default=["Unit Economics (LTV/CAC)", "Growth Rate (YoY)", "Market Traction", "Team Quality"],
    label_visibility="collapsed"
)

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

# ===== SOURCING BUTTON =====
if st.button("Search Investment Pipeline", use_container_width=True):
    if not industry_focus or not funding_stage:
        st.error("Please select industry and funding stage")
        st.stop()

    with st.spinner("Searching deal pipeline..."):
        try:
            st.info("🔍 Filtering investment opportunities...")
            
            search_results = deal_sourcer.search_deals(
                industry_list=industry_focus,
                stage_list=funding_stage,
                revenue_min=revenue_min,
                revenue_max=revenue_max,
                geography_list=geographic_focus,
                screening_factors=criteria_options
            )
            
            matched_deals = search_results['deals']
            st.session_state.matched_deals = matched_deals
            
            st.success(f"✅ Found {len(matched_deals)} matching deals!")
            
            # Display deals found with selection
            if matched_deals:
                st.markdown("### 🎯 Top Deal Opportunities - Select for Next Steps")
                
                # Create checkboxes for deal selection
                selected_deal_names = []
                
                for idx, deal in enumerate(matched_deals[:10], 1):
                    with st.expander(f"#{idx} {deal['name']} - {deal['industry']} ({deal['stage']})"):
                        col1, col2, col3 = st.columns([1, 2, 2])
                        
                        with col1:
                            st.metric("Revenue", f"${deal['revenue']}M")
                            st.metric("Growth", f"{deal['growth']}%")
                        
                        with col2:
                            st.metric("Team Score", f"{deal['team_score']}/5.0")
                            st.metric("Region", deal['geography'])
                        
                        with col3:
                            score_html = f"<div class='deal-score'>{deal['investment_score']:.1f}/5</div>"
                            st.markdown(score_html, unsafe_allow_html=True)
                            st.metric("Traction", deal['traction'], label_visibility="collapsed")
                        
                        # ===== CONTACT INFORMATION PLACEHOLDER =====
                        st.divider()
                        st.markdown("<strong style='color:#16A085;'>📞 Deal Contact Information</strong>", unsafe_allow_html=True)
                        
                        col_contact1, col_contact2 = st.columns(2)
                        with col_contact1:
                            st.markdown("""
                            <div class="contact-badge">
                            👤 Founder: John Smith<br>
                            📧 john@{}.com
                            </div>
                            """.format(deal['name'].lower().replace(' ', '')), unsafe_allow_html=True)
                        
                        with col_contact2:
                            st.markdown("""
                            <div class="contact-badge">
                            💼 Investor Relations: Sarah Johnson<br>
                            📧 ir@{}.com
                            </div>
                            """.format(deal['name'].lower().replace(' ', '')), unsafe_allow_html=True)
                        
                        # Selection checkbox
                        col_sel1, col_sel2 = st.columns([3, 1])
                        with col_sel1:
                            if st.checkbox(f"Select {deal['name']} for next steps", key=f"select_{deal['name']}"):
                                if deal['name'] not in selected_deal_names:
                                    selected_deal_names.append(deal['name'])
                        
                        with col_sel2:
                            st.markdown("<div class='next-step-action'>➜ Next Step →</div>", unsafe_allow_html=True)
                
                # Save selected deals to session state
                st.session_state.selected_deals = selected_deal_names
            
            st.info("📊 Compiling deal analysis...")
            
            deal_data = {
                'industries': ', '.join(industry_focus),
                'stages': ', '.join(funding_stage),
                'revenue_range': f"${revenue_min}M - ${revenue_max}M",
                'geography': ', '.join(geographic_focus),
                'screening_factors': criteria_options,
                'analysis_date': datetime.now().strftime('%B %d, %Y'),
                'total_deals_in_db': 20,
                'matches_found': len(matched_deals)
            }
            
            # Generate AI insights
            insights_prompt = f"""
Based on the following deal matches:
Industries: {deal_data['industries']}
Stages: {deal_data['stages']}
Revenue: {deal_data['revenue_range']}
Found {len(matched_deals)} deals

Provide brief strategic insights on:
1. Attractiveness of these deals
2. Portfolio fit
3. Due diligence priorities
4. Next 90-day action plan
"""
            
            deal_insights = llm.generate(insights_prompt)
            
            # Create comprehensive report
            report = f"""# Deal Sourcing Analysis Report

**Analysis Date:** {deal_data['analysis_date']}

## Search Parameters
- **Industries:** {deal_data['industries']}
- **Funding Stages:** {deal_data['stages']}
- **Revenue Range:** {deal_data['revenue_range']}
- **Geographic Focus:** {deal_data['geography']}

## Pipeline Summary
- **Total Deals Evaluated:** {deal_data['total_deals_in_db']}
- **Matches Found:** {deal_data['matches_found']}
- **Match Rate:** {(deal_data['matches_found']/deal_data['total_deals_in_db']*100):.1f}%
- **Selected for Next Steps:** {len(st.session_state.selected_deals)}

## Top Investment Opportunities
"""
            
            if matched_deals:
                for idx, deal in enumerate(matched_deals[:5], 1):
                    report += f"""
### {idx}. {deal['name']}
**Investment Score:** {deal['investment_score']:.1f}/5.0

| Metric | Value |
|--------|-------|
| Industry | {deal['industry']} |
| Stage | {deal['stage']} |
| Revenue | ${deal['revenue']}M |
| Growth Rate | {deal['growth']}% YoY |
| Team Quality | {deal['team_score']}/5.0 |
| Geography | {deal['geography']} |
| Traction | {deal['traction']} |

"""
            
            report += f"""

## Strategic Insights

{deal_insights}

## Deals Selected for Next Steps
{chr(10).join([f"- {deal_name}" for deal_name in st.session_state.selected_deals]) if st.session_state.selected_deals else "- No deals selected yet"}

## Recommended Next Steps
1. Schedule management presentations with selected deals
2. Request detailed financial models and pitch decks
3. Conduct team background verification
4. Assess IP and technology differentiation
5. Prepare investment committee presentation

---

**Prepared by:** Regulus AI Deal Sourcing Engine  
**Confidence Level:** 95%  
*Confidential - For Authorized Recipients Only*
"""
            
            st.session_state.deal_sourcing_complete = True
            st.session_state.deal_sourcing_report = report
            st.session_state.deal_sourcing_data = deal_data
            
            st.success("✅ Deal Pipeline Analysis Generated!")
        
        except Exception as e:
            st.error(f"Error during sourcing: {str(e)}")
            import traceback
            st.error(traceback.format_exc())
            st.stop()

st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

# ===== DOWNLOAD SECTION =====
if st.session_state.deal_sourcing_complete:
    st.markdown('<div class="section-beige"><div style="font-size:1.2rem; font-weight:700; color:#1B2B4D; margin-bottom:12px;">Download & Next Steps</div>', unsafe_allow_html=True)
    
    data = st.session_state.deal_sourcing_data
    
    col_dl1, col_dl2 = st.columns(2)
    
    with col_dl1:
        try:
            docx_doc = template_gen.markdown_to_docx(st.session_state.deal_sourcing_report)
            docx_buffer = BytesIO()
            docx_doc.save(docx_buffer)
            docx_bytes = docx_buffer.getvalue()
            
            st.download_button(
                label="📥 Download Deal Pipeline (DOCX)",
                data=docx_bytes,
                file_name=f"Deal_Pipeline_{datetime.now().strftime('%Y%m%d')}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"Error generating report: {str(e)}")
    
    with col_dl2:
        if st.session_state.selected_deals:
            st.markdown("""
            <div class='next-step-action' style='width:100%;'>
            ✅ {0} Deal(s) Selected - Ready for Due Diligence
            </div>
            """.format(len(st.session_state.selected_deals)), unsafe_allow_html=True)
            
            if st.button("📋 Proceed to Due Diligence Analysis →", use_container_width=True, key="proceed_dd"):
                st.info("💡 Tip: Next, upload documents from selected deals to Due Diligence page for detailed analysis")
                st.switch_page("pages/2_Due_Diligence_Analysis.py")
        else:
            st.info("ℹ️ Select deals above to proceed to Due Diligence")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
    
    # ===== FULL REPORT =====
    st.markdown('<div class="section-beige"><div style="font-size:1.2rem; font-weight:700; color:#1B2B4D; margin-bottom:12px;">Deal Pipeline Report</div>', unsafe_allow_html=True)
    st.markdown(st.session_state.deal_sourcing_report)
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
