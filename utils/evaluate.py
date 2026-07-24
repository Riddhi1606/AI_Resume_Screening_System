"""
Evaluation Module
Measures how well the composite scoring (semantic + skill overlap) ranks
candidates correctly against a small hand-labeled test set of
(resume, job_description, expected_relevance) triples.

Run directly: python -m utils.evaluate
"""

from utils.matcher import load_model
from utils.skill_extractor import matched_skills, extract_skills
from sklearn.metrics.pairwise import cosine_similarity

# ---------------------------------------------------------------------------
# Labeled test set: each JD has a "high" match resume and a "low" match resume.
# A correct system should score the "high" resume above the "low" resume
# for every JD. This mirrors precision-style evaluation used in real ATS systems.
# ---------------------------------------------------------------------------
TEST_CASES = [
    {
        "jd": "Looking for an AI/ML Engineer skilled in Python, Machine Learning, "
              "Deep Learning, NLP, and TensorFlow to build production ML models.",
        "high_match_resume": (
            "Experienced in Python, Machine Learning, Deep Learning, and NLP. "
            "Built and deployed TensorFlow models for text classification. "
            "Worked on BERT-based semantic search systems."
        ),
        "low_match_resume": (
            "Skilled chef with 5 years of experience in Italian cuisine, "
            "menu planning, and restaurant management. Certified in food safety."
        ),
    },
    {
        "jd": "Hiring a Data Analyst proficient in SQL, Excel, Power BI, and "
              "data visualization to support business reporting.",
        "high_match_resume": (
            "Data analyst with strong SQL and Excel skills. Built dashboards "
            "in Power BI and Tableau for business reporting and data visualization."
        ),
        "low_match_resume": (
            "Civil engineer with expertise in structural design, AutoCAD, "
            "and construction project management."
        ),
    },
    {
        "jd": "Seeking a Full-Stack Developer with React, Node.js, and MongoDB "
              "experience to build scalable web applications.",
        "high_match_resume": (
            "Full-stack developer skilled in React, Node.js, and MongoDB. "
            "Built and deployed multiple scalable web applications using Git and Docker."
        ),
        "low_match_resume": (
            "Graphic designer experienced in Adobe Photoshop, Illustrator, "
            "and brand identity design for marketing campaigns."
        ),
    },
    {
        "jd": "AI Engineer role requiring experience with LLMs, RAG pipelines, "
              "LangChain, and vector databases like FAISS or ChromaDB.",
        "high_match_resume": (
            "Built a RAG-based chatbot using LangChain, FAISS, and OpenAI LLMs. "
            "Experienced with vector databases and semantic retrieval systems."
        ),
        "low_match_resume": (
            "Mechanical engineer specializing in CAD design, thermodynamics, "
            "and manufacturing process optimization."
        ),
    },
    {
        "jd": "Looking for a Cloud/DevOps engineer with AWS, Docker, Kubernetes, "
              "and CI/CD pipeline experience.",
        "high_match_resume": (
            "DevOps engineer with hands-on experience in AWS, Docker, and "
            "Kubernetes. Built CI/CD pipelines using GitHub Actions."
        ),
        "low_match_resume": (
            "Content writer with experience in SEO, blog writing, and "
            "social media marketing campaigns."
        ),
    },
]


def semantic_score(text_a: str, text_b: str, model) -> float:
    emb = model.encode([text_a, text_b])
    return float(cosine_similarity(emb[0].reshape(1, -1), emb[1].reshape(1, -1))[0][0]) * 100


def composite_score(resume_text: str, jd_text: str, model) -> float:
    sem = semantic_score(resume_text, jd_text, model)
    jd_skills = extract_skills(jd_text)
    matched = matched_skills(resume_text, jd_text)
    skill = (len(matched) / len(jd_skills) * 100) if jd_skills else 0
    return round(0.6 * sem + 0.4 * skill, 1)


def run_evaluation(verbose: bool = True) -> dict:
    """
    For each test case, checks whether the high-match resume scores higher
    than the low-match resume. Returns accuracy and per-case details.
    """
    model = load_model()
    correct = 0
    details = []

    for i, case in enumerate(TEST_CASES, 1):
        high_score = composite_score(case["high_match_resume"], case["jd"], model)
        low_score = composite_score(case["low_match_resume"], case["jd"], model)
        is_correct = high_score > low_score
        correct += int(is_correct)

        details.append({
            "case": i,
            "high_match_score": high_score,
            "low_match_score": low_score,
            "correctly_ranked": is_correct,
        })

        if verbose:
            status = "✅" if is_correct else "❌"
            print(f"{status} Case {i}: high={high_score}%  low={low_score}%")

    accuracy = round(correct / len(TEST_CASES) * 100, 1)
    if verbose:
        print(f"\nRanking Accuracy: {accuracy}% ({correct}/{len(TEST_CASES)} cases correctly ranked)")

    return {"accuracy": accuracy, "correct": correct, "total": len(TEST_CASES), "details": details}


if __name__ == "__main__":
    run_evaluation()
