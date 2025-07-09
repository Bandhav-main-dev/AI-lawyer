# courtroom_sim_gui.py

from transformers import pipeline
from sentence_transformers import SentenceTransformer

# ✅ Load a stable, fast Q&A pipeline (no SentencePiece required)
qa_pipeline = pipeline("question-answering", model="deepset/tinyroberta-squad2")

# ✅ Optional: SentenceTransformer for future upgrades (e.g., contradiction check)
semantic_model = SentenceTransformer("all-MiniLM-L6-v2")

def get_courtroom_response(question: str, case_summary: str) -> str:
    """
    Uses a QA model to simulate courtroom-style advocate replies
    based on the case summary as context.
    """
    try:
        result = qa_pipeline(question=question, context=case_summary)
        return f"🧑‍⚖️ AI Advocate: {result['answer']}"
    except Exception as e:
        return f"⚠️ Could not process the question due to error: {str(e)}"
