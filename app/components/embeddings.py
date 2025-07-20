from langchain_huggingface import HuggingFaceEmbeddings
from app.common.logger import get_logger
from app.common.custom_exceptions import CustomException
import os
logger = get_logger(__name__)

def get_hf_embeddings_model():
    try:
        logger.info("=== EMBEDDINGS MODEL LOADING START ===")
        logger.info("INITIALIZING OUR HUGGINGFACE EMBEDDINGS MODEL")
        
        # Check CUDA availability
        use_cuda = os.environ.get("USE_CUDA", "false").lower() == "true"
        device = "cuda" if use_cuda else "cpu"
        logger.info(f"Device selection: {device} (USE_CUDA env var: {os.environ.get('USE_CUDA', 'not set')})")
        
        # Log model details
        model_name = "sentence-transformers/all-MiniLM-L6-v2"
        logger.info(f"Loading model: {model_name}")
        logger.info(f"Model kwargs: device={device}")
        
        model = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs={"device": device}
        )
        
        logger.info(f"HuggingFace embeddings model initialized successfully.")
        logger.info(f"Model type: {type(model)}")
        
        # Test the model with a simple embedding
        try:
            test_text = "This is a test."
            logger.info(f"Testing embeddings model with text: '{test_text}'")
            test_embedding = model.embed_query(test_text)
            logger.info(f"Test embedding successful. Dimension: {len(test_embedding)}")
        except Exception as test_e:
            logger.warning(f"Embeddings model test failed: {str(test_e)}")
            
        logger.info("=== EMBEDDINGS MODEL LOADING SUCCESS ===")
        return model
        
    except Exception as e:
        logger.error("=== EMBEDDINGS MODEL LOADING FAILED ===")
        logger.error(f"Exception type: {type(e)}")
        logger.error(f"Exception details: {repr(e)}")
        error_message = CustomException(message="Error occurred while initializing HuggingFace embeddings model.", error_detail=e)
        logger.error(str(error_message))
        raise error_message