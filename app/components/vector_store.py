from langchain_community.vectorstores import FAISS
import os
from app.config.config import DB_FAISS_PATH
from app.components.embdeddings import get_embeddings_model 
from app.common.logger import get_logger
from app.common.custom_exceptions import CustomException

logger = get_logger(__name__)

def load_vector_store():
    try:
        embedding_model = get_embeddings_model()

        if os.path.exists(DB_FAISS_PATH):
            logger.info("Loading existing vectorstore...")
            return FAISS.load_local(
                DB_FAISS_PATH,
                embedding_model,
                allow_dangerous_deserialization=True
            )
        else:
            logger.warning("No vector store found..")
    except Exception as e :
        raise CustomException("Vector store not found. Please create a new vector store.")

def create_vector_store(text_chunks):
    try:
        embedding_model = get_embeddings_model()
        logger.info("Creating new vector store...")
        vector_store = FAISS.from_documents(
            documents=text_chunks,
            embedding=embedding_model
        )
        vector_store.save_local(DB_FAISS_PATH)
        logger.info("Vector store created and saved successfully.")
        return vector_store
    except Exception as e:
        error_message = CustomException(message="Error occurred while creating vector store.", error_detail=e)
        logger.error(str(error_message))
        raise error_message