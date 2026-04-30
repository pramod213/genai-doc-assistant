from fastapi import APIRouter, UploadFile, File, HTTPException
import uuid

from app.services.document import extract_text, chunk_text
from app.services.embedding import model
from app.services.retrieval import vector_store

router = APIRouter()

DOCUMENT_STORE = {}


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    try:
        doc_id = str(uuid.uuid4())

        text = extract_text(file)

        if not text:
            raise HTTPException(status_code=400, detail="No text extracted")

        chunks = chunk_text(text)

        embeddings = model.encode(chunks)

        vector_store.add(doc_id, chunks, embeddings)

        DOCUMENT_STORE[doc_id] = {
            "filename": file.filename,
            "chunks": len(chunks)
        }

        return {
            "message": "Document uploaded successfully",
            "document_id": doc_id,
            "chunks": len(chunks)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




