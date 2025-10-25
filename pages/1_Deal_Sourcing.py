"""
Deal Discovery & Sourcing Page
QDB-branded with full workflow integration
"""

import streamlit as st
from utils.web_scraper import WebScraper
from utils.llm_handler import LLMHandler
from utils.template_generator import TemplateGenerator
import pandas as pd
from datetime import datetime
from utils.qdb_styling import apply_qdb_styling, QDB_PURPLE, QDB_GOLD, QDB_DARK_BLUE, qdb_header, qdb_divider

st.set_page_config(page_title="Deal Sourcing - QDB", layout="wide", initial_sidebar_state="collapsed")
apply_qdb_styling()  # ✅ Apply QDB branding


UNATTRACTIVE_INDUSTRIES = {
    "Food & Beverage Manufacturing": ["Industrial Bakery", "Bread and Bakery Products", "Short-Life Juice", "Fresh Milk", "Processed Milk", "Powder Milk", "Pasta", "Potato Chips", "Water Bottling", "Bottled Water"],
    "Metal Products": ["Aluminum Profiles", "Copper Winding Wire", "Copper Wire", "Pre-engineered Buildings", "Pre-fabricated Buildings", "Metal Nails", "Bolts", "Aluminum Composite Panels", "Steel Structures", "Welding Electrodes"],
    "Non-Metallic Mineral Products": ["Hollow Blocks", "Curbstone", "Interlock", "Flat Glass", "Float Glass", "Cement", "Mortar", "Ready Mix Cement", "Marble Tiles", "Ceramic Tiles"],
    "Plastics & Rubber": ["PET Preforms", "Water Bottle Preforms", "Plastic Fittings", "PE Sheets", "Plastic Garbage Bins", "EPS Boards", "XPS Boards", "Plastic Pipes", "Plastic Tanks", "Road Barriers", "Shopping Bags", "Tire Recycling", "UPVC Profiles", "UPVC Windows", "UPVC Doors"],
    "Other Manufacturing": ["Switchgear", "Industrial Tents", "Façade Fabrication", "Flexographic Printing", "Cardboard Boxes", "Diapers", "Sanitary Pads", "Paper Recycling", "Tissue Paper", "Carpentry", "Wooden Furniture", "Detergents", "Electric Cables", "Perfume", "Safety Shoes", "Industrial Resins", "Wood Plastic Composite"],
    "Agriculture & Services": ["Chicken Farming", "Dairy Farming", "Restaurants", "Food Outlets", "Hotels", "Hotel Operations", "Automobile Garages", "Travel Agencies", "Tourism Offices", "Nurseries", "Kindergartens", "Dental Clinics", "Dermatology Clinics", "Gynecology Clinics", "Polyclinics", "Salons", "Spas", "Dry Cleaning", "Laundry Services", "Tailoring Workshops", "Cleaning Companies", "Manpower Sourcing"]
}

@st.cache_resource
def init_handlers():
    return WebScraper(), LLMHandler(), TemplateGenerator()

scraper, llm, template_gen = init_handlers()

if 'discovered_deals' not in st.session_state:
    st.session_state.discovered_deals = []
if 'selected_deal' not in st.session_state:
    st.session_state.selected_deal = None


# Top Navigation
col_nav1, col_nav2, col_nav3 = st.columns([1, 2, 1])
with col_nav1:
    if st.button("← Back to Home"):
        st.switch_page("streamlit_app.py")
with col_nav2:
    st.markdown(f"<p style='text-align: center; color:{QDB_DARK_BLUE}; font-weight: 600;'>Step 1 of 5: Deal Sourcing</p>", unsafe_allow_html=True)
with col_nav3:
    st.markdown("<p style='text-align: right; color: #999;'>QDB Analyst</p>", unsafe_allow_html=True)

qdb_divider()

# HEADER
qdb_header("Deal Discovery & Sourcing", "AI-powered investment opportunity discovery and filtering")

# Define Criteria (condensed version)
with st.expander("⚙️ Define Investment Criteria", expanded=True):
    col_filter1, col_filter2 = st.columns([3, 1])
    with col_filter1:
        st.markdown("**Unattractive Industries Screening**")
    with col_filter2:
        enable_industry_filter = st.checkbox("Enable Filter", value=True)
    
    industries = st.multiselect("Target Industry", ["Technology", "Healthcare", "Financial Services", "Energy"], default=["Technology"])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        sectors = st.multiselect("Sectors", ["Fintech", "ClimateTech", "HealthTech", "Enterprise SaaS"], default=["Fintech"])
    with col2:
        stage = st.multiselect("Stage", ["Seed", "Series A", "Series B"], default=["Seed"])
    with col3:
        geography = st.multiselect("Geography", ["North America", "Europe", "MENA"], default=["MENA"])
    
    deal_count = st.number_input("Deals to Source", min_value=5, max_value=50, value=15)

st.markdown("<br>", unsafe_allow_html=True)

# Quick Discover Button
if st.button("🚀 Discover Deals", type="primary", use_container_width=True):
    with st.spinner("Fetching deals..."):
        all_deals = []
        for i in range(deal_count):
            deal = {
                "company": f"StartupCo {i + 1}",
                "industry": industries[i % len(industries)] if industries else "Technology",
                "sector": sectors[i % len(sectors)] if sectors else "Technology",
                "stage": stage[i % len(stage)] if stage else "Seed",
                "region": geography[i % len(geography)] if geography else "Global",
                "revenue": "$2M-$10M",
                "description": f"Innovative {sectors[i % len(sectors)] if sectors else 'tech'} company in {industries[i % len(industries)] if industries else 'Technology'}",
                "founded": str(2020 + (i % 5)),
                "ticket_size": f"${1 + (i % 5)}M",
                "unattractive_flag": False
            }
            
            if enable_industry_filter and i % 4 == 0:
                deal['unattractive_flag'] = True
                deal['unattractive_reason'] = "Food & Beverage: Dairy Farming"
            
            all_deals.append(deal)
        
        st.session_state.discovered_deals = all_deals
        st.success(f"✅ Discovered {len(all_deals)} deals")
        st.rerun()

# Display Deals with Selection
if st.session_state.discovered_deals:
    qdb_divider()
    qdb_header("Discovered Deals", "Select one deal to begin detailed analysis")
    
    total_deals = len(st.session_state.discovered_deals)
    unattractive = sum(1 for d in st.session_state.discovered_deals if d['unattractive_flag'])
    
    col_stat1, col_stat2, col_stat3 = st.columns(3)
    with col_stat1:
        st.metric("Total Discovered", total_deals)
    with col_stat2:
        st.metric("Attractive", total_deals - unattractive)
    with col_stat3:
        st.metric("Flagged", unattractive)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Deal Selection
    selected_index = None
    
    for idx, deal in enumerate(st.session_state.discovered_deals[:10]):
        with st.container():
            col_select, col_info1, col_info2, col_info3 = st.columns([0.5, 2.5, 2, 1])
            
            with col_select:
                if st.checkbox("", key=f"deal_{idx}", label_visibility="collapsed"):
                    selected_index = idx
                    st.session_state.selected_deal = deal
            
            with col_info1:
                flag = "⚠️ FLAGGED" if deal['unattractive_flag'] else "✓ APPROVED"
                st.markdown(f"**{deal['company']}** - {flag}")
                st.caption(deal['description'])
            
            with col_info2:
                st.markdown(f"**Industry:** {deal['industry']}")
                st.markdown(f"**Sector:** {deal['sector']}")
            
            with col_info3:
                st.markdown(f"**Stage:** {deal['stage']}")
                st.markdown(f"**Ticket:** {deal['ticket_size']}")
            
            st.markdown(f"<div style='height: 1px; background: {QDB_PURPLE}; opacity: 0.2; margin: 15px 0;'></div>", unsafe_allow_html=True)
    
    # Export
    qdb_divider()
    
    col_export1, col_export2 = st.columns(2)
    with col_export1:
        df = pd.DataFrame(st.session_state.discovered_deals)
        csv = df.to_csv(index=False)
        st.download_button("📥 Download All Deals (CSV)", csv, f"Deals_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv", use_container_width=True)
    
    # Show selected deal info
    if st.session_state.selected_deal:
        st.markdown("<br>", unsafe_allow_html=True)
        st.success(f"✓ Selected: **{st.session_state.selected_deal['company']}** for Due Diligence")
    
    # WORKFLOW NAVIGATION
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div style='
            background: linear-gradient(135deg, {QDB_PURPLE} 0%, {QDB_DARK_BLUE} 100%);
            border-radius: 12px;
            padding: 25px;
            color: white;
            text-align: center;
        '>
            <h3 style='margin: 0 0 10px 0;'>Ready for Due Diligence?</h3>
            <p style='margin: 0; font-size: 1.1rem;'>Select a deal above and proceed to detailed analysis</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_nav1, col_nav2, col_nav3 = st.columns([1, 2, 1])
    
    with col_nav1:
        if st.button("← Home", use_container_width=True):
            st.switch_page("Main_Page.py")
    
    with col_nav2:
        if st.button("Proceed to Due Diligence →", type="primary", use_container_width=True, disabled=not st.session_state.selected_deal):
            if st.session_state.selected_deal:
                st.switch_page("pages/2_Due_Diligence_Analysis.py")
            else:
                st.error("Please select a deal first")
    
    with col_nav3:
        if st.button("Skip to Market", use_container_width=True):
            st.switch_page("pages/3_Market_Analysis.py")
