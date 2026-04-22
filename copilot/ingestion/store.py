import time
from copilot.db import embeddings_col
from copilot.embeddings import embedder

BATCH_SIZE = 50

async def embed_and_store(repo_id: str, chunks: list[dict]) -> int:
    stored = 0
    for i in range(0, len(chunks), BATCH_SIZE):
        batch = chunks[i : i + BATCH_SIZE]
        texts = [c["text"] for c in batch]
        vectors = embedder.embed_documents(texts)
        docs = [
            {
                "_id": f"{repo_id}_{c['filepath']}_{c['chunk_index']}",
                "repo_id": repo_id,
                "text": c["text"],
                "filepath": c["filepath"],
                "language": c["language"],
                "chunk_index": c["chunk_index"],
                "embedding": v,
                "indexed_at": time.time(),
            }
            for c, v in zip(batch, vectors)
        ]
        for doc in docs:
            await embeddings_col.replace_one({"_id": doc["_id"]}, doc, upsert=True)
        stored += len(docs)
    return stored
