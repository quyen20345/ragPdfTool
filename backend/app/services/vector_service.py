# backend/app/services/vector_service.py
import uuid
from pathlib import Path
from typing import List, Dict, Any
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Qdrant
from langchain.schema import Document
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, Filter, FieldCondition, MatchValue, FilterSelector
from app.core.config import settings

class VectorService:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL)
        self.qdrant_client = QdrantClient(host=settings.QDRANT_HOST, port=settings.QDRANT_PORT)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", " ", ""]
        )
        self.ensure_collection()
    
    def ensure_collection(self):
        """Ensure Qdrant collection exists"""
        try:
            existing = [c.name for c in self.qdrant_client.get_collections().collections]
            if settings.COLLECTION_NAME not in existing:
                # Generate a sample embedding to infer dimension
                sample_embedding = self.embeddings.embed_query("sample text")
                vector_dim = len(sample_embedding)
                self.qdrant_client.recreate_collection(
                    collection_name=settings.COLLECTION_NAME,
                    vectors_config=VectorParams(size=vector_dim, distance=Distance.COSINE),
                )
                print(f"Created collection '{settings.COLLECTION_NAME}' with dimension {vector_dim}")
        except Exception as e:
            print(f"Error ensuring collection: {e}")
            raise
    
    def get_vectorstore(self) -> Qdrant:
        """Get Qdrant vectorstore using the new Qdrant class"""
        return Qdrant(
            client=self.qdrant_client,
            collection_name=settings.COLLECTION_NAME,
            embeddings=self.embeddings,
        )
    
    def process_pdf(self, file_path: str, filename: str) -> int:
        """Process PDF and add to vector database"""
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        texts = self.text_splitter.split_documents(documents)
        
        # Attach metadata
        for idx, text in enumerate(texts):
            text.metadata.update({
                "filename": filename,
                "chunk_id": idx,
                "total_chunks": len(texts),
                "document_id": str(uuid.uuid4())
            })
        
        vectorstore = self.get_vectorstore()
        vectorstore.add_documents(texts)
        return len(texts)
    
    def delete_document_vectors(self, filename: str):
        """Delete vectors for a specific document"""
        filter_cond = Filter(
            must=[FieldCondition(key="metadata.filename", match=MatchValue(value=filename))]
        )
        return self.qdrant_client.delete(
            collection_name=settings.COLLECTION_NAME,
            points_selector=FilterSelector(filter=filter_cond),
            wait=True
        )
    
    def search_similar(self, query: str, k: int = 3) -> List[Document]:
        """Search for similar documents"""
        vectorstore = self.get_vectorstore()
        return vectorstore.similarity_search(query, k=k)
    
    def get_collection_info(self) -> Dict[str, Any]:
        """Get collection information"""
        try:
            info = self.qdrant_client.get_collection(settings.COLLECTION_NAME)
            return {"total_vectors": info.points_count}
        except Exception:
            return {"total_vectors": 0}
