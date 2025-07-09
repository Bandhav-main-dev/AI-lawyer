import spacy
from transformers import pipeline
from difflib import SequenceMatcher

nlp = spacy.load("en_core_web_sm")
qg_pipeline = pipeline("text2text-generation", model="mrm8488/t5-base-finetuned-question-generation-ap")

def is_contradictory(client_line, witness_line, threshold=0.8):
    ratio = SequenceMatcher(None, client_line.lower(), witness_line.lower()).ratio()
    return ratio < threshold

def generate_defense_questions(client_statement, witness_statement):
    client_sents = [sent.text.strip() for sent in nlp(client_statement).sents if len(sent.text.strip()) > 10]
    witness_sents = [sent.text.strip() for sent in nlp(witness_statement).sents if len(sent.text.strip()) > 10]

    if not client_sents:
        print("❌ No client sentences found.")
    if not witness_sents:
        print("❌ No witness sentences found.")

    questions = []

    for w_sent in witness_sents:
        for c_sent in client_sents:
            if is_contradictory(c_sent, w_sent):
                prompt = f"Cross-examine this claim to defend the client: {w_sent}"
                try:
                    result = qg_pipeline(prompt)[0]['generated_text']
                    questions.append(result)
                except Exception as e:
                    print(f"❌ QG failed: {e}")
                break  # Only need to challenge once per witness sentence

    print(f"✅ Generated {len(questions)} questions.")
    return list(set(questions))

def load_qg_model():
    return pipeline("text2text-generation", model="valhalla/t5-small-qg-hl")

def highlight_text(text, max_sentences=50):
    sentences = text.split(". ")
    highlighted = []
    for sentence in sentences:
        input_text = f"highlight: {sentence.strip()} context: {text}"
        highlighted.append(input_text)
    return highlighted[:max_sentences]

def generate_questions_from_evidence(evidence_text):
    highlighted_inputs = highlight_text(evidence_text)
    questions = []
    for item in highlighted_inputs:
        output = qg_pipeline(item, max_length=64)[0]['generated_text']
        questions.append(output)
    return list(set(questions))
