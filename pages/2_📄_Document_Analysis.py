"""
Document Analysis Page - AI-Powered Due Diligence
"""

import streamlit as st
import sys
sys.path.append('.')
from utils.file_processor import FileProcessor
from utils.llm_handler import LLMHandler
from utils.vector_store import VectorStoreManager

st.set_page_config(page_title="Document Analysis", page_icon="📄", layout="wide")

st.title("📄 Automated Document Analysis")
st.markdown("Upload and analyze financial documents, contracts, and reports")

# Initialize components
processor = FileProcessor()
llm = LLMHandler()
vector_store = VectorStoreManager()

# File upload
st.header("📤 Upload Documents")

uploaded_files = st.file_uploader(
    "Upload PDF, DOCX, or XLSX files",
    type=['pdf', 'docx', 'xlsx', 'txt'],
    accept_multiple_files=True
)

if uploaded_files:
    st.success(f"✅ {len(uploaded_files)} file(s) uploaded successfully")
    
    # Process files
    if st.button("🔄 Process Documents", type="primary"):
        with st.spinner("Processing documents..."):
            for file in uploaded_files:
                st.markdown(f"### 📄 {file.name}")
                
                # Process file
                result = processor.process_file(file)
                
                if result:
                    # Display basic info
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("File Type", result['type'].upper())
                    with col2:
                        if 'pages' in result:
                            st.metric("Pages", result['pages'])
                    
                    # Analyze with LLM
                    with st.expander("📊 AI Analysis", expanded=True):
                        analysis = llm.analyze_document(result['text'][:10000])  # Limit text length
                        st.markdown(analysis)
                    
                    # Extract financial data
                    financial_data = processor.extract_financial_data(result['text'])
                    if financial_data:
                        with st.expander("💰 Extracted Financial Data"):
                            st.json(financial_data)
                    
                    # Store in session
                    if 'uploaded_documents' not in st.session_state:
                        st.session_state.uploaded_documents = []
                    st.session_state.uploaded_documents.append({
                        'filename': file.name,
                        'type': result['type'],
                        'content': result,
                        'analysis': analysis
                    })
                    
                    st.markdown("---")
    
    # Document Q&A
    st.header("💬 Ask Questions About Documents")
    
    if 'uploaded_documents' in st.session_state and st.session_state.uploaded_documents:
        question = st.text_input("Ask a question about the uploaded documents:")
        
        if question:
            with st.spinner("Searching for answer..."):
                # Combine all document texts
                all_text = "\n\n".join([
                    doc['content']['text']
                    for doc in st.session_state.uploaded_documents
                ])
                
                # Query LLM
                response = llm.chat_completion([
                    {'role': 'system', 'content': 'You are analyzing financial documents.'},
                    {'role': 'user', 'content': f"Context: {all_text[:5000]}\n\nQuestion: {question}"}
                ])
                
                st.markdown("### Answer")
                st.markdown(response)
