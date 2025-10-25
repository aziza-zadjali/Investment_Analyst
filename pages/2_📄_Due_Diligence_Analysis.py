# Analysis Button
if st.button("🔍 Run Enhanced Due Diligence Analysis", type="primary", use_container_width=True):
    
    # Validation
    if not company_name:
        st.error("⚠️ Please enter company name")
        st.stop()
    
    if enable_web_extraction and not company_website:
        st.error("⚠️ Please enter company website for web extraction")
        st.stop()
    
    if not uploaded_files and not enable_web_extraction:
        st.error("⚠️ Please either upload documents OR enable web data extraction")
        st.stop()
    
    with st.spinner("🤖 Performing comprehensive due diligence analysis..."):
        
        combined_text = ""
        
        # STEP 1: Extract from uploaded documents
        if uploaded_files:
            st.info(f"📄 Processing {len(uploaded_files)} uploaded documents...")
            
            for uploaded_file in uploaded_files:
                try:
                    if uploaded_file.type == "application/pdf":
                        pdf_reader = PyPDF2.PdfReader(uploaded_file)
                        for page in pdf_reader.pages:
                            text = page.extract_text()
                            if text:
                                combined_text += text + "\n"
                    
                    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                        # DOCX handling
                        import docx
                        doc = docx.Document(uploaded_file)
                        for para in doc.paragraphs:
                            combined_text += para.text + "\n"
                    
                    # Add other file types as needed
                    
                except Exception as e:
                    st.warning(f"⚠️ Could not process {uploaded_file.name}: {e}")
            
            if combined_text:
                st.success(f"✅ Processed {len(uploaded_files)} documents ({len(combined_text)} characters)")
        
        # STEP 2: NEW - Extract from company website
        web_data = {}
        web_extraction_success = False
        
        if enable_web_extraction and company_website:
            st.info(f"🌐 Extracting data from {company_website}...")
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # Discover and extract
                status_text.text("🔍 Discovering investor relations pages...")
                progress_bar.progress(20)
                
                web_data = web_scraper.extract_company_data(company_website, company_name)
                
                progress_bar.progress(60)
                status_text.text("📊 Extracting financial data...")
                
                if web_data and any(web_data.values()):
                    # Format for analysis
                    web_formatted = web_scraper.format_for_analysis(web_data, company_name)
                    combined_text += "\n\n" + web_formatted
                    web_extraction_success = True
                    
                    progress_bar.progress(100)
                    status_text.empty()
                    progress_bar.empty()
                    
                    # Show what was extracted
                    st.success(f"✅ Extracted {len(web_data)} data categories from website:")
                    
                    cols = st.columns(min(4, len(web_data)))
                    for idx, category in enumerate(web_data.keys()):
                        with cols[idx % len(cols)]:
                            st.caption(f"✓ {category.replace('_', ' ').title()}")
                else:
                    progress_bar.empty()
                    status_text.empty()
                    st.warning("⚠️ No data found on website. Please check URL or upload documents.")
                
            except Exception as e:
                progress_bar.empty()
                status_text.empty()
                st.error(f"❌ Web extraction failed: {str(e)}")
                st.info("💡 Try uploading documents manually or check if the website is accessible")
        
        # STEP 3: Validation - Ensure we have some data
        if not combined_text or len(combined_text) < 100:
            st.error("⚠️ Insufficient data for analysis.")
            st.info("""
**Please ensure:**
- Documents are uploaded and readable, OR
- Company website URL is correct and accessible
- Website has investor relations/corporate pages
            """)
            st.stop()
        
        # STEP 4: Perform AI Analysis (ONLY if we have data)
        st.info("🤖 Analyzing with AI...")
        
        analysis_results = {
            'company_name': company_name,
            'analyst_name': 'Regulus AI',
            'analysis_date': datetime.now().strftime('%B %d, %Y'),
            'company_website': company_website,
            'data_sources': []
        }
        
        # Track data sources
        if uploaded_files:
            analysis_results['data_sources'].append(f"{len(uploaded_files)} uploaded documents")
        if web_extraction_success:
            analysis_results['data_sources'].append(f"{len(web_data)} website sections")
        
        # Financial Analysis
        st.info("📊 Analyzing financials...")
        
        financial_prompt = f"""
        Analyze the financial health and performance of {company_name} based on the following documents:
        
        {combined_text[:8000]}
        
        Provide detailed analysis covering:
        1. Revenue trends and growth
        2. Profitability metrics
        3. Cash flow and liquidity
        4. Asset quality and leverage
        5. Key financial ratios
        6. Red flags or concerns
        
        Be specific with numbers and dates where available.
        """
        
        try:
            financial_analysis = llm.generate(financial_prompt)
            analysis_results['financial_analysis'] = financial_analysis
        except Exception as e:
            st.error(f"Error in financial analysis: {e}")
            analysis_results['financial_analysis'] = "Analysis unavailable due to error"
        
        # Legal Analysis
        st.info("⚖️ Reviewing legal & compliance...")
        
        legal_prompt = f"""
        Review legal and compliance aspects for {company_name}:
        
        {combined_text[:8000]}
        
        Cover:
        1. Corporate structure and governance
        2. Regulatory compliance status
        3. Legal proceedings or disputes
        4. Intellectual property
        5. Contractual obligations
        6. Compliance risks
        """
        
        try:
            legal_analysis = llm.generate(legal_prompt)
            analysis_results['legal_analysis'] = legal_analysis
        except Exception as e:
            analysis_results['legal_analysis'] = "Analysis unavailable due to error"
        
        # Operational Analysis
        st.info("🏭 Assessing operations...")
        
        operational_prompt = f"""
        Assess operational capabilities of {company_name}:
        
        {combined_text[:8000]}
        
        Analyze:
        1. Business model and operations
        2. Supply chain and distribution
        3. Technology and systems
        4. Human resources and management
        5. Operational efficiency
        6. Scalability
        """
        
        try:
            operational_analysis = llm.generate(operational_prompt)
            analysis_results['operational_analysis'] = operational_analysis
        except Exception as e:
            analysis_results['operational_analysis'] = "Analysis unavailable due to error"
        
        # Risk Assessment
        st.info("⚠️ Evaluating risks...")
        
        risk_prompt = f"""
        Comprehensive risk assessment for {company_name}:
        
        {combined_text[:8000]}
        
        Identify and assess:
        1. Market and competitive risks
        2. Financial risks
        3. Operational risks
        4. Regulatory and legal risks
        5. Strategic risks
        6. Overall risk rating (Low/Medium/High)
        """
        
        try:
            risk_assessment = llm.generate(risk_prompt)
            analysis_results['risk_assessment'] = risk_assessment
        except Exception as e:
            analysis_results['risk_assessment'] = "Assessment unavailable due to error"
        
        # AML/Compliance (if web data available)
        if web_extraction_success or combined_text:
            st.info("🔒 Performing AML/KYC screening...")
            
            # Sanctions screening
            sanctions_prompt = f"""
            Conduct sanctions screening for {company_name}:
            
            {combined_text[:4000]}
            
            Check for:
            - OFAC SDN list concerns
            - EU/UN sanctions exposure
            - High-risk jurisdiction connections
            - Sanctioned activities or parties
            
            Provide screening status and recommendations.
            """
            
            try:
                sanctions_analysis = llm.generate(sanctions_prompt)
                analysis_results['sanctions_screening'] = sanctions_analysis
            except:
                analysis_results['sanctions_screening'] = "Screening pending - insufficient data"
            
            # PEP screening
            pep_prompt = f"""
            PEP (Politically Exposed Persons) screening for {company_name}:
            
            {combined_text[:4000]}
            
            Identify:
            - Key individuals and their roles
            - PEP connections or indicators
            - Enhanced due diligence requirements
            - Risk classification
            """
            
            try:
                pep_analysis = llm.generate(pep_prompt)
                analysis_results['pep_screening'] = pep_analysis
            except:
                analysis_results['pep_screening'] = "Screening pending"
            
            # FATCA compliance
            fatca_prompt = f"""
            FATCA compliance assessment for {company_name}:
            
            {combined_text[:4000]}
            
            Review:
            - Entity classification
            - GIIN status
            - US person indicators
            - Compliance requirements
            """
            
            try:
                fatca_analysis = llm.generate(fatca_prompt)
                analysis_results['fatca_compliance'] = fatca_analysis
            except:
                analysis_results['fatca_compliance'] = "Review pending"
            
            # Adverse media
            adverse_prompt = f"""
            Adverse media screening for {company_name}:
            
            {combined_text[:4000]}
            
            Check for:
            - Financial crime indicators
            - Regulatory actions
            - Negative press
            - Reputational risks
            """
            
            try:
                adverse_analysis = llm.generate(adverse_prompt)
                analysis_results['adverse_media'] = adverse_analysis
            except:
                analysis_results['adverse_media'] = "Screening pending"
            
            # AML risk rating
            analysis_results['aml_risk_rating'] = "To be assessed based on findings"
        
        # Recommendations
        st.info("💡 Generating recommendations...")
        
        rec_prompt = f"""
        Based on all analysis for {company_name}, provide:
        
        1. Investment recommendation (Proceed/Caution/Decline)
        2. Key strengths
        3. Major concerns
        4. Required actions before proceeding
        5. Overall assessment
        
        Context: {combined_text[:5000]}
        """
        
        try:
            recommendations = llm.generate(rec_prompt)
            analysis_results['recommendations'] = recommendations
        except:
            analysis_results['recommendations'] = "Recommendations pending"
        
        # Generate Report
        st.info("📝 Generating comprehensive report...")
        
        markdown_report = template_gen.generate_due_diligence_report(analysis_results)
        
        # Store in session state
        st.session_state.dd_complete = True
        st.session_state.dd_report = markdown_report
        st.session_state.dd_data = analysis_results
        
        st.success("✅ Due Diligence Analysis Complete!")
        st.balloons()
