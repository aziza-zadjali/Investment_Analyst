"""
Regulus AI – Deal Discovery & Intelligence Dashboard
Full Integration: WebScraper + LLMHandler + TemplateGenerator
Features: 
- Live IR extraction (financials, ESG, PDFs)
- AI-powered Regulus Analyst Summary for each deal  
- Attractive / Excluded badges & dynamic sorting
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

# =============================
# PAGE CONFIG
# =============================
st.set_page_config(page_title="Deal Discovery & AI Analyst Summary", layout="wide", initial_sidebar_state="collapsed")
apply_qdb_styling()

# --- Helper for Logo ---
def encode_image(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f"data:image/png;base64," + base64.b64encode(f.read()).decode()
    return ""

qdb_logo = encode_image("QDB_Logo.png")

# --- Initialize Core Modules ---
@st.cache_resource
def init_modules():
    return WebScraper(), LLMHandler(), TemplateGenerator()

scraper, llm, template_gen = init_modules()

if "discovered_deals" not in st.session_state:
    st.session_state.discovered_deals = []

# =============================
# HEADER SECTION
# =============================
st.markdown(
    f"""
<div style="background:linear-gradient(135deg,#1B2B4D,#2C3E5E);color:white;text-align:center;margin:0 -3rem;padding:60px 20px;position:relative;">
  <div style="position:absolute;top:20px;left:35px;">
    {"<img src='"+qdb_logo+"' style='max-height:60px;'>" if qdb_logo else "<b>QDB</b>"}
  </div>
  <h1 style="font-size:2.3rem;font-weight:700;margin-bottom:10px;">Regulus AI – Deal Discovery & Sourcing</h1>
  <p style="color:#CBD5E0;font-size:0.95rem;">AI-powered sourcing, IR extraction, and analyst-grade summarization</p>
</div>
""",
    unsafe_allow_html=True,
)

# =============================
# VISUAL WORKFLOW TRACKER
# =============================
st.markdown(
    """
<style>
.track{background:#F6F5F2;margin:0 -3rem;padding:18px 40px;display:flex;justify-content:space-between;align-items:center;}
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

# =============================
# FILTERS
# =============================
st.markdown("### Define Discovery Criteria")
st.caption("Configure discovery parameters. The system will pull from startup and company data, extract IR materials, and summarize findings.")

col1, col2, col3, col4 = st.columns(4)
with col1:
    industries = st.multiselect("Industries", ["Technology","Healthcare","Energy","Finance","Manufacturing"], default=["Technology"])
with col2:
    sectors = st.multiselect("Sectors", ["FinTech","HealthTech","AI/ML","SaaS","CleanTech"], default=["FinTech"])
with col3:
    stage = st.multiselect("Stage", ["Pre-Seed","Seed","Series A","Series B","Growth"], default=["Seed"])
with col4:
    geography = st.multiselect("Regions", ["MENA","Europe","North America"], default=["MENA"])

col5, col6 = st.columns(2)
with col5:
    deal_count = st.number_input("Deals to Source", min_value=5, max_value=50, value=6)
with col6:
    unattractive_filter = st.checkbox("Exclude Unattractive Industries (QDB Policy)", True)

# =============================
# DISCOVER BUTTON
# =============================
st.markdown("<br>", unsafe_allow_html=True)
colA, colB, colC = st.columns([1, 0.8, 1])
with colB:
    discover_clicked = st.button("Discover Deals", type="primary", use_container_width=True)

st.markdown(
    """
<style>
div.stButton>button:first-child{
 background:linear-gradient(135deg,#138074,#0e5f55)!important;color:#fff!important;
 border:none!important;border-radius:40px!important;padding:12px 30px!important;
 font-weight:700!important;font-size:0.95rem!important;
 box-shadow:0 4px 10px rgba(19,128,116,0.3)!important;transition:all 0.2s ease;
}
div.stButton>button:first-child:hover{
 background:linear-gradient(135deg,#0e5f55,#138074)!important;
 transform:translateY(-2px)!important;
}
</style>
""",
    unsafe_allow_html=True,
)

# =============================
# DISCOVERY PIPELINE
# =============================
if discover_clicked:
    with st.spinner("Performing startup discovery and real-time IR document extraction..."):
        startups = scraper.scrape_startup_data("demo")
        deals = []

        for s in startups[:deal_count]:
            website = s.get("website","")
            name = s.get("name","")
            try:
                ir_links = scraper.discover_investor_relations(website)
                ir_data = scraper.extract_company_data(website, name)

                ir_summary = ""
                for category, content in ir_data.items():
                    if len(content) > 10:  # summarizable
                        summary_snippet = llm.generate_short_summary(content[:3000])
                        ir_summary += f"### {category.title()}\n{summary_snippet}\n\n"

                analyst_summary = llm.generate_short_summary(
                    f"""
                    Company Name: {name}
                    Industry: {s['industry']}
                    Description: {s['description']}
                    IR Insights: {ir_summary}
                    """
                )

                deals.append({
                    "name": name,
                    "industry": s["industry"],
                    "stage": s["stage"],
                    "funding": s["funding"],
                    "region": s["location"],
                    "website": website,
                    "description": s["description"],
                    "qdb_tag": "Excluded" if unattractive_filter and "CleanTech" not in s["industry"] else "Preferred",
                    "ir_summary": ir_summary or "No IR data detected",
                    "analyst_summary": analyst_summary or "Summary unavailable"
                })
            except Exception as e:
                deals.append({
                    "name": name, "industry": s["industry"], "stage": s["stage"], 
                    "funding": s["funding"], "region": s["location"], 
                    "website": website, "description": s["description"],
                    "qdb_tag": "Preferred", 
                    "ir_summary": "IR data unavailable", "analyst_summary": f"Extraction Error: {e}"
                })

        st.session_state.discovered_deals = deals
        st.success(f"{len(deals)} deals discovered and enriched with Regulus Analyst Summaries.")

# =============================
# OUTPUT DISPLAY
# =============================
if st.session_state.discovered_deals:
    df = pd.DataFrame(st.session_state.discovered_deals)

    st.subheader("Enriched Deals with AI Insights")
    sort_by = st.radio("Sort By:", ["Industry", "Funding Stage", "Ticket Size"], horizontal=True, index=0)

    def parse_ticket(v): 
        if "M" in str(v): return float(v.replace("$","").replace("M",""))
        return 0.0

    df["ticket_value"] = df["funding"].apply(parse_ticket)
    if sort_by=="Industry": df=df.sort_values("industry")
    elif sort_by=="Funding Stage":
        order={"Pre-Seed":1,"Seed":2,"Series A":3,"Series B":4,"Growth":5}
        df["order"]=df["stage"].map(order); df=df.sort_values("order").drop(columns=["order"])
    else: df=df.sort_values("ticket_value",ascending=False)

    df["QDB Status"] = df["qdb_tag"].apply(lambda x:"🟢 Attractive" if "Pref" in x else "🔴 Excluded Sector")
    st.dataframe(df[["QDB Status","name","industry","stage","funding","region","website"]],use_container_width=True)
    st.caption("🟢 = QDB-Aligned | 🔴 = Excluded Sector | Sorted dynamically as per user selection")

    # --- IR Details + Analyst Summaries ---
    st.markdown("<hr>",unsafe_allow_html=True)
    for idx,row in df.iterrows():
        with st.expander(f"{row['name']} – Analytical Summary & IR Data"):
            st.markdown(f"**Industry:** {row['industry']} | **Stage:** {row['stage']} | **Funding:** {row['funding']} | **Region:** {row['region']}")
            st.markdown(f"#### Regulus Analyst Summary")
            st.markdown(row["analyst_summary"])
            st.markdown(f"#### Investor Relations Insights")
            st.markdown(row["ir_summary"])

    # Export
    csv = df.to_csv(index=False)
    st.download_button("Download Full CSV", csv, file_name=f"Deals_{datetime.now().strftime('%Y%m%d')}.csv", mime="text/csv")

# =============================
# FOOTER
# =============================
st.markdown("""
<div style="background:#1B2B4D;color:#E2E8F0;padding:30px 40px;margin:40px -3rem 0 -3rem;">
 <div style="display:flex;justify-content:space-between;align-items:center;max-width:1400px;margin:0 auto;">
  <ul style="list-style:none;display:flex;gap:30px;flex-wrap:wrap;padding:0;margin:0;">
   <li><a href="#" style="color:#E2E8F0;text-decoration:none;">About Regulus</a></li>
   <li><a href="#" style="color:#E2E8F0;text-decoration:none;">Careers</a></li>
   <li><a href="#" style="color:#E2E8F0;text-decoration:none;">Contact Us</a></li>
   <li><a href="#" style="color:#E2E8F0;text-decoration:none;">Privacy Policy</a></li>
  </ul>
  <p style="margin:0;color:#A0AEC0;font-size:0.9rem;">Powered by Regulus AI</p>
 </div>
</div>
""", unsafe_allow_html=True)
