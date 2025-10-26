"""
Deal Discovery & Sourcing | Regulus x QDB
QDB-branded design | Workflow step ribbon | Ticket size filter | Robust execution
"""

import streamlit as st
import pandas as pd
import random
from datetime import datetime
from utils.qdb_styling import apply_qdb_styling, qdb_section_start, qdb_section_end, QDB_DARK_BLUE
from utils.llm_handler import LLMHandler

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Deal Sourcing | Regulus AI",
    layout="wide",
    initial_sidebar_state="collapsed",
)
apply_qdb_styling()

# ---------- HERO ----------
st.markdown(
    f"""
<div style="background:linear-gradient(135deg,#1B2B4D 0%,#2C3E5E 100%);
    color:white;text-align:center;margin:0 -3rem;padding:75px 20px 65px;position:relative;">
  <h1 style="font-size:2.3rem;font-weight:700;">Deal Discovery & Sourcing</h1>
  <p style="color:#CBD5E0;font-size:1rem;max-width:740px;margin:10px auto;">
    AI-powered sourcing and qualification engine – refined by Regulus LLMs and QDB’s strategic insight.
  </p>
</div>
""",
    unsafe_allow_html=True,
)

# ---------- WORKFLOW (ribbon style identical to screenshot) ----------
st.markdown(
    """
<style>
.workflow{background:#F6F5F2;margin:0 -3rem;padding:30px 45px 20px;
display:flex;justify-content:center;align-items:flex-start;gap:90px;flex-wrap:nowrap;}
.step{text-align:center;position:relative;}
.circle{width:46px;height:46px;border-radius:50%;
display:flex;align-items:center;justify-content:center;font-weight:700;}
.active{background-color:#138074;color:#fff;box-shadow:0 3px 10px rgba(19,128,116,0.4);}
.inactive{background-color:#CBD5E0;color:#475569;}
.label{margin-top:8px;font-weight:600;font-size:0.88rem;}
.label.active{color:#138074;}
.label.inactive{color:#94A3B8;}
.connector{position:absolute;top:22px;right:-65px;width:130px;height:2px;background-color:#CBD5E0;}
.step:last-child .connector{display:none;}
</style>

<div class="workflow">
  <div class="step"><div class="circle active">1</div><div class="label active">Deal Sourcing</div><div class="connector"></div></div>
  <div class="step"><div class="circle inactive">2</div><div class="label inactive">Due Diligence</div><div class="connector"></div></div>
  <div class="step"><div class="circle inactive">3</div><div class="label inactive">Market Analysis</div><div class="connector"></div></div>
  <div class="step"><div class="circle inactive">4</div><div class="label inactive">Financial Modeling</div><div class="connector"></div></div>
  <div class="step"><div class="circle inactive">5</div><div class="label inactive">Investment Memo</div></div>
</div>
""",
    unsafe_allow_html=True,
)

# ========== INPUT SECTION ==========
qdb_section_start("light")
st.markdown(
    f"""
<div style='text-align:center;max-width:940px;margin:auto;'>
  <h2 style='color:{QDB_DARK_BLUE};font-weight:700;font-size:1.8rem;margin-bottom:6px;'>Set Sourcing Parameters</h2>
  <p style='color:#555;font-size:1.05rem;'>Refine your deal criteria for AI discovery. Filter by industry, stage, region & ticket size.</p>
</div>
""",
    unsafe_allow_html=True,
)

# ---- search filters ----
cols1 = st.columns(3)
with cols1[0]:
    industries = st.multiselect(
        "Industries",
        ["Technology", "Healthcare", "Finance", "Energy", "Manufacturing", "Agritech"],
        ["Technology"],
    )
with cols1[1]:
    regions = st.multiselect(
        "Regions",
        ["MENA", "Europe", "North America", "Asia Pacific"],
        ["MENA"],
    )
with cols1[2]:
    stage = st.selectbox(
        "Funding Stage", ["Pre‑Seed", "Seed", "Series A", "Series B", "Growth"]
    )

cols2 = st.columns([2, 1])
with cols2[0]:
    keywords = st.text_input("Keywords", "AI, Fintech, Green Tech")
with cols2[1]:
    ticket_range = st.slider("Ticket Size (USD M)", 1.0, 50.0, (2.0, 10.0), step=0.5)

st.markdown("<br>", unsafe_allow_html=True)

# -------- DEAL DISCOVERY EXECUTION --------
cA, cB, cC = st.columns([1, 0.7, 1])
with cB:
    run_btn = st.button("🚀 Discover Deals", use_container_width=True)

qdb_section_end()
st.markdown("<br>", unsafe_allow_html=True)

# ========== EXECUTION LOGIC ==========
if run_btn:
    st.markdown("<hr>", unsafe_allow_html=True)
    st.header("Discovery and Sourcing in Progress")

    # placeholder simulated dataset
    progress = st.progress(0)
    deal_results = []
    total = 10
    for i in range(total):
        progress.progress((i + 1) / total)
        deal_results.append(
            {
                "Company": f"Startup {i+1}",
                "Industry": random.choice(industries or ["Technology"]),
                "Region": random.choice(regions or ["Global"]),
                "Stage": stage,
                "Ticket Size": f"${random.randint(int(ticket_range[0]), int(ticket_range[1]))} M",
                "Founded": str(random.randint(2016, 2023)),
                "Employees": random.randint(10, 200),
                "Contact Name": f"CEO {i+1}",
                "Contact Email": f"startup{i+1}@mail.com",
            }
        )

    st.success(f"✅ Discovered {len(deal_results)} potential deals matching your parameters.")

    qdb_section_start("white")
    st.subheader("Recommended Deals 📊")
    df = pd.DataFrame(deal_results)
    st.dataframe(df, use_container_width=True)
    qdb_section_end()

    # ---- optional AI summary ----
    with st.spinner("Generating AI summary…"):
        try:
            llm = LLMHandler()
            text_query = (
                f"Summarize {len(deal_results)} startup deals found in industries {', '.join(industries)} "
                f"within regions {', '.join(regions)} for {stage} stage, ticket ${ticket_range[0]}‑{ticket_range[1]} M."
            )
            result = llm.generate_text(text_query)
            if result and result.strip():
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("### AI Highlights 🔍")
                st.markdown(result)
            else:
                st.warning("⚠️ No AI summary available for current results.")
        except Exception as e:
            st.warning(f"⚠️ AI response not available — {e}")

    # ---- next step ----
    st.markdown(
        f"""
        <div style="background-color:#F6F5F2;padding:60px 20px;margin:60px -3rem -2rem;text-align:center;">
          <h3 style="color:{QDB_DARK_BLUE};font-size:1.6rem;margin-bottom:10px;">Workflow Next Step</h3>
          <p style="color:#555;margin-bottom:30px;">Continue to due diligence for compliance and performance screening.</p>
          <a href="?page=dd" style="
              background-color:#319795;color:white;text-decoration:none;
              border-radius:40px;padding:12px 35px;font-weight:600;
              box-shadow:0 3px 10px rgba(49,151,149,0.3);">→ Proceed to Due Diligence</a>
        </div>
        """,
        unsafe_allow_html=True,
    )
