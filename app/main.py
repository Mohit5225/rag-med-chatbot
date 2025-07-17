from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.components.retriver import create_qa_chain
from app.common.logger import get_logger
import dotenv; dotenv.load_dotenv()
from fastapi.responses import StreamingResponse
import asyncio
from app.components.retriver import load_vector_store  # Add this import
from app.components.llm import load_llm  # Add this import (adjust path if needed)

# ...existing code...
app = FastAPI()
logger = get_logger(__name__)

# Define the custom prompt template
CUSTOM_PROMPT_TEMPLATE = (
    "Given the following context, answer the user's question.\n\n"
    "Context:\n{context}\n\n"
    "Question:\n{question}\n\n"
    "Answer:"
)

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
@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        logger.info(f"Received chat request with question: {request.question}")
        vector_store = load_vector_store()
        retriever = vector_store.as_retriever()
        docs = retriever.get_relevant_documents(query=request.question)
        context = "\n".join([doc.page_content for doc in docs])
        prompt = CUSTOM_PROMPT_TEMPLATE.format(context=context, question=request.question)
        llm = load_llm(model_name="llama-3.1-8b-instant")

        async def stream_response():
            for chunk in llm.stream(prompt):
                content = ""
                if hasattr(chunk, "content"):
                    content = chunk.content
                elif isinstance(chunk, dict) and "content" in chunk:
                    content = chunk["content"]
                if content:
                    yield content
                    await asyncio.sleep(0.05)  # <-- Slow down streaming (50ms per chunk)

        return StreamingResponse(stream_response(), media_type="text/plain")
    except Exception as e:
        logger.error(f"Error in /api/chat: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")