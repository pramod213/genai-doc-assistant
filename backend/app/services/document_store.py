import uuid
import json
import os

DOCUMENTS_FILE = "app/data/documents.json"


def load_documents():

    if not os.path.exists(DOCUMENTS_FILE):
        return []

    with open(DOCUMENTS_FILE, "r") as f:

        content = f.read().strip()

        if not content:
            return []

        return json.loads(content)


def save_documents(documents):
    with open(DOCUMENTS_FILE, "w") as f:
        json.dump(documents, f, indent=4)


def add_document(filename):
    documents = load_documents()

    new_doc = {
        "id": str(uuid.uuid4()),
        "filename": filename
    }

    documents.append(new_doc)

    save_documents(documents)

    return new_doc


def delete_document_by_id(doc_id):
    documents = load_documents()

    updated_documents = [
        doc for doc in documents
        if doc["id"] != doc_id
    ]

    save_documents(updated_documents)

    return len(updated_documents) != len(documents)