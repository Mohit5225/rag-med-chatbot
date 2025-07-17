from langchain_huggingface import HuggingFaceEmbeddings
from app.common.logger import get_logger
from app.common.custom_exceptions import CustomException
import os
logger = get_logger(__name__)

def get_hf_embeddings_model():
    try:
        logger.info("INITIALIZING OUR HUGGINGFACE EMBEDDINGS MODEL")
        model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={"device": "cuda" if os.environ.get("USE_CUDA", "false").lower() == "true" else "cpu"}
        )
        logger.info("HuggingFace embeddings model initialized successfully.")
        return model
    except Exception as e:
        error_message = CustomException(message="Error occurred while initializing HuggingFace embeddings model.", error_detail=e)
        logger.error(str(error_message))
        raise error_message