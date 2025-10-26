"""
Deal Discovery & Sourcing – Regulus Edition
Integrated with WebScraper, LLMHandler, TemplateGenerator
AI-powered discovery, IR insights extraction, badges, and analyst summaries
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from utils.web_scraper import WebScraper
from utils.llm_handler import LLMHandler
from utils.template_generator import TemplateGenerator
from utils.qdb_styling import apply_qdb_styling
import base64, os

# ---------------- Page Config ----------------
st.set_page_config(page_title="Deal Discovery – Regulus", layout="wide", initial_sidebar_state="collapsed")
apply_qdb_styling()

# ---------------- Logo Helper ----------------
def encode_image(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f"data:image/png;base64," + base64.b64encode(f.read()).decode()
    return ""
qdb_logo = encode_image("QDB_Logo.png")

# ---------------- Initialize Modules ----------------
@st.cache_resource
def init_modules():
    return WebScraper(), LLMHandler(), TemplateGenerator()
scraper, llm, template_gen = init_modules()
if "deals" not in st.session_state:
    st.session_state.deals = []

# ---------------- Header ----------------
st.markdown(
f"""
<div style="background:linear-gradient(135deg,#1B2B4D,#2C3E5E);
color:white;text-align:center;margin:0 -3rem;padding:60px 20px;">
<div style="position:absolute;top:20px;left:35px;">
{"<img src='"+qdb_logo+"' style='max-height:60px;'>" if qdb_logo else "<b>QDB</b>"}
</div>
<h1 style="font-size:2.2rem;font-weight:700;margin-bottom:10px;">
Deal Discovery & Intelligence
</h1>
<p style="color:#CBD5E0;font-size:0.95rem;">
AI‑powered deal sourcing integrated with IR analysis and LLM summaries
</p>
</div>
""",
unsafe_allow_html=True,
)

# ---------------- Step Tracker ----------------
st.markdown("""
<style>
.track{background:#F6F5F2;margin:0 -3rem;padding:18px 40px;display:flex;
justify-content:space-between;align-items:center;}
.steps{display:flex;align-items:center;gap:12px;justify-content:center;}
.step{display:flex;flex-direction:column;align-items:center;}
.circle{width:42px;height:42px;border-radius:50%;display:flex;justify-content:center;align-items:center;font-weight:700;}
.circle.active{background:#138074;color:white;box-shadow:0 3px 10px rgba(19,128,116,0.4);}
.circle.inactive{background:#D1D5DB;color:#9CA3AF;}
.label{font-size:0.8rem;font-weight:600;margin-top:4px;}
.label.active{color:#138074;}
.label.inactive{color:#9CA3AF;}
.line{height:2px;width:50px;background:#D1D5DB;}
.link{color:#138074;text-decoration:none;font-weight:600;}
.link:hover{color:#0e5f55;}
</style>
<div class="track">
  <a href="streamlit_app.py" class="link">Back to Home</a>
  <div class="steps">
    <div class="step"><div class="circle active">1</div><div class="label active">Deal Sourcing</div></div>
    <div class="line"></div>
    <div class="step"><div class="circle inactive">2</div><div class="label inactive">Due Diligence</div></div>
    <div class="line"></div>
    <div class="step"><div class="circle inactive">3</div><div class="label inactive">Market</div></div>
    <div class="line"></div>
    <div class="step"><div class="circle inactive">4</div><div class="label inactive">Financials</div></div>
    <div class="line"></div>
    <div class="step"><div class="circle inactive">5</div><div class="label inactive">Memo</div></div>
  </div>
  <span style="color:#999;">Regulus AI</span>
</div>
""", unsafe_allow_html=True)

# ---------------- Filters ----------------
st.markdown("### Define Sourcing Criteria")
col1,col2,col3,col4 = st.columns(4)
with col1:
    industries = st.multiselect("Industries",
        ["Technology","Healthcare","CleanTech","Finance","Manufacturing"], ["Technology"])
with col2:
    sectors = st.multiselect("Sectors",
        ["AI","HealthTech","FinTech","ClimateTech","SaaS"], ["FinTech"])
with col3:
    stage = st.multiselect("Funding Stage",
        ["Pre‑Seed","Seed","Series A","Series B","Growth"], ["Seed"])
with col4:
    geo = st.multiselect("Regions",["MENA","Europe","North America"],["MENA"])
col5,col6 = st.columns(2)
with col5:
    deal_count = st.number_input("Number of Deals",5,50,10,5)
with col6:
    unattractive = st.checkbox("Exclude Unattractive (QDB Filter)", True)

st.markdown("<br>", unsafe_allow_html=True)
center = st.columns([1,0.8,1])[1]
with center:
    discover_clicked = st.button("Discover Deals", type="primary", use_container_width=True)

st.markdown("""
<style>
div.stButton>button:first-child{
background:linear-gradient(135deg,#138074,#0e5f55)!important;color:white!important;
border:none!important;border-radius:40px!important;
padding:12px 32px!important;font-weight:700!important;font-size:0.95rem!important;
box-shadow:0 4px 10px rgba(19,128,116,0.3)!important;transition:all 0.2s ease!important;}
div.stButton>button:first-child:hover{
background:linear-gradient(135deg,#0e5f55,#138074)!important;
transform:translateY(-2px)!important;}
</style>
""", unsafe_allow_html=True)

# ---------------- Discovery ----------------
if discover_clicked:
    with st.spinner("Discovering deals and analyzing IR documents via Regulus AI..."):
        startup_list = scraper.scrape_startup_data()
        enriched = []

        for s in startup_list[:deal_count]:
            name, website = s["name"], s["website"]
            ir_data = scraper.extract_company_data(website, name)

            # --- Summarize IR content ---
            ir_summary = ""
            for cat, content in ir_data.items():
                if len(content) > 200:
                    result = llm.summarize(content, max_length="medium")
                    ir_summary += f"### {cat.replace('_',' ').title()}\n{result}\n\n"

            # --- Analyst summary ---
            analyst_summary = llm.summarize(
                f"""
Company Name: {name}
Industry: {s['industry']}
Stage: {s['stage']}
Funding: {s['funding']}
Description: {s['description']}
""",
                max_length="short"
            )

            enriched.append({
                "Company": name,
                "Industry": s["industry"],
                "Stage": s["stage"],
                "Funding": s["funding"],
                "Region": s["location"],
                "Website": website,
                "AnalystSummary": analyst_summary,
                "IR_Summary": ir_summary or "No IR data found.",
                "QDB": "Excluded" if unattractive and "Clean" not in s["industry"] else "Preferred",
            })

        st.session_state.deals = enriched
        st.success(f"{len(enriched)} deals discovered and IR data summarized.")

# ---------------- Display ----------------
if st.session_state.deals:
    df = pd.DataFrame(st.session_state.deals)
    st.markdown("### Discovered Deals & Analyst Insights")
    sort_by = st.radio("Sort results by:", ["Industry","Stage","Funding"], horizontal=True)
    if sort_by == "Industry":
        df = df.sort_values("Industry")
    elif sort_by == "Stage":
        order = {"Pre‑Seed":1,"Seed":2,"Series A":3,"Series B":4,"Growth":5}
        df["ord"] = df["Stage"].map(order)
        df = df.sort_values("ord")
    elif sort_by == "Funding":
        df["FundingValue"] = df["Funding"].str.extract(r"(\\d+)").astype(float)
        df = df.sort_values("FundingValue", ascending=False)

    df["QDB Status"] = df["QDB"].apply(
        lambda x: "🟢 Attractive" if "Pref" in x else "🔴 Excluded Sector")
    st.dataframe(df[["QDB Status","Company","Industry","Stage","Funding","Region","Website"]],
                 use_container_width=True)
    st.caption("🟢 Aligned with QDB Priorities | 🔴 Excluded Sector")

    for _, row in df.iterrows():
        with st.expander(row["Company"]):
            st.markdown(f"**Industry:** {row['Industry']} | **Stage:** {row['Stage']} | **Funding:** {row['Funding']} | **Region:** {row['Region']}")
            st.markdown("#### Regulus Analyst Summary")
            st.markdown(row["AnalystSummary"])
            st.markdown("---\n#### Investor Relations Synopsis")
            st.markdown(row["IR_Summary"])

    csv = df.to_csv(index=False)
    st.download_button(" Download Results (CSV) ", csv, "Deals.csv", "text/csv")

# ---------------- Footer ----------------
st.markdown("""
<div style="background:#1B2B4D;color:#E2E8F0;padding:30px 40px;margin:40px -3rem 0 -3rem;">
<div style="display:flex;justify-content:space-between;align-items:center;max-width:1400px;margin:0 auto;">
<ul style="list-style:none;display:flex;gap:30px;flex-wrap:wrap;padding:0;margin:0;">
<li><a href="#" style="color:#E2E8F0;text-decoration:none;">About Regulus</a></li>
<li><a href="#" style="color:#E2E8F0;text-decoration:none;">Careers</a></li>
<li><a href="#" style="color:#E2E8F0;text-decoration:none;">Contact Us</a></li>
<li><a href="#" style="color:#E2E8F0;text-decoration:none;">Privacy Policy</a></li>
</ul>
<p style="margin:0;color:#A0AEC0;font-size:0.9rem;">Powered by Regulus AI</p></div></div>
""", unsafe_allow_html=True)
