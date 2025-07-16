import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from app.components.retriver import create_qa_chain
from app.common.logger import get_logger
from app.common.custom_exceptions import CustomException

# Load environment variables from .env file
load_dotenv()

# Initialize logger
logger = get_logger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Medical RAG Chatbot API",
    description="API for the Medical RAG Chatbot",
    version="1.0.0"
)

# Pydantic model for the request body
class ChatRequest(BaseModel):
    query: str

# Global variable to hold the QA chain
qa_chain = None

@app.on_event("startup")
def startup_event():
    """
    Load the QA chain at application startup to avoid loading it on every request.
    """
    global qa_chain
    logger.info("Application startup: Loading QA chain...")
    try:
        qa_chain = create_qa_chain()
        if qa_chain is None:
            raise CustomException("Failed to create QA chain on startup.")
        logger.info("QA chain loaded successfully.")
    except Exception as e:
        logger.error(f"Fatal error during startup: {e}")
        qa_chain = None

async def stream_response_generator(query: str):
    """
    Asynchronously generates the response from the RAG chain.
    """
    if qa_chain is None:
        error_msg = "QA chain is not available. The application might have failed to start correctly."
        logger.error(error_msg)
        yield f"Error: {error_msg}"
        return

    try:
        logger.info(f"Received query: {query}")
        loop = asyncio.get_running_loop()
        response = await loop.run_in_executor(None, qa_chain, {"query": query})
        
        result = response.get("result", "Sorry, I could not find an answer.")
        logger.info(f"Generated response: {result}")
        yield result

    except Exception as e:
        error_message = CustomException(message="Error occurred while processing chat request.", error_detail=e)
        logger.error(str(error_message))
        yield f"Error: An internal error occurred. Please check the server logs."


@app.post("/api/chat")
async def chat(request: ChatRequest):
    """
    Endpoint to handle chat requests. It receives a query and returns a streaming response.
    """
    logger.info(f"Received request for /api/chat with query: {request.query}")
    if not request.query:
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    return StreamingResponse(stream_response_generator(request.query), media_type="text/plain")

@app.get("/")
def read_root():
    """
    Root endpoint to check if the API is running.
    """
    return {"message": "Welcome to the Medical RAG Chatbot API"}
