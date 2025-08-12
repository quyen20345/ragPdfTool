# backend/app/services/chat_service.py
from typing import List, Optional
from sqlalchemy.orm import Session
import json
from app.models.models import ChatSession, ChatMessage
from app.schemas.schemas import ChatSessionCreate, ChatSessionResponse, ChatMessageCreate, ChatMessageResponse

class ChatService:
    def create_session(self, db: Session, session: ChatSessionCreate) -> ChatSessionResponse:
        """Create new chat session"""
        db_session = ChatSession(**session.dict())
        db.add(db_session)
        db.commit()
        db.refresh(db_session)
        return ChatSessionResponse.from_orm(db_session)
    
    def get_sessions(self, db: Session) -> List[ChatSessionResponse]:
        """Get all chat sessions"""
        sessions = db.query(ChatSession).order_by(ChatSession.updated_at.desc()).all()
        return [ChatSessionResponse.from_orm(session) for session in sessions]
    
    def get_session(self, db: Session, session_id: int) -> Optional[ChatSessionResponse]:
        """Get session by ID"""
        session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
        return ChatSessionResponse.from_orm(session) if session else None
    
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
        db_message = ChatMessage(**message.dict())
        db.add(db_message)
        db.commit()
        db.refresh(db_message)
        return ChatMessageResponse.from_orm(db_message)
    
    def get_messages(self, db: Session, session_id: int) -> List[ChatMessageResponse]:
        """Get all messages in a session"""
        messages = db.query(ChatMessage).filter(
            ChatMessage.session_id == session_id
        ).order_by(ChatMessage.created_at.asc()).all()
        return [ChatMessageResponse.model_validate(msg) for msg in messages]
