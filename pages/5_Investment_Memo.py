"""
Investment Memo & Pitch Deck Generator
FIXED: Properly handles markdown to DOCX conversion with Document object
"""
import streamlit as st
import base64
import os
from datetime import datetime
from io import BytesIO
from utils.qdb_styling import apply_qdb_styling
from utils.llm_handler import LLMHandler
from utils.template_generator import TemplateGenerator

st.set_page_config(page_title="Investment Memo", page_icon="📋", layout="wide", initial_sidebar_state="collapsed")
apply_qdb_styling()

# ===== Initialize Handlers =====
@st.cache_resource
def init_handlers():
    try:
        llm = LLMHandler()
        template_gen = TemplateGenerator()
        return llm, template_gen
    except Exception as e:
        st.error(f"Error initializing handlers: {e}")
        return None, None

llm, template_gen = init_handlers()

if llm is None or template_gen is None:
    st.error("Failed to initialize handlers")
    st.stop()

# ===== Image Loader =====
def encode_image(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f"data:image/png;base64,{base64.b64encode(f.read()).decode()}"
    return None

qdb_logo = encode_image("QDB_Logo.png")
regulus_logo = encode_image("regulus_logo.png")

# ===== Session State =====
if 'memo_complete' not in st.session_state:
    st.session_state.memo_complete = False
if 'pitch_deck_content' not in st.session_state:
    st.session_state.pitch_deck_content = ""
if 'memo_data' not in st.session_state:
    st.session_state.memo_data = {}

# ===== CUSTOM STYLING =====
st.markdown("""
<style>
.stButton>button {
    background: linear-gradient(135deg,#16A085 0%,#138074 100%)!important;
    color:white!important;
    border:none!important;
    border-radius:8px!important;
    padding:12px 24px!important;
    font-weight:700!important;
    font-size:0.95rem!important;
    box-shadow:0 4px 12px rgba(22,160,133,0.3)!important;
    transition:all 0.25s ease!important;
}

.stButton>button:hover{
    background: linear-gradient(135deg,#0E5F55 0%,#107563 100%)!important;
    transform:translateY(-2px)!important;
    box-shadow:0 6px 18px rgba(22,160,133,0.4)!important;
}

.section-beige {
    background-color: #F6F5F2;
    border-radius: 10px;
    padding: 20px;
    margin: 12px 0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}

.required-asterisk {
    color: #E74C3C;
    font-weight: 700;
    margin-left: 2px;
}
</style>
""", unsafe_allow_html=True)

# ===== HERO HEADER =====
st.markdown(f"""
<div style="
    background: linear-gradient(135deg,#1B2B4D 0%,#2C3E5E 100%);
    color: white;
    text-align: center;
    margin: 0 -3rem;
    padding: 40px 20px 50px 20px;
    position: relative;
    overflow:visible;
    width: calc(100% + 6rem);
    border-bottom: 3px solid #16A085;">

  <div style="position:absolute; top:15px; left:35px;">
    {'<img src="'+qdb_logo+'" style="max-height:55px;">' if qdb_logo else ''}
  </div>

  <div style="position:absolute; top:15px; right:35px;">
    {'<img src="'+regulus_logo+'" style="max-height:55px;">' if regulus_logo else ''}
  </div>

  <div style="max-width:800px; margin:0 auto;">
    <h1 style="font-size:2rem; font-weight:800; margin-bottom:6px;">Investment Memorandum</h1>
    <p style="color:#E2E8F0; font-size:0.95rem; margin:0;">Generate professional pitch decks from investment data</p>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

# ===== HOME BUTTON =====
if st.button("← Return Home", key="home_btn"):
    st.switch_page("streamlit_app.py")

st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

# ===== MEMO INFORMATION SECTION =====
st.markdown('<div class="section-beige"><div style="font-size:1.2rem; font-weight:700; color:#1B2B4D; margin-bottom:12px;">Investment Memorandum Details</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown("<div style='color:#1B2B4D; font-size:0.85rem; margin-bottom:4px; font-weight:600;'>Company Name <span class='required-asterisk'>*</span></div>", unsafe_allow_html=True)
    company_name = st.text_input("Company Name", placeholder="e.g., TechStartup Inc", label_visibility="collapsed", key="company")

with col2:
    st.markdown("<div style='color:#1B2B4D; font-size:0.85rem; margin-bottom:4px; font-weight:600;'>Industry <span class='required-asterisk'>*</span></div>", unsafe_allow_html=True)
    industry = st.text_input("Industry", placeholder="e.g., FinTech", label_visibility="collapsed", key="industry")

col3, col4 = st.columns(2)
with col3:
    st.markdown("<div style='color:#1B2B4D; font-size:0.85rem; margin-bottom:4px; font-weight:600;'>Annual Revenue (ARR)</div>", unsafe_allow_html=True)
    arr = st.text_input("Annual Revenue", placeholder="e.g., $5M", label_visibility="collapsed", key="arr")

with col4:
    st.markdown("<div style='color:#1B2B4D; font-size:0.85rem; margin-bottom:4px; font-weight:600;'>Growth Rate YoY</div>", unsafe_allow_html=True)
    growth_rate = st.text_input("Growth Rate", placeholder="e.g., 35%", label_visibility="collapsed", key="growth")

# ===== FINANCIAL METRICS =====
col5, col6, col7 = st.columns(3)
with col5:
    st.markdown("<div style='color:#1B2B4D; font-size:0.85rem; margin-bottom:4px; font-weight:600;'>Gross Margin</div>", unsafe_allow_html=True)
    gross_margin = st.text_input("Gross Margin", placeholder="e.g., 70%", label_visibility="collapsed", key="gm")

with col6:
    st.markdown("<div style='color:#1B2B4D; font-size:0.85rem; margin-bottom:4px; font-weight:600;'>Monthly Burn Rate</div>", unsafe_allow_html=True)
    burn_rate = st.text_input("Burn Rate", placeholder="e.g., $150K", label_visibility="collapsed", key="br")

with col7:
    st.markdown("<div style='color:#1B2B4D; font-size:0.85rem; margin-bottom:4px; font-weight:600;'>LTV/CAC Ratio</div>", unsafe_allow_html=True)
    ltv_cac = st.text_input("LTV/CAC Ratio", placeholder="e.g., 3.5", label_visibility="collapsed", key="ltv")

# ===== KEY BUSINESS DATA =====
col8, col9 = st.columns(2)
with col8:
    st.markdown("<div style='color:#1B2B4D; font-size:0.85rem; margin-bottom:4px; font-weight:600;'>Market TAM</div>", unsafe_allow_html=True)
    tam = st.text_input("TAM", placeholder="e.g., $2.5B", label_visibility="collapsed", key="tam")

with col9:
    st.markdown("<div style='color:#1B2B4D; font-size:0.85rem; margin-bottom:4px; font-weight:600;'>Investment Ask</div>", unsafe_allow_html=True)
    investment_ask = st.text_input("Investment Ask", placeholder="e.g., $5M", label_visibility="collapsed", key="ask")

# ===== QUALITATIVE DATA =====
st.markdown("<div style='color:#1B2B4D; font-size:0.85rem; margin-bottom:4px; font-weight:600;'>Competitive Advantage</div>", unsafe_allow_html=True)
competitive_advantage = st.text_area("Competitive Advantage", placeholder="e.g., Proprietary AI technology with 95% accuracy", height=80, label_visibility="collapsed", key="comp_adv")

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

# ===== GENERATE BUTTON =====
if st.button("Generate Pitch Deck", use_container_width=True, key="gen_btn"):
    if not company_name or not industry:
        st.error("❌ Please enter company name and industry")
        st.stop()

    with st.spinner("🔄 Generating pitch deck..."):
        try:
            # Compile memo data
            memo_data = {
                'company_name': company_name,
                'industry': industry,
                'arr': arr or '$TBD',
                'growth_rate': growth_rate or 'TBD',
                'gross_margin': gross_margin or '60-75%',
                'burn_rate': burn_rate or '<$200K/mo',
                'ltv_cac_ratio': ltv_cac or '3.0+',
                'tam': tam or '$TBD',
                'investment_ask': investment_ask or '$TBD',
                'competitive_advantage': competitive_advantage or 'Technology differentiation',
                'analysis_date': datetime.now().strftime('%B %d, %Y'),
                'analyst_name': 'Regulus AI Investment Platform',
            }
            
            st.session_state.memo_data = memo_data
            
            # Step 1: Generate pitch deck (returns string)
            st.info("📝 Creating pitch deck content...")
            pitch_content = template_gen.generate_pitch_deck(memo_data)
            
            # Verify we got a string
            if not isinstance(pitch_content, str):
                raise TypeError(f"generate_pitch_deck() must return string, got {type(pitch_content)}")
            
            st.session_state.pitch_deck_content = pitch_content
            st.success("✅ Pitch deck content created")
            
            st.session_state.memo_complete = True
            st.success("✅ Investment Memo Generated!")

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            import traceback
            st.error(traceback.format_exc())
            st.stop()

st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

# ===== DOWNLOAD & PREVIEW SECTION =====
if st.session_state.memo_complete and st.session_state.pitch_deck_content:
    st.markdown('<div class="section-beige"><div style="font-size:1.2rem; font-weight:700; color:#1B2B4D; margin-bottom:12px;">📥 Download Pitch Deck</div>', unsafe_allow_html=True)
    
    col_dl1, col_dl2, col_dl3 = st.columns([2, 1, 1])
    
    with col_dl1:
        try:
            # Step 2: Convert markdown to DOCX (returns Document object)
            docx_doc = template_gen.markdown_to_docx(st.session_state.pitch_deck_content)
            
            # Verify we got a Document object with .save() method
            if not hasattr(docx_doc, 'save'):
                raise TypeError(f"markdown_to_docx() must return Document object with .save() method, got {type(docx_doc)}")
            
            # Step 3: Save to BytesIO buffer
            docx_buffer = BytesIO()
            docx_doc.save(docx_buffer)
            docx_bytes = docx_buffer.getvalue()
            
            # Step 4: Create download button
            st.download_button(
                label="📄 Download Pitch Deck (DOCX)",
                data=docx_bytes,
                file_name=f"{st.session_state.memo_data.get('company_name', 'Company')}_Pitch_Deck_{datetime.now().strftime('%Y%m%d')}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )
            st.success("✅ DOCX Download Ready")
            
        except TypeError as te:
            st.error(f"❌ Type Error: {str(te)}")
            st.error("**Issue:** markdown_to_docx() not returning Document object")
        except Exception as e:
            st.error(f"❌ Download Error: {str(e)}")
            import traceback
            st.error(traceback.format_exc())
    
    with col_dl2:
        st.info("✅ Ready")
    
    with col_dl3:
        if st.button("📋 Copy", key="copy_btn"):
            st.success("Ready to share")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
    
    # ===== FULL PITCH DECK PREVIEW =====
    st.markdown('<div class="section-beige"><div style="font-size:1.2rem; font-weight:700; color:#1B2B4D; margin-bottom:12px;">🎯 Pitch Deck Preview</div>', unsafe_allow_html=True)
    
    # Display in expandable sections for better readability
    with st.expander("📖 View Full Pitch Deck", expanded=True):
        st.markdown(st.session_state.pitch_deck_content)
    
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)

# ===== FOOTER =====
st.markdown(f"""
<div style="
    background-color:#1B2B4D;
    color:#E2E8F0;
    padding:28px 40px;
    margin:40px -3rem -2rem -3rem;
    font-size:0.92rem;
    width: calc(100% + 6rem);">
  <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; max-width:1400px; margin:auto;">
    <div style="flex:2;">
      <ul style="list-style:none; display:flex; gap:30px; flex-wrap:wrap; padding:0; margin:0;">
        <li><a href="#" style="text-decoration:none; color:#E2E8F0; font-weight:500;">About</a></li>
        <li><a href="#" style="text-decoration:none; color:#E2E8F0; font-weight:500;">Contact</a></li>
      </ul>
    </div>
    <div style="flex:1; text-align:right; display:flex; align-items:center; justify-content:flex-end; gap:12px;">
      <p style="margin:0; color:#A0AEC0; font-size:0.88rem; font-weight:600;">Powered by Regulus AI</p>
      {'<img src="'+regulus_logo+'" style="max-height:45px; opacity:0.92;">' if regulus_logo else ''}
    </div>
  </div>
</div>
""", unsafe_allow_html=True)
