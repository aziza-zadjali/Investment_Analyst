# ==== RESULTS DISPLAY ====
if st.session_state.memo_complete and st.session_state.get('memo_data'):
    st.markdown("---")
    st.markdown("""
<div style="background:white;margin:30px -3rem 0 -3rem;padding:45px 3rem;
border-top:3px solid #138074;box-shadow:0 0 12px rgba(0,0,0,0.05);">
<h2 style="text-align:center;color:#1B2B4D;font-weight:700;">Investment Memo Generated</h2>
</div>
""", unsafe_allow_html=True)
    
    # Download DOCX Only
    try:
        doc = template_gen.markdown_to_docx(st.session_state.memo_content)
        bio = BytesIO()
        doc.save(bio)
        col_center = st.columns([1, 1, 1])[1]
        with col_center:
            st.download_button(
                "Download Investment Memo (DOCX)",
                bio.getvalue(),
                f"Investment_Memo_{st.session_state.memo_data['company_name'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.docx",
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )
    except Exception as e:
        st.error(f"DOCX generation error: {str(e)}")
    
    # Preview
    with st.expander("View Full Memo", expanded=True):
        st.markdown(st.session_state.memo_content)
    
    # Completion Message
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(f"""
<div style='background:linear-gradient(135deg,{QDB_PURPLE} 0%,{QDB_DARK_BLUE} 100%);
border-radius:12px;padding:40px;color:white;text-align:center;'>
<h2 style='margin:0 0 10px 0;'>Workflow Complete!</h2>
<p style='margin:0;font-size:1.1rem;'>Investment analysis and memo generation finished successfully.</p>
</div>
""", unsafe_allow_html=True)
    
    # Navigation
    st.markdown("<br>", unsafe_allow_html=True)
    col_nav1, col_nav2, col_nav3 = st.columns(3)
    
    with col_nav1:
        if st.button("Back to Financial Modeling", use_container_width=True, key="back_fin"):
            st.switch_page("pages/4_Financial_Modeling.py")
    
    with col_nav2:
        if st.button("Return Home", use_container_width=True, key="home_final"):
            st.switch_page("streamlit_app.py")
    
    with col_nav3:
        if st.button("Start New Analysis", use_container_width=True, key="restart"):
            st.switch_page("pages/1_Deal_Sourcing.py")
