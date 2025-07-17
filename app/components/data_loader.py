import os 
from app.components.pdf_Loader import load_pdf_documents, create_text_chunks
from app.components.vector_store import create_vector_store
from app.common.logger import get_logger
from app.common.custom_exceptions import CustomException
from app.config.config import DATA_PATH, DB_FAISS_PATH
 
logger = get_logger(__name__)

def process_and_store_pdf():
    try:
        if not os.path.exists(DATA_PATH):
            logger.error(f"Data directory does not exist: {DATA_PATH}")
            raise CustomException(f"Data path '{DATA_PATH}' does not exist.")
            
        logger.info(f"Starting PDF processing and vector store creation from {DATA_PATH}")
        pdf_documents = load_pdf_documents(directory_path=DATA_PATH)
        
        if not pdf_documents:
            logger.error("No PDF documents were loaded")
            return
            
        logger.info(f"Successfully loaded {len(pdf_documents)} documents, creating text chunks...")
        text_chunks = create_text_chunks(pdf_documents)
        
        if not text_chunks:
            logger.error("No text chunks were created")
            return
            
        logger.info(f"Successfully created {len(text_chunks)} text chunks, creating vector store...")
        vector_store = create_vector_store(text_chunks)
        logger.info("Process completed successfully")
        return vector_store
        
    except Exception as e:
        error_message = CustomException(message="Error occurred while processing PDF.", error_detail=e)
        logger.error(str(error_message))
        raise error_message
    
if __name__=="__main__":
    print(f"Current working directory: {os.getcwd()}")
    print(f"DATA_PATH: {DATA_PATH}")
    print(f"DATA_PATH exists: {os.path.exists(DATA_PATH)}")
    if os.path.exists(DATA_PATH):
        print(f"Contents of DATA_PATH: {os.listdir(DATA_PATH)}")
    process_and_store_pdf()