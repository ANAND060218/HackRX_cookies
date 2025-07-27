import fitz
import requests
from tempfile import NamedTemporaryFile

def extract_text_from_url(pdf_url: str) -> str:
    response = requests.get(pdf_url)
    with NamedTemporaryFile(delete=False, suffix=".pdf") as f:
        f.write(response.content)
        doc = fitz.open(f.name)
        return "\n".join([page.get_text() for page in doc])

def chunk_text(text: str, chunk_size: int = 500) -> list:
    words = text.split()
    return [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]
