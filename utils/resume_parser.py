"""
Resume Parser Module
Extracts raw text from uploaded resume files (PDF or DOCX).
"""

import pdfplumber
import docx
import io


def _group_words_into_lines(words, line_tolerance: float = 3.0) -> str:
    """Group word boxes into lines based on vertical position, then order left-to-right."""
    if not words:
        return ""

    words_sorted = sorted(words, key=lambda w: (w["top"], w["x0"]))
    lines = []
    current_line = [words_sorted[0]]
    current_top = words_sorted[0]["top"]

    for w in words_sorted[1:]:
        if abs(w["top"] - current_top) <= line_tolerance:
            current_line.append(w)
        else:
            lines.append(current_line)
            current_line = [w]
            current_top = w["top"]
    lines.append(current_line)

    line_texts = []
    for line in lines:
        line_sorted = sorted(line, key=lambda w: w["x0"])
        line_texts.append(" ".join(w["text"] for w in line_sorted))
    return "\n".join(line_texts)


def _extract_page_text(page) -> str:
    """
    Extract text from a page, handling two-column resume layouts correctly.
    Splits words into left/right halves by x-position and reads each column
    top-to-bottom fully, instead of pdfplumber's default reading order which
    interleaves columns row-by-row and breaks up skill phrases.
    """
    words = page.extract_words()
    if not words:
        return ""

    mid_x = page.width / 2
    left_words = [w for w in words if w["x0"] < mid_x]
    right_words = [w for w in words if w["x0"] >= mid_x]

    # Only treat as two-column if both halves have a meaningful amount of text —
    # otherwise this is a normal single-column resume and should be read as one block.
    if len(left_words) >= 5 and len(right_words) >= 5:
        return _group_words_into_lines(left_words) + "\n" + _group_words_into_lines(right_words)
    else:
        return _group_words_into_lines(words)


def extract_text_from_pdf(file) -> str:
    """Extract text from a PDF file object (bytes or file-like), handling multi-column layouts."""
    text_parts = []
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = _extract_page_text(page)
            if page_text:
                text_parts.append(page_text)
    return "\n".join(text_parts).strip()


def extract_text_from_docx(file) -> str:
    """Extract text from a DOCX file object (bytes or file-like)."""
    document = docx.Document(file)
    text = "\n".join([para.text for para in document.paragraphs if para.text.strip()])
    return text.strip()


def extract_resume_text(uploaded_file) -> str:
    """
    Main entry point: detects file type from filename and extracts text.
    `uploaded_file` should be a Streamlit UploadedFile object (has .name and is file-like).
    """
    filename = uploaded_file.name.lower()

    if filename.endswith(".pdf"):
        return extract_text_from_pdf(uploaded_file)
    elif filename.endswith(".docx"):
        return extract_text_from_docx(uploaded_file)
    else:
        raise ValueError(f"Unsupported file type: {filename}. Please upload PDF or DOCX.")


def clean_text(text: str) -> str:
    """Basic cleanup: remove excessive whitespace and newlines."""
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return " ".join(lines)
