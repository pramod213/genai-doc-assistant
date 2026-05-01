import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.document import process_document
from app.services.embedding import create_embeddings
from app.services.retrieval import store_vectors
from app.services.document_store import add_document

router = APIRouter()


@router.post("/")
async def upload_file(file: UploadFile = File(...)):

    # Allowed file types
    allowed_extensions = (".pdf", ".txt")

    # Safe filename handling
    filename = file.filename or ""

    # Validate file extension
    if not filename.lower().endswith(allowed_extensions):
        raise HTTPException(
            status_code=400,
            detail="Only PDF and TXT files are allowed"
        )
        
        
    # Save document metadata
    document = add_document(filename)
    doc_id = document["id"]

    # Process document (extract text + chunking)
    chunks = await process_document(file,doc_id)

    # Generate embeddings
    vectors = create_embeddings(chunks)

    # Store vectors in FAISS
    store_vectors(chunks, vectors)
    

    return {
        "message": "File processed successfully",
        "document": document,
        "chunks": len(chunks)
    }
