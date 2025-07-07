from evidence_analyzer import auto_analyze
from smart_cross_examinator import (
    cross_examine_evidence,
    detect_contradictions,
    generate_cross_questions,
    print_cross_examination
)
import os

# Set your evidence folder path
evidence_dir = "/home/user123/Bandhav_project/AI_lawyer/data/client/ravi_case/evidence/"
evidence_summary = {}

# Step 1: Auto Analyze All Evidence
print("\n🧾 Auto Evidence Analysis:")
print(os.listdir(evidence_dir))

for filename in os.listdir(evidence_dir):
    path = os.path.join(evidence_dir, filename)
    try:
        summary = auto_analyze(path)
        evidence_summary[filename] = summary
        print(f"\n📁 {filename}:\n{summary[:500]}...")
    except Exception as e:
        print(f"\n⚠️ Error analyzing {filename}: {e}")

# Step 2: Detect Potential Contradictions Between Evidence
conflicts = detect_contradictions(evidence_summary)

print("\n⚠️ Potential Contradictions:")
if conflicts:
    for c in conflicts:
        print(f"❗ Between {c['evidence_1']} and {c['evidence_2']} — Similarity: {c['similarity']:.2f}")
else:
    print("✅ No major contradictions found.")

# Step 3: Generate Cross-Examination Questions
print("\n🤖 AI Cross-Examination Based on Evidence:")
questions = generate_cross_questions(evidence_summary)
print(questions)
print_cross_examination(questions)

# Step 4: Final Legal Summary
#print(cross_examine_evidence(evidence_summary))
