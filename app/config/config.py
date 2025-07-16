import os

HF_TOKEN = os.getenv("HF_TOKEN")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
if not HF_TOKEN or not HUGGINGFACE_API_KEY:
    raise ValueError("HF_TOKEN and HUGGINGFACE_API_KEY must be set in the environment variables.")
 
HUGGINGFACE_REPO_ID="mistralai/Mistral-7B-Instruct-v0.3"
DB_FAISS_PATH ="vectorstore/db_faiss"
DATA_PATH="data/"
CHUNK_SIZE=500
CHUNK_OVERLAP=50
GROQ_API_KEY = os.getenv("GROQ_API_KEY")