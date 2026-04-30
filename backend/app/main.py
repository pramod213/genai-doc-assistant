from fastapi import FastAPI
from app.routers import upload, chat

app = FastAPI(
    title="GenAI Document Assistant",
    description="RAG-based document Q&A system using FastAPI, FAISS, and LLM.",
    version="1.0.0"
)

app.include_router(upload.router)
app.include_router(chat.router)


@app.get("/")
def root():
    return {
        "message": "GenAI Document Assistant API is running",
        "docs": "/docs"
    }


@app.get("/status")
def system_status():
    return {
        "status": "running"
    }






