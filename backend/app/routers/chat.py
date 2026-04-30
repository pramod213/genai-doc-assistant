




from fastapi import APIRouter
from pydantic import BaseModel

from app.services.embedding import embed_query
from app.services.retrieval import vector_store
from app.services.llm import generate_answer

router = APIRouter()


class Question(BaseModel):
    query: str


@router.post("/ask")
def ask_question(data: Question):

    query_embedding = embed_query(data.query)
    docs = vector_store.search(query_embedding, k=4)

    # 1. No results fallback
    if not docs:
        return {
            "answer": "I don't know based on the document. Please ask questions related to the document.",
            "sources": []
        }

    # 2. Build clean context (still used for LLM)
    context = "\n\n".join(d["text"][:800] for d in docs)

    # 3. Get LLM response
    raw_answer = generate_answer(data.query, context)

    # 4. Fallback enforcement
    if not raw_answer or "i don't know" in raw_answer.lower():
        return {
            "answer": "I don't know based on the document. Please ask questions related to the document.",
            "sources": []
        }

    # 5. Force bullet format
    if "\n" in raw_answer and not raw_answer.strip().startswith("-"):
        lines = [l.strip("-• ").strip() for l in raw_answer.split("\n") if l.strip()]
        raw_answer = "\n".join([f"- {l}" for l in lines])

    # 6. FINAL RESPONSE SHAPE (THIS IS KEY FIX)
    return {
        "answer": raw_answer.strip(),
        "sources": [
            {
                "doc_id": d.get("doc_id", "unknown"),
                "excerpt": d["text"][:100].replace("\n", " ") + "..."
            }
            for d in docs
        ]
    }




