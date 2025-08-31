# from langchain_community.vectorstores import FAISS
# from langchain_community.embeddings import HuggingFaceEmbeddings
# from typing import List
# from langchain_community.vectorstores import FAISS

# def create_faiss_index(texts: List[str]) :
#     embeddings = HuggingFaceEmbeddings(model_name = "sentence-transformers/all-mpnet-base-v2")
#     return FAISS.from_texts(texts, embeddings)


# def retrive_relevant_docs(vectorstore: FAISS, query: str, k: int = 4):
#     return vectorstore.similarity_search(query, k=k)


from typing import List, Union
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

# Use a small, fast sentence-transformers model (384-dim)
_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

def _ensure_list(texts: Union[str, List[str]]) -> List[str]:
    if isinstance(texts, str):
        return [texts]
    return list(texts)

def create_faiss_index(texts: Union[str, List[str]]) -> FAISS:
    """
    Build a FAISS vector store from one or more text chunks.
    Raises ValueError if texts are empty after cleaning.
    """
    texts = [t.strip() for t in _ensure_list(texts) if isinstance(t, str) and t.strip()]
    if not texts:
        raise ValueError("No non-empty text chunks provided to create_faiss_index().")

    embeddings_model = HuggingFaceEmbeddings(model_name=_MODEL_NAME)
    # Correct API: pass the embedding function via the 'embedding' kwarg
    vectorstore = FAISS.from_texts(texts, embedding=embeddings_model)
    return vectorstore

def retrive_relevant_docs(vectorstore: FAISS, query: str, k: int = 3):
    """
    kNN search over FAISS. Returns top-k Documents.
    """
    return vectorstore.similarity_search(query, k=k)
