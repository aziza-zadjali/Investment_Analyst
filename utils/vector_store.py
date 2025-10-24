"""
Vector store management for document retrieval
"""

import faiss
import numpy as np
from typing import List, Dict, Any, Tuple
import pickle
from pathlib import Path
import streamlit as st
from config.constants import CHUNK_SIZE, CHUNK_OVERLAP, TOP_K_RESULTS

class VectorStoreManager:
    """Manage vector embeddings and similarity search"""
    
    def __init__(self):
        """Initialize vector store"""
        self.index = None
        self.documents = []
        self.embeddings = []
        self.dimension = 1536  # OpenAI embedding dimension
        
    def create_index(self):
        """Create new FAISS index"""
        self.index = faiss.IndexFlatL2(self.dimension)
        
    def add_documents(self, documents: List[str], embeddings: List[List[float]]):
        """Add documents and their embeddings to the store"""
        if self.index is None:
            self.create_index()
        
        # Convert to numpy array
        embeddings_array = np.array(embeddings).astype('float32')
        
        # Add to index
        self.index.add(embeddings_array)
        
        # Store documents
        self.documents.extend(documents)
        self.embeddings.extend(embeddings)
        
    def search(self, query_embedding: List[float], k: int = TOP_K_RESULTS) -> List[Tuple[str, float]]:
        """Search for similar documents"""
        if self.index is None or self.index.ntotal == 0:
            return []
        
        # Convert query to numpy array
        query_array = np.array([query_embedding]).astype('float32')
        
        # Search
        distances, indices = self.index.search(query_array, k)
        
        # Return documents with scores
        results = []
        for idx, distance in zip(indices[0], distances[0]):
            if idx < len(self.documents):
                results.append((self.documents[idx], float(distance)))
        
        return results
    
    def chunk_text(self, text: str, chunk_size: int = CHUNK_SIZE, 
                   chunk_overlap: int = CHUNK_OVERLAP) -> List[str]:
        """Split text into overlapping chunks"""
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            end = start + chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            start += chunk_size - chunk_overlap
            
        return chunks
    
    def save_index(self, filepath: str):
        """Save index to disk"""
        if self.index is not None:
            faiss.write_index(self.index, f"{filepath}.faiss")
            
            # Save documents and metadata
            with open(f"{filepath}.pkl", 'wb') as f:
                pickle.dump({
                    'documents': self.documents,
                    'embeddings': self.embeddings
                }, f)
    
    def load_index(self, filepath: str):
        """Load index from disk"""
        try:
            self.index = faiss.read_index(f"{filepath}.faiss")
            
            with open(f"{filepath}.pkl", 'rb') as f:
                data = pickle.load(f)
                self.documents = data['documents']
                self.embeddings = data['embeddings']
                
            return True
        except Exception as e:
            st.error(f"Failed to load index: {str(e)}")
            return False
    
    def clear(self):
        """Clear the vector store"""
        self.index = None
        self.documents = []
        self.embeddings = []
