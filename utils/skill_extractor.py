"""
Skill Extractor Module
Matches known skills/keywords present in both resume and job description.
"""

import re

# A reasonably broad skill dictionary — extend this as needed for your domain.
SKILL_DB = [
    # Programming languages
    "python", "java", "c++", "c#", "javascript", "typescript", "sql", "r",
    # ML / AI
    "machine learning", "deep learning", "nlp", "natural language processing",
    "computer vision", "bert", "transformers", "scikit-learn", "tensorflow",
    "pytorch", "keras", "xgboost", "random forest", "neural networks",
    "sentence-bert", "llm", "generative ai", "data science",
    # Data
    "pandas", "numpy", "data analysis", "data visualization", "matplotlib",
    "seaborn", "power bi", "tableau", "excel",
    # Web / tools
    "streamlit", "flask", "django", "fastapi", "react", "node.js", "git",
    "github", "docker", "kubernetes", "aws", "azure", "gcp",
    # Databases
    "mysql", "postgresql", "mongodb", "faiss", "chromadb", "vector database",
    # Soft/process
    "agile", "communication", "teamwork", "leadership", "problem solving",
]


def extract_skills(text: str, skill_db=None) -> set:
    """Return the set of known skills found in the given text (case-insensitive)."""
    if skill_db is None:
        skill_db = SKILL_DB

    text_lower = text.lower()
    found = set()
    for skill in skill_db:
        # word-boundary aware match so 'r' doesn't match inside 'for' etc.
        pattern = r"(?<![a-zA-Z0-9])" + re.escape(skill.lower()) + r"(?![a-zA-Z0-9])"
        if re.search(pattern, text_lower):
            found.add(skill)
    return found


def matched_skills(resume_text: str, jd_text: str) -> list:
    """Skills that appear in BOTH resume and job description."""
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)
    return sorted(resume_skills & jd_skills)


def missing_skills(resume_text: str, jd_text: str) -> list:
    """Skills required by JD but not found in the resume."""
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)
    return sorted(jd_skills - resume_skills)