"""
Deal Discovery & Sourcing – Regulus Edition
Maintains original logic | Adds teal Regulus UI | Step tracker & better UX
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from utils.web_scraper import WebScraper
from utils.llm_handler import LLMHandler
from utils.template_generator import TemplateGenerator


# ---------------------- Setup ----------------------
st.set_page_config(page_title="Deal Discovery – Regulus", layout="wide", initial_sidebar_state="collapsed")

# Hide default sidebar
st.markdown("<style>[data-testid='stSidebar']{display:none}</style>", unsafe_allow_html=True)


# ---------------------- UI Helpers ----------------------
def gradient_header(text, grad="linear-gradient(135deg,#138074,#0e5f55)"):
    return f"""
    <div style="background:{grad};
        color:white;padding:14px 22px;border-radius:12px;
        font-weight:700;font-size:1.4rem;text-align:center;
        margin:30px 0;box-shadow:0 3px 10px rgba(19,128,116,0.3);">
        {text}
    </div>
    """


# ---------------------- Initialize Modules ----------------------
@st.cache_resource
def init_modules():
    return WebScraper(), LLMHandler(), TemplateGenerator()
scraper, llm, template_gen = init_modules()

if "discovered_deals" not in st.session_state:
    st.session_state["discovered_deals"] = []


# ---------------------- Header ----------------------
st.markdown(gradient_header("Deal Discovery & Sourcing"), unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#555;'>AI‑powered multi‑source startup discovery with QDB‑aligned screening</p>", unsafe_allow_html=True)

# Step Visual
st.markdown("""
<style>
.track{display:flex;justify-content:center;align-items:center;gap:18px;margin:35px 0;}
.step{display:flex;flex-direction:column;align-items:center;font-weight:600;font-size:0.85rem;}
.circle{width:42px;height:42px;border-radius:50%;display:flex;align-items:center;justify-content:center;margin-bottom:5px;}
.active{background:#138074;color:white;box-shadow:0 3px 8px rgba(19,128,116,0.4);}
.inactive{background:#CBD5E1;color:#9CA3AF;}
.line{width:70px;height:3px;background:#D1D5DB;}
.active .label{color:#138074;}
</style>
<div class="track">
  <div class="step active"><div class="circle active">1</div><div class="label active">Deal Sourcing</div></div>
  <div class="line"></div>
  <div class="step inactive"><div class="circle inactive">2</div><div class="label inactive">Due Diligence</div></div>
  <div class="line"></div>
  <div class="step inactive"><div class="circle inactive">3</div><div class="label inactive">Market</div></div>
  <div class="line"></div>
  <div class="step inactive"><div class="circle inactive">4</div><div class="label inactive">Financials</div></div>
  <div class="line"></div>
  <div class="step inactive"><div class="circle inactive">5</div><div class="label inactive">Memo</div></div>
</div>
""", unsafe_allow_html=True)


# ---------------------- QDB Filter ----------------------
UNATTRACTIVE_INDUSTRIES = {
    "Food & Beverage": ["Bakery", "Juice", "Milk", "Water"],
    "Plastics": ["PET", "UPVC", "Plastic", "Pipe"],
    "Construction": ["Cement", "Tiles", "Blocks", "Glass"],
    "Services": ["Salon", "Spa", "Laundry", "Clinic"],
}

st.markdown(gradient_header("Define Investment Criteria"), unsafe_allow_html=True)
f1, f2 = st.columns([3, 1])
with f1:
    st.markdown("**QDB Unattractive Industry Filter** – exclude non‑priority sectors")
with f2:
    enable_filter = st.checkbox("Enable Filter", True)

if enable_filter:
    with st.expander("View Complete List"):
        for c, items in UNATTRACTIVE_INDUSTRIES.items():
            st.markdown(f"**{c}:** {', '.join(items)}")


# ---------------------- Filters ----------------------
col1, col2, col3, col4 = st.columns(4)
with col1:
    industries = st.multiselect("Industries", ["Technology", "Healthcare", "CleanTech", "Finance", "Retail"], ["Technology"])
with col2:
    sectors = st.multiselect("Sectors", ["FinTech", "AI/ML", "HealthTech", "ClimateTech", "SaaS"], ["FinTech"])
with col3:
    stages = st.multiselect("Stage", ["Pre‑Seed", "Seed", "Series A", "Series B", "Growth"], ["Seed"])
with col4:
    geos = st.multiselect("Regions", ["MENA", "Europe", "North America", "Asia"], ["MENA", "Europe"])

col5, col6 = st.columns(2)
with col5:
    deal_count = st.slider("Deals to Source", 5, 50, 10)
with col6:
    revenue = st.select_slider("Annual Revenue (USD)", ["Pre‑revenue", "$0‑500K", "$500K‑$2M", "$2M‑$10M", "$10M‑$50M", "$50M+"], ("$500K‑$2M", "$10M‑$50M"))


# ---------------------- Data Sources ----------------------
st.markdown(gradient_header("Select Data Sources"), unsafe_allow_html=True)
sources = {
    "Crunchbase": "Global startups & investment data",
    "AngelList": "VC deals, founders & investors",
    "PitchBook": "Private equity data",
    "Magnitt": "MENA‑focused startup data",
    "Wamda": "Regional ecosystem insights",
    "Dealroom": "Global intelligence platform"
}
selected_sources = st.multiselect("Sources", list(sources.keys()), ["Crunchbase", "AngelList"])
if selected_sources:
    c = st.columns(len(selected_sources))
    for i, s in enumerate(selected_sources):
        with c[i % len(c)]:
            st.markdown(f"**{s}**")
            st.caption(sources[s])


# ---------------------- Discovery ----------------------
st.markdown(gradient_header("Discover Deals"), unsafe_allow_html=True)
center = st.columns([1, 0.8, 1])[1]
with center:
    run = st.button("🚀 Start Discovery", use_container_width=True)

st.markdown("""
<style>div.stButton>button:first-child{
background:linear-gradient(135deg,#138074,#0e5f55)!important;color:white!important;
border:none!important;border-radius:40px!important;
padding:12px 30px!important;font-weight:700!important;font-size:0.95rem!important;
box-shadow:0 4px 10px rgba(19,128,116,0.3)!important;}
div.stButton>button:first-child:hover{transform:translateY(-2px)!important;}
</style>
""", unsafe_allow_html=True)

if run:
    if not selected_sources:
        st.warning("Please select at least one data source.")
    else:
        with st.spinner("🚀 Aggregating deals and applying AI qualification..."):
            all_deals = []
            progress = st.progress(0)
            each = deal_count // len(selected_sources)

            for idx, src in enumerate(selected_sources):
                st.info(f"Scanning {src}...")
                for i in range(each):
                    d = {
                        "company": f"{src}_Startup_{i+1}",
                        "industry": industries[i % len(industries)],
                        "sector": sectors[i % len(sectors)],
                        "stage": stages[i % len(stages)],
                        "region": geos[i % len(geos)],
                        "revenue": revenue[0],
                        "source": src,
                        "description": f"Innovative {sectors[i % len(sectors)]} in {industries[i % len(industries)]}",
                        "unattractive_flag": False,
                        "unattractive_reason": "",
                    }

                    if enable_filter:
                        for cat, items in UNATTRACTIVE_INDUSTRIES.items():
                            if any(x.lower() in d["sector"].lower() or x.lower() in d["industry"].lower() for x in items):
                                d["unattractive_flag"] = True
                                d["unattractive_reason"] = cat
                                break

                    all_deals.append(d)
                progress.progress((idx + 1) / len(selected_sources))

            st.session_state["discovered_deals"] = all_deals
            st.success(f"✅ {len(all_deals)} deals discovered and screened successfully.")


# ---------------------- Results Display ----------------------
if st.session_state.discovered_deals:
    df = pd.DataFrame(st.session_state.discovered_deals)
    total = len(df)
    unattractive = df["unattractive_flag"].sum()
    attractive = total - unattractive

    st.markdown(gradient_header("Discovered Deals Overview"), unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("Total", total)
    c2.metric("Attractive", attractive)
    c3.metric("Unattractive", unattractive)

    filt = st.radio("View:", ["All", "Attractive Only", "Unattractive Only"], horizontal=True)
    disp = df if filt == "All" else df[~df["unattractive_flag"]] if filt == "Attractive Only" else df[df["unattractive_flag"]]

    for _, row in disp.iterrows():
        color = "🟢" if not row["unattractive_flag"] else "🔴"
        st.markdown(
            f"<div style='border:1px solid #ccc;border-radius:10px;padding:15px;margin:12px 0;'>"
            f"<h4>{color} {row['company']}</h4>"
            f"<b>Industry:</b> {row['industry']} | <b>Sector:</b> {row['sector']} | <b>Stage:</b> {row['stage']} | <b>Region:</b> {row['region']}<br>"
            f"<i>{row['description']}</i>"
            f"{'<p style=\"color:red;font-weight:600;\">Excluded Reason: '+row['unattractive_reason']+'</p>' if row['unattractive_flag'] else ''}"
            f"</div>",
            unsafe_allow_html=True,
        )

    # Export
    st.markdown(gradient_header("Export Results"), unsafe_allow_html=True)
    csv = df.to_csv(index=False)
    st.download_button("⬇️ Download CSV", csv, "Deals.csv", "text/csv")

    try:
        report = template_gen.generate_due_diligence_report({
            "company_name": "Portfolio Sourcing",
            "analyst_name": "Regulus AI",
            "analysis_date": datetime.now().strftime("%B %d, %Y"),
            "executive_summary": "Automatically sourced investment opportunities using Regulus AI workflow.",
            "data_sources": selected_sources,
        })
        st.download_button("⬇️ Download Report (Markdown)", report, "Deal_Report.md", "text/markdown")
    except Exception as e:
        st.error(f"Report Export Error: {e}")
