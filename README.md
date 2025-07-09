# ⚖️ AI Lawyer Assist – Your Intelligent Legal Companion

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-red)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/status-Active-brightgreen)

> AI Lawyer Assist is a robust legal automation system designed to streamline case registration, simulate courtroom behavior, perform intelligent legal document search, and generate personalized legal documents such as rental or NDA agreements. Powered by NLP models like Legal-BERT and tools like FAISS and Streamlit, the app bridges the gap between legal professionals and AI assistance.

---

## 🔍 Project Overview

AI Lawyer Assist is a full-stack AI legal assistant built to serve individuals, clients, and legal professionals with advanced NLP capabilities. It provides:
- Case registration and management
- Secure client and admin login
- Semantic search across Indian laws like IPC, IT Act, and NDA
- Real-time courtroom-style Q&A simulation
- Legal document generation (rental agreement/NDA)

---

## 🎯 Key Features

### 👨‍⚖️ Client Panel
- 📝 Register and manage legal cases
- 🔐 Secure login with case ID & password
- 🧠 Ask legal questions or send case notes
- ⚔️ Simulate courtroom interaction with AI advocate
- 🔍 Semantic legal search (IPC, IT Act, NDA)
- 📄 Generate rental/NDA agreement with auto-filled data

### 🛡 Admin Panel
- 🔑 Admin login (via environment variable)
- 📂 View all registered cases
- 🔎 Filter/search by case ID or law
- 🗃 Export all cases to JSON/CSV

---

## 🛠 Tech Stack

| Component       | Technology                              |
|------------------|------------------------------------------|
| UI               | Streamlit                               |
| Backend Logic    | Python                                   |
| Semantic Search  | FAISS + Legal-BERT (from HuggingFace)   |
| Templating       | Jinja2                                   |
| File Uploads     | Streamlit FileUploader                   |
| Auth Management  | Session State + dotenv                   |
| Data Storage     | JSON files (for demo, upgradable)        |
| Model            | `nlpaueb/legal-bert-base-uncased`        |

---

## 🗂 Folder Structure

```
AI-lawyer/
├── backend/
│   ├── streamlit_app.py           # Main Streamlit app
│   ├── chat_engine.py             # Legal search engine
│   ├── courtroom_sim_gui.py       # Advocate Q&A simulation
├── data/
│   └── client/
│       └── cases.json             # Case registry (JSON DB)
├── embeddings/
│   └── faiss_index/               # FAISS + pickle files
├── templates/
│   └── rental_agreement_template.html
├── requirements.txt
├── .env
└── README.md
```

---

## 🚀 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/AI-lawyer.git
cd AI-lawyer
```

### 2. Setup Python Virtual Environment

```bash
python -m venv ai_lawyer_env
source ai_lawyer_env/bin/activate  # Windows: ai_lawyer_env\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Add Admin Credentials

```bash
echo "ADMIN_PASSWORD=admin123" > .env
```

### 5. Launch Streamlit App

```bash
cd backend
streamlit run streamlit_app.py
```

---

## 🔐 Authentication

- **Client Login**: Via Case ID + Password (created during registration)
- **Admin Login**: Password stored securely in `.env` file (`ADMIN_PASSWORD=admin123`)

---

## 🧠 Semantic Search (Legal NLP)

- Documents from IPC, NDA, and IT Act are embedded using Legal-BERT (`nlpaueb/legal-bert-base-uncased`)
- FAISS is used to perform fast approximate nearest neighbor searches
- Users can type natural language queries and get semantically relevant clauses or sections from the law

---

## 📄 Agreement Generation

- Powered by Jinja2 templating engine
- Agreements generated include:
  - Rental Agreement
  - Non-Disclosure Agreement (NDA)
- Users input party names, terms, and duration
- Agreements are rendered into HTML and downloaded as files

---

## ✅ Future Enhancements

- 📎 Upload & preview chargesheets and evidence
- 📄 Export agreements and summaries as PDF
- 🐳 Docker support for containerized deployment
- ☁️ Render or HuggingFace Spaces live hosting
- 📊 Admin dashboard analytics
- ✨ Add speech-to-text for legal dictation

---

## 📜 License

This project is licensed under the MIT License. See `LICENSE` for details.

---

## 🤝 Acknowledgments

- [Streamlit](https://streamlit.io/)
- [FAISS by Meta](https://github.com/facebookresearch/faiss)
- [HuggingFace Transformers](https://huggingface.co)
- [Legal-BERT](https://huggingface.co/nlpaueb/legal-bert-base-uncased)
