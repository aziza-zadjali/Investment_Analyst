"""
Deal Discovery & Sourcing – Regulus Edition
Teal-branded interface | Step tracker | IR + AI enrichment | Fast UX
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from utils.web_scraper import WebScraper
from utils.llm_handler import LLMHandler
from utils.template_generator import TemplateGenerator

# -----------------------------------
# Streamlit Page Config
# -----------------------------------
st.set_page_config(page_title="Deal Discovery - Regulus", layout="wide", initial_sidebar_state="collapsed")
st.markdown("<style>[data-testid='stSidebar']{display:none;}</style>", unsafe_allow_html=True)

# -----------------------------------
# Theme Helpers
# -----------------------------------
def gradient_title(text):
    return f"<div style='background:linear-gradient(135deg,#138074,#0e5f55);padding:14px 20px;border-radius:12px;color:white;font-weight:600;font-size:1.4rem;text-align:center;margin:25px 0;box-shadow:0 4px 10px rgba(19,128,116,0.3);'>{text}</div>"

# -----------------------------------
# Module Init
# -----------------------------------
@st.cache_resource(show_spinner=False)
def init():
    return WebScraper(), LLMHandler(), TemplateGenerator()
scraper, llm, template = init()

if "deals" not in st.session_state: st.session_state["deals"] = []

# -----------------------------------
# Header & Step Visual
# -----------------------------------
st.markdown(gradient_title("Deal Discovery & Sourcing"), unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#555;'>Automated sourcing, IR documentation analysis & AI summarization</p>", unsafe_allow_html=True)
st.markdown("""
<style>
.steps{display:flex;justify-content:center;align-items:center;gap:20px;margin:15px 0 40px;}
.step{display:flex;flex-direction:column;align-items:center;font-weight:600;font-size:0.85rem;}
.circle{width:42px;height:42px;border-radius:50%;display:flex;align-items:center;justify-content:center;margin-bottom:5px;}
.active{background:#138074;color:#fff;box-shadow:0 3px 8px rgba(19,128,116,0.4);}
.inactive{background:#CBD5E1;color:#9CA3AF;}
.line{width:70px;height:3px;background:#D1D5DB;}
.active .label{color:#138074;}
.inactive .label{color:#9CA3AF;}
</style>
<div class="steps">
  <div class="step active"><div class="circle active">1</div><div class="label">Deal Sourcing</div></div>
  <div class="line"></div>
  <div class="step inactive"><div class="circle inactive">2</div><div class="label">Due Diligence</div></div>
  <div class="line"></div>
  <div class="step inactive"><div class="circle inactive">3</div><div class="label">Market</div></div>
  <div class="line"></div>
  <div class="step inactive"><div class="circle inactive">4</div><div class="label">Financials</div></div>
  <div class="line"></div>
  <div class="step inactive"><div class="circle inactive">5</div><div class="label">Memo</div></div>
</div>
""", unsafe_allow_html=True)

# -----------------------------------
# Filters
# -----------------------------------
st.markdown(gradient_title("Define Investment Criteria"), unsafe_allow_html=True)
col1,col2,col3,col4=st.columns(4)
with col1: industries = st.multiselect("Industries",["Technology","Healthcare","CleanTech","Finance","Retail"],["Technology"])
with col2: sectors=st.multiselect("Sectors",["FinTech","AI/ML","ClimateTech","SaaS","HealthTech"],["FinTech","AI/ML"])
with col3: stages=st.multiselect("Stage",["Pre‑Seed","Seed","Series A","Series B","Growth"],["Seed","Series A"])
with col4: regions=st.multiselect("Regions",["MENA","Europe","North America","Asia"],["MENA","Europe"])
col5,col6=st.columns(2)
with col5: deals_to_get=st.slider("Number of Deals",5,50,10)
with col6: unattractive=st.checkbox("Exclude Unattractive Industries (QDB Policy)",True)

# -----------------------------------
# Discovery
# -----------------------------------
st.markdown(gradient_title("AI‑Powered Deal Discovery"), unsafe_allow_html=True)
colX=st.columns([1,0.8,1])[1]
with colX: click=st.button("Start Discovery",use_container_width=True)

if click:
    with st.spinner("Running discovery engine … extracting IR data and summaries."):
        dataset=scraper.scrape_startup_data()
        results=[]
        progress=st.progress(0)
        total=min(len(dataset),deals_to_get)

        for i,data in enumerate(dataset[:total]):
            try:
                name=data["name"]; web=data["website"]
                ir=scraper.extract_company_data(web,name)
                ir_summary=""
                for k,v in ir.items():
                    if len(v)>150:
                        ir_summary+=f"### {k.title()}\n{llm.summarize(v,max_length='medium')}\n\n"
                analyst=llm.summarize(
                    f"Company:{name}\nIndustry:{data['industry']}\nDescription:{data['description']}\nStage:{data['stage']}",
                    max_length="short"
                )

                unattractive_flag=False
                if unattractive and any(bad in data['description'].lower() for bad in["bakery","cement","laundry","salon","plastic"]):
                    unattractive_flag=True

                results.append({
                    "Company":name,"Industry":data["industry"],"Stage":data["stage"],
                    "Funding":data["funding"],"Region":data["location"],
                    "Description":data["description"],
                    "Analyst Summary":analyst,
                    "IR Insights":ir_summary or "No IR content available.",
                    "Excluded":unattractive_flag
                })
            except Exception as e: st.warning(f"Error parsing {name}: {e}")
            progress.progress((i+1)/total)
        st.session_state.deals=results
        st.success(f"{len(results)} opportunities analyzed using Regulus AI.")

# -----------------------------------
# Display Results
# -----------------------------------
if st.session_state.deals:
    df=pd.DataFrame(st.session_state.deals)
    total=len(df); excluded=sum(df["Excluded"]); attractive=total-excluded
    st.markdown(gradient_title("Discovered Deals Overview"),unsafe_allow_html=True)
    c1,c2,c3=st.columns(3)
    c1.metric("Total",total); c2.metric("Attractive",attractive); c3.metric("Excluded",excluded)

    sel=st.radio("Show:",["All","Attractive Only","Excluded Only"],horizontal=True)
    if sel=="All": disp=df
    elif sel=="Attractive Only": disp=df[~df.Excluded]
    else: disp=df[df.Excluded]

    for _,r in disp.iterrows():
        st.markdown(
            f"<div style='border:1px solid #DDD;border-radius:10px;padding:16px;margin:12px 0;'>"
            f"<h4 style='margin-bottom:6px;'>{r['Company']} {'🟢' if not r['Excluded'] else '🔴'}</h4>"
            f"<p><b>Industry:</b> {r['Industry']} | <b>Stage:</b> {r['Stage']} | <b>Funding:</b> {r['Funding']} | <b>Region:</b> {r['Region']}</p>"
            f"<i>{r['Description']}</i>"
            f"{'<p style=\"color:red;font-weight:600;\">Excluded as unattractive sector.</p>' if r['Excluded'] else ''}"
            f"<details><summary style='color:#138074;font-weight:600;margin-top:5px;'>Regulus Analyst Summary</summary><p>{r['Analyst Summary']}</p></details>"
            f"<details><summary style='color:#0e5f55;font-weight:600;'>Investor Relations Insights</summary><p>{r['IR Insights']}</p></details>"
            f"</div>",unsafe_allow_html=True)

    st.markdown(gradient_title("Export Options"),unsafe_allow_html=True)
    csv=df.to_csv(index=False)
    st.download_button("Download CSV",csv,"Deals.csv","text/csv")

    try:
        md=template.generate_due_diligence_report({
            "company_name":"Multi‑Company Batch",
            "analyst_name":"Regulus AI",
            "analysis_date":datetime.now().strftime("%B %d, %Y"),
            "executive_summary":"This report summarizes discovered deals and AI insights.",
            "data_sources":["Crunchbase","AngelList","Dealroom"]
        })
        st.download_button("Download Report (Markdown)",md,"Deal_Report.md","text/markdown")
    except Exception as e:
        st.error(f"Report build failed: {e}")
