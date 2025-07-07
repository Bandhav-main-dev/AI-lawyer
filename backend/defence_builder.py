from chat_engine import search_legal_docs

def build_defense(case_data):
    query = f"How to defend a person charged with {', '.join(case_data['charges'])} if he claims: {case_data['summary']}"
    legal_refs = search_legal_docs(query, top_k=3)

    argument = f"Your Honour, as per the case summary and evidence, we submit the following defense:\n"
    for ref in legal_refs:
        argument += f"\n🔹 {ref['title']}: {ref['text'][:300]}..."

    return argument
