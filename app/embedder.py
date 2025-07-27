from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

from langchain.docstore.document import Document

def embed_chunks(chunks: list) -> FAISS:
    docs = [Document(page_content=chunk) for chunk in chunks]
    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5") 
    db = FAISS.from_documents(docs, embeddings)
    return db
