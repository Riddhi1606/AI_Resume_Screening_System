"""
Skill Extractor Module
Uses spaCy's PhraseMatcher against a curated skill taxonomy to extract
canonical skills from text. Handles synonyms/aliases (e.g. "ML" -> "machine learning")
so matching is far more robust than plain string search.
"""

import spacy
from spacy.matcher import PhraseMatcher

from utils.skill_taxonomy import SKILL_TAXONOMY, build_alias_lookup

_ALIAS_LOOKUP = build_alias_lookup()


def _load_nlp():
    """
    Use spaCy's blank English pipeline (tokenizer only). We only need
    tokenization for PhraseMatcher — no need for the full downloadable
    en_core_web_sm model, which avoids a fragile extra download step.
    """
    return spacy.blank("en")


_NLP = _load_nlp()


def _build_matcher(nlp) -> PhraseMatcher:
    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    for canonical, aliases in SKILL_TAXONOMY.items():
        patterns = [nlp.make_doc(alias) for alias in aliases]
        matcher.add(canonical, patterns)
    return matcher


_MATCHER = _build_matcher(_NLP)


def extract_skills(text: str) -> set:
    """
    Return the set of canonical skills found in the given text.
    Recognizes synonyms/aliases via the skill taxonomy (e.g. 'ML', 'sklearn').
    """
    doc = _NLP(text)
    matches = _MATCHER(doc)
    found = set()
    for match_id, start, end in matches:
        canonical = _NLP.vocab.strings[match_id]
        found.add(canonical)
    return found


def matched_skills(resume_text: str, jd_text: str) -> list:
    """Canonical skills that appear in BOTH resume and job description."""
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)
    return sorted(resume_skills & jd_skills)


def missing_skills(resume_text: str, jd_text: str) -> list:
    """Canonical skills required by the JD but not found in the resume."""
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)
    return sorted(jd_skills - resume_skills)
