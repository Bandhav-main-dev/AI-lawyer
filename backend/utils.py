import os
import json

def load_all_chat_for_case(case_id):
    chat_file = f"case_data/{case_id}_chat.json"
    if os.path.exists(chat_file):
        with open(chat_file, "r") as f:
            chat_data = json.load(f)
            return "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in chat_data])
    return ""

def load_defense_notes(case_id):
    notes_file = f"case_data/{case_id}_defense_notes.txt"
    if os.path.exists(notes_file):
        with open(notes_file, "r") as f:
            return f.read()
    return ""
