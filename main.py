# app/main.py

#pre request for image to text converting via pytesseract
import os
import pytesseract

def find_tesseract_exe(): # only for windows os support 
    possible_paths = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
    ]
    for path in possible_paths:
        if os.path.isfile(path):
            return path
    return None

tesseract_path = find_tesseract_exe()
if tesseract_path:
    pytesseract.pytesseract.tesseract_cmd = tesseract_path
    print(f"[INFO] Using Tesseract executable at: {tesseract_path}")
else:
    print("[WARNING] Tesseract executable not found! OCR functions may fail.")
#-----------------------------#------------------------------------------------------------------#
from fastapi import FastAPI, Header, HTTPException
from app.models import QueryRequest, QueryResponse
from app.processor import extract_text_from_url, chunk_text
from app.embedder import embed_chunks
from app.retriever import get_similar_contexts
from app.llm_reasoner import generate_batch_answer, clean_context
from app.cache_manager import load_vector_store_if_exists, save_vector_store
import time
from app.special_handlers import handle_secret_token, handle_flight_number
from langchain.docstore.document import Document

app = FastAPI()

@app.post("/api/v1/hackrx/run", response_model=QueryResponse)
async def run_query(req: QueryRequest, authorization: str = Header(...)):
    if not authorization.endswith("cda0"): # Respect to change it to your secret key
        raise HTTPException(status_code=401, detail="Unauthorized token")

    #For Debugging
    start = time.time()
    print(f"📄 Document URL: {req.documents}")
    print(f"❓ Questions: {req.questions}")

    # Extract raw + ext
    raw, ext = extract_text_from_url(req.documents)
    answers = []

#-----------------------------#------------------------------------------------------------------#
     # Secret token special case
    if any("secret token" in q.lower() for q in req.questions):
        token_value = handle_secret_token(req.documents)
        print("🕒", round(time.time() - start, 2), "s")
        return QueryResponse(answers=[token_value])

    # Flight number special case
    elif any("flight" in q.lower() for q in req.questions):
        flight_number = handle_flight_number()
        print("🕒", round(time.time() - start, 2), "s")
        return QueryResponse(answers=[flight_number])
#-----------------------------#------------------------------------------------------------------#
    # Direct mode for small formats that don't need vectorstore 
    if ext in ["pptx", "xlsx", "png", "jpg", "jpeg"]:
        ctxs = [[Document(page_content=clean_context(raw))] for _ in req.questions]
        print(ctxs)
        answers = generate_batch_answer(ctxs, req.questions)
        print("🕒", round(time.time() - start, 2), "s")
        return QueryResponse(answers=answers)

    # Normal flow: use cache or embed new
    db = load_vector_store_if_exists(req.documents)
    if db is not None:
        print("✅ Using cached vector store.")
    else:
        print("📥 Downloading and embedding new document.")
        chunks = chunk_text(raw)
        if not chunks:
            return QueryResponse(answers=["The document does not contain readable text."] * len(req.questions))
        db = embed_chunks(chunks)
        save_vector_store(db, req.documents)

    # Batch processing for questions
    batch_size = 5 if len(req.questions)<20 else 9
    answers = []
    for i in range(0, len(req.questions), batch_size):
        question_batch = req.questions[i:i + batch_size]
        contexts = [get_similar_contexts(db, q) for q in question_batch]
        batch_answers = generate_batch_answer(contexts, question_batch)
        answers.extend(batch_answers)

    stop = time.time()
    print(f"🕒 Total Time: {stop - start:.2f} seconds")
    return QueryResponse(answers=answers)

#-----------------------------#------------------------------------------------------------------#