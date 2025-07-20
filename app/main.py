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
import os

# ...existing code...
app = FastAPI()
logger = get_logger(__name__)

# Enhanced startup logging
logger.info("=== APPLICATION STARTUP ===")
logger.info(f"Python version: {os.sys.version}")
logger.info(f"Current working directory: {os.getcwd()}")

# Log environment variables (safely)
env_vars_to_check = ["HF_TOKEN", "HUGGINGFACE_API_KEY", "GROQ_API_KEY", "USE_CUDA"]
for var in env_vars_to_check:
    value = os.getenv(var)
    if value:
        if "TOKEN" in var or "KEY" in var:
            logger.info(f"{var}: SET (length: {len(value)})")
        else:
            logger.info(f"{var}: {value}")
    else:
        logger.warning(f"{var}: NOT SET")

# Log configuration paths
from app.config.config import DB_FAISS_PATH, DATA_PATH, PROJECT_ROOT
logger.info(f"PROJECT_ROOT: {PROJECT_ROOT}")
logger.info(f"DB_FAISS_PATH: {DB_FAISS_PATH}")
logger.info(f"DATA_PATH: {DATA_PATH}")
logger.info("=== APPLICATION STARTUP COMPLETE ===")

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

@app.get("/health")
async def health_check():
    """Enhanced health check endpoint with detailed diagnostics"""
    try:
        logger.info("=== HEALTH CHECK START ===")
        
        health_status = {
            "status": "healthy",
            "timestamp": str(asyncio.get_event_loop().time()),
            "checks": {}
        }
        
        # Check 1: Vector store
        try:
            logger.info("Health check: Testing vector store...")
            vector_store = load_vector_store()
            if vector_store is None:
                health_status["checks"]["vector_store"] = {"status": "FAILED", "error": "Vector store is None"}
                health_status["status"] = "unhealthy"
            else:
                health_status["checks"]["vector_store"] = {"status": "OK", "type": str(type(vector_store))}
        except Exception as e:
            health_status["checks"]["vector_store"] = {"status": "FAILED", "error": str(e)}
            health_status["status"] = "unhealthy"
        
        # Check 2: Embeddings
        try:
            logger.info("Health check: Testing embeddings...")
            from app.components.embeddings import get_hf_embeddings_model
            embeddings = get_hf_embeddings_model()
            health_status["checks"]["embeddings"] = {"status": "OK", "type": str(type(embeddings))}
        except Exception as e:
            health_status["checks"]["embeddings"] = {"status": "FAILED", "error": str(e)}
            health_status["status"] = "unhealthy"
        
        # Check 3: LLM
        try:
            logger.info("Health check: Testing LLM...")
            llm = load_llm()
            health_status["checks"]["llm"] = {"status": "OK", "type": str(type(llm))}
        except Exception as e:
            health_status["checks"]["llm"] = {"status": "FAILED", "error": str(e)}
            health_status["status"] = "unhealthy"
        
        # Check 4: Environment variables
        env_check = {}
        for var in ["HF_TOKEN", "HUGGINGFACE_API_KEY", "GROQ_API_KEY"]:
            env_check[var] = "SET" if os.getenv(var) else "NOT_SET"
        health_status["checks"]["environment"] = env_check
        
        # Check 5: File system
        health_status["checks"]["filesystem"] = {
            "db_faiss_path_exists": os.path.exists(DB_FAISS_PATH),
            "data_path_exists": os.path.exists(DATA_PATH),
            "working_directory": os.getcwd()
        }
        
        logger.info(f"Health check completed: {health_status['status']}")
        logger.info("=== HEALTH CHECK END ===")
        
        return health_status
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": str(asyncio.get_event_loop().time())
        }
@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        logger.info(f"=== CHAT REQUEST START ===")
        logger.info(f"Received chat request with question: {request.question}")
        logger.info(f"Question length: {len(request.question)} characters")
        
        # Step 1: Load vector store with enhanced logging
        logger.info("STEP 1: Loading vector store...")
        vector_store = load_vector_store()
        
        if vector_store is None:
            logger.error("CRITICAL: Vector store is None! Cannot proceed.")
            raise HTTPException(status_code=500, detail="Vector store failed to load")
        
        logger.info(f"Vector store loaded successfully. Type: {type(vector_store)}")
        
        # Step 2: Create retriever with enhanced logging
        logger.info("STEP 2: Creating retriever...")
        try:
            retriever = vector_store.as_retriever()
            logger.info(f"Retriever created successfully. Type: {type(retriever)}")
        except Exception as e:
            logger.error(f"CRITICAL: Failed to create retriever: {str(e)}")
            raise e
        
        # Step 3: Retrieve relevant documents
        logger.info("STEP 3: Retrieving relevant documents...")
        try:
            docs = retriever.get_relevant_documents(query=request.question)
            logger.info(f"Retrieved {len(docs)} documents")
            for i, doc in enumerate(docs):
                logger.info(f"Document {i+1}: {len(doc.page_content)} characters")
        except Exception as e:
            logger.error(f"CRITICAL: Failed to retrieve documents: {str(e)}")
            raise e
        
        # Step 4: Build context
        logger.info("STEP 4: Building context...")
        context = "\n".join([doc.page_content for doc in docs])
        logger.info(f"Context built: {len(context)} characters")
        
        # Step 5: Format prompt
        logger.info("STEP 5: Formatting prompt...")
        prompt = CUSTOM_PROMPT_TEMPLATE.format(context=context, question=request.question)
        logger.info(f"Prompt formatted: {len(prompt)} characters")
        
        # Step 6: Load LLM
        logger.info("STEP 6: Loading LLM...")
        llm = load_llm(model_name="llama-3.1-8b-instant")

        # Step 6: Load LLM
        logger.info("STEP 6: Loading LLM...")
        llm = load_llm(model_name="llama-3.1-8b-instant")
        logger.info(f"LLM loaded successfully. Type: {type(llm)}")

        # Step 7: Stream response
        logger.info("STEP 7: Starting streaming response...")
        
        async def stream_response():
            chunk_count = 0
            total_content = ""
            try:
                logger.info("Beginning LLM streaming...")
                for chunk in llm.stream(prompt):
                    chunk_count += 1
                    content = ""
                    if hasattr(chunk, "content"):
                        content = chunk.content
                    elif isinstance(chunk, dict) and "content" in chunk:
                        content = chunk["content"]
                    
                    if content:
                        total_content += content
                        yield content
                        await asyncio.sleep(0.05)  # <-- Slow down streaming (50ms per chunk)
                
                logger.info(f"Streaming completed. Total chunks: {chunk_count}, Total content length: {len(total_content)}")
                logger.info(f"=== CHAT REQUEST END ===")
                
            except Exception as stream_e:
                logger.error(f"CRITICAL: Error during streaming: {str(stream_e)}")
                yield f"Error during streaming: {str(stream_e)}"

        return StreamingResponse(stream_response(), media_type="text/plain")
        
    except Exception as e:
        logger.error(f"=== CHAT REQUEST FAILED ===")
        logger.error(f"Error in /api/chat: {str(e)}", exc_info=True)
        logger.error(f"Error type: {type(e)}")
        logger.error(f"Error details: {repr(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")