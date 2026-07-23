"""
AI Resume Screening System
Main Streamlit app: upload resumes, paste a job description, get ranked candidates.
"""

import streamlit as st
import pandas as pd

from utils.resume_parser import extract_resume_text, clean_text
from utils.matcher import load_model, rank_resumes
from utils.skill_extractor import matched_skills, missing_skills

st.set_page_config(page_title="AI Resume Screening System", page_icon="🧠", layout="wide")

st.title("🧠 AI Resume Screening System")
st.caption("Upload resumes, paste a job description, and get ranked candidates instantly.")

# Warm up the model once at app start
with st.spinner("Loading semantic matching model..."):
    load_model()

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📄 Upload Resumes")
    uploaded_files = st.file_uploader(
        "Drag & drop files here (PDF/DOCX)",
        type=["pdf", "docx"],
        accept_multiple_files=True
    )

with col2:
    st.subheader("📋 Job Description")
    jd_text = st.text_area("Paste the job description here...", height=200)

st.divider()

analyze = st.button("🔍 Analyze", type="primary", use_container_width=True)

if analyze:
    if not uploaded_files:
        st.warning("Please upload at least one resume.")
    elif not jd_text.strip():
        st.warning("Please paste a job description.")
    else:
        with st.spinner("Extracting text and computing matches..."):
            resume_texts = {}
            for file in uploaded_files:
                raw_text = extract_resume_text(file)
                resume_texts[file.name] = clean_text(raw_text)

            ranked = rank_resumes(resume_texts, jd_text)

            # Build results table with skill matches
            rows = []
            for entry in ranked:
                fname = entry["filename"]
                score = entry["score"]
                matched = matched_skills(resume_texts[fname], jd_text)
                missing = missing_skills(resume_texts[fname], jd_text)
                rows.append({
                    "Candidate": fname,
                    "Match Score (%)": score,
                    "Skills Matched": ", ".join(matched) if matched else "—",
                    "Skills Missing": ", ".join(missing) if missing else "—",
                })

            df = pd.DataFrame(rows)

        st.subheader("🏆 Ranked Candidates")
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Match Score (%)": st.column_config.ProgressColumn(
                    "Match Score (%)", min_value=0, max_value=100, format="%.1f%%"
                )
            }
        )

        st.download_button(
            "⬇️ Download Results as CSV",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="resume_screening_results.csv",
            mime="text/csv"
        )
