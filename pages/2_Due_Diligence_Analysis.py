# ==== RESULTS DISPLAY ====
if st.session_state.dd_report_doc and company_name:
    st.markdown("---")
    st.markdown(
        """
<div style="background:white;margin:30px -3rem 0 -3rem;padding:45px 3rem;
border-top:3px solid #138074;box-shadow:0 0 12px rgba(0,0,0,0.05);">
<h2 style="text-align:center;color:#1B2B4D;font-weight:700;">
Analysis Results
</h2>
<p style="text-align:center;color:#555;margin-top:6px;">
Download comprehensive due diligence report in DOCX format.
</p>
</div>
""",
        unsafe_allow_html=True,
    )
    
    # Generate DOCX file from report data
    try:
        # Always create fresh DOCX from report data
        doc = Document()
        
        # Header
        doc.add_heading(f"Due Diligence Report: {company_name}", 0)
        doc.add_paragraph(f"Analyst: Regulus AI - QDB Investment Team")
        doc.add_paragraph(f"Analysis Date: {datetime.now().strftime('%B %d, %Y')}")
        doc.add_paragraph()
        
        # Company Details
        doc.add_heading("Company Information", 1)
        doc.add_paragraph(f"Company: {company_name}")
        doc.add_paragraph(f"Industry: {st.session_state.dd_report_doc.get('industry', 'N/A')}")
        doc.add_paragraph(f"Sector: {st.session_state.dd_report_doc.get('sector', 'N/A')}")
        doc.add_paragraph(f"Funding Stage: {st.session_state.dd_report_doc.get('stage', 'N/A')}")
        doc.add_paragraph(f"Website: {st.session_state.dd_report_doc.get('company_website', 'Not provided')}")
        doc.add_paragraph()
        
        # Executive Summary
        doc.add_heading("Executive Summary", 1)
        doc.add_paragraph(st.session_state.dd_report_doc.get('executive_summary', 'Analysis completed.'))
        doc.add_paragraph()
        
        # Financial Analysis
        doc.add_heading("Financial Analysis", 1)
        doc.add_paragraph(st.session_state.dd_report_doc.get('financial_analysis', 'Financial review completed.'))
        doc.add_paragraph()
        
        # Legal & Compliance
        doc.add_heading("Legal & Regulatory Compliance", 1)
        doc.add_paragraph(st.session_state.dd_report_doc.get('legal_analysis', 'Legal review completed.'))
        doc.add_paragraph()
        
        # Operational Assessment
        doc.add_heading("Operational Assessment", 1)
        doc.add_paragraph(st.session_state.dd_report_doc.get('operational_analysis', 'Operational assessment completed.'))
        doc.add_paragraph()
        
        # Management Team
        doc.add_heading("Management Team", 1)
        doc.add_paragraph(st.session_state.dd_report_doc.get('management_team', 'Management evaluation completed.'))
        doc.add_paragraph()
        
        # Risk Assessment
        doc.add_heading("Risk Assessment", 1)
        doc.add_paragraph(st.session_state.dd_report_doc.get('risk_assessment', 'Risk assessment completed.'))
        doc.add_paragraph()
        
        # Compliance Status
        if st.session_state.dd_report_doc.get('compliance_status'):
            doc.add_heading("Compliance Status", 1)
            doc.add_paragraph(f"AML/PEP/FATCA: {st.session_state.dd_report_doc.get('compliance_status', 'Not screened')}")
            doc.add_paragraph(st.session_state.dd_report_doc.get('aml_pep_fatca', ''))
            doc.add_paragraph()
        
        # Recommendations
        doc.add_heading("Recommendations", 1)
        doc.add_paragraph(st.session_state.dd_report_doc.get('recommendations', 'Further evaluation recommended.'))
        doc.add_paragraph()
        
        # Data Sources
        doc.add_heading("Data Sources & Documentation", 1)
        sources = st.session_state.dd_report_doc.get('data_sources', [])
        for source in sources:
            doc.add_paragraph(f"- {source}", style='List Bullet')
        doc.add_paragraph(f"Documents Reviewed: {st.session_state.dd_report_doc.get('documents_reviewed', 0)}")
        
        # Convert to bytes
        bio = io.BytesIO()
        doc.save(bio)
        docx_bytes = bio.getvalue()
        
        # Download button
        col1 = st.columns(1)[0]
        with col1:
            st.download_button(
                "Download Report (DOCX)",
                docx_bytes,
                f"DD_Report_{company_name}_{datetime.now().strftime('%Y%m%d')}.docx",
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )
    
    except Exception as e:
        st.error(f"Error generating report: {str(e)}")
    
    # Navigation
    st.markdown("<br><br>", unsafe_allow_html=True)
    col_nav1, col_nav2, col_nav3 = st.columns(3)
    
    with col_nav1:
        if st.button("Back to Deal Sourcing", use_container_width=True, key="back_deals"):
            st.switch_page("pages/1_Deal_Sourcing.py")
    
    with col_nav2:
        if st.button("Go to Market Analysis", use_container_width=True, key="to_market"):
            st.switch_page("pages/3_Market_Analysis.py")
    
    with col_nav3:
        if st.button("Go to Financial Modeling", use_container_width=True, key="to_financial"):
            st.switch_page("pages/4_Financial_Modeling.py")

# ==== FOOTER ====
st.markdown(
    f"""
<div style="background:{QDB_DARK_BLUE};color:#E2E8F0;padding:26px 36px;margin:80px -3rem -2rem;
display:flex;justify-content:space-between;align-items:center;">
  <p style="margin:0;font-size:0.9rem;">© 2025 Regulus AI | All Rights Reserved</p>
  <p style="margin:0;color:#A0AEC0;font-size:0.9rem;">Powered by Regulus AI</p>
</div>
""",
    unsafe_allow_html=True,
)
