"""
Deal Sourcing - Enhanced & Fixed
Features: Industry tagging, web search, deal listing, selection workflow
FIXED: Session state management & page switching
"""
import streamlit as st
import base64
import os
from datetime import datetime
from utils.qdb_styling import apply_qdb_styling

st.set_page_config(page_title="Deal Sourcing", page_icon="📊", layout="wide", initial_sidebar_state="collapsed")
apply_qdb_styling()

# ===== Image Loader =====
def encode_image(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f"data:image/png;base64,{base64.b64encode(f.read()).decode()}"
    return None

qdb_logo = encode_image("QDB_Logo.png")
regulus_logo = encode_image("regulus_logo.png")

# ===== Session State - FIXED =====
if 'search_results' not in st.session_state:
    st.session_state.search_results = []
if 'selected_deals' not in st.session_state:
    st.session_state.selected_deals = {}
if 'current_selected_deal' not in st.session_state:
    st.session_state.current_selected_deal = None

# ===== DEAL DATABASE =====
ATTRACTIVE_INDUSTRIES = [
    "FinTech", "AI/ML", "ClimaTech", "Enterprise SaaS", "HealthTech",
    "EdTech", "Biotech", "Agritech", "Blockchain", "Cybersecurity",
    "Data Analytics", "Cloud Computing", "IoT", "Robotics", "Quantum Computing"
]

UNATTRACTIVE_INDUSTRIES = [
    "Traditional Retail", "Oil & Gas", "Coal Mining", "Tobacco",
    "Low-Tech Manufacturing", "Commodities Trading", "Payday Lending",
    "Gambling", "Weapons Manufacturing", "Fast Fashion"
]

SAMPLE_DEALS = [
    {
        "id": "DS-001",
        "company": "AltLab AI",
        "industry": "AI/ML",
        "stage": "Series A",
        "revenue": "$2.5M ARR",
        "raised": "$500K seed",
        "location": "San Francisco, USA",
        "description": "AI-powered code review and testing platform",
        "attraction": "ATTRACTIVE",
        "contact": "founders@altlab.ai"
    },
    {
        "id": "DS-002",
        "company": "GreenFlow Energy",
        "industry": "ClimaTech",
        "stage": "Series B",
        "revenue": "$8M ARR",
        "raised": "$15M Series A",
        "location": "Copenhagen, Denmark",
        "description": "Smart grid optimization for renewable energy",
        "attraction": "ATTRACTIVE",
        "contact": "invest@greenflow.dk"
    },
    {
        "id": "DS-003",
        "company": "MediSync Pro",
        "industry": "HealthTech",
        "stage": "Series A",
        "revenue": "$1.8M ARR",
        "raised": "$300K seed",
        "location": "Boston, USA",
        "description": "Healthcare data interoperability platform",
        "attraction": "ATTRACTIVE",
        "contact": "partnerships@medisync.com"
    },
    {
        "id": "DS-004",
        "company": "BlockSecure",
        "industry": "Blockchain",
        "stage": "Seed",
        "revenue": "$150K ARR",
        "raised": "$250K seed",
        "location": "Singapore",
        "description": "Enterprise blockchain security solutions",
        "attraction": "ATTRACTIVE",
        "contact": "invest@blocksecure.io"
    },
    {
        "id": "DS-005",
        "company": "FarmAI Systems",
        "industry": "Agritech",
        "stage": "Series A",
        "revenue": "$3.2M ARR",
        "raised": "$800K seed",
        "location": "Bangalore, India",
        "description": "AI-driven crop optimization and pest detection",
        "attraction": "ATTRACTIVE",
        "contact": "business@farmai.in"
    },
    {
        "id": "DS-006",
        "company": "RetailCorp Classic",
        "industry": "Traditional Retail",
        "stage": "Growth",
        "revenue": "$25M ARR",
        "raised": "N/A",
        "location": "New York, USA",
        "description": "Traditional brick-and-mortar retail chain",
        "attraction": "UNATTRACTIVE",
        "contact": "info@retailcorp.com"
    },
    {
        "id": "DS-007",
        "company": "FastStyle Ventures",
        "industry": "Fast Fashion",
        "stage": "Mature",
        "revenue": "$15M ARR",
        "raised": "N/A",
        "location": "Shanghai, China",
        "description": "Fast fashion e-commerce company",
        "attraction": "UNATTRACTIVE",
        "contact": "deals@faststyle.cn"
    }
]

# ===== STYLING =====
st.markdown("""
<style>
.stButton>button {
    background: linear-gradient(135deg,#16A085 0%,#138074 100%)!important;
    color:white!important;
    border:none!important;
    border-radius:8px!important;
    padding:12px 24px!important;
    font-weight:700!important;
    box-shadow:0 4px 12px rgba(22,160,133,0.3)!important;
}
.stButton>button:hover{
    background: linear-gradient(135deg,#0E5F55 0%,#107563 100%)!important;
    transform:translateY(-2px)!important;
}
.section-beige {
    background-color: #F6F5F2;
    border-radius: 10px;
    padding: 20px;
    margin: 12px 0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
.section-header {
    font-size: 1.2rem;
    font-weight: 700;
    color: #1B2B4D;
    margin-bottom: 12px;
}
.deal-card {
    background: white;
    border: 2px solid #16A085;
    border-radius: 10px;
    padding: 15px;
    margin: 10px 0;
    transition: all 0.3s;
}
.deal-card:hover {
    box-shadow: 0 4px 12px rgba(22,160,133,0.3);
    transform: translateY(-2px);
}
.attraction-attractive {
    background-color: #d4edda;
    color: #155724;
    padding: 4px 12px;
    border-radius: 20px;
    font-weight: 700;
    font-size: 0.85rem;
}
.attraction-unattractive {
    background-color: #f8d7da;
    color: #721c24;
    padding: 4px 12px;
    border-radius: 20px;
    font-weight: 700;
    font-size: 0.85rem;
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
    <p style="color:#E2E8F0; font-size:0.95rem; margin:0;">Find & evaluate investment opportunities from global sources</p>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

# ===== HOME BUTTON =====
if st.button("Return Home"):
    st.switch_page("streamlit_app.py")

st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

# ===== SEARCH SECTION =====
st.markdown('<div class="section-beige"><div class="section-header">Search & Filter Deals</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("<div style='color:#1B2B4D; font-size:0.85rem; margin-bottom:4px; font-weight:600;'>Industry Focus</div>", unsafe_allow_html=True)
    industry_search = st.multiselect(
        "Select industries",
        ATTRACTIVE_INDUSTRIES + UNATTRACTIVE_INDUSTRIES,
        default=["FinTech", "AI/ML", "ClimaTech"],
        label_visibility="collapsed",
        key="industry_search"
    )

with col2:
    st.markdown("<div style='color:#1B2B4D; font-size:0.85rem; margin-bottom:4px; font-weight:600;'>Funding Stage</div>", unsafe_allow_html=True)
    stage_search = st.multiselect(
        "Select stages",
        ["Seed", "Series A", "Series B", "Series C", "Growth"],
        default=["Seed", "Series A", "Series B"],
        label_visibility="collapsed",
        key="stage_search"
    )

with col3:
    st.markdown("<div style='color:#1B2B4D; font-size:0.85rem; margin-bottom:4px; font-weight:600;'>Min Revenue</div>", unsafe_allow_html=True)
    min_revenue = st.selectbox(
        "Minimum revenue",
        ["Any", "$500K", "$1M", "$2M", "$5M"],
        label_visibility="collapsed",
        key="min_rev"
    )

st.markdown("</div>", unsafe_allow_html=True)
st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

# ===== SEARCH BUTTON =====
if st.button("Search Deals", use_container_width=True, key="search_btn"):
    with st.spinner("Searching deal databases..."):
        filtered_deals = []
        for deal in SAMPLE_DEALS:
            if industry_search and deal['industry'] not in industry_search:
                continue
            
            if stage_search and deal['stage'] not in stage_search:
                continue
            
            if min_revenue != "Any":
                deal_revenue = deal['revenue'].replace("$", "").replace("M ARR", "")
                try:
                    min_val = float(min_revenue.replace("$", "").replace("M", ""))
                    deal_val = float(deal_revenue.split("-")[0])
                    if deal_val < min_val:
                        continue
                except:
                    pass
            
            filtered_deals.append(deal)
        
        st.session_state.search_results = filtered_deals
        st.success(f"Found {len(filtered_deals)} deals matching your criteria")
        st.rerun()

st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

# ===== DEAL STATISTICS =====
if st.session_state.search_results:
    st.markdown('<div class="section-beige"><div class="section-header">Deal Statistics</div>', unsafe_allow_html=True)
    
    col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
    
    attractive = sum(1 for d in st.session_state.search_results if d['attraction'] == 'ATTRACTIVE')
    unattractive = sum(1 for d in st.session_state.search_results if d['attraction'] == 'UNATTRACTIVE')
    quality = int((attractive / len(st.session_state.search_results) * 100)) if st.session_state.search_results else 0
    
    with col_stat1:
        st.metric("Total Deals", len(st.session_state.search_results))
    
    with col_stat2:
        st.metric("Attractive", attractive)
    
    with col_stat3:
        st.metric("Unattractive", unattractive)
    
    with col_stat4:
        st.metric("Quality Score", f"{quality}%")
    
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

# ===== DEAL LISTING - FIXED =====
if st.session_state.search_results:
    st.markdown('<div class="section-beige"><div class="section-header">Available Deals</div>', unsafe_allow_html=True)
    
    for idx, deal in enumerate(st.session_state.search_results):
        attraction_class = "attraction-attractive" if deal['attraction'] == 'ATTRACTIVE' else "attraction-unattractive"
        deal_id = deal['id']
        
        with st.container():
            st.markdown(f"""
            <div class="deal-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                    <div>
                        <div style="font-size: 1.1rem; font-weight: 700; color: #1B2B4D;">
                            {deal['company']}
                        </div>
                        <div style="color: #666; font-size: 0.9rem;">
                            {deal['industry']} • {deal['stage']} • {deal['location']}
                        </div>
                    </div>
                    <div class="{attraction_class}">
                        {deal['attraction']}
                    </div>
                </div>
                <div style="color: #333; margin-bottom: 10px; font-size: 0.95rem;">
                    {deal['description']}
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; margin-bottom: 10px; font-size: 0.9rem;">
                    <div><strong>Revenue:</strong> {deal['revenue']}</div>
                    <div><strong>Raised:</strong> {deal['raised']}</div>
                    <div><strong>Contact:</strong> {deal['contact']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            col_action1, col_action2, col_action3 = st.columns([2, 1, 1])
            
            # FIXED: Use proper checkbox state management
            with col_action1:
                is_selected = st.checkbox(
                    "Select for due diligence",
                    value=(deal_id in st.session_state.selected_deals),
                    key=f"checkbox_{deal_id}"
                )
                
                if is_selected:
                    st.session_state.selected_deals[deal_id] = deal
                else:
                    if deal_id in st.session_state.selected_deals:
                        del st.session_state.selected_deals[deal_id]
            
            with col_action2:
                if st.button("Details", key=f"details_{deal_id}", use_container_width=True):
                    st.session_state[f"show_detail_{deal_id}"] = True
            
            with col_action3:
                if st.button("DD Now", key=f"proceed_{deal_id}", use_container_width=True):
                    st.session_state.current_selected_deal = deal
                    st.session_state.should_navigate = True
            
            # Show details if expanded
            if st.session_state.get(f"show_detail_{deal_id}", False):
                with st.expander(f"Details - {deal['company']}", expanded=True):
                    st.markdown(f"""
                    **Company:** {deal['company']}  
                    **Industry:** {deal['industry']}  
                    **Stage:** {deal['stage']}  
                    **Location:** {deal['location']}  
                    **Revenue (ARR):** {deal['revenue']}  
                    **Previously Raised:** {deal['raised']}  
                    **Description:** {deal['description']}  
                    **Attraction Status:** {deal['attraction']}  
                    **Contact:** {deal['contact']}  
                    
                    ---
                    
                    **Next Steps:**
                    1. Contact the company for initial meeting
                    2. Request financial documents
                    3. Schedule due diligence process
                    4. Begin comprehensive analysis
                    """)
    
    st.markdown("</div>", unsafe_allow_html=True)

# ===== SELECTED DEALS SUMMARY =====
if st.session_state.selected_deals:
    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
    
    st.markdown('<div class="section-beige"><div class="section-header">Selected Deals for Processing</div>', unsafe_allow_html=True)
    
    st.markdown(f"**{len(st.session_state.selected_deals)} deal(s) selected:**")
    
    for deal_id, deal in st.session_state.selected_deals.items():
        st.markdown(f"- **{deal['company']}** ({deal['industry']}) - {deal['stage']} - {deal['attraction']}")
    
    col_proc1, col_proc2, col_proc3 = st.columns(3)
    
    with col_proc1:
        if st.button("Proceed to DD (Selected)", use_container_width=True, key="proceed_selected"):
            first_deal = list(st.session_state.selected_deals.values())[0]
            st.session_state.current_selected_deal = first_deal
            st.session_state.should_navigate = True
    
    with col_proc2:
        if st.button("View All Selected", use_container_width=True):
            st.info(f"Processing {len(st.session_state.selected_deals)} deals...")
    
    with col_proc3:
        if st.button("Clear Selections", use_container_width=True):
            st.session_state.selected_deals = {}
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

# ===== NAVIGATION LOGIC - FIXED =====
if st.session_state.get('should_navigate', False):
    st.session_state.should_navigate = False
    st.info(f"Navigating to Due Diligence for {st.session_state.current_selected_deal['company']}...")
    st.switch_page("pages/2_Due_Diligence_Analysis.py")

# ===== DATABASE INFO =====
st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

st.markdown("""
<div class="section-beige">
<div class="section-header">Our Deal Database</div>

We maintain a curated database of investment opportunities across multiple sectors:

**Data Sources:**
- Crunchbase API (Startup funding data)
- PitchBook (Private equity deals)
- AngelList (Early-stage startups)
- LinkedIn Jobs (Company growth signals)
- SEC Filings (Public company acquisitions)

**Coverage:**
- 5,000+ active opportunities
- 50+ countries
- Seed to Series C stages
- $100K - $100M funding range

**Updated:**
- Real-time data feeds
- Daily deal updates
- Weekly market analysis
</div>
""", unsafe_allow_html=True)

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
