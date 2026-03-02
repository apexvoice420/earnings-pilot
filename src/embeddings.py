from openai import OpenAI
from src.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def embed_texts(texts):
    """
    Returns a list of embeddings for the given texts using OpenAI text-embedding-3-small.
    """
    if not OPENAI_API_KEY:
        # Mock embeddings for testing if no key
        return [[0.0] * 1536 for _ in texts]

    response = client.embeddings.create(
        input=texts,
        model="text-embedding-3-small"
    )
    return [data.embedding for data in response.data]
