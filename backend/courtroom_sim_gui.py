import streamlit as st
import os
import tempfile

from evidence_analyzer import auto_analyze
from smart_cross_examinator import (
    detect_contradictions,
    generate_cross_questions,
    print_cross_examination,
    cross_examine_evidence
)

st.set_page_config(page_title="AI Lawyer: Courtroom Simulator", layout="wide")
st.title("⚖️ AI Lawyer - Courtroom Simulation Interface")
st.markdown("Upload your **case evidence files** below (images, audio, or text) for analysis, contradiction detection, and AI cross-examination.")

# Store evidence summaries
evidence_summary = {}
uploaded_files = st.file_uploader("📎 Upload Evidence Files", type=["txt", "jpg", "jpeg", "png", "wav"], accept_multiple_files=True)

if uploaded_files:
    st.success(f"✅ {len(uploaded_files)} files uploaded. Starting analysis...")

    with st.spinner("🔍 Analyzing evidence..."):
        for file in uploaded_files:
            # Save to temporary directory
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.name)[1]) as temp_file:
                temp_file.write(file.read())
                temp_path = temp_file.name

            try:
                summary = auto_analyze(temp_path)
                evidence_summary[file.name] = summary
                st.markdown(f"#### 📁 {file.name}")
                st.text_area("📄 Summary", value=summary[:1000], height=200)
            except Exception as e:
                st.error(f"⚠️ Error analyzing {file.name}: {e}")

    if evidence_summary:
        st.divider()
        st.header("🎯 AI Cross-Examination Questions")
        questions = generate_cross_questions(evidence_summary)
        if questions:
            for q in questions:
                st.markdown(f"**❓ Q (From {q['from']} → To {q['to']}):**")
                st.markdown(f"- {q['question']} (Similarity: `{q['similarity']}`)")
        else:
            st.info("No major contradiction-based questions generated.")

        st.divider()
        st.header("📚 Full Legal Summary")
        st.text_area("📝 Summary", value=cross_examine_evidence(evidence_summary), height=400)
