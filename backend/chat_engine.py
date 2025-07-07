import os
import faiss
import pickle
import numpy as np
from typing import List, Dict
from sentence_transformers import SentenceTransformer

# Load the SentenceTransformer model
MODEL_PATH = "nlpaueb/legal-bert-base-uncased"
model = SentenceTransformer(MODEL_PATH)

# FAISS and document paths
INDEX_PATH = "embeddings/faiss_index/legal_index.faiss"
DOCS_PATH = "embeddings/faiss_index/legal_docs.pkl"

# Load FAISS index
index = faiss.read_index(INDEX_PATH)

# Load document metadata
with open(DOCS_PATH, "rb") as f:
    documents = pickle.load(f)  # List of dicts: [{'title': ..., 'text': ...}, ...]

def search_legal_docs(query: str, top_k: int = 5) -> List[Dict[str, str]]:
    """
    Semantic search for relevant legal documents using FAISS and Legal-BERT.
    """
    query_vector = model.encode([query], convert_to_numpy=True)
    D, I = index.search(query_vector, top_k)

    results = []
    for idx, score in zip(I[0], D[0]):
        if idx < len(documents):
            results.append({
                "title": documents[idx]["title"],
                "text": documents[idx]["text"],
                "score": float(score)
            })

    return results

# Standalone test
if __name__ == "__main__":
    print("⚖️ AI Lawyer - Semantic Search Engine ⚖️")
    while True:
        query = input("\nAsk a legal question (or type 'exit'): ")
        if query.lower() == 'exit':
            break

        top_results = search_legal_docs(query, top_k=3)
        for i, res in enumerate(top_results, 1):
            print(f"\n🔹 Result {i}: {res['title']}")
            print(f"📘 {res['text'][:500]}...\n")
