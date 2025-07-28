from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.docstore.document import Document

def embed_chunks(chunks: list) -> FAISS:
    docs = [Document(page_content=chunk) for chunk in chunks]

    # ✅ Use local model path
    embeddings = HuggingFaceEmbeddings(
        model_name="models/bge-small-en",  # 👈 point to local model folder
        model_kwargs={"device": "cpu"}     # or "cuda" if using GPU
    )

    db = FAISS.from_documents(docs, embeddings)
    return db
