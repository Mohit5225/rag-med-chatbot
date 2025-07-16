import os 
from app.components.pdf_Loader import load_pdf_documents , create_text_chunks

from app.components.vector_store import create_vector_store
from app.common.logger import get_logger
from app.common.custom_exceptions import CustomException
from app.config.config import DATA_PATH

logger = get_logger(__name__)

def process_and_store_pdf():
    try:
        logger.info("Starting PDF processing and vector store creation.")
        pdf_documents = load_pdf_documents(directory_path=DATA_PATH)
        text_chunks = create_text_chunks(pdf_documents)
        create_vector_store(text_chunks)
    except Exception as e:
        error_message = CustomException(message="Error occurred while processing PDF.", error_detail=e)
        logger.error(str(error_message))
        raise error_message
    
if __name__=="__main__":
    process_and_store_pdf()