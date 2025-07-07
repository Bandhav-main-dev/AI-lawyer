from chat_engine import search_legal_docs
from typing import List
import random

# Legal court-style reply templates
INTRO_LINES = [
    "Your honor, with due respect,",
    "May it please the court,",
    "With the court's permission, I submit that",
    "Respected judge, I would like to bring to light that"
]

CLOSING_LINES = [
    "Therefore, I seek your kind consideration in this matter.",
    "Thus, I respectfully request the court to evaluate this in favor of my client.",
    "Hence, I appeal to the court for dismissal of the accusation.",
    "Accordingly, the defense rests its submission."
]

def format_legal_response(query: str, results: List[dict]) -> str:
    """
    Compose a courtroom-style legal argument using retrieved IPC sections.
    """
    intro = random.choice(INTRO_LINES)
    closing = random.choice(CLOSING_LINES)

    argument = f"{intro} the query raised is: \"{query}\".\n"

    for doc in results:
        argument += (
            f"\n📘 As per *{doc['title']}*,\n"
            f"{doc['text'][:500].strip()}...\n"
        )

    argument += f"\n{closing}"
    return argument

def ai_advocate_reply(query: str, top_k: int = 3) -> str:
    results = search_legal_docs(query, top_k)
    return format_legal_response(query, results)
