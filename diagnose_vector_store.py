#!/usr/bin/env python3
"""
Vector Store Diagnostic Script
This script helps diagnose issues with the vector store loading
"""

import os
import sys
import logging

# Add the app directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def main():
    print("=== VECTOR STORE DIAGNOSTIC ===")
    
    try:
        # Import after path setup
        from app.config.config import DB_FAISS_PATH, PROJECT_ROOT
        from app.components.vector_store import load_vector_store
        from app.components.embeddings import get_hf_embeddings_model
        
        print(f"Project Root: {PROJECT_ROOT}")
        print(f"DB FAISS Path: {DB_FAISS_PATH}")
        print(f"Current Working Directory: {os.getcwd()}")
        
        # Check if paths exist
        print(f"\nPath Checks:")
        print(f"Project root exists: {os.path.exists(PROJECT_ROOT)}")
        print(f"DB FAISS path exists: {os.path.exists(DB_FAISS_PATH)}")
        
        if os.path.exists(DB_FAISS_PATH):
            contents = os.listdir(DB_FAISS_PATH)
            print(f"DB FAISS contents: {contents}")
            
            # Check file sizes
            for file in contents:
                file_path = os.path.join(DB_FAISS_PATH, file)
                if os.path.isfile(file_path):
                    size = os.path.getsize(file_path)
                    print(f"  {file}: {size} bytes")
        
        # Test embeddings model
        print(f"\n=== Testing Embeddings Model ===")
        embeddings = get_hf_embeddings_model()
        print(f"Embeddings model loaded: {type(embeddings)}")
        
        # Test vector store loading
        print(f"\n=== Testing Vector Store Loading ===")
        vector_store = load_vector_store()
        
        if vector_store is None:
            print("ERROR: Vector store is None!")
            return False
        
        print(f"Vector store loaded successfully: {type(vector_store)}")
        
        # Test retriever creation
        print(f"\n=== Testing Retriever Creation ===")
        retriever = vector_store.as_retriever()
        print(f"Retriever created successfully: {type(retriever)}")
        
        # Test document retrieval
        print(f"\n=== Testing Document Retrieval ===")
        test_query = "What is diabetes?"
        docs = retriever.get_relevant_documents(query=test_query)
        print(f"Retrieved {len(docs)} documents for query: '{test_query}'")
        
        if docs:
            print(f"First document preview: {docs[0].page_content[:200]}...")
        
        print(f"\n=== ALL TESTS PASSED ===")
        return True
        
    except Exception as e:
        print(f"\n=== ERROR OCCURRED ===")
        print(f"Error type: {type(e)}")
        print(f"Error message: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
