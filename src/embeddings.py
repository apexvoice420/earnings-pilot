"""
Embeddings - Mock implementation for Railway deployment
Uses simple hash-based embeddings that don't require external API
"""
import hashlib

def embed_texts(texts):
    """
    Generate deterministic embeddings based on text hash.
    No external API required - works on Railway without OPENAI_API_KEY.
    """
    embeddings = []
    for text in texts:
        # Create a deterministic 1536-dim embedding from text hash
        text_hash = hashlib.sha256(text.encode()).hexdigest()
        
        # Convert hash to numbers and normalize
        embedding = []
        for i in range(0, len(text_hash), 2):
            val = int(text_hash[i:i+2], 16) / 255.0
            embedding.append(val)
        
        # Pad or truncate to 1536 dimensions
        while len(embedding) < 1536:
            embedding.extend(embedding[:min(len(embedding), 1536 - len(embedding))])
        
        embeddings.append(embedding[:1536])
    
    return embeddings
