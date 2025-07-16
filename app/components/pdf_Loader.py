import os 
from langchain_community.document_loaders import PyPDFLoader , DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.common.logger import get_logger
from app.config.config import CHUNK_SIZE, CHUNK_OVERLAP, DATA_PATH
from app.common.custom_exceptions import CustomException

logger = get_logger(__name__)

def load_pdf_documents(directory_path : str):
    try :
        if not os.path.exists(DATA_PATH):
            raise CustomException(f"Data path '{DATA_PATH}' does not exist.")
        logger.info(f"Loading PDF documents from directory: {DATA_PATH}")
        loader = DirectoryLoader(
            directory_path=directory_path,
            glob="**/*.pdf",
            loader_cls=PyPDFLoader
        )
        documents = loader.load()
        logger.info(f"Loaded {len(documents)} PDF documents.")
        return  documents
    except Exception as e:
         error_message = CustomException( message="Error occurred while loading PDF documents.", error_detail=e)
         logger.error(str(error_message))
         return []


def create_text_chunks(documents):
    try :
        if not documents:
            raise CustomException("No documents provided for text chunking.")
        
        logger.info(f"splitting {len(documents)} documents into text chunks.")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP
        )
        text_chunks = text_splitter.split_documents(documents)
        logger.info(f"Generated  {len(text_chunks)} text chunks.")
        return text_chunks
    except Exception as e:
        error_message = CustomException(message="Error occurred while creating text chunks.", error_detail=e)
        logger.error(str(error_message))
        return []