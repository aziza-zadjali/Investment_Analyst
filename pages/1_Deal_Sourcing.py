"""
Deal Discovery & Sourcing – Regulus Edition
Professional gradient UI + intelligent deal discovery + QDB unattractive filter + AI summaries
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from utils.web_scraper import WebScraper
from utils.llm_handler import LLMHandler
from utils.template_generator import TemplateGenerator

st.set_page_config(page_title="Deal Discovery - Regulus", layout="wide")

# --------------------------------------------------
# Global Styling Helpers
# --------------------------------------------------
def gradient_box(text, gradient="linear-gradient(90deg, #138074, #0e5f55)"):
    return f"""
    <div style="background: {gradient};
        padding:15px 20px;border-radius:10px;color:white;
        font-weight:600;font-size:1.4rem;text-align:center;
        margin-bottom:25px;box-shadow:0 4px 10px rgba(0,0,0,0.25);">
        {text}
    </div>
    """

# --------------------------------------------------
# Initialize Core Modules
# --------------------------------------------------
@st.cache_resource
def init_handlers():
    return WebScraper(), LLMHandler(), TemplateGenerator()

scraper, llm, template_gen = init_handlers()

if "discovered_deals" not in st.session_state:
    st.session_state.discovered_deals = []

# --------------------------------------------------
# Header
# --------------------------------------------------
st.markdown(gradient_box("Deal Discovery & Sourcing"), unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center;color:#666;font-size:1.05rem;'>"
    "Discover and qualify investment opportunities from leading global startup platforms</p>",
    unsafe_allow_html=True,
)
st.markdown("<hr style='height:4px;border:none;background:linear-gradient(90deg,#138074,#0e5f55);border-radius:3px;'>", unsafe_allow_html=True)

# --------------------------------------------------
# Unattractive Industries
# --------------------------------------------------
UNATTRACTIVE_INDUSTRIES = {
    "Food & Beverage": ["Bakery", "Bread", "Juice", "Milk", "Pasta", "Chips", "Water"],
    "Plastics": ["PET", "Plastic Pipe", "Garbage Bin", "Sheet", "UPVC"],
    "Construction": ["Cement", "Blocks", "Tiles", "Glass", "Stone"],
    "Services": ["Salon", "Laundry", "Restaurant", "Clinic", "Hotel", "Manpower"],
}

# Filter Toggle
col_f1, col_f2 = st.columns([3, 1])
with col_f1:
    st.markdown("**Industry Screening Filter (QDB):** Exclude unattractive, low-priority sectors")
with col_f2:
    enable_filter = st.checkbox("Enable Filter", value=True)

if enable_filter:
    with st.expander("View Complete Unattractive Industry List"):
        for k, v in UNATTRACTIVE_INDUSTRIES.items():
            st.markdown(f"**{k}:**")
            st.caption(", ".join(v))

st.markdown("<br>", unsafe_allow_html=True)

# --------------------------------------------------
# Filters – Industries, Sectors, Stage, Region
# --------------------------------------------------
col1, col2, col3, col4 = st.columns(4)
with col1:
    industries = st.multiselect(
        "Target Industries",
        ["Technology","Healthcare","CleanTech","Finance","Manufacturing","Retail"],
        ["Technology","Healthcare"]
    )
with col2:
    sectors = st.multiselect(
        "Sectors",
        ["FinTech","AI/ML","ClimateTech","HealthTech","SaaS","EdTech","Logistics"],
        ["FinTech","AI/ML"]
    )
with col3:
    stages = st.multiselect("Stage",["Pre-Seed","Seed","Series A","Series B","Growth"],["Seed"])
with col4:
    regions = st.multiselect("Regions",["MENA","Europe","North America","Asia"],["MENA","Europe"])

col5, col6 = st.columns(2)
with col5:
    deal_count = st.number_input("Deals to Discover", 5, 50, 10, 5)
with col6:
    revenue_range = st.select_slider("Annual Revenue (USD)",
        options=["Pre-revenue","$0-500K","$500K-$2M","$2M-$10M","$10M-$50M","$50M+"],
        value=("$500K-$2M", "$10M-$50M"))

# --------------------------------------------------
# Start Discovery
# --------------------------------------------------
st.markdown(gradient_box("Start Deal Discovery"), unsafe_allow_html=True)
if st.button("Run Discovery", type="primary", use_container_width=True):
    with st.spinner("Fetching and analyzing opportunities..."):
        dataset = scraper.scrape_startup_data()
        results = []

        for data in dataset[:deal_count]:
            company, website = data["name"], data["website"]

            # --- Discover IR & generate summaries
            ir_data = scraper.extract_company_data(website, company)
            ir_summary_text = ""
            for cat, content in ir_data.items():
                if len(content) > 200:
                    ir_summary_text += f"### {cat.title()}\n{llm.summarize(content, max_length='medium')}\n\n"

            analyst_note = llm.summarize(
                f"Company: {company}\nDescription: {data['description']}\nIndustry: {data['industry']}\nStage: {data['stage']}",
                max_length="short"
            )

            unattractive_flag, unattractive_reason = False, ""
            if enable_filter:
                for sector, items in UNATTRACTIVE_INDUSTRIES.items():
                    if any(i.lower() in data["industry"].lower() or i.lower() in data["description"].lower() for i in items):
                        unattractive_flag, unattractive_reason = True, f"{sector} Sector"
                        break

            results.append({
                "company": company,
                "industry": data["industry"],
                "stage": data["stage"],
                "funding": data["funding"],
                "region": data["location"],
                "description": data["description"],
                "analyst_summary": analyst_note,
                "ir_summary": ir_summary_text or "No IR data available.",
                "unattractive": unattractive_flag,
                "reason": unattractive_reason,
            })

        st.session_state.discovered_deals = results
        st.success(f"{len(results)} deals processed with Regulus Analyst Summaries")

# --------------------------------------------------
# Results Display
# --------------------------------------------------
if st.session_state.discovered_deals:
    df = pd.DataFrame(st.session_state.discovered_deals)
    total, bad = len(df), sum(df["unattractive"])
    good = total - bad

    st.markdown("<hr style='margin:30px 0;background:linear-gradient(90deg,#138074,#0e5f55);height:3px;border:none;'>", unsafe_allow_html=True)
    st.markdown(gradient_box("Discovered Deals"), unsafe_allow_html=True)
    c1,c2,c3 = st.columns(3)
    c1.metric("Total", total)
    c2.metric("Attractive", good)
    c3.metric("Excluded", bad)

    sel = st.radio("Show Results:", ["All", "Attractive Only", "Excluded Only"], horizontal=True)
    disp = df if sel=="All" else df[~df.unattractive] if sel=="Attractive Only" else df[df.unattractive]

    for _, row in disp.iterrows():
        st.markdown(
            f"<div style='border:1px solid #ccc;border-radius:10px;padding:15px;margin:10px 0;'>"
            f"<h4>{row['company']} {'🟢' if not row['unattractive'] else '🔴'}</h4>"
            f"<p><b>Industry:</b> {row['industry']} | <b>Stage:</b> {row['stage']} | <b>Funding:</b> {row['funding']} | <b>Region:</b> {row['region']}</p>"
            f"<p><i>{row['description']}</i></p>"
            f"{'<p style=\"color:red;font-weight:600;\">Excluded: '+row['reason']+'</p>' if row['unattractive'] else ''}"
            f"<details><summary style='color:#138074;font-weight:600;'>Regulus Analyst Summary</summary><p>{row['analyst_summary']}</p></details>"
            f"<details><summary style='color:#0e5f55;font-weight:600;'>Investor Relations Synopsis</summary><p>{row['ir_summary']}</p></details>"
            f"</div>", unsafe_allow_html=True)

    st.markdown(gradient_box("Export Results"), unsafe_allow_html=True)
    csv = df.to_csv(index=False)
    st.download_button("Download CSV", csv, "Deals.csv", "text/csv")

    # Optional Report Export
    try:
        report = template_gen.generate_deal_sourcing_report({
            "analyst_name": "Regulus AI",
            "analysis_date": datetime.now().strftime("%B %d, %Y"),
            "total_deals": total,
            "attractive_deals": good,
            "unattractive_deals": bad,
            "deals": st.session_state.discovered_deals
        })
        st.download_button("Download Report (Markdown)", report, "Deal_Report.md", "text/markdown")
    except Exception as e:
        st.error(f"Report Export Failed: {e}")
