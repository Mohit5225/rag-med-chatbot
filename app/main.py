from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.components.retriver import create_qa_chain
from app.common.logger import get_logger
import dotenv; dotenv.load_dotenv()
# ...existing code...
app = FastAPI()
logger = get_logger(__name__)

# Allow frontend dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    question: str  # changed from query

class ChatResponse(BaseModel):
    answer: str

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        logger.info(f"Received chat request with question: {request.question}")
        
        qa_chain = create_qa_chain()
        if not qa_chain:
            logger.error("QA chain initialization failed")
            raise HTTPException(status_code=500, detail="QA chain could not be initialized.")
        
        logger.info("QA chain initialized successfully, invoking with question")
        result = qa_chain.invoke({"query": request.question})
        
        answer = result.get("result", "") if isinstance(result, dict) else str(result)
        logger.info(f"Generated answer: {answer[:50]}...")
        
        return ChatResponse(answer=answer)
    except Exception as e:
        logger.error(f"Error in /api/chat: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")