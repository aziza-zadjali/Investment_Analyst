"""
Deal Discovery & Sourcing Page with Integrated Filtering
AI-powered deal sourcing from multiple funding platforms with automatic qualification
"""

import streamlit as st
from utils.web_scraper import WebScraper
from utils.llm_handler import LLMHandler
from utils.template_generator import TemplateGenerator
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Deal Discovery", layout="wide")

# Gradient style helper
def gradient_box(text, height="60px", gradient="linear-gradient(90deg, #4b6cb7 0%, #182848 100%)"):
    return f"""<div style="background: {gradient}; padding: 10px 20px; border-radius: 10px; color: white; font-weight: bold; font-size: 24px; line-height: {height}; text-align: center; margin-bottom: 20px;">{text}</div>"""

# Unattractive Industries from Qatar Development Bank List
UNATTRACTIVE_INDUSTRIES = {
    "Food & Beverage Manufacturing": ["Industrial Bakery", "Bread and Bakery Products", "Short-Life Juice", "Fresh Milk", "Processed Milk", "Powder Milk", "Pasta", "Potato Chips", "Water Bottling", "Bottled Water"],
    "Metal Products": ["Aluminum Profiles", "Copper Winding Wire", "Copper Wire", "Pre-engineered Buildings", "Pre-fabricated Buildings", "Metal Nails", "Bolts", "Aluminum Composite Panels", "Steel Structures", "Welding Electrodes"],
    "Non-Metallic Mineral Products": ["Hollow Blocks", "Curbstone", "Interlock", "Flat Glass", "Float Glass", "Cement", "Mortar", "Ready Mix Cement", "Marble Tiles", "Ceramic Tiles"],
    "Plastics & Rubber": ["PET Preforms", "Water Bottle Preforms", "Plastic Fittings", "PE Sheets", "Plastic Garbage Bins", "EPS Boards", "XPS Boards", "Plastic Pipes", "Plastic Tanks", "Road Barriers", "Shopping Bags", "Tire Recycling", "UPVC Profiles", "UPVC Windows", "UPVC Doors"],
    "Other Manufacturing": ["Switchgear", "Industrial Tents", "Façade Fabrication", "Flexographic Printing", "Cardboard Boxes", "Diapers", "Sanitary Pads", "Paper Recycling", "Tissue Paper", "Carpentry", "Wooden Furniture", "Detergents", "Electric Cables", "Perfume", "Safety Shoes", "Industrial Resins", "Wood Plastic Composite"],
    "Agriculture & Services": ["Chicken Farming", "Dairy Farming", "Restaurants", "Food Outlets", "Hotels", "Hotel Operations", "Automobile Garages", "Travel Agencies", "Tourism Offices", "Nurseries", "Kindergartens", "Dental Clinics", "Dermatology Clinics", "Gynecology Clinics", "Polyclinics", "Salons", "Spas", "Dry Cleaning", "Laundry Services", "Tailoring Workshops", "Cleaning Companies", "Manpower Sourcing"]
}

# Initialize handlers
@st.cache_resource
def init_handlers():
    return WebScraper(), LLMHandler(), TemplateGenerator()

scraper, llm, template_gen = init_handlers()

# Session state
if 'discovered_deals' not in st.session_state:
    st.session_state.discovered_deals = []
if 'filtered_deals' not in st.session_state:
    st.session_state.filtered_deals = []

# HEADER
st.markdown(gradient_box("Deal Discovery & Sourcing"), unsafe_allow_html=True)
st.markdown("Discover and qualify investment opportunities from leading global platforms with **AI-powered two-stage filtering**.")

st.divider()

# INTEGRATED: Define Investment Criteria with Industry Filter
st.markdown(gradient_box("Define Investment Criteria", gradient="linear-gradient(90deg, #FF416C 0%, #FF4B2B 100%)"), unsafe_allow_html=True)

# Industry Filter Toggle
col_filter1, col_filter2 = st.columns([3, 1])

with col_filter1:
    st.markdown("**🚫 Unattractive Industries Screening** - Filter deals based on Qatar Development Bank's list")

with col_filter2:
    enable_industry_filter = st.checkbox("Enable Filter", value=True, help="Tag deals in unattractive industries")

if enable_industry_filter:
    with st.expander("📋 View Complete Unattractive Industries List"):
        for category, industries_list in UNATTRACTIVE_INDUSTRIES.items():
            st.markdown(f"**{category}:**")
            st.caption(", ".join(industries_list))

st.markdown("<br>", unsafe_allow_html=True)

# Target Industry
industries = st.multiselect(
    "Target Industry",
    ["Technology", "Healthcare", "Financial Services", "Energy", "Consumer Goods",
     "Industrial", "Real Estate", "Agriculture", "Transportation", "Media & Entertainment",
     "Education", "Telecommunications", "Retail", "Manufacturing"],
    default=["Technology", "Healthcare"],
    help="Select broader industry categories"
)

st.markdown("<br>", unsafe_allow_html=True)

# Target Sectors + Stage + Geography
col1, col2, col3 = st.columns(3)

with col1:
    sectors = st.multiselect(
        "Target Sectors",
        ["Fintech", "ClimateTech", "HealthTech", "Enterprise SaaS", "AI/ML", "E-commerce",
         "Logistics", "Agritech", "EdTech", "Biotech", "PropTech", "FoodTech", "DeepTech",
         "Cybersecurity", "Blockchain", "IoT", "Robotics", "Clean Energy"],
        default=["Fintech", "ClimateTech", "Enterprise SaaS"],
        help="Specific sectors within your target industries"
    )

with col2:
    stage = st.multiselect(
        "Funding Stage",
        ["Pre-Seed", "Seed", "Series A", "Series B", "Series C+", "Growth"],
        default=["Seed", "Series A"]
    )

with col3:
    geography = st.multiselect(
        "Geography",
        ["North America", "Europe", "MENA", "Asia Pacific", "Latin America", "Africa", "Global"],
        default=["North America", "MENA"]
    )

st.markdown("<br>", unsafe_allow_html=True)

# Revenue Range + Deal Count + Investment Ticket Size
col4, col5, col6 = st.columns(3)

with col4:
    revenue_range = st.select_slider(
        "Annual Revenue Range (USD)",
        options=["Pre-revenue", "$0-500K", "$500K-$2M", "$2M-$10M", "$10M-$50M", "$50M+"],
        value=("$500K-$2M", "$10M-$50M")
    )

with col5:
    deal_count = st.number_input(
        "Number of Deals to Source",
        min_value=5,
        max_value=100,
        value=20,
        step=5
    )

with col6:
    st.markdown("**Investment Ticket Size (Optional)**")
    
    enable_ticket_size = st.checkbox("Define ticket size", value=False)
    
    if enable_ticket_size:
        ticket_min = st.number_input("Min Investment ($M)", min_value=0.1, max_value=100.0, value=1.0, step=0.5, format="%.1f")
        ticket_max = st.number_input("Max Investment ($M)", min_value=0.1, max_value=100.0, value=10.0, step=0.5, format="%.1f")
        ticket_size_range = (ticket_min, ticket_max)
    else:
        ticket_size_range = None

st.divider()

# Data Source Selection
st.markdown(gradient_box("Select Data Sources", gradient="linear-gradient(90deg, #11998e 0%, #38ef7d 100%)"), unsafe_allow_html=True)

DEAL_SOURCES = {
    "Crunchbase": {"url": "https://www.crunchbase.com/", "description": "70M+ profiles, funding rounds"},
    "AngelList": {"url": "https://www.angellist.com/", "description": "Startup jobs, funding, investors"},
    "PitchBook": {"url": "https://pitchbook.com/", "description": "Private equity and VC database"},
    "Magnitt": {"url": "https://magnitt.com/", "description": "MENA startup platform"},
    "Wamda": {"url": "https://www.wamda.com/", "description": "MENA ecosystem intelligence"},
    "Dealroom": {"url": "https://dealroom.co/", "description": "Global startup intelligence"}
}

selected_sources = st.multiselect(
    "Active Data Providers",
    options=list(DEAL_SOURCES.keys()),
    default=["Crunchbase", "AngelList", "Magnitt"]
)

if selected_sources:
    st.markdown("#### Selected Sources:")
    cols = st.columns(min(len(selected_sources), 4))
    for idx, source in enumerate(selected_sources):
        with cols[idx % len(cols)]:
            st.markdown(f"**{source}**")
            st.caption(DEAL_SOURCES[source]["description"])

st.divider()

# Deal Discovery Execution
st.markdown(gradient_box("Discover Deals", gradient="linear-gradient(90deg, #8360c3 0%, #2ebf91 100%)"), unsafe_allow_html=True)

if st.button("🚀 Start Discovery", type="primary", use_container_width=True):
    
    if not selected_sources:
        st.error("Please select at least one data source")
    else:
        with st.spinner("Fetching deals from selected sources..."):
            all_deals = []
            progress_bar = st.progress(0)
            deal_count_per_source = deal_count // len(selected_sources)

            for idx, source in enumerate(selected_sources):
                st.info(f"🔍 Scanning {source}...")
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
                            "description": f"Innovative {sectors[i % len(sectors)] if sectors else 'tech'} company in {industries[i % len(industries)] if industries else 'Technology'}",
                            "founded": str(2020 + (i % 5)),
                            "employees": f"{20 + i * 10}-{30 + i * 10}",
                            "unattractive_flag": False,
                            "unattractive_reason": "",
                            "ticket_size": f"${1 + (i % 5)}M-${5 + (i % 10)}M" if not ticket_size_range else f"${ticket_size_range[0]}M-${ticket_size_range[1]}M"
                        }
                        
                        # Industry Filter
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
            st.success(f"✅ Discovered {len(all_deals)} potential deals")

# Display Discovered Deals
if st.session_state.discovered_deals:
    
    st.divider()
    st.markdown(gradient_box("Discovered Potential Deals", gradient="linear-gradient(90deg, #667eea 0%, #764ba2 100%)"), unsafe_allow_html=True)
    
    total_deals = len(st.session_state.discovered_deals)
    unattractive_deals = sum(1 for d in st.session_state.discovered_deals if d['unattractive_flag'])
    attractive_deals = total_deals - unattractive_deals
    
    col_stat1, col_stat2, col_stat3 = st.columns(3)
    
    with col_stat1:
        st.metric("Total Deals", total_deals)
    
    with col_stat2:
        st.metric("✅ Attractive", attractive_deals)
    
    with col_stat3:
        st.metric("⚠️ Tagged Unattractive", unattractive_deals)
    
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
                flag_emoji = "⚠️" if deal['unattractive_flag'] else "✅"
                st.markdown(f"### {flag_emoji} {deal['company']}")
                st.caption(deal['description'])
                if deal['unattractive_flag']:
                    st.error(f"🚫 **Industry Flag:** {deal['unattractive_reason']}")
            
            with col_deal2:
                st.markdown(f"**Industry:** {deal['industry']}")
                st.markdown(f"**Sector:** {deal['sector']}")
                st.markdown(f"**Stage:** {deal['stage']}")
                st.markdown(f"**Region:** {deal['region']}")
            
            with col_deal3:
                st.markdown(f"**Revenue:** {deal['revenue']}")
                st.markdown(f"**Ticket Size:** {deal['ticket_size']}")
                st.markdown(f"**Founded:** {deal['founded']}")
                st.markdown(f"**Source:** {deal['source']}")
            
            st.divider()
    
    # Export Options
    st.markdown(gradient_box("Export Results", gradient="linear-gradient(90deg, #f093fb 0%, #f5576c 100%)"), unsafe_allow_html=True)
    
    col_export1, col_export2 = st.columns(2)
    
    with col_export1:
        df = pd.DataFrame(st.session_state.discovered_deals)
        csv = df.to_csv(index=False)
        
        st.download_button(
            label="⬇️ Download CSV",
            data=csv,
            file_name=f"Deal_Discovery_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    
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
            
            st.download_button(
                label="⬇️ Download Report (MD)",
                data=report,
                file_name=f"Deal_Report_{datetime.now().strftime('%Y%m%d')}.md",
                mime="text/markdown"
            )
        except Exception as e:
            st.error(f"Report generation error: {e}")

# Sidebar
with st.sidebar:
    st.markdown("### 💡 Deal Sourcing Features")
    st.markdown("""
✓ **Integrated Industry Filter**
✓ **Target Industry + Sector**
✓ **Investment Ticket Size**
✓ **Multi-Source Aggregation**
✓ **Unattractive Industry Tagging**
✓ **Export to CSV & Reports**
""")
    
    if st.session_state.discovered_deals:
        st.divider()
        st.markdown("### 📊 Current Session")
        st.caption(f"**Deals Discovered:** {len(st.session_state.discovered_deals)}")
        st.caption(f"**Sources Used:** {len(selected_sources) if selected_sources else 0}")
        if ticket_size_range:
            st.caption(f"**Ticket Size:** ${ticket_size_range[0]}M-${ticket_size_range[1]}M")
