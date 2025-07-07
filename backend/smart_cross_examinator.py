from sentence_transformers import SentenceTransformer, util
from transformers import pipeline

# Load models
semantic_model = SentenceTransformer("all-MiniLM-L6-v2")
qg_model = pipeline("text2text-generation", model="valhalla/t5-small-qg-hl")

# Detect contradictions between evidence entries
def detect_contradictions(evidence_summary, threshold=0.6):
    """
    Compares all pieces of evidence with each other and detects possible contradictions
    based on semantic dissimilarity. Returns a list of dicts with evidence pairs.
    """
    summaries = list(evidence_summary.values())
    keys = list(evidence_summary.keys())
    embeddings = semantic_model.encode(summaries, convert_to_tensor=True)
    similarity_matrix = util.pytorch_cos_sim(embeddings, embeddings)

    contradictions = []

    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            sim_score = similarity_matrix[i][j].item()
            if sim_score < threshold:
                contradictions.append({
                    "evidence_1": keys[i],
                    "evidence_2": keys[j],
                    "similarity": round(sim_score, 2)
                })

    return contradictions

# Generate questions using AI from contradictory pairs
def generate_cross_questions(evidence_summary):
    """
    Generates courtroom-style cross-examination questions based on contradictions in evidence.
    """
    contradictions = detect_contradictions(evidence_summary)
    questions = []

    for contradiction in contradictions:
        e1 = contradiction['evidence_1']
        e2 = contradiction['evidence_2']
        e1_text = evidence_summary[e1]
        e2_text = evidence_summary[e2]

        hl_input = f"generate question: {e1_text.strip()} <hl> {e2_text.strip()} <hl>"

        try:
            result = qg_model(hl_input, max_length=64, do_sample=False)
            question = result[0]['generated_text']
        except Exception as e:
            question = f"⚠️ Error generating question: {str(e)}"

        questions.append({
            "from": e1,
            "to": e2,
            "question": question,
            "similarity": contradiction['similarity']
        })

    return questions

# Print questions in a courtroom cross-examination style
def print_cross_examination(questions):
    """
    Prints cross-examination questions in courtroom-style format.
    """
    print("\n🎯 Cross-Examination Questions Based on Conflicting Evidence:\n")
    if not questions:
        print("✅ No major contradictions found between evidence.")
        return

    for q in questions:
        print(f"❓ Contradiction between [{q['from']}] and [{q['to']}]:")
        print(f"   🔍 Q: {q['question']} (Similarity: {q['similarity']})\n")

# Optionally return all summaries in a readable format
def cross_examine_evidence(evidence_summary):
    """
    Returns a consolidated report of all evidence summaries.
    """
    print("\n📚 Legal Evidence Summary:\n")
    summary = ""
    for key, value in evidence_summary.items():
        summary += f"📁 {key}:\n{value.strip()[:400]}...\n\n"
    return summary
