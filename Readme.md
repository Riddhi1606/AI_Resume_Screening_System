# 🧠 AI Resume Screening System

An AI-powered system that automatically screens resumes and ranks candidates based on how well they match a given job description — using semantic understanding (Sentence-BERT) instead of simple keyword matching.

**Build. Showcase. Get Hired.**

---

## 📌 Overview

Recruiters spend hours manually screening resumes for every job opening. This project automates that process: upload resumes (PDF/DOCX), paste a job description, and get a ranked shortlist of candidates in seconds — complete with match scores and matched/missing skills.

---

## ✨ Key Features

- 📄 Extract text from resumes in **PDF** and **DOCX** formats
- 🧬 Match resumes against a job description using **Sentence-BERT semantic similarity**
- 🎯 Identify **matched** and **missing** skills automatically
- 📊 Rank and shortlist top candidates in a clean, interactive dashboard
- ⬇️ Export ranked results as a downloadable CSV
- 🖥️ Simple, recruiter-friendly Streamlit UI

---

## 🛠️ Tech Stack

| Category         | Tools Used                                  |
|-------------------|----------------------------------------------|
| Language          | Python                                       |
| NLP / Embeddings  | Sentence-BERT (`all-MiniLM-L6-v2`)           |
| Text Extraction   | pdfplumber, python-docx                      |
| Similarity        | scikit-learn (cosine similarity)             |
| Web App           | Streamlit                                    |
| Data Handling     | pandas, numpy                                |

---

## ⚙️ How It Works

1. **Upload Resumes** — Drag & drop one or more resumes (PDF/DOCX)
2. **Extract Text** — Raw text is pulled from each resume
3. **Semantic Understanding** — Sentence-BERT converts resume and job description into embeddings
4. **Rank & Shortlist** — Cosine similarity scores rank candidates; matched/missing skills are surfaced

```
Upload Resumes → Extract Text → BERT Semantic Understanding → Rank & Shortlist
```

---

## 📂 Project Structure

```
ai-resume-screening/
├── app.py                     # Main Streamlit application
├── requirements.txt           # Python dependencies
└── utils/
    ├── __init__.py
    ├── resume_parser.py        # PDF/DOCX text extraction
    ├── matcher.py               # Sentence-BERT semantic matching
    └── skill_extractor.py       # Keyword-based skill matching
```

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/riddhi1606/ai-resume-screening.git
cd ai-resume-screening
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the app
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`.

---

## 🌐 Live Demo

🔗 [Add your Streamlit Cloud deployment link here]

---

## 📈 Future Improvements

- Named Entity Recognition (spaCy) for more robust skill/experience extraction
- Support for bulk resume screening (100+ resumes) with batching
- Candidate experience-level detection (fresher / mid / senior)
- Export shortlist directly to email or ATS integration

---

## 👩‍💻 Author

**Riddhi Sharma**
B.Tech, Artificial Intelligence & Data Science
Arya College of Engineering & IT, Jaipur
