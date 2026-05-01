
import faiss
import numpy as np

dimension = 384
index = faiss.IndexFlatL2(dimension)

stored_chunks = []
stored_sources = []


def store_vectors(chunks, vectors):
    global stored_chunks, stored_sources

    for chunk in chunks:
        stored_chunks.append(chunk["text"])
        stored_sources.append(chunk["source"])

    index.add(np.array(vectors))             #type:ignore


def search_vectors(query_vector, top_k=3):
    D, I = index.search(np.array([query_vector]), top_k)   #type:ignore

    results = []
    sources = set()

    for idx in I[0]:
        if idx < len(stored_chunks):
            results.append(stored_chunks[idx])
            sources.add(stored_sources[idx])

    return results, list(sources)






