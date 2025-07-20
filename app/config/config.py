import os

# --- START: MODIFIED CODE ---
# Get the absolute path of the project root directory
# This assumes config.py is in app/config/
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# Enhanced logging for config initialization
print(f"CONFIG: __file__ = {__file__}")
print(f"CONFIG: os.path.dirname(__file__) = {os.path.dirname(__file__)}")
print(f"CONFIG: PROJECT_ROOT = {PROJECT_ROOT}")
print(f"CONFIG: PROJECT_ROOT exists = {os.path.exists(PROJECT_ROOT)}")
# --- END: MODIFIED CODE ---

HF_TOKEN = os.getenv("HF_TOKEN")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

print(f"CONFIG: HF_TOKEN = {'SET' if HF_TOKEN else 'NOT SET'}")
print(f"CONFIG: HUGGINGFACE_API_KEY = {'SET' if HUGGINGFACE_API_KEY else 'NOT SET'}")

if not HF_TOKEN or not HUGGINGFACE_API_KEY:
    raise ValueError("HF_TOKEN and HUGGINGFACE_API_KEY must be set in the environment variables.")
 
HUGGINGFACE_REPO_ID="mistralai/Mistral-7B-Instruct-v0.3"
# --- START: MODIFIED CODE ---
DB_FAISS_PATH = os.path.join(PROJECT_ROOT, "vectorstore/db_faiss")
DATA_PATH = os.path.join(PROJECT_ROOT, "app/DATA/")

print(f"CONFIG: DB_FAISS_PATH = {DB_FAISS_PATH}")
print(f"CONFIG: DB_FAISS_PATH exists = {os.path.exists(DB_FAISS_PATH)}")
print(f"CONFIG: DATA_PATH = {DATA_PATH}")
print(f"CONFIG: DATA_PATH exists = {os.path.exists(DATA_PATH)}")
# --- END: MODIFIED CODE ---
CHUNK_SIZE=500
CHUNK_OVERLAP=50
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
print(f"CONFIG: GROQ_API_KEY = {'SET' if GROQ_API_KEY else 'NOT SET'}")