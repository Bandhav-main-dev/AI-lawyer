# courtroom_simulator.py (Phase 1 MVP)

import streamlit as st
from datetime import datetime
from chat_engine import search_similar_sections


def simulate_courtroom():
    st.title("⚖️ AI Courtroom Advocate Simulator")
    st.markdown("""
    Welcome to the AI Courtroom. Enter your questions as a judge, prosecutor, or opposition lawyer.
    The AI Advocate will respond using legal context (IPC, IT Act, NDA) and evidence (if provided).
    """)

    # Show Case Summary if available
    if "case_summary" in st.session_state:
        st.info(f"📄 **Case Summary**:\n{st.session_state['case_summary']}")

    # Initialize chat log
    if "court_log" not in st.session_state:
        st.session_state.court_log = []

    # Display chat history
    for msg in st.session_state.court_log:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input from judge or opponent
    prompt = st.chat_input("Ask a courtroom question (e.g., 'What is your defense for this evidence?')")

    if prompt:
        st.session_state.court_log.append({"role": "user", "content": prompt})

        # Search legal context using FAISS + Legal-BERT
        relevant_sections = search_similar_sections(prompt, top_k=2)
        law_summary = "\n".join([
            f"- **{r.get('title', 'Untitled')}**: {r.get('content', '[No content]')[:200]}..."
            for r in relevant_sections
        ])

        # Contextual evidence (optional)
        case_evidence = st.session_state.get("case_summary", "")

        # Simulated response
        title = relevant_sections[0].get('title', 'a legal section')
        content = relevant_sections[0].get('content', '[No content provided]')
        response = f"Your Honour, based on the provided facts and {title}, I submit the following:\n\n"
        response += f"**Legal Reference:** {content[:350]}...\n\n"

        if case_evidence:
            response += f"Additionally, the chargesheet indicates:\n> {case_evidence[:300]}..."

        st.session_state.court_log.append({"role": "ai", "content": response})
        with st.chat_message("ai"):
            st.markdown(response)


# To be used inside main streamlit_app.py sidebar routing:
# if selection == "Courtroom Simulator":
#     simulate_courtroom()

if __name__ == "__main__":
    simulate_courtroom()