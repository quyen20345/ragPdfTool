# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import engine, Base
from app.api import documents, chat
from app.services.vector_service import VectorService
from app.services.llm_service import LLMService
from app.core.config import settings

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="RAG PDF System", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(documents.router, prefix="/api/documents", tags=["documents"])
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])

# Initialize services
vector_service = VectorService()
llm_service = LLMService()

@app.get("/")
def read_root():
    return {
        "message": "RAG PDF System is ready!",
        "embedding_model": settings.EMBEDDING_MODEL,
        "llm_model": settings.OLLAMA_MODEL,
        "collection": settings.COLLECTION_NAME
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    try:
        # Check Qdrant
        collection_info = vector_service.get_collection_info()
        
        # Check Ollama
        ollama_ok, ollama_response = llm_service.test_connection()
        
        return {
            "status": "healthy",
            "qdrant": f"connected - {collection_info['total_vectors']} vectors",
            "ollama": "connected" if ollama_ok else f"error: {ollama_response}",
            "ollama_response_sample": ollama_response if ollama_ok else None
        }
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
