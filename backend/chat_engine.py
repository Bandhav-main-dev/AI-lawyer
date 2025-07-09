import os
import faiss
import pickle
from typing import List, Dict
from sentence_transformers import SentenceTransformer
import numpy as np

# Model and file paths
MODEL_PATH = "nlpaueb/legal-bert-base-uncased"
INDEX_PATH = "/workspaces/AI-lawyer/embeddings/faiss_index/legal_index.faiss"
DOCS_PATH = "/workspaces/AI-lawyer/embeddings/faiss_index/legal_docs.pkl"

# Load the SentenceTransformer model
try:
    model = SentenceTransformer(MODEL_PATH)
except Exception as e:
    print(f"⚠️ Error loading SentenceTransformer: {e}")
    model = None

# Initialize variables
index = None
documents = []

# Try loading FAISS index and legal documents
if os.path.exists(INDEX_PATH) and os.path.exists(DOCS_PATH):
    try:
        index = faiss.read_index(INDEX_PATH)
        with open(DOCS_PATH, "rb") as f:
            documents = pickle.load(f)
        print(f"✅ Loaded {len(documents)} documents for semantic search.")
    except Exception as e:
        print(f"⚠️ Failed to load FAISS index or documents: {e}")
        index = None
        documents = []
else:
    print("⚠️ Semantic search disabled — index or documents not found.")

with open("/workspaces/AI-lawyer/embeddings/faiss_index/legal_docs.pkl", "rb") as f:
    metadata = pickle.load(f)

def search_similar_sections(query, top_k=2):
    embedding = model.encode([query])
    distances, indices = index.search(np.array(embedding), top_k)
    results = []
    for i in indices[0]:
        results.append(metadata[i])  # Should have 'content'
    return results


def search_legal_docs(query: str, top_k: int = 5) -> List[Dict[str, str]]:
    """
    Semantic search for relevant legal documents using FAISS + Legal-BERT.
    """
    if index is None or model is None or not documents:
        return [{
            "title": "Search Engine Unavailable",
            "text": "Legal search is disabled. Please generate FAISS index and document embeddings.",
            "score": 0.0
        }]
    
    try:
        query_vector = model.encode([query], convert_to_numpy=True)
        D, I = index.search(query_vector, top_k)

        results = []
        for idx, score in zip(I[0], D[0]):
            if 0 <= idx < len(documents):
                results.append({
                    "title": documents[idx].get("title", f"Document {idx+1}"),
                    "text": documents[idx].get("text", "No content found."),
                    "score": float(score)
                })

        return results
    except Exception as e:
        return [{
            "title": "Search Error",
            "text": f"Error during semantic search: {str(e)}",
            "score": 0.0
        }]
