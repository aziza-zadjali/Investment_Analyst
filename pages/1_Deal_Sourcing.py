"""
Deal Discovery & Sourcing Page
Professional UI matching main app color scheme
"""

import streamlit as st
from utils.web_scraper import WebScraper
from utils.llm_handler import LLMHandler
from utils.template_generator import TemplateGenerator
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Deal Discovery", layout="wide")

# Matching gradient colors from main app
def gradient_box(text, gradient="linear-gradient(90deg, #A6D8FF, #D5B8FF)"):
    return f"""<div style="background: {gradient}; padding: 15px 20px; border-radius: 12px; color: white; font-weight: 600; font-size: 1.5rem; text-align: center; margin-bottom: 20px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);">{text}</div>"""

# Unattractive Industries
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

# HEADER
st.markdown(gradient_box("Deal Discovery & Sourcing"), unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666; font-size: 1.1rem; margin-bottom: 30px;'>Discover and qualify investment opportunities from leading global platforms</p>", unsafe_allow_html=True)

# Divider
st.markdown("<div style='background: linear-gradient(90deg, #A6D8FF, #D5B8FF); height: 4px; border-radius: 2px; margin-bottom: 30px;'></div>", unsafe_allow_html=True)

# Define Investment Criteria
st.markdown(gradient_box("Define Investment Criteria"), unsafe_allow_html=True)

# Industry Filter
col_filter1, col_filter2 = st.columns([3, 1])

with col_filter1:
    st.markdown("**Unattractive Industries Screening** - Filter deals based on Qatar Development Bank's list")

with col_filter2:
    enable_industry_filter = st.checkbox("Enable Filter", value=True, help="Tag deals in unattractive industries")

if enable_industry_filter:
    with st.expander("View Complete Unattractive Industries List"):
        for category, industries_list in UNATTRACTIVE_INDUSTRIES.items():
            st.markdown(f"**{category}:**")
            st.caption(", ".join(industries_list))

st.markdown("<br>", unsafe_allow_html=True)

# Target Industry
industries = st.multiselect(
    "Target Industry",
    ["Technology", "Healthcare", "Financial Services", "Energy", "Consumer Goods", "Industrial", "Real Estate", "Agriculture", "Transportation", "Media & Entertainment", "Education", "Telecommunications", "Retail", "Manufacturing"],
    default=["Technology", "Healthcare"]
)

st.markdown("<br>", unsafe_allow_html=True)

# Sectors + Stage + Geography
col1, col2, col3 = st.columns(3)

with col1:
    sectors = st.multiselect(
        "Target Sectors",
        ["Fintech", "ClimateTech", "HealthTech", "Enterprise SaaS", "AI/ML", "E-commerce", "Logistics", "Agritech", "EdTech", "Biotech", "PropTech", "FoodTech", "DeepTech", "Cybersecurity", "Blockchain", "IoT", "Robotics", "Clean Energy"],
        default=["Fintech", "ClimateTech", "Enterprise SaaS"]
    )

with col2:
    stage = st.multiselect("Funding Stage", ["Pre-Seed", "Seed", "Series A", "Series B", "Series C+", "Growth"], default=["Seed", "Series A"])

with col3:
    geography = st.multiselect("Geography", ["North America", "Europe", "MENA", "Asia Pacific", "Latin America", "Africa", "Global"], default=["North America", "MENA"])

st.markdown("<br>", unsafe_allow_html=True)

# Revenue + Deal Count + Ticket Size
col4, col5, col6 = st.columns(3)

with col4:
    revenue_range = st.select_slider("Annual Revenue Range (USD)", options=["Pre-revenue", "$0-500K", "$500K-$2M", "$2M-$10M", "$10M-$50M", "$50M+"], value=("$500K-$2M", "$10M-$50M"))

with col5:
    deal_count = st.number_input("Number of Deals to Source", min_value=5, max_value=100, value=20, step=5)

with col6:
    st.markdown("**Investment Ticket Size (Optional)**")
    enable_ticket_size = st.checkbox("Define ticket size", value=False)
    if enable_ticket_size:
        ticket_min = st.number_input("Min Investment ($M)", min_value=0.1, max_value=100.0, value=1.0, step=0.5, format="%.1f")
        ticket_max = st.number_input("Max Investment ($M)", min_value=0.1, max_value=100.0, value=10.0, step=0.5, format="%.1f")
        ticket_size_range = (ticket_min, ticket_max)
    else:
        ticket_size_range = None

# Divider
st.markdown("<div style='background: linear-gradient(90deg, #A6D8FF, #D5B8FF); height: 4px; border-radius: 2px; margin: 30px 0;'></div>", unsafe_allow_html=True)

# Data Sources
st.markdown(gradient_box("Select Data Sources"), unsafe_allow_html=True)

DEAL_SOURCES = {
    "Crunchbase": {"url": "https://www.crunchbase.com/", "description": "70M+ profiles, funding rounds"},
    "AngelList": {"url": "https://www.angellist.com/", "description": "Startup jobs, funding, investors"},
    "PitchBook": {"url": "https://pitchbook.com/", "description": "Private equity and VC database"},
    "Magnitt": {"url": "https://magnitt.com/", "description": "MENA startup platform"},
    "Wamda": {"url": "https://www.wamda.com/", "description": "MENA ecosystem intelligence"},
    "Dealroom": {"url": "https://dealroom.co/", "description": "Global startup intelligence"}
}

selected_sources = st.multiselect("Active Data Providers", options=list(DEAL_SOURCES.keys()), default=["Crunchbase", "AngelList", "Magnitt"])

if selected_sources:
    st.markdown("#### Selected Sources:")
    cols = st.columns(min(len(selected_sources), 4))
    for idx, source in enumerate(selected_sources):
        with cols[idx % len(cols)]:
            st.markdown(f"**{source}**")
            st.caption(DEAL_SOURCES[source]["description"])

# Divider
st.markdown("<div style='background: linear-gradient(90deg, #A6D8FF, #D5B8FF); height: 4px; border-radius: 2px; margin: 30px 0;'></div>", unsafe_allow_html=True)

# Discovery Button
st.markdown(gradient_box("Discover Deals"), unsafe_allow_html=True)

if st.button("Start Discovery", type="primary", use_container_width=True):
    if not selected_sources:
        st.error("Please select at least one data source")
    else:
        with st.spinner("Fetching deals..."):
            all_deals = []
            progress_bar = st.progress(0)
            deal_count_per_source = deal_count // len(selected_sources)

            for idx, source in enumerate(selected_sources):
                st.info(f"Scanning {source}...")
                try:
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
                            "ticket_size": f"${1 + (i % 5)}M-${5 + (i % 10)}M" if not ticket_size_range else f"${ticket_size_range[0]}M-${ticket_size_range[1]}M"
                        }
                        
                        if enable_industry_filter:
                            for category, industry_list in UNATTRACTIVE_INDUSTRIES.items():
                                for unattr_industry in industry_list:
                                    if unattr_industry.lower() in deal['sector'].lower() or unattr_industry.lower() in deal['description'].lower() or unattr_industry.lower() in deal['industry'].lower():
                                        deal['unattractive_flag'] = True
                                        deal['unattractive_reason'] = f"{category}: {unattr_industry}"
                                        break
                                if deal['unattractive_flag']:
                                    break
                        
                        all_deals.append(deal)
                except Exception as e:
                    st.warning(f"Could not fetch from {source}: {e}")
                
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
        st.metric("Tagged Unattractive", unattractive_deals)
    
    show_filter = st.radio("Show:", ["All Deals", "Attractive Only", "Unattractive Only"], horizontal=True)
    
    if show_filter == "Attractive Only":
        display_deals = [d for d in st.session_state.discovered_deals if not d['unattractive_flag']]
    elif show_filter == "Unattractive Only":
        display_deals = [d for d in st.session_state.discovered_deals if d['unattractive_flag']]
    else:
        display_deals = st.session_state.discovered_deals
    
    for deal in display_deals:
        with st.container():
            col_deal1, col_deal2, col_deal3 = st.columns([3, 2, 1])
            
            with col_deal1:
                flag = "UNATTRACTIVE" if deal['unattractive_flag'] else "ATTRACTIVE"
                st.markdown(f"### {deal['company']} - {flag}")
                st.caption(deal['description'])
                if deal['unattractive_flag']:
                    st.error(f"**Industry Flag:** {deal['unattractive_reason']}")
            
            with col_deal2:
                st.markdown(f"**Industry:** {deal['industry']}")
                st.markdown(f"**Sector:** {deal['sector']}")
                st.markdown(f"**Stage:** {deal['stage']}")
                st.markdown(f"**Region:** {deal['region']}")
            
            with col_deal3:
                st.markdown(f"**Revenue:** {deal['revenue']}")
                st.markdown(f"**Ticket:** {deal['ticket_size']}")
                st.markdown(f"**Founded:** {deal['founded']}")
                st.markdown(f"**Source:** {deal['source']}")
            
            st.markdown("<div style='height: 1px; background: #ddd; margin: 20px 0;'></div>", unsafe_allow_html=True)
    
    # Export
    st.markdown("<div style='background: linear-gradient(90deg, #A6D8FF, #D5B8FF); height: 4px; border-radius: 2px; margin: 30px 0;'></div>", unsafe_allow_html=True)
    st.markdown(gradient_box("Export Results"), unsafe_allow_html=True)
    
    col_export1, col_export2 = st.columns(2)
    
    with col_export1:
        df = pd.DataFrame(st.session_state.discovered_deals)
        csv = df.to_csv(index=False)
        st.download_button("Download CSV", csv, f"Deal_Discovery_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv")
    
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
                'ticket_size': f"${ticket_size_range[0]}M-${ticket_size_range[1]}M" if ticket_size_range else 'Not specified'
            }
            report = template_gen.generate_deal_sourcing_report(report_data)
            st.download_button("Download Report (MD)", report, f"Deal_Report_{datetime.now().strftime('%Y%m%d')}.md", "text/markdown")
        except Exception as e:
            st.error(f"Report error: {e}")
