# app/retriever.py
def get_similar_contexts(vector_store, question: str, k: int = 5):
    # return top similar docs (tunable)
    return vector_store.similarity_search(question, k=5, fetch_k=15)
#-----------------------------#------------------------------------------------------------------#