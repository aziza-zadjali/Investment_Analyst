"""
Deal Discovery & Sourcing – Regulus Edition
Integrated with WebScraper, LLMHandler, TemplateGenerator
Features:
 🟢 Live scraping  |  🟡 Industry Filtering |  🔵 Analyst Summarization |  🟣 Visual Badges & Sorting
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from utils.web_scraper import WebScraper
from utils.llm_handler import LLMHandler
from utils.template_generator import TemplateGenerator
from utils.qdb_styling import apply_qdb_styling
import base64
import os

# --- Streamlit Config ---
st.set_page_config(page_title="Deal Discovery - Regulus", layout="wide", initial_sidebar_state="collapsed")
apply_qdb_styling()

# --- Helper for Logos ---
def encode_image(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f"data:image/png;base64," + base64.b64encode(f.read()).decode()
    return ""

qdb_logo = encode_image("QDB_Logo.png")

# --- Safe Initialization ---
@st.cache_resource
def init_modules():
    return WebScraper(), LLMHandler(), TemplateGenerator()

# Initialize and ensure no recursion
scraper, llm, template_gen = init_modules()

# --- Session Data ---
if "discovered_deals" not in st.session_state:
    st.session_state.discovered_deals = []

# ======================================================
# HEADER
# ======================================================
st.markdown(
    f"""
<div style="background:linear-gradient(135deg,#1B2B4D,#2C3E5E);
color:white;text-align:center;margin:0 -3rem;padding:60px 20px;position:relative;">
 <div style="position:absolute;top:20px;left:35px;">
  {"<img src='"+qdb_logo+"' style='max-height:60px;'>" if qdb_logo else "<b>QDB</b>"}
 </div>
 <h1 style="font-size:2.2rem;font-weight:700;margin-bottom:10px;">
  Deal Discovery & Sourcing
 </h1>
 <p style="color:#CBD5E0;font-size:0.95rem;">
  AI‑powered multi‑source sourcing, live IR data extraction & QDB priority analysis
 </p>
</div>
""",
    unsafe_allow_html=True,
)

# ======================================================
# VISUAL STEP TRACKER
# ======================================================
st.markdown(
    """
<style>
.track{background:#F6F5F2;margin:0 -3rem;padding:18px 40px;
display:flex;justify-content:space-between;align-items:center;}
.steps{display:flex;align-items:center;gap:12px;justify-content:center;}
.step{display:flex;flex-direction:column;align-items:center;}
.circle{width:42px;height:42px;border-radius:50%;
display:flex;justify-content:center;align-items:center;font-weight:700;}
.circle.active{background:#138074;color:white;
box-shadow:0 3px 10px rgba(19,128,116,0.4);}
.circle.inactive{background:#D1D5DB;color:#9CA3AF;}
.label{font-size:0.8rem;font-weight:600;margin-top:4px;}
.label.active{color:#138074;}
.label.inactive{color:#9CA3AF;}
.line{height:2px;width:50px;background:#D1D5DB;}
.link{color:#138074;text-decoration:none;font-weight:600;}
.link:hover{color:#0e5f55;}
</style>
<div class="track">
  <a href="streamlit_app.py" class="link">Back to Home</a>
  <div class="steps">
    <div class="step"><div class="circle active">1</div><div class="label active">Deal Sourcing</div></div>
    <div class="line"></div>
    <div class="step"><div class="circle inactive">2</div><div class="label inactive">Due Diligence</div></div>
    <div class="line"></div>
    <div class="step"><div class="circle inactive">3</div><div class="label inactive">Market</div></div>
    <div class="line"></div>
    <div class="step"><div class="circle inactive">4</div><div class="label inactive">Financials</div></div>
    <div class="line"></div>
    <div class="step"><div class="circle inactive">5</div><div class="label inactive">Memo</div></div>
  </div>
  <span style="color:#999;">Regulus AI</span>
</div>
""",
    unsafe_allow_html=True,
)

# ======================================================
# FILTERS SECTION
# ======================================================
st.markdown("### Define Sourcing Parameters")
st.caption("Configure filters for AI‑driven discovery and automatic QDB compliance screening.")

col1, col2, col3, col4 = st.columns(4)
with col1:
    industries = st.multiselect("Target Industries",
        ["Technology", "Healthcare", "CleanTech", "Finance", "Retail", "Manufacturing"],
        default=["Technology"])
with col2:
    sectors = st.multiselect("Target Sectors",
        ["AI", "FinTech", "HealthTech", "ClimateTech", "SaaS"],
        default=["FinTech"])
with col3:
    stage = st.multiselect("Funding Stage",
        ["Pre-Seed", "Seed", "Series A", "Series B", "Growth"],
        default=["Seed"])
with col4:
    geography = st.multiselect("Regions",
        ["MENA", "Europe", "North America"], default=["MENA"])

col5, col6 = st.columns(2)
with col5:
    deal_count = st.number_input("Number of Deals to Source", 5, 50, 10, 5)
with col6:
    unattractive_filter = st.checkbox("Exclude Unattractive Industries (QDB Filter)", True)

st.markdown("<br>", unsafe_allow_html=True)
center = st.columns([1, 0.8, 1])[1]
with center:
    discover = st.button("Discover Deals", type="primary", use_container_width=True)

st.markdown(
    """
<style>
div.stButton>button:first-child{
 background:linear-gradient(135deg,#138074,#0e5f55)!important;color:white!important;
 border:none!important;border-radius:40px!important;padding:12px 32px!important;
 font-weight:700!important;font-size:0.95rem!important;
 box-shadow:0 4px 10px rgba(19,128,116,0.3)!important;
 transition:all 0.2s ease!important;}
div.stButton>button:first-child:hover{
 background:linear-gradient(135deg,#0e5f55,#138074)!important;
 transform:translateY(-2px)!important;}
</style>
""",
    unsafe_allow_html=True,
)

# ======================================================
# DEAL DISCOVERY EXECUTION
# ======================================================
if discover:
    with st.spinner("Fetching live data and performing IR document analysis..."):
        data = scraper.scrape_startup_data("demo")
        deals = []

        for d in data[:deal_count]:
            website = d.get("website", "")
            name = d.get("name", "")
            industry = d.get("industry", "")
            try:
                ir = scraper.extract_company_data(website, name)
                full_summary = ""
                for cat, txt in ir.items():
                    if len(txt) > 60:
                        summary = llm.generate_short_summary(txt[:3000])
                        full_summary += f"### {cat.title()}\n{summary}\n\n"
                analyst_summary = llm.generate_short_summary(
                    f"Company: {name}\nIndustry: {industry}\nIR Data: {full_summary}"
                )
            except Exception:
                full_summary, analyst_summary = "Data unavailable", "No analyst overview generated"

            deals.append({
                "name": name,
                "industry": industry,
                "stage": d.get("stage", ""),
                "funding": d.get("funding", ""),
                "region": d.get("location", ""),
                "website": website,
                "description": d.get("description", ""),
                "ir_summary": full_summary,
                "analyst_summary": analyst_summary,
                "qdb_priority": "Excluded" if unattractive_filter and (industry not in ["CleanTech","Tech","Healthcare"]) else "Preferred"
            })

        st.session_state.discovered_deals = deals
        st.success("Discovery complete. Analyst summaries attached for each deal.")

# ======================================================
# DISPLAY RESULTS
# ======================================================
if st.session_state.discovered_deals:
    df = pd.DataFrame(st.session_state.discovered_deals)
    st.subheader("🟢 AI‑Enriched Discovered Deals")
    sort_opt = st.radio("Sort results by:", ["Industry", "Funding Stage", "Ticket Size"], horizontal=True)

    def to_float(v): return float(v.replace("$","").replace("M","")) if "M" in str(v) else 0.0
    df["ticket_value"] = df["funding"].apply(to_float)

    if sort_opt == "Funding Stage":
        order={"Pre-Seed":1,"Seed":2,"Series A":3,"Series B":4,"Growth":5}
        df["stage_order"]=df["stage"].map(order)
        df=df.sort_values(["stage_order","industry"]).drop(columns=["stage_order"])
    elif sort_opt == "Ticket Size":
        df=df.sort_values("ticket_value",ascending=False)
    else:
        df=df.sort_values("industry")

    df["QDB Status"] = df["qdb_priority"].apply(lambda x:"🟢 Attractive" if "Pref" in x else "🔴 Excluded Sector")
    st.caption("🟢 = QDB‑aligned | 🔴 = Excluded Sector | Includes Analyst Insights & IR Extracts")
    st.dataframe(df[["QDB Status","name","industry","stage","funding","description","region","website"]],use_container_width=True)

    st.markdown("<hr>",unsafe_allow_html=True)
    for i,row in df.iterrows():
        with st.expander(f"{row['name']} – Regulus Analyst Summary & IR Insights"):
            st.markdown(f"**Industry:** {row['industry']} | **Stage:** {row['stage']} | **Funding:** {row['funding']} | **Region:** {row['region']}")
            st.markdown("#### Regulus Analyst Summary")
            st.markdown(row["analyst_summary"])
            st.markdown("#### Investor Relations Extracts")
            st.markdown(row["ir_summary"])

    st.download_button("Download Full Report (CSV)",
        data=df.to_csv(index=False),
        file_name=f"Deals_{datetime.now().strftime('%Y%m%d')}.csv", mime="text/csv")

# ======================================================
# FOOTER
# ======================================================
st.markdown(
    """
<div style="background:#1B2B4D;color:#E2E8F0;
padding:30px 40px;margin:40px -3rem 0 -3rem;">
 <div style="display:flex;justify-content:space-between;align-items:center;
 max-width:1400px;margin:0 auto;">
  <ul style="list-style:none;display:flex;gap:30px;flex-wrap:wrap;
  padding:0;margin:0;">
   <li><a href="#" style="color:#E2E8F0;text-decoration:none;">About Regulus</a></li>
   <li><a href="#" style="color:#E2E8F0;text-decoration:none;">Careers</a></li>
   <li><a href="#" style="color:#E2E8F0;text-decoration:none;">Contact Us</a></li>
   <li><a href="#" style="color:#E2E8F0;text-decoration:none;">Privacy Policy</a></li>
  </ul>
  <p style="margin:0;color:#A0AEC0;font-size:0.9rem;">Powered by Regulus AI</p>
 </div>
</div>
""",
    unsafe_allow_html=True,
)
