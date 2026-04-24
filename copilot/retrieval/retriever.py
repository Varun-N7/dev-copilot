import numpy as np
from pymongo import MongoClient
from copilot.embeddings import embedder
import os

def cosine_similarity(a, b):
    a, b = np.array(a), np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-10))

def retrieve_sync(query: str, repo_id: str, top_k: int = 5) -> list[dict]:
    client = MongoClient(os.environ["MONGO_URI"])
    db = client[os.environ.get("MONGO_DB_NAME", "devcopilot")]
    embeddings_col = db["embeddings"]
    query_vec = embedder.embed_query(query)
    docs = list(embeddings_col.find({"repo_id": repo_id}, {"text": 1, "filepath": 1, "embedding": 1}))
    if not docs:
        return []
    scored = [(cosine_similarity(query_vec, d["embedding"]), d) for d in docs]
    scored.sort(key=lambda x: x[0], reverse=True)
    return [
        {"text": d["text"], "filepath": d["filepath"], "score": round(s, 4)}
        for s, d in scored[:top_k]
    ]

async def retrieve(query: str, repo_id: str, top_k: int = 5) -> list[dict]:
    return retrieve_sync(query, repo_id, top_k)