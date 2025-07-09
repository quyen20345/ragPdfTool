import os
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_community.vectorstores import FAISS
from pathlib import Path

class VectorStore:
    def __init__(self, index_path: str) -> None:
        self.index_path = index_path
        self.base_dir = Path(__file__).resolve().parent
        self.model_embedding_path = self.base_dir / "models" / "models/all-MiniLM-L6-v2-f16.gguf"
        self.embedding_model = None
        self.vector_store = None

    def create_vector_store(self) -> FAISS:
        if self.model_embedding_path.exists():
            self.embedding_model = GPT4AllEmbeddings(model_file=str(self.model_embedding_path), allow_download=False)
            self.vector_store = FAISS(
                embedding_function=self.embedding_model.embed_documents,
                index=None,
                docstore=None,
                index_to_docstore_id={},
            )
            return self.vector_store
        else:
            raise FileNotFoundError(f"Embedding model file not found at {self.model_embedding_path}")
        
    def load_vector_store(self) -> FAISS:
        if self.vector_store is None:
            self.create_vector_store()
        