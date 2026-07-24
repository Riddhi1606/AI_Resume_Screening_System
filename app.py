"""
AI Resume Screening System
Main Streamlit app: upload resumes, paste a job description, get ranked candidates
with an explainable composite score (semantic similarity + skill overlap).
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from utils.resume_parser import extract_resume_text, clean_text
from utils.matcher import load_model, rank_resumes
from utils.skill_extractor import matched_skills, missing_skills, extract_skills

st.set_page_config(page_title="AI Resume Screening System", page_icon="🧠", layout="wide")

st.title("🧠 AI Resume Screening System")
st.caption(
    "Upload resumes, paste a job description, and get ranked candidates — "
    "scored using Sentence-BERT semantic similarity combined with explicit skill matching."
)

tab_screen, tab_eval = st.tabs(["📋 Screen Resumes", "📊 Model Evaluation"])

# ---------------------------------------------------------------------------
# TAB 1: Resume Screening
# ---------------------------------------------------------------------------
with tab_screen:
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

                semantic_ranked = rank_resumes(resume_texts, jd_text)
                semantic_scores = {e["filename"]: e["score"] for e in semantic_ranked}

                jd_skills = extract_skills(jd_text)

                # Composite score: 60% semantic similarity + 40% skill overlap.
                # This mirrors how real ATS tools score candidates and is more
                # explainable than a raw embedding-similarity number.
                results = []
                for fname in resume_texts:
                    sem_score = semantic_scores[fname]
                    matched = matched_skills(resume_texts[fname], jd_text)
                    missing = missing_skills(resume_texts[fname], jd_text)
                    skill_score = (len(matched) / len(jd_skills) * 100) if jd_skills else 0
                    composite = round(0.6 * sem_score + 0.4 * skill_score, 1)

                    results.append({
                        "filename": fname,
                        "composite_score": composite,
                        "semantic_score": round(sem_score, 1),
                        "skill_score": round(skill_score, 1),
                        "matched": matched,
                        "missing": missing,
                    })

                results.sort(key=lambda x: x["composite_score"], reverse=True)

            st.subheader("🏆 Ranked Candidates")

            # Summary table
            table_df = pd.DataFrame([{
                "Candidate": r["filename"],
                "Match Score (%)": r["composite_score"],
                "Skills Matched": ", ".join(r["matched"]) if r["matched"] else "—",
                "Skills Missing": ", ".join(r["missing"]) if r["missing"] else "—",
            } for r in results])

            st.dataframe(
                table_df,
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
                data=table_df.to_csv(index=False).encode("utf-8"),
                file_name="resume_screening_results.csv",
                mime="text/csv"
            )

            st.divider()
            st.subheader("🔎 Score Breakdown per Candidate")
            st.caption("Explains *why* each candidate got their score — semantic fit vs. explicit skill overlap.")

            for r in results:
                with st.expander(f"**{r['filename']}** — {r['composite_score']}% overall match"):
                    c1, c2 = st.columns([1, 1])

                    with c1:
                        fig = go.Figure(go.Bar(
                            x=[r["semantic_score"], r["skill_score"]],
                            y=["Semantic Similarity", "Skill Overlap"],
                            orientation="h",
                            marker_color=["#6C63FF", "#00C2A8"],
                            text=[f"{r['semantic_score']}%", f"{r['skill_score']}%"],
                            textposition="auto",
                        ))
                        fig.update_layout(
                            xaxis_range=[0, 100],
                            height=200,
                            margin=dict(l=10, r=10, t=10, b=10),
                        )
                        st.plotly_chart(fig, use_container_width=True)

                    with c2:
                        st.markdown("**✅ Matched Skills**")
                        st.write(", ".join(r["matched"]) if r["matched"] else "None found")
                        st.markdown("**❌ Missing Skills**")
                        st.write(", ".join(r["missing"]) if r["missing"] else "None — full coverage!")

# ---------------------------------------------------------------------------
# TAB 2: Model Evaluation
# ---------------------------------------------------------------------------
with tab_eval:
    st.subheader("📊 Ranking Accuracy Evaluation")
    st.caption(
        "Tests whether the scoring system correctly ranks a strong-match resume "
        "above a clearly irrelevant resume, across 5 different job roles."
    )

    if st.button("▶️ Run Evaluation"):
        from utils.evaluate import run_evaluation

        with st.spinner("Running evaluation on labeled test set..."):
            result = run_evaluation(verbose=False)

        st.metric("Ranking Accuracy", f"{result['accuracy']}%",
                   help=f"{result['correct']} / {result['total']} test cases correctly ranked")

        eval_df = pd.DataFrame(result["details"])
        eval_df.columns = ["Case #", "High-Match Score", "Low-Match Score", "Correctly Ranked"]
        st.dataframe(eval_df, use_container_width=True, hide_index=True)

        st.info(
            "Each test case pairs a job description with one strongly relevant resume "
            "and one clearly irrelevant resume. A correct system should always score "
            "the relevant resume higher."
        )
