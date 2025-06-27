# main/rag_model/src/rag_utils.py

from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_community.vectorstores import FAISS
from pathlib import Path

def load_vector_db():
    base_dir = Path(__file__).resolve().parent
    vector_db_path = base_dir / "vectorstores" / "db_faiss"
    embedding_model_path = base_dir / "models" / "models/all-MiniLM-L6-v2-f16.gguf"

    embedding_model = GPT4AllEmbeddings(model_file=embedding_model_path, allow_download=False)
    db = FAISS.load_local(vector_db_path, embedding_model, allow_dangerous_deserialization=True)
    return db
