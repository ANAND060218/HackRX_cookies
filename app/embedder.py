# app/embedder.py
import torch
from langchain.docstore.document import Document
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

# Device detection
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print(f"🔍 embedder: using device -> {DEVICE}")

# Initialize embedding model with device-aware kwargs
embedding_model = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en",   # we can also use BAAI/bge-base-en it will be faster but less accurate
    model_kwargs={"device": DEVICE}
)
#-----------------------------#------------------------------------------------------------------#
def embed_chunks(chunks):
    """
    Accepts list[str] -> returns FAISS index object.
    FAISS index is CPU-persisted and picklable.
    """
    docs = [Document(page_content=c) for c in chunks]
    db = FAISS.from_documents(docs, embedding_model)
    return db

#-----------------------------#------------------------------------------------------------------#