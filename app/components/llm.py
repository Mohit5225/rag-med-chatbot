from langchain_groq import ChatGroq
from app.common.logger import get_logger
from app.common.custom_exceptions import CustomException
from app.config.config import GROQ_API_KEY

logger = get_logger(__name__)


def load_llm(model_name="llama-3.1-8b-instant"):
    """
    Load the language model from Groq

    Args:
        model_name (str): The name of the model to load

    Returns:
        ChatGroq: The loaded language model
    """
    try:
        logger.info(f"Loading language model: {model_name}")

        # Check if API key is available
        if not GROQ_API_KEY:
            raise CustomException("GROQ_API_KEY is not set in environment variables")

        # Initialize the Groq model
        llm = ChatGroq(
            groq_api_key=GROQ_API_KEY,
            model_name=model_name,
            temperature=0.2,
            max_tokens=512,
        )

        logger.info(f"Successfully loaded language model: {model_name}")
        return llm

    except Exception as e:
        error_message = CustomException(
            message=f"Error loading language model {model_name}", error_detail=e
        )
        logger.error(str(error_message))
        raise error_message
