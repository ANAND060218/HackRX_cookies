from fastapi import FastAPI, Header, HTTPException
from app.models import QueryRequest, QueryResponse
from app.processor import extract_text_from_url, chunk_text
from app.embedder import embed_chunks
from app.retriever import get_similar_contexts
from app.llm_reasoner import generate_batch_answer
from app.cache_manager import load_vector_store_if_exists, save_vector_store

import time

app = FastAPI()

@app.post("/api/v1/hackrx/run", response_model=QueryResponse)
async def run_query(req: QueryRequest, authorization: str = Header(...)):
    if not authorization.endswith("cda0"):
        raise HTTPException(status_code=401, detail="Unauthorized token")

    start = time.time()
    print(f"📄 Document URL: {req.documents}")
    print(f"❓ Questions: {req.questions}")

    # Use the URL directly to load/save cache
    db = load_vector_store_if_exists(req.documents)

    if db is not None:
        print("✅ Using cached vector store.")
    else:
        print("📥 Downloading and embedding new document.")
        raw_text = extract_text_from_url(req.documents)
        chunks = chunk_text(raw_text)
        db = embed_chunks(chunks)
        save_vector_store(db, req.documents)

    # Batch Question Processing
    batch_size = 5
    answers = []

    for i in range(0, len(req.questions), batch_size):
        question_batch = req.questions[i:i + batch_size]
        contexts = [get_similar_contexts(db, q) for q in question_batch]
        batch_answers = generate_batch_answer(contexts, question_batch)
        answers.extend(batch_answers)

    stop = time.time()
    print(f"🕒 Total Time: {stop - start:.2f} seconds")
    return QueryResponse(answers=answers)
