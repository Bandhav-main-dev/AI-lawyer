from ai_advocate import ai_advocate_reply

print("🧑‍⚖️ Courtroom AI Advocate - Ask Legal Questions\n")
while True:
    query = input("🗨️  Judge/Opponent asks: ")
    if query.lower() in ["exit", "quit"]:
        break

    reply = ai_advocate_reply(query)
    print(f"\n🧑‍💼 AI Advocate Response:\n{reply}\n")
