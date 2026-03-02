import chromadb
from src.embeddings import embed_texts

class VectorStore:
    def __init__(self, path="./chroma_db"):
        self.client = chromadb.PersistentClient(path=path)
        self.collection = self.client.get_or_create_collection("earnings_data")

    def add_documents(self, texts, metadatas):
        if not texts:
            return
            
        embeddings = embed_texts(texts)
        ids = [f"doc_{i}_{hash(text)}" for i, text in enumerate(texts)]
        
        self.collection.add(
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )

    def search(self, query, k=5):
        query_embeddings = embed_texts([query])
        results = self.collection.query(
            query_embeddings=query_embeddings,
            n_results=k
        )
        return results

    def clear_all(self):
        self.client.delete_collection("earnings_data")
        self.collection = self.client.get_or_create_collection("earnings_data")

def get_store():
    return VectorStore()
