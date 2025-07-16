from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from app.components.llm import load_llm
from app.components.vector_store import load_vector_store
from app.config.config import HUGGINGFACE_REPO_ID , GROQ_API_KEY
from app.common.logger import get_logger
from app.common.custom_exceptions import CustomException

logger = get_logger(__name__)


CUSTOM_PROMPT_TEMPLATE = """ Answer the following medical question in 2-3 lines maximum using only the information provided in the context.

Context:
{context}

Question:
{question}

Answer:
"""


def set_custom_prompt():
    return PromptTemplate(template=CUSTOM_PROMPT_TEMPLATE, input_variables=["context", "question"])

def create_qa_chain():
    try:
        logger.info("Loading vector store...")
        vector_store = load_vector_store()
        if not vector_store:
            raise CustomException("Vector store is empty or not found. Please create a vector store first.")
        
        logger.info("Loading LLM...")
        llm = load_llm(model_name=HUGGINGFACE_REPO_ID, groq_api_key=GROQ_API_KEY)
        if not llm:
            raise CustomException("LLM could not be loaded. Please check your configuration.")
        
        logger.info("Setting up custom prompt template...")
        prompt = set_custom_prompt()
        
        logger.info("Creating RetrievalQA chain...")
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vector_store.as_retriever(),
            return_source_documents=False,
            chain_type_kwargs={"prompt": prompt}
        )
        
        logger.info("RetrievalQA chain created successfully.")
        return qa_chain
    except Exception as e:
        error_message = CustomException(message="Error occurred while creating QA chain.", error_detail=e)
        logger.error(str(error_message))
        return None