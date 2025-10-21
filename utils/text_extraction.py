"""
Module for extracting text from different file formats.
Supports: TXT, PDF, DOCX
"""

import os
import logging
from typing import Optional

try:
    import PyPDF2
except ImportError:
    PyPDF2 = None

try:
    from docx import Document
except ImportError:
    Document = None

# Configurazione logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def extract_text(file_path: str) -> Optional[str]:
    """
    Extract text from a supported file.
    
    Args:
        file_path (str): Path to file to process
        
    Returns:
        Optional[str]: Extracted text or None if error
    """
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        return None
    
    file_extension = os.path.splitext(file_path)[1].lower()
    
    try:
        if file_extension == '.txt':
            return _extract_from_txt(file_path)
        elif file_extension == '.pdf':
            return _extract_from_pdf(file_path)
        elif file_extension == '.docx':
            return _extract_from_docx(file_path)
        else:
            logger.error(f"Unsupported file format: {file_extension}")
            return None
            
    except Exception as e:
        logger.error(f"Error extracting text from {file_path}: {str(e)}")
        return None


def _extract_from_txt(file_path: str) -> str:
    """Extract text from TXT file."""
    encodings = ['utf-8', 'latin-1', 'cp1252']
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                return file.read()
        except UnicodeDecodeError:
            continue
    
    # If all encodings fail, try with error handling
    with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
        return file.read()


def _extract_from_pdf(file_path: str) -> str:
    """Extract text from PDF file."""
    if PyPDF2 is None:
        raise ImportError("PyPDF2 not installed. Install with: pip install pypdf2")
    
    text = ""
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text() + "\n"
    
    return text.strip()


def _extract_from_docx(file_path: str) -> str:
    """Extract text from DOCX file."""
    if Document is None:
        raise ImportError("python-docx not installed. Install with: pip install python-docx")
    
    doc = Document(file_path)
    text = ""
    
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    
    return text.strip()


def get_supported_extensions() -> list:
    """Return supported file extensions."""
    return ['.txt', '.pdf', '.docx']
