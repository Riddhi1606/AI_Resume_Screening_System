"""
Skill Taxonomy
A structured, categorized set of technical skills with common synonyms/aliases.
Each canonical skill maps to a list of surface forms that should be recognized.
"""

SKILL_TAXONOMY = {
    # Programming Languages
    "python": ["python", "python3"],
    "java": ["java"],
    "c++": ["c++", "cpp"],
    "c#": ["c#", "csharp"],
    "javascript": ["javascript", "js"],
    "typescript": ["typescript", "ts"],
    "sql": ["sql", "mysql", "structured query language"],
    "r": ["r programming", "r language"],

    # Machine Learning / AI
    "machine learning": ["machine learning", "ml"],
    "deep learning": ["deep learning", "dl"],
    "nlp": ["nlp", "natural language processing"],
    "computer vision": ["computer vision", "cv"],
    "bert": ["bert", "sentence-bert", "sbert"],
    "transformers": ["transformers", "transformer models", "attention models"],
    "generative ai": ["generative ai", "genai", "gen ai"],
    "llm": ["llm", "large language model", "large language models"],
    "reinforcement learning": ["reinforcement learning", "rl"],
    "neural networks": ["neural network", "neural networks", "ann"],
    "data science": ["data science"],

    # ML/DL Frameworks & Libraries
    "scikit-learn": ["scikit-learn", "sklearn", "scikit learn"],
    "tensorflow": ["tensorflow"],
    "pytorch": ["pytorch", "torch"],
    "keras": ["keras"],
    "xgboost": ["xgboost", "xg boost"],
    "random forest": ["random forest"],

    # Data Tools
    "pandas": ["pandas"],
    "numpy": ["numpy"],
    "data analysis": ["data analysis", "data analytics"],
    "data visualization": ["data visualization", "data viz"],
    "matplotlib": ["matplotlib"],
    "seaborn": ["seaborn"],
    "power bi": ["power bi", "powerbi"],
    "tableau": ["tableau"],
    "excel": ["excel", "ms excel", "microsoft excel"],

    # Web / App Frameworks
    "streamlit": ["streamlit"],
    "flask": ["flask"],
    "django": ["django"],
    "fastapi": ["fastapi", "fast api"],
    "react": ["react", "react.js", "reactjs"],
    "node.js": ["node.js", "nodejs", "node"],

    # DevOps / Cloud
    "git": ["git"],
    "github": ["github"],
    "docker": ["docker"],
    "kubernetes": ["kubernetes", "k8s"],
    "aws": ["aws", "amazon web services"],
    "azure": ["azure", "microsoft azure"],
    "gcp": ["gcp", "google cloud", "google cloud platform"],

    # Databases / Retrieval
    "mongodb": ["mongodb", "mongo"],
    "postgresql": ["postgresql", "postgres"],
    "faiss": ["faiss"],
    "chromadb": ["chromadb", "chroma"],
    "vector database": ["vector database", "vector db", "vector store"],
    "rag": ["rag", "retrieval augmented generation"],
    "langchain": ["langchain"],

    # Soft / process skills
    "problem solving": ["problem solving", "problem-solving"],
    "communication": ["communication", "communication skills"],
    "teamwork": ["teamwork", "collaboration"],
    "leadership": ["leadership"],
    "agile": ["agile", "scrum"],
}


def build_alias_lookup() -> dict:
    """Returns {alias_lowercase: canonical_skill_name} for fast reverse lookup."""
    lookup = {}
    for canonical, aliases in SKILL_TAXONOMY.items():
        for alias in aliases:
            lookup[alias.lower()] = canonical
    return lookup
