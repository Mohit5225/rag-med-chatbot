import os 
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.common.logger import get_logger
from app.config.config import CHUNK_SIZE, CHUNK_OVERLAP, DATA_PATH
from app.common.custom_exceptions import CustomException

logger = get_logger(__name__)

def load_pdf_documents(directory_path: str):
    try:
        if not os.path.exists(directory_path):
            raise CustomException(f"Data path '{directory_path}' does not exist.")
        
        # Check if directory contains any PDF files
        pdf_files = [f for f in os.listdir(directory_path) if f.lower().endswith('.pdf')]
        if not pdf_files:
            raise CustomException(f"No PDF files found in '{directory_path}'")
            
        logger.info(f"Loading PDF documents from directory: {directory_path}")
        logger.info(f"Found {len(pdf_files)} PDF files: {', '.join(pdf_files)}")
        
        loader = DirectoryLoader(
            path=directory_path,
            glob="**/*.pdf",
            loader_cls=PyPDFLoader
        )
        documents = loader.load()
        
        if not documents:
            raise CustomException(f"No documents were loaded from the PDF files in {directory_path}")
            
        logger.info(f"Loaded {len(documents)} PDF documents.")
        print(f"DEBUG: Loaded {len(documents)} PDF documents from {directory_path}")
        return documents
    except Exception as e:
        error_message = CustomException(message="Error occurred while loading PDF documents.", error_detail=e)
        logger.error(str(error_message))
        raise error_message  # Raise the error instead of returning empty list

def create_text_chunks(documents):
    try:
        if not documents:
            raise CustomException("No documents provided for text chunking.")
        
        logger.info(f"Splitting {len(documents)} documents into text chunks.")  # Fixed f-string
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP
        )
        text_chunks = text_splitter.split_documents(documents)
        
        if not text_chunks:
            raise CustomException("No text chunks were generated from the documents")
            
        logger.info(f"Generated {len(text_chunks)} text chunks.")
        return text_chunks
    except Exception as e:
        error_message = CustomException(message="Error occurred while creating text chunks.", error_detail=e)
        logger.error(str(error_message))
        raise error_message  # Raise the error instead of returning empty list