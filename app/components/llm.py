from langchain_groq import ChatGroq
from app.common.logger import get_logger
from app.common.custom_exceptions import CustomException
from app.config.config import GROQ_API_KEY

logger = get_logger(__name__)


def load_llm(model_name: str = "llama-3.1-8b-instant", groq_api_key: str = GROQ_API_KEY):
    try:
        logger.info("INITIALIZING OUR GROQ LLM")
        llm = ChatGroq(
            model=model_name,
            api_key=groq_api_key,
            max_retries=3,
            timeout=60,
            temperature=0.7,
            max_tokens=500

        )
        logger.info("Groq LLM initialized successfully.")
        return llm
    except Exception as e:
        error_message = CustomException(message="Error occurred while initializing Groq LLM.", error_detail=e)
        logger.error(str(error_message))
        raise error_message
