# backend/app/schemas/schemas.py
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional, Dict, Any

# Document schemas
class DocumentBase(BaseModel):
    filename: str
    original_filename: str
    file_size: int

class DocumentCreate(DocumentBase):
    file_path: str

class DocumentResponse(DocumentBase):
    id: int
    total_chunks: int
    is_processed: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Chat schemas
class ChatSessionCreate(BaseModel):
    session_name: str

class ChatSessionResponse(BaseModel):
    id: int
    session_name: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class ChatMessageCreate(BaseModel):
    session_id: int
    message_type: str
    content: str
    metadata: Optional[str] = None

class ChatMessageResponse(BaseModel):
    id: int
    session_id: int
    message_type: str
    content: str
    metadata: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

# Query schemas
class QueryRequest(BaseModel):
    query: str
    session_id: Optional[int] = None
    max_results: int = 3
    temperature: float = 0.7

class QueryResponse(BaseModel):
    query: str
    answer: str
    session_id: Optional[int] = None
    source_documents: List[Dict[str, Any]]
    model_used: str
