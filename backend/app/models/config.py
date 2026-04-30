import os
from dotenv import load_dotenv

load_dotenv()

# LLM CONFIG (Ollama)
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral")

# Full endpoint (used in llm.py)
OLLAMA_GENERATE_URL = f"{OLLAMA_BASE_URL}/api/generate"


# RAG CONFIG

TOP_K = int(os.getenv("TOP_K", 4))


# EMBEDDING CONFIG
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")