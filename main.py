from fastapi import FastAPI, Header, HTTPException
from app.models import QueryRequest, QueryResponse
from app.processor import extract_text_from_url, chunk_text
from app.embedder import embed_chunks
from app.retriever import get_similar_contexts
from app.llm_reasoner import generate_answer
from dotenv import load_dotenv
import os
import json  # ✅ Import json

load_dotenv()

app = FastAPI()

@app.get("/")
def home():
    return {"message": "FastAPI is live!"}
@app.post("/api/v1/hackrx/run", response_model=QueryResponse)
async def run_query(req: QueryRequest, authorization: str = Header(...)):
    if not authorization.endswith("cda0"):
        raise HTTPException(status_code=401, detail="Unauthorized token")
    
   
    print(f"📄 Document URL: {req.documents}")
    print(f"❓ Questions: {req.questions}")

    raw_text = extract_text_from_url(req.documents)
    chunks = chunk_text(raw_text)
    db = embed_chunks(chunks)
    
    answers = []
    for q in req.questions:
        context = get_similar_contexts(db, q)
        answer = generate_answer(context, q)
        answers.append(answer)

    response = QueryResponse(answers=answers)

    # ✅ Save the response to a JSON file
    # with open("response_output2.json", "w", encoding="utf-8") as f:
    #     json.dump(response.dict(), f, indent=4, ensure_ascii=False)

    return response
