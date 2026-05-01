from fastapi import APIRouter, HTTPException

from app.services.document_store import (
    load_documents,
    delete_document_by_id
)

router = APIRouter()


@router.get("/documents")
def get_documents():
    return {
        "documents": load_documents()
    }

@router.delete("/documents/{doc_id}")
def delete_document_by_document_id(doc_id: int):

    deleted = delete_document_by_id(doc_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    return {
        "message": "Document deleted successfully"
    }