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
        logger.info(f"=== VECTOR STORE LOADING START ===")
        logger.info(f"Loading vector store from {DB_FAISS_PATH}...")
        logger.info(f"Current working directory: {os.getcwd()}")
        logger.info(f"DB_FAISS_PATH absolute path: {os.path.abspath(DB_FAISS_PATH)}")
        logger.info(f"DB_FAISS_PATH exists: {os.path.exists(DB_FAISS_PATH)}")
        logger.info(f"DB_FAISS_PATH is dir: {os.path.isdir(DB_FAISS_PATH)}")
        
        if os.path.exists(DB_FAISS_PATH):
            contents = os.listdir(DB_FAISS_PATH)
            logger.info(f"DB_FAISS_PATH contents: {contents}")
            
            # Check individual files
            index_faiss_path = os.path.join(DB_FAISS_PATH, "index.faiss")
            index_pkl_path = os.path.join(DB_FAISS_PATH, "index.pkl")
            
            logger.info(f"index.faiss exists: {os.path.exists(index_faiss_path)}")
            logger.info(f"index.pkl exists: {os.path.exists(index_pkl_path)}")
            
            if os.path.exists(index_faiss_path):
                logger.info(f"index.faiss size: {os.path.getsize(index_faiss_path)} bytes")
            if os.path.exists(index_pkl_path):
                logger.info(f"index.pkl size: {os.path.getsize(index_pkl_path)} bytes")
        else:
            logger.info(f"DB_FAISS_PATH contents: N/A (path doesn't exist)")
        
        if not os.path.exists(DB_FAISS_PATH):
            logger.error(f"CRITICAL: Vector store path {DB_FAISS_PATH} does not exist")
            return None
        
        # Step 1: Load embeddings model
        logger.info("Loading embeddings model for vector store...")
        embeddings = get_hf_embeddings_model()
        logger.info(f"Embeddings model loaded successfully. Type: {type(embeddings)}")
        
        # Step 2: Load FAISS vector store
        logger.info("Loading FAISS vector store from disk...")
        vector_store = FAISS.load_local(
            DB_FAISS_PATH, 
            embeddings, 
            allow_dangerous_deserialization=True
        )
        
        logger.info(f"Vector store loaded successfully. Type: {type(vector_store)}")
        logger.info(f"Vector store docstore type: {type(vector_store.docstore)}")
        logger.info(f"Vector store index type: {type(vector_store.index)}")
        
        # Test vector store functionality
        try:
            # Try to get the number of vectors
            vector_count = vector_store.index.ntotal
            logger.info(f"Vector store contains {vector_count} vectors")
        except Exception as count_e:
            logger.warning(f"Could not get vector count: {str(count_e)}")
        
        logger.info(f"=== VECTOR STORE LOADING SUCCESS ===")
        return vector_store
        
    except Exception as e:
        logger.error(f"=== VECTOR STORE LOADING FAILED ===")
        logger.error(f"Exception type: {type(e)}")
        logger.error(f"Exception details: {repr(e)}")
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