import os

# OpenAI API key (optional - will use mock embeddings if not set)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def embed_texts(texts):
    """
    Returns a list of embeddings for the given texts.
    Uses OpenAI text-embedding-3-small if API key is available.
    Otherwise returns mock embeddings for testing.
    """
    if not OPENAI_API_KEY:
        # Mock embeddings for testing (1536 dimensions for text-embedding-3-small)
        print("Warning: No OPENAI_API_KEY set, using mock embeddings")
        return [[0.0] * 1536 for _ in texts]
    
    try:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)
        
        response = client.embeddings.create(
            input=texts,
            model="text-embedding-3-small"
        )
        return [data.embedding for data in response.data]
    except Exception as e:
        print(f"Embedding error: {e}")
        # Return mock embeddings on failure
        return [[0.0] * 1536 for _ in texts]
