from langchain_groq import ChatGroq
from app.common.logger import get_logger
from app.common.custom_exceptions import CustomException

logger = get_logger(__name__)


def load_llm(model_name: str, groq_api_key: str):
    """
    Loads the Language Model from Groq.
    """
    try:
        logger.info(f"Loading LLM: {model_name} from Groq...")
        if not groq_api_key:
            raise ValueError("Groq API key is not set.")

        llm = ChatGroq(
            groq_api_key=groq_api_key,
            model_name=model_name
        )
        logger.info("LLM loaded successfully from Groq.")
        return llm
    except Exception as e:
        error_message = CustomException(message="Error loading LLM from Groq.", error_detail=e)
        logger.error(str(error_message))
        raise error_message
