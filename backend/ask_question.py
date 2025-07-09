import json
import os
import streamlit as st
from question_generator import generate_defense_questions


def render_qa_form(questions, case_id=None, statement_text=None, evidence_file=None):
    st.markdown("### 🎯 Cross-Examination Q&A")
    answers = {}

    with st.form("qa_form"):
        for i, question in enumerate(questions):
            answers[question] = st.text_input(f"Q{i+1}: {question}", key=f"q{i}")
        submitted = st.form_submit_button("📩 Submit Answers")

    if submitted:
        refusal_list = [
            "i don't want to answer",
            "i prefer not to say",
            "no comment",
            "i won't answer",
            "not answering"
        ]
        refused_any = False

        for q, a in answers.items():
            if a.strip().lower() in refusal_list:
                st.warning(f"⚖️ Judge: The witness must respond. Question is compulsory:\n**→ {q}**")
                refused_any = True

        if refused_any:
            st.info("📌 Please revise your answers and resubmit.")
            return None  # Don’t continue if refusal

        st.success("✅ Answers recorded.")

        # Save answers to JSON
        if case_id and evidence_file:
            save_path = f"/workspaces/AI-lawyer/data/client/CASE001/evidence/{case_id}_{evidence_file}_evidence_qa.json"
            os.makedirs("case_data", exist_ok=True)
            with open(save_path, "w") as f:
                json.dump(answers, f, indent=2)

        # Re-run generation with answers + statement
        combined_text = statement_text + "\n\nWitness Answers:\n" + "\n".join([f"{q} {a}" for q, a in answers.items()])
        client_statement = st.session_state.logged_in_case.get("issue_summary", "")
        new_questions = generate_defense_questions(client_statement, combined_text)

        st.markdown("### 🔁 Follow-up Questions Generated")
        for i, q in enumerate(new_questions):
            st.write(f"**Q{i+1}:** {q}")

        return answers

