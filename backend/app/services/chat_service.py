# backend/app/services/chat_service.py
from typing import List, Optional
from sqlalchemy.orm import Session
import json
from app.models.models import ChatSession, ChatMessage
from app.schemas.schemas import ChatSessionCreate, ChatSessionResponse, ChatMessageCreate, ChatMessageResponse

class ChatService:
    def create_session(self, db: Session, session: ChatSessionCreate) -> ChatSessionResponse:
        """Create new chat session"""
        db_session = ChatSession(**session.model_dump())  # v2: dùng model_dump thay dict()
        db.add(db_session)
        db.commit()
        db.refresh(db_session)
        return ChatSessionResponse.model_validate(db_session) # thay doi .from_orm tu pydantic v1 -> v2 .model_validate
    
    def get_sessions(self, db: Session) -> List[ChatSessionResponse]:
        """Get all chat sessions"""
        sessions = db.query(ChatSession).order_by(ChatSession.updated_at.desc()).all()
        return [ChatSessionResponse.model_validate(session) for session in sessions] # thay doi .from_orm tu pydantic v1 -> v2 .model_validate
    
    def get_session(self, db: Session, session_id: int) -> Optional[ChatSessionResponse]:
        """Get session by ID"""
        session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
        return ChatSessionResponse.model_validate(session) if session else None # thay doi .from_orm tu pydantic v1 -> v2 .model_validate
    
    def delete_session(self, db: Session, session_id: int) -> bool:
        """Delete chat session and all its messages"""
        session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
        if not session:
            return False
        
        # Delete all messages in session
        db.query(ChatMessage).filter(ChatMessage.session_id == session_id).delete()
        db.delete(session)
        db.commit()
        return True
    
    def add_message(self, db: Session, message: ChatMessageCreate) -> ChatMessageResponse:
        """Add message to chat session"""
        # DÙNG ALIAS khi serialize: 'metadata' (client) -> 'extra_metadata' (ORM attribute)
        payload = message.model_dump(by_alias=True)   # <— quan trọng
        db_message = ChatMessage(**payload)
        db.add(db_message)
        db.commit()
        db.refresh(db_message)
        return ChatMessageResponse.model_validate(db_message) # thay doi .from_orm tu pydantic v1 -> v2 .model_validate
    
    def get_messages(self, db: Session, session_id: int) -> List[ChatMessageResponse]:
        """Get all messages in a session"""
        messages = db.query(ChatMessage).filter(
            ChatMessage.session_id == session_id
        ).order_by(ChatMessage.created_at.asc()).all()
        return [ChatMessageResponse.model_validate(msg) for msg in messages] # thay doi .from_orm tu pydantic v1 -> v2 .model_validate
