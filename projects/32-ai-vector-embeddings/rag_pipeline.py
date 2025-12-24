import json
import random
import math

# Simulating an Embedding Model (e.g., OpenAI text-embedding-ada-002)
# Real models return 1536-dimensional vectors. We mock 4 dimensions.
def mock_embedding_model(text):
    random.seed(len(text)) # Deterministic for demo
    return [round(random.uniform(-1, 1), 4) for _ in range(4)]

def chunk_text(text, chunk_size=50):
    """Simple character chunker"""
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def cosine_similarity(v1, v2):
    "Compute similarity between two vectors"
    dot_product = sum(a*b for a, b in zip(v1, v2))
    magnitude = math.sqrt(sum(a*a for a in v1)) * math.sqrt(sum(b*b for b in v2))
    return dot_product / magnitude

def run_pipeline():
    # 1. Raw Data (Unstructured)
    document = """
    AWS Glue is a serverless data integration service that makes it easy to discover, prepare, and combine data for analytics, machine learning, and application development. 
    Amazon Kinesis makes it easy to collect, process, and analyze real-time, streaming data so you can get timely insights and react quickly to new information.
    """
    
    print("--- 1. Ingestion: Raw Text ---")
    print(document.strip()[:100] + "...")
    
    # 2. Chunking
    chunks = chunk_text(document.strip())
    print(f"\n--- 2. ETL: Splitting into {len(chunks)} Chunks ---")
    
    # 3. Embedding (The Magic)
    vector_db = []
    for i, chunk in enumerate(chunks):
        vector = mock_embedding_model(chunk)
        record = {"id": i, "text": chunk, "vector": vector}
        vector_db.append(record)
        print(f"Chunk {i}: '{chunk[:20]}...' -> Vector: {vector}")

    # 4. Retrieval (Semantic Search Simulation)
    print("\n--- 4. Query: 'Streaming Data' ---")
    query_text = "Streaming Data"
    query_vector = mock_embedding_model(query_text)
    
    # Brute Force Nearest Neighbor Search
    best_match = None
    best_score = -1
    
    for record in vector_db:
        score = cosine_similarity(query_vector, record['vector'])
        if score > best_score:
            best_score = score
            best_match = record
            
    print(f"Nearest Neighbor Finding...")
    print(f"Best Match (Score {best_score:.4f}):")
    print(f" -> '{best_match['text']}...'")
    # Notice: In a real model, 'Streaming' would semantically match the Kinesis chunk.

if __name__ == "__main__":
    run_pipeline()
