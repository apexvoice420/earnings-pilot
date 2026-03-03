import chromadb
import os

# Use /tmp for Railway ephemeral storage or local ./chroma_db
CHROMA_PATH = os.getenv("CHROMA_PATH", "/tmp/chroma_db" if os.environ.get("RAILWAY_ENVIRONMENT") else "./chroma_db")

class VectorStore:
    def __init__(self, path=None):
        self.path = path or CHROMA_PATH
        try:
            self.client = chromadb.PersistentClient(path=self.path)
            self.collection = self.client.get_or_create_collection("earnings_data")
        except Exception as e:
            print(f"ChromaDB init error: {e}")
            self.client = None
            self.collection = None

    def add_documents(self, texts, metadatas):
        if not texts or not self.collection:
            return
        
        try:
            from src.embeddings import embed_texts
            embeddings = embed_texts(texts)
            if not embeddings:
                # Fallback: add without embeddings
                ids = [f"doc_{i}_{hash(text)}" for i, text in enumerate(texts)]
                self.collection.add(
                    documents=texts,
                    metadatas=metadatas,
                    ids=ids
                )
            else:
                ids = [f"doc_{i}_{hash(text)}" for i, text in enumerate(texts)]
                self.collection.add(
                    embeddings=embeddings,
                    documents=texts,
                    metadatas=metadatas,
                    ids=ids
                )
        except Exception as e:
            print(f"Error adding documents: {e}")

    def search(self, query, k=5):
        if not self.collection:
            return {"documents": [], "metadatas": []}
        
        try:
            from src.embeddings import embed_texts
            query_embeddings = embed_texts([query])
            if query_embeddings:
                return self.collection.query(
                    query_embeddings=query_embeddings,
                    n_results=k
                )
            else:
                return self.collection.query(
                    query_texts=[query],
                    n_results=k
                )
        except Exception as e:
            print(f"Search error: {e}")
            return {"documents": [], "metadatas": []}

    def clear_all(self):
        try:
            if self.client:
                self.client.delete_collection("earnings_data")
                self.collection = self.client.get_or_create_collection("earnings_data")
        except Exception as e:
            print(f"Clear error: {e}")

def get_store():
    return VectorStore()
