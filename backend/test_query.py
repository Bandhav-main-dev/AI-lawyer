import chat_engine

# Example query to test the search engine
if __name__ == "__main__":
    print("⚖️ Testing AI Lawyer Query Engine ⚖️")
    query = "What is the punishment for theft?"
    results = chat_engine.search_legal_docs(query, top_k=3)

    for i, res in enumerate(results, 1):
        print(f"\n🔹 Result {i}: {res['title']}")
        print(f"📘 {res['text'][:500]}...\n")
