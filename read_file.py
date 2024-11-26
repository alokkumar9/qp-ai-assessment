import fitz  # PyMuPDF for PDFs
from docx import Document  # python-docx for Word documents
import fitz
import PyPDF2
import docx
from io import BytesIO


def read_docx(file_bytes):
    """Read text from a Word document using python-docx."""
    content=""
    print(file_bytes)
    # Use BytesIO to create a file-like object from bytes
    doc = docx.Document(BytesIO(file_bytes))
    for para in doc.paragraphs:
        content += para.text + "\n"
    return content

