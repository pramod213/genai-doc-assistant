from fastapi import APIRouter

from app.models.chat import ChatRequest
from app.services.embedding import embed_query
from app.services.retrieval import search_vectors
from app.services.llm import generate_answer

router = APIRouter()


@router.post("/")
def ask(request: ChatRequest):
    query_vector = embed_query(request.query)

    relevant_chunks, sources = search_vectors(query_vector)

    answer = generate_answer(request.query, relevant_chunks)

    return {
        "query": request.query,
        "answer": answer,
        "sources": list(set(sources))
    }