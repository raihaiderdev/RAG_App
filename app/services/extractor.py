"""
extractor.py
PDF → raw text using PyMuPDF (fitz).
"""
import fitz  # PyMuPDF


def extract_text(file_path: str) -> str:
    """
    Open a PDF at *file_path* and return all page text concatenated.

    Args:
        file_path: Absolute or relative path to a .pdf file.

    Returns:
        A single string containing the extracted text from all pages.
    """
    text_parts = []

    with fitz.open(file_path) as doc:
        for page_num, page in enumerate(doc, start=1):
            page_text = page.get_text("text")
            if page_text.strip():
                text_parts.append(page_text)

    return "\n".join(text_parts)
