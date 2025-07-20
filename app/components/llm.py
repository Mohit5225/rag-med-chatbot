from langchain_groq import ChatGroq
from app.common.logger import get_logger
from app.common.custom_exceptions import CustomException
from app.config.config import GROQ_API_KEY

logger = get_logger(__name__)


def load_llm(model_name="llama-3.1-8b-instant"):
    """
    Load and return a Groq language model for chat

    Args:
        model_name (str): The model to use. Default is "llama-3.1-8b-instant"

    Returns:
        ChatGroq: Configured language model instance
    """
    try:
        logger.info(f"=== LLM LOADING START ===")
        logger.info(f"Loading LLM: {model_name}")
        
        # Check API key
        if not GROQ_API_KEY:
            logger.error("CRITICAL: GROQ_API_KEY is not set in environment variables.")
            raise CustomException("GROQ_API_KEY is not set in environment variables.")
        
        logger.info(f"GROQ_API_KEY is set: {GROQ_API_KEY[:10]}..." if len(GROQ_API_KEY) > 10 else "GROQ_API_KEY is set (short key)")
        
        # Initialize LLM
        logger.info(f"Initializing ChatGroq with model: {model_name}")
        llm = ChatGroq(
            api_key=GROQ_API_KEY,
            model_name=model_name,
        )
        
        logger.info(f"ChatGroq initialized successfully. Type: {type(llm)}")
        
        # Test the LLM with a simple query
        try:
            logger.info("Testing LLM with simple query...")
            test_response = llm.invoke("Hello, this is a test. Please respond with 'Test successful'.")
            logger.info(f"LLM test successful. Response type: {type(test_response)}")
            if hasattr(test_response, 'content'):
                logger.info(f"LLM test response content: {test_response.content[:100]}...")
        except Exception as test_e:
            logger.warning(f"LLM test failed (but continuing): {str(test_e)}")

        logger.info(f"=== LLM LOADING SUCCESS ===")
        return llm
        
    except Exception as e:
        logger.error(f"=== LLM LOADING FAILED ===")
        logger.error(f"Exception type: {type(e)}")
        logger.error(f"Exception details: {repr(e)}")
        error_message = CustomException(
            message=f"Error loading LLM model {model_name}", error_detail=e
        )
        logger.error(str(error_message))
        raise error_message
