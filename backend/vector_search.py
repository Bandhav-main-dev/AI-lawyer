import os
import pickle

# Folder with all your section_xxx.txt files
DOCS_DIR = "/home/user123/Bandhav_project/AI_lawyer/data/bare_acts/ipc"
OUTPUT_PKL = "/home/user123/Bandhav_project/AI_lawyer/embeddings/faiss_index/legal_docs.pkl"

documents = []

for filename in os.listdir(DOCS_DIR):
    if filename.endswith(".txt"):
        section_path = os.path.join(DOCS_DIR, filename)
        with open(section_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            documents.append({
                "title": filename.replace(".txt", "").replace("_", " ").title(),
                "text": content
            })

# Save list of dicts to pickle
with open(OUTPUT_PKL, "wb") as f:
    pickle.dump(documents, f)

print(f"✅ Created {len(documents)} legal documents and saved to ipc_docs.pkl")
