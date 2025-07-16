import os
from langchain_community.vectorstores import FAISS
from app.components.embdeddings import load_huggingface_embeddings
from app.config.config import DB_FAISS_PATH
from app.common.logger import get_logger
from app.common.custom_exceptions import CustomException

logger = get_logger(__name__)

def create_vector_store(text_chunks):
    """
    Creates and saves a FAISS vector store from text chunks.
    """
    try:
        if not text_chunks:
            raise CustomException("No text chunks provided to create vector store.")
        
        logger.info("Loading embeddings for vector store creation...")
        embeddings = load_huggingface_embeddings()
        
        logger.info("Creating FAISS vector store...")
        vector_store = FAISS.from_documents(documents=text_chunks, embedding=embeddings)
        
        logger.info(f"Saving vector store to: {DB_FAISS_PATH}")
        vector_store.save_local(DB_FAISS_PATH)
        logger.info("Vector store created and saved successfully.")
        
    except Exception as e:
        error_message = CustomException(message="Error creating vector store.", error_detail=e)
        logger.error(str(error_message))
        raise error_message

def load_vector_store():
    """
    Loads an existing FAISS vector store from the local path.
    """
    try:
        if not os.path.exists(DB_FAISS_PATH):
            raise CustomException(f"Vector store not found at path: {DB_FAISS_PATH}")
            
        logger.info(f"Loading vector store from: {DB_FAISS_PATH}")
        embeddings = load_huggingface_embeddings()
        vector_store = FAISS.load_local(DB_FAISS_PATH, embeddings, allow_dangerous_deserialization=True)
        logger.info("Vector store loaded successfully.")
        return vector_store
        
    except Exception as e:
        error_message = CustomException(message="Error loading vector store.", error_detail=e)
        logger.error(str(error_message))
        raise error_message