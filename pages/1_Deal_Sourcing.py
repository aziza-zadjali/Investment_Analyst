"""
Deal Sourcing - Enterprise Grade
FEATURES: Web scraping, advanced filtering, scoring, ranking
ARCHITECTURE: Follows Crunchbase/PitchBook patterns
"""
import streamlit as st
import base64
import os
from datetime import datetime
from utils.qdb_styling import apply_qdb_styling
from utils.deal_scraper import DealScraper
from utils.deal_ranker import DealRanker

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

# ===== Initialize =====
@st.cache_resource
def init_services():
    return DealScraper(), DealRanker()

scraper, ranker = init_services()

# ===== Session State =====
if 'search_results' not in st.session_state:
    st.session_state.search_results = []
if 'selected_deals' not in st.session_state:
    st.session_state.selected_deals = {}
if 'current_selected_deal' not in st.session_state:
    st.session_state.current_selected_deal = None
if 'should_navigate' not in st.session_state:
    st.session_state.should_navigate = False

# ===== Industry Lists =====
ATTRACTIVE = ["FinTech", "AI/ML", "ClimaTech", "Enterprise SaaS", "HealthTech", "EdTech", "Biotech", "Agritech", "Blockchain", "Cybersecurity", "Data Analytics", "Cloud Computing", "IoT", "Robotics", "Quantum Computing"]
UNATTRACTIVE = ["Traditional Retail", "Oil & Gas", "Coal Mining", "Tobacco", "Low-Tech", "Commodities", "Payday Lending"]

# ===== Styling =====
st.markdown("""
<style>
.stButton>button { background: linear-gradient(135deg,#16A085 0%,#138074 100%)!important; color:white!important; border-radius:8px!important; padding:12px 24px!important; font-weight:700!important; }
.section-beige { background-color: #F6F5F2; border-radius: 10px; padding: 20px; margin: 12px 0; }
.section-header { font-size: 1.2rem; font-weight: 700; color: #1B2B4D; margin-bottom: 12px; }
.deal-card { background: white; border: 2px solid #16A085; border-radius: 10px; padding: 15px; margin: 10px 0; }
.score-high { background: #d4edda; color: #155724; padding: 6px 12px; border-radius: 20px; font-weight: 700; }
.score-med { background: #fff3cd; color: #856404; padding: 6px 12px; border-radius: 20px; font-weight: 700; }
.score-low { background: #f8d7da; color: #721c24; padding: 6px 12px; border-radius: 20px; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

# ===== HERO HEADER =====
st.markdown(f"""
<div style="background: linear-gradient(135deg,#1B2B4D 0%,#2C3E5E 100%);color:white;text-align:center;margin:0 -3rem;padding:40px 20px 50px;width:calc(100% + 6rem);border-bottom:3px solid #16A085;">
  <div style="position:absolute;top:15px;left:35px;">{'<img src="'+qdb_logo+'" style="max-height:55px;">' if qdb_logo else ''}</div>
  <div style="position:absolute;top:15px;right:35px;">{'<img src="'+regulus_logo+'" style="max-height:55px;">' if regulus_logo else ''}</div>
  <h1 style="font-size:2rem;font-weight:800;margin-bottom:6px;">Deal Sourcing</h1>
  <p style="color:#E2E8F0;font-size:0.95rem;margin:0;">AI-powered deal discovery from 50+ global sources</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

if st.button("Return Home"):
    st.switch_page("streamlit_app.py")

st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

# ===== SEARCH SECTION =====
st.markdown('<div class="section-beige"><div class="section-header">Advanced Deal Search</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("<div style='color:#1B2B4D; font-size:0.85rem; margin-bottom:4px; font-weight:600;'>Industries</div>", unsafe_allow_html=True)
    industries = st.multiselect("Select", ATTRACTIVE + UNATTRACTIVE, default=["AI/ML", "FinTech", "ClimaTech"], label_visibility="collapsed", key="ind")

with col2:
    st.markdown("<div style='color:#1B2B4D; font-size:0.85rem; margin-bottom:4px; font-weight:600;'>Funding Stage</div>", unsafe_allow_html=True)
    stages = st.multiselect("Select", ["Seed", "Series A", "Series B", "Series C", "Growth"], default=["Seed", "Series A"], label_visibility="collapsed", key="stage")

with col3:
    st.markdown("<div style='color:#1B2B4D; font-size:0.85rem; margin-bottom:4px; font-weight:600;'>Min Score</div>", unsafe_allow_html=True)
    min_score = st.select_slider("Minimum Deal Score", 0, 10, 7, key="score")

with col4:
    st.markdown("<div style='color:#1B2B4D; font-size:0.85rem; margin-bottom:4px; font-weight:600;'>Data Source</div>", unsafe_allow_html=True)
    sources = st.multiselect("Sources", ["AngelList", "Crunchbase", "LinkedIn", "TechCrunch", "SEC"], default=["AngelList", "Crunchbase"], label_visibility="collapsed", key="src")

st.markdown("</div>", unsafe_allow_html=True)
st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

# ===== SEARCH BUTTON =====
if st.button("Search Deals (Web Scraping)", use_container_width=True):
    with st.spinner("Scraping 50+ data sources..."):
        filters = {
            'industries': industries,
            'stages': stages,
            'min_score': min_score,
            'sources': sources
        }
        
        # Scrape all sources
        raw_deals = scraper.scrape_all_sources(filters)
        
        # Rank and score
        ranked_deals = ranker.rank_deals(raw_deals)
        
        st.session_state.search_results = ranked_deals
        st.success(f"Found {len(ranked_deals)} qualified deals from {len(set(d['source'] for d in ranked_deals))} sources")
        st.rerun()

st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

# ===== STATISTICS =====
if st.session_state.search_results:
    st.markdown('<div class="section-beige"><div class="section-header">Deal Intelligence Dashboard</div>', unsafe_allow_html=True)
    
    col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
    
    deals = st.session_state.search_results
    high_score = sum(1 for d in deals if d.get('composite_score', 0) >= 8)
    avg_score = sum(d.get('composite_score', 0) for d in deals) / len(deals) if deals else 0
    sources_used = len(set(d['source'] for d in deals))
    
    with col_stat1:
        st.metric("Total Deals", len(deals))
    with col_stat2:
        st.metric("High Quality", high_score)
    with col_stat3:
        st.metric("Avg Score", f"{avg_score:.1f}/10")
    with col_stat4:
        st.metric("Sources", sources_used)
    
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

# ===== DEAL LISTING =====
if st.session_state.search_results:
    st.markdown('<div class="section-beige"><div class="section-header">Ranked Deals</div>', unsafe_allow_html=True)
    
    for deal in st.session_state.search_results:
        score = deal.get('composite_score', 0)
        score_class = "score-high" if score >= 8 else "score-med" if score >= 7 else "score-low"
        
        st.markdown(f"""
        <div class="deal-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <div>
                    <div style="font-size: 1.1rem; font-weight: 700; color: #1B2B4D;">#{deal['rank']} {deal['company']}</div>
                    <div style="color: #666; font-size: 0.9rem;">{deal['industry']} • {deal['stage']} • {deal['location']}</div>
                </div>
                <div class="{score_class}"><strong>{score}/10</strong> {ranker.get_recommendation(score)}</div>
            </div>
            <div style="color: #333; margin-bottom: 10px;">{deal['description']}</div>
            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 10px; font-size: 0.85rem;">
                <div><strong>Amount:</strong> {deal.get('funding_amount', 'N/A')}</div>
                <div><strong>Source:</strong> {deal['source']}</div>
                <div><strong>Growth:</strong> {deal.get('growth', 'N/A')}</div>
                <div><strong>Website:</strong> {deal.get('website', 'N/A')}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col_a1, col_a2, col_a3 = st.columns([2, 1, 1])
        
        with col_a1:
            if st.checkbox("Select", value=(deal['id'] in st.session_state.selected_deals), key=f"cb_{deal['id']}"):
                st.session_state.selected_deals[deal['id']] = deal
            else:
                if deal['id'] in st.session_state.selected_deals:
                    del st.session_state.selected_deals[deal['id']]
        
        with col_a2:
            if st.button("Details", key=f"det_{deal['id']}", use_container_width=True):
                st.session_state[f"detail_{deal['id']}"] = True
        
        with col_a3:
            if st.button("DD Now", key=f"proc_{deal['id']}", use_container_width=True):
                st.session_state.current_selected_deal = deal
                st.session_state.should_navigate = True
        
        if st.session_state.get(f"detail_{deal['id']}", False):
            with st.expander(f"Details - {deal['company']}", expanded=True):
                st.json(deal)
    
    st.markdown("</div>", unsafe_allow_html=True)

# ===== SELECTED DEALS =====
if st.session_state.selected_deals:
    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
    st.markdown('<div class="section-beige"><div class="section-header">Selected Deals</div>', unsafe_allow_html=True)
    
    for did, deal in st.session_state.selected_deals.items():
        st.write(f"✓ {deal['company']} ({deal['industry']}) - Score: {deal.get('composite_score', 0)}")
    
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        if st.button("Proceed to DD", use_container_width=True):
            st.session_state.current_selected_deal = list(st.session_state.selected_deals.values())[0]
            st.session_state.should_navigate = True
    with col_p2:
        if st.button("Clear", use_container_width=True):
            st.session_state.selected_deals = {}
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

# ===== NAVIGATION =====
if st.session_state.should_navigate:
    st.session_state.should_navigate = False
    st.info(f"Proceeding with {st.session_state.current_selected_deal['company']}...")
    st.switch_page("pages/2_Due_Diligence_Analysis.py")

# ===== FOOTER =====
st.markdown(f"""
<div style="background-color:#1B2B4D;color:#E2E8F0;padding:28px 40px;margin:40px -3rem -2rem;width:calc(100% + 6rem);">
  <p style="text-align:center;margin:0;">Powered by Regulus AI | Data from 50+ Global Sources</p>
</div>
""", unsafe_allow_html=True)
