import faiss
import numpy as np


class VectorStore:
    def __init__(self, dim=384):
        self.index = faiss.IndexFlatIP(dim)
        self.data = []

    def normalize(self, vectors):
        vectors = np.array(vectors)

        if vectors.ndim == 1:
            vectors = vectors.reshape(1, -1)

        norm = np.linalg.norm(vectors, axis=1, keepdims=True) + 1e-10
        return vectors / norm

    def add(self, doc_id, chunks, embeddings):
        embeddings = np.array(embeddings)

        if embeddings.ndim == 1:
            embeddings = embeddings.reshape(1, -1)

        embeddings = self.normalize(embeddings).astype("float32")

        self.index.add(embeddings) #type:ignore

        for chunk in chunks:
            self.data.append({
                "doc_id": doc_id,
                "text": chunk
            })

    def search(self, query_embedding, k=4):
        if self.index.ntotal == 0:
            return []

        query_embedding = np.array(query_embedding)

        if query_embedding.ndim == 1:
            query_embedding = query_embedding.reshape(1, -1)

        query = self.normalize(query_embedding).astype("float32")

        k = min(k, self.index.ntotal)

        _, I = self.index.search(query, k)      #type:ignore

        results = []
        for i in I[0]:
            if 0 <= i < len(self.data):
                results.append(self.data[i])

        return results


vector_store = VectorStore()








