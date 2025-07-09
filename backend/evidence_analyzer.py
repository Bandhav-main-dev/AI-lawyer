import os
import uuid
import json
import pytesseract
import whisper
import moviepy.editor as mp
from PIL import Image

# Load Whisper model once
_whisper_model = None
def get_whisper_model():
    global _whisper_model
    if _whisper_model is None:
        _whisper_model = whisper.load_model("base")
    return _whisper_model


def extract_text_from_image(image_path):
    image = Image.open(image_path)
    return pytesseract.image_to_string(image)


def extract_text_from_audio(audio_path):
    model = get_whisper_model()
    result = model.transcribe(audio_path)
    return result["text"]


def extract_text_from_video(video_path):
    clip = mp.VideoFileClip(video_path)
    audio_temp = f"/tmp/audio_{uuid.uuid4()}.wav"
    clip.audio.write_audiofile(audio_temp)
    return extract_text_from_audio(audio_temp)


def extract_text_from_txt(txt_path):
    with open(txt_path, "r", encoding="utf-8") as f:
        return f.read()


def process_uploaded_evidence(case_id, file_bytes, file_name, evidence_dir, generate_defense_questions_func):
    file_ext = file_name.split(".")[-1].lower()
    filename_base = f"{case_id}_{file_name}"
    saved_path = os.path.join(evidence_dir, filename_base)

    # Save the uploaded file
    with open(saved_path, "wb") as f:
        f.write(file_bytes)

    # Extract text from file based on type
    if file_ext in ["png", "jpg", "jpeg"]:
        evidence_text = extract_text_from_image(saved_path)
    elif file_ext in ["wav", "mp3", "m4a"]:
        evidence_text = extract_text_from_audio(saved_path)
    elif file_ext in ["mp4", "avi", "mkv"]:
        evidence_text = extract_text_from_video(saved_path)
    elif file_ext == "txt":
        evidence_text = extract_text_from_txt(saved_path)
    else:
        raise ValueError("Unsupported file type for evidence processing")

    # Generate questions
    questions = generate_defense_questions_func("", evidence_text)
    question_path = os.path.join(evidence_dir, f"{filename_base}_pending_questions.json")
    with open(question_path, "w") as f:
        json.dump(questions, f, indent=2)

    return {
        "filename": filename_base,
        "saved_path": saved_path,
        "extracted_text": evidence_text,
        "questions": questions,
        "questions_path": question_path
    }