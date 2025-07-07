EVIDENCE_BASE_PATH = "/home/user123/Bandhav_project/AI_lawyer/data/client/ravi_case/evidence"

def analyze_evidence(case):
    result = "\n📎 Evidence Analysis:\n"
    for ev in case["evidence"]:
        try:
            with open(f"{EVIDENCE_BASE_PATH}/{ev}", "r", encoding="utf-8") as f:
                content = f.read().strip()
                result += f"📄 {ev}: {content[:300]}...\n"
        except FileNotFoundError:
            result += f"❌ Could not find {ev}\n"
    return result
