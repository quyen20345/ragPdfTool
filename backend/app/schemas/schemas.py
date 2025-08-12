# backend/app/schemas/schemas.py
from pydantic import BaseModel,Field , ConfigDict
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
    # from_attributes=True cho phep khoi tao model tu object co thuoc tinh.
    model_config = ConfigDict(from_attributes=True)  # pydantic v2-style

# Chat schemas
class ChatSessionCreate(BaseModel):
    session_name: str

class ChatSessionResponse(BaseModel):
    id: int
    session_name: str
    created_at: datetime
    # from_attributes=True cho phep khoi tao model tu object co thuoc tinh.
    model_config = ConfigDict(from_attributes=True)  # pydantic v2-style

class ChatMessageCreate(BaseModel):
    session_id: int
    message_type: str
    content: str
    metadata: Optional[str] = None
    # client vẫn gửi "metadata", nhưng khi dump sẽ ra key extra_metadata
    metadata: Optional[str] = Field(default=None, alias="extra_metadata")
    model_config = ConfigDict(populate_by_name=True)  # cho phép dùng alias khi dump


class ChatMessageResponse(BaseModel):
    id: int
    session_id: int
    message_type: str
    content: str
    # đọc từ attribute ORM 'extra_metadata', trả về key 'metadata'
    metadata: Optional[str] = Field(default=None, alias="extra_metadata") # alias bi danh thay the cho bien goc.
    created_at: datetime
    # from_attributes=True cho phep khoi tao model tu object co thuoc tinh.
    # populate_by_name=True: cho phep khoi tao model bang ten truong goc khi co ca alias 
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

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
