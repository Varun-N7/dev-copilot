from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

class LocalEmbedder:
    def embed_query(self, text: str) -> list:
        return model.encode(text).tolist()
    
    def embed_documents(self, texts: list) -> list:
        return model.encode(texts).tolist()

embedder = LocalEmbedder()