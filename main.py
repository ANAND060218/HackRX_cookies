from fastapi import FastAPI, Header, HTTPException
from app.models import QueryRequest, QueryResponse
from app.processor import extract_text_from_url, chunk_text
from app.embedder import embed_chunks
from app.retriever import get_similar_contexts
from app.llm_reasoner import generate_answer
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

@app.post("/api/v1/hackrx/run", response_model=QueryResponse)
async def run_query(req: QueryRequest, authorization: str = Header(...)):
    if not authorization.endswith("cda0"):
        raise HTTPException(status_code=401, detail="Unauthorized token")

    raw_text = extract_text_from_url(req.documents)
    chunks = chunk_text(raw_text)
    db = embed_chunks(chunks)

    answers = []
    for q in req.questions:
        context = get_similar_contexts(db, q)
        answer = generate_answer(context, q)
        answers.append(answer)

    return QueryResponse(answers=answers)
