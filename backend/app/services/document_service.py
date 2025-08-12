# backend/app/services/document_service.py
import os
import uuid
from pathlib import Path
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, UploadFile
from app.models.models import Document
from app.schemas.schemas import DocumentCreate, DocumentResponse
from app.services.vector_service import VectorService
from app.core.config import settings

class DocumentService:
    def __init__(self):
        self.vector_service = VectorService()
    
    def create_document(self, db: Session, file: UploadFile, content: bytes) -> DocumentResponse:
        """Create and process document"""
        # Validate file
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")
        
        if len(content) > settings.MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail="File too large")
        
        # Generate unique filename
        file_extension = Path(file.filename).suffix
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = settings.UPLOAD_DIR / unique_filename
        
        # Initialize db_document to None for proper cleanup
        db_document = None
        
        try:
            # Save file
            with open(file_path, "wb") as f:
                f.write(content)
            
            # Create database record
            db_document = Document(
                filename=unique_filename,
                original_filename=file.filename,
                file_path=str(file_path),
                file_size=len(content)
            )
            db.add(db_document)
            db.commit()
            db.refresh(db_document)
            
            # Process with vector database
            total_chunks = self.vector_service.process_pdf(str(file_path), unique_filename)
            
            # Update document with processing info
            db_document.total_chunks = total_chunks
            db_document.is_processed = True
            db.commit()
            db.refresh(db_document)
            
            return DocumentResponse.model_validate(db_document)  # Updated for Pydantic v2
            
        except Exception as e:
            # Cleanup on error
            if file_path.exists():
                file_path.unlink()
            if db_document.id:
                db.delete(db_document)
                db.commit()
            raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")
    
    def get_documents(self, db: Session) -> List[DocumentResponse]:
        """Get all documents"""
        documents = db.query(Document).all()
        return [DocumentResponse.from_orm(doc) for doc in documents]
    
    def get_document(self, db: Session, document_id: int) -> Optional[DocumentResponse]:
        """Get document by ID"""
        document = db.query(Document).filter(Document.id == document_id).first()
        return DocumentResponse.from_orm(document) if document else None
    
    def delete_document(self, db: Session, document_id: int) -> bool:
        """Delete document and its vectors"""
        document = db.query(Document).filter(Document.id == document_id).first()
        if not document:
            return False
        
        try:
            # Delete vectors
            self.vector_service.delete_document_vectors(document.filename)
            
            # Delete file
            file_path = Path(document.file_path)
            if file_path.exists():
                file_path.unlink()
            
            # Delete database record
            db.delete(document)
            db.commit()
            return True
            
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Error deleting document: {str(e)}")
