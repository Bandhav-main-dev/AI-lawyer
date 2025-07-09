import streamlit as st
import json
import os
from jinja2 import Environment, FileSystemLoader
from datetime import date
from courtroom_sim_gui import get_courtroom_response
from chat_engine import search_legal_docs, search_similar_sections
from dotenv import load_dotenv
from question_generator import generate_defense_questions, generate_questions_from_evidence
from ask_question import render_qa_form
from utils import load_all_chat_for_case, load_defense_notes
from evidence_analyzer import process_uploaded_evidence
load_dotenv()

env = Environment(loader=FileSystemLoader("/workspaces/AI-lawyer/templetes"))


# ---------------------- CONSTANTS ----------------------
AGREEMENT_FILE_PATH = "/workspaces/AI-lawyer/templates/rental_agreement_template.html"
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
CASE_DATA_FILE = "/workspaces/AI-lawyer/data/client/cases.json"

# ---------------------- HELPERS ----------------------
def format_as_lawyer_question(raw_question):
    raw = raw_question.strip(" ?").capitalize()
    if "your name" in raw.lower():
        return "Please state your full name for the court record."
    elif "where" in raw.lower() and "incident" in raw.lower():
        return "Mr./Ms., could you clearly describe your whereabouts on the night of the incident?"
    elif raw.lower().startswith("why"):
        return "Can you explain to the court the reason behind your actions?"
    elif raw.lower().startswith("what"):
        return f"Could you please clarify: {raw}?"
    elif raw.lower().startswith("how"):
        return f"Could you explain in detail: {raw}?"
    else:
        return f"For the record, please answer: {raw}?"

# --- Save Answer ---
def save_question_answers(case_id, evidence_file, new_entry):
    os.makedirs("case_data", exist_ok=True)
    file_path = f"case_data/{case_id}_{evidence_file}_onebyone.json"
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            data = json.load(f)
    else:
        data = []
    existing_questions = {entry['question'] for entry in data}
    if new_entry['question'] not in existing_questions:
        data.append(new_entry)
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)


def load_cases():
    if not os.path.exists(CASE_DATA_FILE):
        with open(CASE_DATA_FILE, "w") as f:
            json.dump([], f)
        return []
    with open(CASE_DATA_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_case(case_data):
    cases = load_cases()
    cases.append(case_data)
    with open(CASE_DATA_FILE, "w") as f:
        json.dump(cases, f, indent=4)

def generate_case_number():
    cases = load_cases()
    return f"CASE{len(cases) + 1:03d}"

def authenticate_case(case_id, password):
    cases = load_cases()
    for case in cases:
        if case.get("case_id") == case_id and case.get("password") == password:
            return case
    return None

# ---------------------- APP SETUP ----------------------
st.set_page_config("AI Lawyer Assist", layout="centered")
st.title("⚖️ AI Lawyer Assist")

# ---------------------- SESSION INIT ----------------------
if "logged_in_case" not in st.session_state:
    st.session_state.logged_in_case = None
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False
if "chat_log" not in st.session_state:
    st.session_state.chat_log = []
if "courtroom_log" not in st.session_state:
    st.session_state.courtroom_log = []

# ---------------------- SIDEBAR NAV ----------------------
if st.session_state.logged_in_case:
    sidebar_choice = st.sidebar.radio("📁 Case Menu", ["📄 Case Summary", "💬 Chat with Lawyer", "📂 Evidence Submit", "⚖️ Courtroom Simulation", "🔎 Semantic Legal Search", "📝 Generate Agreement", "🚪 Logout"])
elif st.session_state.admin_logged_in:
    sidebar_choice = st.sidebar.radio("🛡️ Admin Menu", ["🗂️ View All Cases", "📤 Export JSON/CSV", "🚪 Logout"])
else:
    sidebar_choice = st.sidebar.radio("Menu", ["🔐 Login to Case", "📁 Register New Case", "🛡️ Admin Dashboard"])

# ---------------------- CASE LOGIN ----------------------
if sidebar_choice == "🔐 Login to Case":
    st.subheader("🔐 Login to Existing Case")
    cid = st.text_input("Case ID (e.g. CASE001)")
    pwd = st.text_input("Password", type="password")
    if st.button("Login"):
        case = authenticate_case(cid, pwd)
        if case:
            st.session_state.logged_in_case = case
            st.success("Logged in successfully.")
            st.rerun()
        else:
            st.error("Invalid Case ID or Password")

# ---------------------- CASE REGISTRATION ----------------------
elif sidebar_choice == "📁 Register New Case":
    st.subheader("📁 Register New Case")
    name = st.text_input("Client Name")
    age = st.number_input("Age", 1, 120)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    law = st.selectbox("Applicable Law", ["IPC", "IT Act", "NDA", "Other"])
    issue = st.text_area("Case Summary")
    client_statement = st.text_area("Client Statement")
    password = st.text_input("Set Password", type="password")
    if st.button("Register"):
        if name and issue and password:
            cid = generate_case_number()
            save_case({"case_id": cid, "client_name": name, "age": age, "gender": gender, "act_type": law, "issue_summary": issue, "client_statement":client_statement, "password": password})
            st.success(f"✅ Case Registered with ID: {cid}")
        else:
            st.error("Please fill all required fields.")

# ---------------------- ADMIN LOGIN ----------------------
elif sidebar_choice == "🛡️ Admin Dashboard":
    st.subheader("🛡️ Admin Login")
    pwd = st.text_input("Admin Password", type="password")
    if st.button("Login as Admin"):
        if pwd == ADMIN_PASSWORD:
            st.session_state.admin_logged_in = True
            st.success("Admin logged in.")
            st.rerun()
        else:
            st.error("Incorrect password.")

# ---------------------- ADMIN VIEW ----------------------
elif sidebar_choice == "🗂️ View All Cases" and st.session_state.admin_logged_in:
    st.subheader("📁 All Registered Cases")
    cases = load_cases()
    search = st.text_input("🔍 Search by Client or Law")
    results = [c for c in cases if search.lower() in c['client_name'].lower() or search.lower() in c['act_type'].lower()] if search else cases
    for case in results:
        st.text(f"{case['case_id']} | {case['client_name']} | {case['act_type']}")
        st.caption(f"Summary: {case['issue_summary']}")
        st.divider()

# ---------------------- EXPORT DATA ----------------------
elif sidebar_choice == "📤 Export JSON/CSV" and st.session_state.admin_logged_in:
    import pandas as pd
    st.subheader("📤 Export Cases")
    data = load_cases()
    st.download_button("Download JSON", data=json.dumps(data, indent=2), file_name="cases.json")
    df = pd.DataFrame(data)
    st.download_button("Download CSV", data=df.to_csv(index=False), file_name="cases.csv")

# ---------------------- CASE SUMMARY ----------------------
elif sidebar_choice == "📄 Case Summary" and st.session_state.logged_in_case:
    c = st.session_state.logged_in_case
    st.subheader("📄 Case Summary")
    st.text(f"Client: {c['client_name']} | Age: {c['age']} | Gender: {c['gender']}")
    st.text(f"Law: {c['act_type']} | Summary: {c['issue_summary']}")

# ---------------------- CHAT WITH LAWYER ----------------------
elif sidebar_choice == "💬 Chat with Lawyer" and st.session_state.logged_in_case:
    case_id = st.session_state.logged_in_case["case_id"]
    st.subheader("💬 Chat with AI Lawyer")

    if "chat_log" not in st.session_state:
        st.session_state.chat_log = []

    if "client_statement" not in st.session_state:
        st.session_state.client_statement = st.session_state.logged_in_case.get("issue_summary", "")

    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("Enter your message:")
        use_in_defense = st.checkbox("💼 Use this message to strengthen client statement")
        send = st.form_submit_button("Send")

    if send and user_input:
        # Add to chat log
        st.session_state.chat_log.append({"role": "user", "content": user_input})

        # AI Placeholder
        ai_response = f"📌 Info recorded: '{user_input}'"
        st.session_state.chat_log.append({"role": "ai", "content": ai_response})

        if use_in_defense:
            from datetime import datetime
            import os, json

            # Save to client chat folder
            chat_dir = f"data/client/{case_id}/chat"
            os.makedirs(chat_dir, exist_ok=True)
            timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
            chat_data = {
                "timestamp": timestamp,
                "from": "client",
                "content": user_input
            }
            with open(os.path.join(chat_dir, f"{timestamp}_chatlog.json"), "w") as f:
                json.dump(chat_data, f, indent=2)

            # Update client statement dynamically
            st.session_state.client_statement += f"\nAdditional Input: {user_input}"
            st.success("✅ Input saved and added to client defense.")

    # Display full chat
    for msg in st.session_state.chat_log:
        speaker = "👤 You" if msg["role"] == "user" else "🧑‍⚖️ AI"
        st.markdown(f"**{speaker}**: {msg['content']}")


    # Display chat log
    for msg in st.session_state.chat_log:
        speaker = "👤 You" if msg["role"] == "user" else "🧑‍⚖️ AI"
        st.markdown(f"**{speaker}**: {msg['content']}")

# ---------------------- EVIDENCE UPLOAD ----------------------

elif sidebar_choice == "📂 Evidence Submit" and st.session_state.logged_in_case:
    case = st.session_state.logged_in_case
    case_id = case["case_id"]
    EVIDENCE_DIR = f"/workspaces/AI-lawyer/data/client/{case_id}/evidence"
    os.makedirs(EVIDENCE_DIR, exist_ok=True)

    st.title("📂 Submit Case Evidence")
    uploaded_file = st.file_uploader(
        "Upload evidence (image, audio, video, or text)",
        type=["png", "jpg", "jpeg", "wav", "mp3", "m4a", "mp4", "avi", "mkv", "txt"]
    )

    if uploaded_file:
        result = process_uploaded_evidence(
            case_id=case_id,
            file_bytes=uploaded_file.read(),
            file_name=uploaded_file.name,
            evidence_dir=EVIDENCE_DIR,
            generate_defense_questions_func=generate_defense_questions
        )

        st.success(f"✅ File processed and saved: `{result['filename']}`")
        st.text_area("📜 Extracted Evidence Text", result["extracted_text"], height=300)
        st.info(f"🧠 {len(result['questions'])} questions saved to: `{os.path.basename(result['questions_path'])}`")



# ---------------------- COURTROOM SIMULATION ----------------------
elif sidebar_choice == "⚖️ Courtroom Simulation" and st.session_state.logged_in_case:
    case = st.session_state.logged_in_case
    case_id = case["case_id"]
    EVIDENCE_DIR = f"/workspaces/AI-lawyer/data/client/{case_id}/evidence"
    os.makedirs(EVIDENCE_DIR, exist_ok=True)

    st.title("⚖️ Courtroom Simulation")
    st.subheader("📁 Choose Witness Statement")

    option = st.radio("Select input method:", ["📄 Upload New", "📂 Choose from Saved"])
    evidence_text, filename = "", ""

    # ----------------------------------------
    # 📄 Upload New Witness Statement
    if option == "📄 Upload New":
        uploaded_file = st.file_uploader("Upload a .txt file", type=["txt"])
        if uploaded_file:
            filename = f"{case_id}_{uploaded_file.name}"
            file_path = os.path.join(EVIDENCE_DIR, filename)
            evidence_text = uploaded_file.read().decode("utf-8")
            with open(file_path, "w") as f:
                f.write(evidence_text)
            st.success(f"✅ Statement saved as: {filename}")

    # ----------------------------------------
    # 📂 Choose from Saved Witness Statements
    elif option == "📂 Choose from Saved":
        saved_files = [
            f for f in os.listdir(EVIDENCE_DIR)
            if f.startswith(case_id) and f.endswith(".txt")
        ]

        if saved_files:
            selected_file = st.selectbox("Choose a saved statement:", saved_files, key="courtroom_saved_statement")
            filename = selected_file
            file_path = os.path.join(EVIDENCE_DIR, filename)
            with open(file_path, "r") as f:
                evidence_text = f.read()
            st.success(f"📄 Loaded: {filename}")
        else:
            st.warning("⚠️ No saved statements found.")

    # ----------------------------------------
    # 🧠 Session State Initialization
    for key in ["qa_history", "current_question", "awaiting_answer", "simulation_ready", "evidence_text", "context"]:
        if key not in st.session_state:
            st.session_state[key] = [] if key == "qa_history" else ""

    # ----------------------------------------
    # 🤖 Generate Initial Question if Needed
    if evidence_text and not st.session_state.simulation_ready:
        st.session_state.evidence_text = evidence_text

        client_statement = case.get("issue_summary", "")
        chat = load_all_chat_for_case(case_id)
        notes = load_defense_notes(case_id)
        context = client_statement + "\n\n" + chat + "\n\n" + notes
        st.session_state.context = context
        st.session_state.simulation_ready = True

        # 🔁 Generate questions
        initial_qs = generate_defense_questions(context, evidence_text)
        asked = [qa["question"] for qa in st.session_state.qa_history]
        next_qs = [q for q in initial_qs if q not in asked]

        if next_qs:
            st.session_state.current_question = next_qs[0]
            st.session_state.awaiting_answer = True
        else:
            st.warning("No initial questions generated.")

    # ----------------------------------------
    # 🎯 Witness Question & Answer Flow
    if st.session_state.simulation_ready and st.session_state.awaiting_answer:
        st.subheader("🎯 Witness Cross-Examination")
        formatted_q = format_as_lawyer_question(st.session_state.current_question)
        st.markdown(f"**🧑‍⚖️ Advocate:** {formatted_q}")

        with st.form("answer_form", clear_on_submit=True):
            answer = st.text_input("🗣️ Your answer:")
            submit = st.form_submit_button("Submit Answer")

        if submit and answer.strip():
            entry = {
                "question": st.session_state.current_question,
                "answer": answer.strip()
            }
            st.session_state.qa_history.append(entry)
            save_question_answers(case_id, filename, entry)

            # Update context with history
            full_context = st.session_state.context
            for qa in st.session_state.qa_history:
                full_context += f"\nQ: {qa['question']}\nA: {qa['answer']}"

            # 🔁 Get next question
            next_qs = generate_defense_questions(full_context, st.session_state.evidence_text)
            asked = [qa["question"] for qa in st.session_state.qa_history]
            remaining_qs = [q for q in next_qs if q not in asked]

            if remaining_qs:
                st.session_state.current_question = remaining_qs[0]
                st.session_state.awaiting_answer = True
            else:
                st.success("✅ Cross-examination complete.")
                st.session_state.awaiting_answer = False
                st.session_state.current_question = ""

    # ----------------------------------------
    # 🔁 Reset Button
    if st.button("🔁 Reset Simulation"):
        for key in ["qa_history", "current_question", "awaiting_answer", "simulation_ready", "evidence_text", "context"]:
            st.session_state.pop(key, None)
        st.success("🔄 Courtroom simulation has been reset.")




# ---------------------- AGREEMENT GENERATOR ----------------------
elif sidebar_choice == "📝 Generate Agreement" and st.session_state.logged_in_case:
    st.subheader("📝 Agreement Generator")
    p1 = st.text_input("Party 1")
    p2 = st.text_input("Party 2")
    terms = st.text_area("Terms")
    duration = st.text_input("Duration")

    generate_btn = st.button("Generate", key="agreement_generate_btn")

    if generate_btn:
        if p1 and p2 and terms:
            env = Environment(loader=FileSystemLoader("/workspaces/AI-lawyer/templetes"))  # adjust path if needed
            template = env.get_template("rental_agreement_template.html")
            html = template.render(
                party1=p1,
                party2=p2,
                terms=terms,
                duration=duration,
                date=str(date.today())
            )
            st.download_button("📩 Download Agreement", data=html, file_name="agreement.html")
        else:
            st.error("Please complete all fields.")

# ---------------------- LOGOUT ----------------------
elif sidebar_choice == "🚪 Logout":
    st.session_state.logged_in_case = None
    st.session_state.admin_logged_in = False
    st.session_state.chat_log = []
    st.session_state.courtroom_log = []
    st.rerun()
