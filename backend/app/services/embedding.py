from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_query(query):
    embedding = model.encode(query)
    return np.array(embedding).astype("float32")






