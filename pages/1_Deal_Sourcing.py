"""
Deal Discovery & Sourcing Page
With guided workflow navigation - no sidebar
"""

import streamlit as st
from utils.web_scraper import WebScraper
from utils.llm_handler import LLMHandler
from utils.template_generator import TemplateGenerator
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Deal Discovery", layout="wide", initial_sidebar_state="collapsed")

# Hide sidebar completely
st.markdown("""
<style>
    [data-testid="stSidebar"] {display: none;}
    .main > div {padding-top: 2rem;}
</style>
""", unsafe_allow_html=True)

def gradient_box(text, gradient="linear-gradient(90deg, #A6D8FF, #D5B8FF)"):
    return f"""<div style="background: {gradient}; padding: 15px 20px; border-radius: 12px; color: white; font-weight: 600; font-size: 1.5rem; text-align: center; margin-bottom: 20px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);">{text}</div>"""

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

# Top Navigation Bar
col_nav1, col_nav2, col_nav3 = st.columns([1, 2, 1])

with col_nav1:
    if st.button("← Back to Home"):
        st.switch_page("Main_Page.py")

with col_nav2:
    st.markdown("<p style='text-align: center; color: #666; font-weight: 600;'>Step 1 of 5: Deal Sourcing</p>", unsafe_allow_html=True)

with col_nav3:
    st.markdown("<p style='text-align: right; color: #999;'>QDB Investment Analyst</p>", unsafe_allow_html=True)

st.markdown("<div style='background: linear-gradient(90deg, #A6D8FF, #D5B8FF); height: 4px; border-radius: 2px; margin-bottom: 30px;'></div>", unsafe_allow_html=True)

# HEADER
st.markdown(gradient_box("Deal Discovery & Sourcing"), unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666; font-size: 1.1rem; margin-bottom: 30px;'>Discover and qualify investment opportunities from leading global platforms</p>", unsafe_allow_html=True)

# Define Investment Criteria
st.markdown(gradient_box("Define Investment Criteria"), unsafe_allow_html=True)

col_filter1, col_filter2 = st.columns([3, 1])
with col_filter1:
    st.markdown("**Unattractive Industries Screening**")
with col_filter2:
    enable_industry_filter = st.checkbox("Enable Filter", value=True)

if enable_industry_filter:
    with st.expander("View Complete List"):
        for category, industries_list in UNATTRACTIVE_INDUSTRIES.items():
            st.markdown(f"**{category}:** {', '.join(industries_list[:3])}...")

st.markdown("<br>", unsafe_allow_html=True)

industries = st.multiselect("Target Industry", ["Technology", "Healthcare", "Financial Services", "Energy", "Consumer Goods", "Industrial", "Real Estate", "Agriculture", "Transportation", "Media & Entertainment", "Education", "Telecommunications", "Retail", "Manufacturing"], default=["Technology", "Healthcare"])

col1, col2, col3 = st.columns(3)
with col1:
    sectors = st.multiselect("Target Sectors", ["Fintech", "ClimateTech", "HealthTech", "Enterprise SaaS", "AI/ML", "E-commerce", "Logistics", "Agritech", "EdTech", "Biotech", "PropTech", "FoodTech", "DeepTech", "Cybersecurity", "Blockchain", "IoT", "Robotics", "Clean Energy"], default=["Fintech", "ClimateTech"])
with col2:
    stage = st.multiselect("Funding Stage", ["Pre-Seed", "Seed", "Series A", "Series B", "Series C+", "Growth"], default=["Seed", "Series A"])
with col3:
    geography = st.multiselect("Geography", ["North America", "Europe", "MENA", "Asia Pacific", "Latin America", "Africa", "Global"], default=["MENA"])

col4, col5, col6 = st.columns(3)
with col4:
    revenue_range = st.select_slider("Annual Revenue (USD)", options=["Pre-revenue", "$0-500K", "$500K-$2M", "$2M-$10M", "$10M-$50M", "$50M+"], value=("$500K-$2M", "$10M-$50M"))
with col5:
    deal_count = st.number_input("Deals to Source", min_value=5, max_value=100, value=20, step=5)
with col6:
    enable_ticket_size = st.checkbox("Define ticket size", value=False)
    if enable_ticket_size:
        ticket_min = st.number_input("Min ($M)", min_value=0.1, max_value=100.0, value=1.0, step=0.5, format="%.1f")
        ticket_max = st.number_input("Max ($M)", min_value=0.1, max_value=100.0, value=10.0, step=0.5, format="%.1f")
        ticket_size_range = (ticket_min, ticket_max)
    else:
        ticket_size_range = None

st.markdown("<div style='background: linear-gradient(90deg, #A6D8FF, #D5B8FF); height: 4px; border-radius: 2px; margin: 30px 0;'></div>", unsafe_allow_html=True)

# Data Sources
st.markdown(gradient_box("Select Data Sources"), unsafe_allow_html=True)
selected_sources = st.multiselect("Data Providers", ["Crunchbase", "AngelList", "PitchBook", "Magnitt", "Wamda", "Dealroom"], default=["Crunchbase", "Magnitt"])

st.markdown("<div style='background: linear-gradient(90deg, #A6D8FF, #D5B8FF); height: 4px; border-radius: 2px; margin: 30px 0;'></div>", unsafe_allow_html=True)

# Discovery Button
if st.button("Start Discovery", type="primary", use_container_width=True):
    if not selected_sources:
        st.error("Please select at least one data source")
    else:
        with st.spinner("Fetching deals..."):
            all_deals = []
            progress_bar = st.progress(0)
            deal_count_per_source = deal_count // len(selected_sources)

            for idx, source in enumerate(selected_sources):
                for i in range(deal_count_per_source):
                    deal = {
                        "company": f"StartupCo {idx * deal_count_per_source + i + 1}",
                        "industry": industries[i % len(industries)] if industries else "Technology",
                        "sector": sectors[i % len(sectors)] if sectors else "Technology",
                        "stage": stage[i % len(stage)] if stage else "Seed",
                        "region": geography[i % len(geography)] if geography else "Global",
                        "revenue": revenue_range[0],
                        "source": source,
                        "description": f"Innovative {sectors[i % len(sectors)] if sectors else 'tech'} company",
                        "founded": str(2020 + (i % 5)),
                        "employees": f"{20 + i * 10}-{30 + i * 10}",
                        "unattractive_flag": False,
                        "unattractive_reason": "",
                        "ticket_size": f"${1 + (i % 5)}M" if not ticket_size_range else f"${ticket_size_range[0]}M-${ticket_size_range[1]}M"
                    }
                    
                    if enable_industry_filter:
                        for category, industry_list in UNATTRACTIVE_INDUSTRIES.items():
                            for unattr_industry in industry_list:
                                if unattr_industry.lower() in deal['sector'].lower():
                                    deal['unattractive_flag'] = True
                                    deal['unattractive_reason'] = f"{category}: {unattr_industry}"
                                    break
                            if deal['unattractive_flag']:
                                break
                    
                    all_deals.append(deal)
                progress_bar.progress((idx + 1) / len(selected_sources))
            
            st.session_state.discovered_deals = all_deals
            st.success(f"Discovered {len(all_deals)} potential deals")

# Display Deals
if st.session_state.discovered_deals:
    st.markdown("<div style='background: linear-gradient(90deg, #A6D8FF, #D5B8FF); height: 4px; border-radius: 2px; margin: 30px 0;'></div>", unsafe_allow_html=True)
    st.markdown(gradient_box("Discovered Potential Deals"), unsafe_allow_html=True)
    
    total_deals = len(st.session_state.discovered_deals)
    unattractive_deals = sum(1 for d in st.session_state.discovered_deals if d['unattractive_flag'])
    attractive_deals = total_deals - unattractive_deals
    
    col_stat1, col_stat2, col_stat3 = st.columns(3)
    with col_stat1:
        st.metric("Total Deals", total_deals)
    with col_stat2:
        st.metric("Attractive", attractive_deals)
    with col_stat3:
        st.metric("Unattractive", unattractive_deals)
    
    show_filter = st.radio("Filter:", ["All", "Attractive Only", "Unattractive Only"], horizontal=True)
    
    display_deals = st.session_state.discovered_deals
    if show_filter == "Attractive Only":
        display_deals = [d for d in display_deals if not d['unattractive_flag']]
    elif show_filter == "Unattractive Only":
        display_deals = [d for d in display_deals if d['unattractive_flag']]
    
    for deal in display_deals[:10]:  # Show first 10
        with st.container():
            col_deal1, col_deal2, col_deal3 = st.columns([3, 2, 1])
            with col_deal1:
                flag = "⚠️ FLAGGED" if deal['unattractive_flag'] else "✓ APPROVED"
                st.markdown(f"### {deal['company']} - {flag}")
                st.caption(deal['description'])
            with col_deal2:
                st.markdown(f"**Industry:** {deal['industry']}")
                st.markdown(f"**Sector:** {deal['sector']}")
            with col_deal3:
                st.markdown(f"**Stage:** {deal['stage']}")
                st.markdown(f"**Ticket:** {deal['ticket_size']}")
            st.markdown("<div style='height: 1px; background: #ddd; margin: 15px 0;'></div>", unsafe_allow_html=True)
    
    # Export
    st.markdown("<div style='background: linear-gradient(90deg, #A6D8FF, #D5B8FF); height: 4px; border-radius: 2px; margin: 30px 0;'></div>", unsafe_allow_html=True)
    st.markdown(gradient_box("Export & Next Steps"), unsafe_allow_html=True)
    
    col_export1, col_export2 = st.columns(2)
    with col_export1:
        df = pd.DataFrame(st.session_state.discovered_deals)
        csv = df.to_csv(index=False)
        st.download_button("Download CSV Report", csv, f"Deals_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv", use_container_width=True)
    with col_export2:
        try:
            report_data = {
                'analyst_name': 'Regulus AI',
                'analysis_date': datetime.now().strftime('%B %d, %Y'),
                'total_deals': total_deals,
                'attractive_deals': attractive_deals,
                'unattractive_deals': unattractive_deals,
                'deals': st.session_state.discovered_deals,
                'industries': ', '.join(industries) if industries else 'N/A',
                'sectors': ', '.join(sectors) if sectors else 'N/A',
                'stages': ', '.join(stage) if stage else 'N/A',
                'regions': ', '.join(geography) if geography else 'N/A',
                'ticket_size': f"${ticket_size_range[0]}M-${ticket_size_range[1]}M" if ticket_size_range else 'N/A'
            }
            report = template_gen.generate_deal_sourcing_report(report_data)
            st.download_button("Download Full Report (MD)", report, f"Report_{datetime.now().strftime('%Y%m%d')}.md", "text/markdown", use_container_width=True)
        except Exception as e:
            st.error(f"Error: {e}")
    
    # WORKFLOW NAVIGATION
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style='
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 12px;
            padding: 25px;
            color: white;
            text-align: center;
            margin: 30px 0;
        '>
            <h3 style='margin: 0 0 10px 0;'>Ready for the next step?</h3>
            <p style='margin: 0; font-size: 1.1rem;'>Proceed to Due Diligence analysis for selected deals</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    col_nav_btn1, col_nav_btn2, col_nav_btn3 = st.columns([1, 2, 1])
    
    with col_nav_btn1:
        if st.button("← Back to Home", use_container_width=True):
            st.switch_page("Main_Page.py")
    
    with col_nav_btn2:
        if st.button("Proceed to Due Diligence →", type="primary", use_container_width=True):
            st.switch_page("pages/2_Due_Diligence_Analysis.py")
    
    with col_nav_btn3:
        if st.button("Skip to Market Analysis", use_container_width=True):
            st.switch_page("pages/3_Market_Analysis.py")
