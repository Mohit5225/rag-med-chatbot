from langchain_community.vectorstores import FAISS
import os
from app.config.config import DB_FAISS_PATH
from app.components.embeddings import get_hf_embeddings_model  # <-- fixed spelling here
from app.common.logger import get_logger
from app.common.custom_exceptions import CustomException
logger = get_logger(__name__)

def load_vector_store():
    """Load FAISS vector store from disk"""
    try:
        logger.info(f"Loading vector store from {DB_FAISS_PATH}...")
        logger.info(f"Current working directory: {os.getcwd()}")
        logger.info(f"DB_FAISS_PATH exists: {os.path.exists(DB_FAISS_PATH)}")
        logger.info(f"DB_FAISS_PATH is dir: {os.path.isdir(DB_FAISS_PATH)}")
        logger.info(f"DB_FAISS_PATH contents: {os.listdir(DB_FAISS_PATH) if os.path.exists(DB_FAISS_PATH) else 'N/A'}")
        
        if not os.path.exists(DB_FAISS_PATH):
            logger.error(f"Vector store path {DB_FAISS_PATH} does not exist")
            return None
            
        embeddings = get_hf_embeddings_model()
        vector_store = FAISS.load_local(DB_FAISS_PATH, embeddings, allow_dangerous_deserialization=True)
        
        logger.info("Vector store loaded successfully")
        return vector_store
    except Exception as e:
        error_message = CustomException(message="Error occurred while loading vector store.", error_detail=e)
        logger.error(str(error_message))
        # Return None instead of raising an exception to handle the case gracefully
        return None

def create_vector_store(text_chunks):
    """Create FAISS vector store from text chunks"""
    try:
        logger.info("Creating FAISS vector store...")
        embeddings = get_hf_embeddings_model()

        # Create directory for vector store if it doesn't exist
        os.makedirs(os.path.dirname(DB_FAISS_PATH), exist_ok=True)
        
        vector_store = FAISS.from_documents(text_chunks, embeddings)
        
        # Save the vector store for future use
        vector_store.save_local(DB_FAISS_PATH)
        
        logger.info(f"Vector store created and saved to {DB_FAISS_PATH}")
        return vector_store
    except Exception as e:
        error_message = CustomException(message="Error occurred while creating vector store.", error_detail=e)
        logger.error(str(error_message))
        raise error_message