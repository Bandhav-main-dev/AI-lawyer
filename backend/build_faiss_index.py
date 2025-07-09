# generate_faiss_index.py

import os
import pickle
import faiss
from sentence_transformers import SentenceTransformer

# Load Legal-BERT model
model = SentenceTransformer("nlpaueb/legal-bert-base-uncased")

documents = []
metadata = []

# Update this path to match your actual IPC section folder
IPC_FOLDER = "/workspaces/AI-lawyer/data/bare_acts/ipc"  # or "data/laws/ipc" if running from project root

for filename in os.listdir(IPC_FOLDER):
    if filename.endswith(".txt"):
        section_path = os.path.join(IPC_FOLDER, filename)
        with open(section_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            title = filename.replace("_", " ").replace(".txt", "")
            
            documents.append(content)
            metadata.append({
                "title": title,
                "content": content
            })

# Generate embeddings
print(f"Embedding {len(documents)} sections...")
embeddings = model.encode(documents, show_progress_bar=True)

# Build FAISS index
dimension = embeddings[0].shape[0]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# Ensure output directory exists
output_dir = "../embeddings/faiss_index"
os.makedirs(output_dir, exist_ok=True)

# Save index and metadata
faiss.write_index(index, os.path.join(output_dir, "index.faiss"))
with open(os.path.join(output_dir, "metadata.pkl"), "wb") as f:
    pickle.dump(metadata, f)

print(f"✅ Saved FAISS index and metadata for {len(documents)} legal sections.")
