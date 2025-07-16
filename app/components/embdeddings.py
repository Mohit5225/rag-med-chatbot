from langchain_community.embeddings import HuggingFaceEmbeddings
from app.common.logger import get_logger
from app.common.custom_exceptions import CustomException

logger = get_logger(__name__)

def load_huggingface_embeddings():
    """
    Loads HuggingFace embeddings for text vectorization.
    """
    try:
        logger.info("Loading HuggingFace embeddings...")
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'}
        )
        logger.info("HuggingFace embeddings loaded successfully.")
        return embeddings
    except Exception as e:
        error_message = CustomException(message="Error loading HuggingFace embeddings.", error_detail=e)
        logger.error(str(error_message))
        raise error_message