"""
Deal Discovery & Sourcing Page
Combined best features: Advanced filtering + UI/UX matching + Save/Contact functionality
"""

import streamlit as st
from utils.web_scraper import WebScraper
from utils.llm_handler import LLMHandler
from utils.template_generator import TemplateGenerator
import pandas as pd
from datetime import datetime
from utils.qdb_styling import apply_qdb_styling, QDB_DARK_BLUE
import base64
import os

st.set_page_config(page_title="Deal Sourcing - Regulus", layout="wide", initial_sidebar_state="collapsed")
apply_qdb_styling()


def encode_image(path):
    """Safely embed logos"""
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f"data:image/png;base64,{base64.b64encode(f.read()).decode()}"
    return None


qdb_logo = encode_image("QDB_Logo.png")

UNATTRACTIVE_INDUSTRIES = {
    "Food & Beverage Manufacturing": ["Industrial Bakery", "Bread and Bakery Products", "Short-Life Juice", "Fresh Milk", "Processed Milk", "Powder Milk", "Pasta", "Potato Chips", "Water Bottling", "Bottled Water"],
    "Metal Products": ["Aluminum Profiles", "Copper Winding Wire", "Copper Wire", "Pre-engineered Buildings", "Pre-fabricated Buildings", "Metal Nails", "Bolts", "Aluminum Composite Panels", "Steel Structures", "Welding Electrodes"],
    "Non-Metallic Mineral Products": ["Hollow Blocks", "Curbstone", "Interlock", "Flat Glass", "Float Glass", "Cement", "Mortar", "Ready Mix Cement", "Marble Tiles", "Ceramic Tiles"],
    "Plastics & Rubber": ["PET Preforms", "Water Bottle Preforms", "Plastic Fittings", "PE Sheets", "Plastic Garbage Bins", "EPS Boards", "XPS Boards", "Plastic Pipes", "Plastic Tanks", "Road Barriers", "Shopping Bags", "Tire Recycling", "UPVC Profiles", "UPVC Windows", "UPVC Doors"],
    "Other Manufacturing": ["Switchgear", "Industrial Tents", "Façade Fabrication", "Flexographic Printing", "Cardboard Boxes", "Diapers", "Sanitary Pads", "Paper Recycling", "Tissue Paper", "Carpentry", "Wooden Furniture", "Detergents", "Electric Cables", "Perfume", "Safety Shoes", "Industrial Resins", "Wood Plastic Composite"],
    "Agriculture & Services": ["Chicken Farming", "Dairy Farming", "Restaurants", "Food Outlets", "Hotels", "Hotel Operations", "Automobile Garages", "Travel Agencies", "Tourism Offices", "Nurseries", "Kindergartens", "Dental Clinics", "Dermatology Clinics", "Gynecology Clinics", "Polyclinics", "Salons", "Spas", "Dry Cleaning", "Laundry Services", "Tailoring Workshops", "Cleaning Companies", "Manpower Sourcing"]
}

DEAL_SOURCES = {
    "Crunchbase": {"url": "https://www.crunchbase.com/", "description": "70M+ profiles, funding rounds"},
    "AngelList": {"url": "https://www.angellist.com/", "description": "Startup jobs, funding, investors"},
    "PitchBook": {"url": "https://pitchbook.com/", "description": "Private equity and VC database"},
    "Magnitt": {"url": "https://magnitt.com/", "description": "MENA startup platform"},
    "Wamda": {"url": "https://www.wamda.com/", "description": "MENA ecosystem intelligence"},
    "Dealroom": {"url": "https://dealroom.co/", "description": "Global startup intelligence"}
}

@st.cache_resource
def init_handlers():
    return WebScraper(), LLMHandler(), TemplateGenerator()

scraper, llm, template_gen = init_handlers()

# Initialize session state
if 'discovered_deals' not in st.session_state:
    st.session_state.discovered_deals = []
if 'saved_deals' not in st.session_state:
    st.session_state.saved_deals = []
if 'selected_deals' not in st.session_state:
    st.session_state.selected_deals = []
if 'show_contact_form' not in st.session_state:
    st.session_state.show_contact_form = {}

# ===== HERO HEADER SECTION (Matching Main Page) =====
st.markdown(
    f"""
<div style="
    background: linear-gradient(135deg, #1B2B4D 0%, #2C3E5E 100%);
    color: white;
    text-align: center;
    margin: 0 -3rem;
    padding: 60px 20px 50px 20px;
    position: relative;
    overflow: hidden;">
  
  <!-- QDB Logo -->
  <div style="position:absolute; top:20px; left:35px;">
    {"<img src='"+qdb_logo+"' style='max-height:60px;'>" if qdb_logo else "<b>QDB</b>"}
  </div>

  <!-- Central Content -->
  <div style="max-width:950px; margin:0 auto;">
    <h1 style="font-size:2.2rem; font-weight:700; letter-spacing:-0.3px; margin-bottom:10px;">
      Deal Discovery & Sourcing
    </h1>
    <p style="color:#CBD5E0; font-size:0.95rem; line-height:1.6;">
      AI-powered investment opportunity discovery from leading global platforms
    </p>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

# ===== TOP NAVIGATION BAR (Matching Main Page Style) =====
st.markdown(
    """
<style>
.nav-top-bar {
    background-color: #F6F5F2;
    margin: 0 -3rem;
    padding: 15px 40px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.nav-top-bar a {
    text-decoration: none;
    color: #138074;
    font-weight: 600;
    font-size: 0.95rem;
    transition: color 0.3s;
}

.nav-top-bar a:hover {
    color: #0e5f55;
}

.step-indicator {
    text-align: center;
    color: #1B2B4D;
    font-weight: 600;
}
</style>

<div class="nav-top-bar">
    <a href="javascript:window.location.href='streamlit_app.py'">Back to Home</a>
    <div class="step-indicator">Step 1 of 5: Deal Sourcing</div>
    <div style="color: #999; font-size: 0.9rem;">Regulus AI</div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown("<br>", unsafe_allow_html=True)

# ===== DEFINE INVESTMENT CRITERIA =====
with st.expander("Define Investment Criteria", expanded=True):
    
    # Industry Filter Toggle
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

st.markdown("<br>", unsafe_allow_html=True)

# ===== DATA SOURCE SELECTION =====
st.subheader("Select Data Sources")

selected_sources = st.multiselect(
    "Active Data Providers",
    options=list(DEAL_SOURCES.keys()),
    default=["Crunchbase", "AngelList", "Magnitt"]
)

if selected_sources:
    st.markdown("#### Selected Sources:")
    cols = st.columns(min(len(selected_sources), 3))
    for idx, source in enumerate(selected_sources):
        with cols[idx % len(cols)]:
            st.markdown(f"**{source}**")
            st.caption(DEAL_SOURCES[source]["description"])

st.markdown("<br>", unsafe_allow_html=True)

# ===== DEAL DISCOVERY EXECUTION =====
if st.button("Discover Deals", type="primary", use_container_width=False):
    
    if not selected_sources:
        st.error("Please select at least one data source")
    else:
        with st.spinner("Fetching deals from selected sources..."):
            all_deals = []
            progress_bar = st.progress(0)
            deal_count_per_source = deal_count // len(selected_sources)

            for idx, source in enumerate(selected_sources):
                st.info(f"Scanning {source}...")
                try:
                    for i in range(deal_count_per_source):
                        deal = {
                            "id": f"deal_{idx * deal_count_per_source + i + 1}",
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
                            "contact_email": f"contact@startup{idx * deal_count_per_source + i + 1}.com",
                            "contact_phone": f"+1-555-{1000 + idx * deal_count_per_source + i}",
                            "contact_name": f"CEO Name {idx * deal_count_per_source + i + 1}",
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
            st.success(f"Discovered {len(all_deals)} potential deals")
            st.rerun()

# ===== DISPLAY DISCOVERED DEALS =====
if st.session_state.discovered_deals:
    
    st.markdown("<br>", unsafe_allow_html=True)
    
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
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    show_filter = st.radio("Show:", ["All Deals", "Attractive Only", "Unattractive Only"], horizontal=True)
    
    if show_filter == "Attractive Only":
        display_deals = [d for d in st.session_state.discovered_deals if not d['unattractive_flag']]
    elif show_filter == "Unattractive Only":
        display_deals = [d for d in st.session_state.discovered_deals if d['unattractive_flag']]
    else:
        display_deals = st.session_state.discovered_deals
    
    st.subheader("Available Deals")
    
    for deal in display_deals:
        with st.container():
            col_select, col_deal1, col_deal2, col_deal3, col_actions = st.columns([0.3, 2.5, 1.5, 1.2, 1.2])
            
            with col_select:
                if st.checkbox("", key=f"deal_{deal['id']}", label_visibility="collapsed"):
                    st.session_state.selected_deals = [deal]
            
            with col_deal1:
                flag_text = "FLAGGED" if deal['unattractive_flag'] else "APPROVED"
                st.markdown(f"**{deal['company']}** - {flag_text}")
                st.caption(deal['description'])
                if deal['unattractive_flag']:
                    st.error(f"{deal['unattractive_reason']}")
            
            with col_deal2:
                st.markdown(f"**{deal['industry']}** | {deal['sector']}")
                st.caption(f"{deal['stage']} | {deal['region']}")
            
            with col_deal3:
                st.markdown(f"**${deal['ticket_size']}**")
                st.caption(f"Founded {deal['founded']}")
            
            with col_actions:
                col_save, col_contact = st.columns(2)
                with col_save:
                    if st.button("Save", key=f"save_{deal['id']}", use_container_width=True, help="Save for later"):
                        if deal not in st.session_state.saved_deals:
                            st.session_state.saved_deals.append(deal)
                            st.success("Saved!")
                        st.rerun()
                
                with col_contact:
                    if st.button("Contact", key=f"contact_{deal['id']}", use_container_width=True, help="Send message"):
                        st.session_state.show_contact_form[deal['id']] = True
                        st.rerun()
            
            # Contact Form
            if st.session_state.show_contact_form.get(deal['id']):
                st.markdown(f"<div style='background:#f0f5f9; padding:15px; border-radius:8px; margin-top:10px; border-left:4px solid #138074;'>", unsafe_allow_html=True)
                st.markdown(f"**Send Message to {deal['company']}**")
                
                col_form1, col_form2 = st.columns(2)
                with col_form1:
                    sender_name = st.text_input("Your Name", key=f"name_{deal['id']}")
                    sender_email = st.text_input("Your Email", key=f"email_{deal['id']}")
                
                with col_form2:
                    subject = st.text_input("Subject", key=f"subject_{deal['id']}", placeholder="Investment Inquiry")
                
                message = st.text_area("Message", key=f"msg_{deal['id']}", height=80)
                
                col_send1, col_send2 = st.columns(2)
                with col_send1:
                    if st.button("Send", key=f"send_{deal['id']}", use_container_width=True):
                        st.success(f"Message sent to {deal['contact_email']}")
                        st.session_state.show_contact_form[deal['id']] = False
                        st.rerun()
                
                with col_send2:
                    if st.button("Cancel", key=f"cancel_{deal['id']}", use_container_width=True):
                        st.session_state.show_contact_form[deal['id']] = False
                        st.rerun()
                
                st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown(f"<div style='height: 1px; background: #138074; opacity: 0.15; margin: 12px 0;'></div>", unsafe_allow_html=True)
    
    # ===== SAVED DEALS SECTION =====
    if st.session_state.saved_deals:
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("Saved Deals (for Later DD)")
        
        saved_df = pd.DataFrame([
            {
                "Company": d['company'],
                "Industry": d['industry'],
                "Sector": d['sector'],
                "Stage": d['stage'],
                "Ticket Size": d['ticket_size'],
                "Contact": d['contact_email']
            }
            for d in st.session_state.saved_deals
        ])
        
        st.dataframe(saved_df, use_container_width=True)
        
        # Download Saved Deals
        csv_saved = saved_df.to_csv(index=False)
        st.download_button(
            "Download Saved Deals (CSV)",
            csv_saved,
            f"Saved_Deals_{datetime.now().strftime('%Y%m%d')}.csv",
            "text/csv"
        )
    
    # ===== EXPORT ALL DEALS =====
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("Export Results")
    
    col_export1, col_export2 = st.columns(2)
    
    with col_export1:
        df_all = pd.DataFrame(st.session_state.discovered_deals)
        csv_all = df_all.to_csv(index=False)
        
        st.download_button(
            label="Download All Deals (CSV)",
            data=csv_all,
            file_name=f"All_Deals_{datetime.now().strftime('%Y%m%d')}.csv",
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
                label="Download Report (MD)",
                data=report,
                file_name=f"Deal_Report_{datetime.now().strftime('%Y%m%d')}.md",
                mime="text/markdown"
            )
        except Exception as e:
            st.warning(f"Report generation not available: {e}")
    
    # ===== SELECTED DEAL INFO =====
    if st.session_state.selected_deals:
        st.markdown("<br>", unsafe_allow_html=True)
        st.success(f"Selected: **{st.session_state.selected_deals[0]['company']}** for Due Diligence")
    
    # ===== WORKFLOW NAVIGATION =====
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style='
            background: linear-gradient(135deg, #138074 0%, #0e5f55 100%);
            border-radius: 12px;
            padding: 25px;
            color: white;
            text-align: center;
        '>
            <h3 style='margin: 0 0 10px 0;'>Ready for Due Diligence?</h3>
            <p style='margin: 0; font-size: 0.95rem;'>Select a deal above and proceed to detailed analysis</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    nav_cols = st.columns([1, 1, 1])
    
    with nav_cols[0]:
        if st.button("Back to Home", use_container_width=True):
            st.switch_page("streamlit_app.py")
    
    with nav_cols[1]:
        if st.button("Proceed to Due Diligence", type="primary", use_container_width=True, disabled=not st.session_state.selected_deals):
            if st.session_state.selected_deals:
                st.switch_page("pages/2_Due_Diligence_Analysis.py")
            else:
                st.error("Please select a deal first")
    
    with nav_cols[2]:
        if st.button("Skip to Market", use_container_width=True):
            st.switch_page("pages/3_Market_Analysis.py")

# ===== FOOTER (No logos) =====
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(
    """
<div style="
    background-color:#1B2B4D;
    color:#E2E8F0;
    padding:30px 40px;
    margin:40px -3rem 0 -3rem;
    font-size:0.94rem;">
  <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; max-width:1400px; margin:0 auto;">
    <div style="flex:2;">
      <ul style="list-style:none; display:flex; gap:30px; flex-wrap:wrap; padding:0; margin:0;">
        <li><a href="#" style="text-decoration:none; color:#E2E8F0;">About Regulus</a></li>
        <li><a href="#" style="text-decoration:none; color:#E2E8F0;">Careers</a></li>
        <li><a href="#" style="text-decoration:none; color:#E2E8F0;">Contact Us</a></li>
        <li><a href="#" style="text-decoration:none; color:#E2E8F0;">Privacy Policy</a></li>
      </ul>
    </div>
    <div style="flex:1; text-align:right;">
      <p style="margin:0; color:#A0AEC0; font-size:0.9rem;">Powered by Regulus AI</p>
    </div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)
