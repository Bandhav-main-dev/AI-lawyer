import os
import whisper
import pytesseract
from PIL import Image
import cv2
import torch
import torchvision.transforms as T
from transformers import pipeline

# OCR & vision tools
ocr = pytesseract.pytesseract
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

# Whisper for audio
whisper_model = whisper.load_model("base")

def analyze_text_file(file_path):
    with open(file_path, 'r') as f:
        text = f.read()
    return summarizer(text, max_length=100, min_length=30, do_sample=False)[0]['summary_text']

def analyze_image(file_path):
    image = Image.open(file_path)
    text = ocr.image_to_string(image)
    return f"🖼️ Image Analysis:\nText Detected: {text.strip()[:300]}..."

def analyze_audio(file_path):
    result = whisper_model.transcribe(file_path)
    return f"🔊 Audio Transcript:\n{result['text']}"

def analyze_video(file_path, frame_interval=30):
    cap = cv2.VideoCapture(file_path)
    frame_texts = []
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret: break
        if frame_count % frame_interval == 0:
            img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            text = ocr.image_to_string(img)
            if text.strip(): frame_texts.append(text.strip())
        frame_count += 1

    cap.release()
    return f"🎥 Video OCR Summary:\n{''.join(frame_texts[:5])}..."

def auto_analyze(file_path):
    ext = os.path.splitext(file_path)[-1].lower()
    if ext in ['.txt']:
        return analyze_text_file(file_path)
    elif ext in ['.jpg', '.png', '.jpeg']:
        return analyze_image(file_path)
    elif ext in ['.mp4', '.avi', '.mov']:
        return analyze_video(file_path)
    elif ext in ['.mp3', '.wav', '.aac']:
        return analyze_audio(file_path)
    else:
        return "❌ Unsupported evidence format."
