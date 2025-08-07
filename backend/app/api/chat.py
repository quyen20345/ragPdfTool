# backend/app/api/chat.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.services.chat_service import ChatService
from app.services.llm_service import LLMService
from app.schemas.schemas import (
    ChatSessionCreate, ChatSessionResponse, 
    ChatMessageResponse, QueryRequest, QueryResponse
)
import json

router = APIRouter()
chat_service = ChatService()
llm_service = LLMService()

@router.post("/sessions", response_model=ChatSessionResponse)
def create_session(session: ChatSessionCreate, db: Session = Depends(get_db)):
    """Create new chat session"""
    return chat_service.create_session(db, session)

@router.get("/sessions", response_model=List[ChatSessionResponse])
def list_sessions(db: Session = Depends(get_db)):
    """List all chat sessions"""
    return chat_service.get_sessions(db)

@router.get("/sessions/{session_id}", response_model=ChatSessionResponse)
def get_session(session_id: int, db: Session = Depends(get_db)):
    """Get chat session"""
    session = chat_service.get_session(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@router.delete("/sessions/{session_id}")
def delete_session(session_id: int, db: Session = Depends(get_db)):
    """Delete chat session"""
    success = chat_service.delete_session(db, session_id)
    if not success:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"message": "Session deleted successfully"}

@router.get("/sessions/{session_id}/messages", response_model=List[ChatMessageResponse])
def get_messages(session_id: int, db: Session = Depends(get_db)):
    """Get messages in session"""
    return chat_service.get_messages(db, session_id)

@router.post("/query", response_model=QueryResponse)
def query_documents(request: QueryRequest, db: Session = Depends(get_db)):
    """Query documents using RAG"""
    try:
        # Save user message if session provided
        if request.session_id:
            from app.schemas.schemas import ChatMessageCreate
            user_msg = ChatMessageCreate(
                session_id=request.session_id,
                message_type="user",
                content=request.query
            )
            chat_service.add_message(db, user_msg)
        
        # Get answer from LLM
        result = llm_service.query(request.query, request.temperature)
        
        # Format source documents
        source_docs = []
        for doc in result.get("source_documents", []):
            source_docs.append({
                "content": doc.page_content[:500] + "..." if len(doc.page_content) > 500 else doc.page_content,
                "metadata": doc.metadata
            })
        
        answer = result["result"]
        
        # Save assistant message if session provided
        if request.session_id:
            assistant_msg = ChatMessageCreate(
                session_id=request.session_id,
                message_type="assistant",
                content=answer,
                metadata=json.dumps({"source_documents": source_docs})
            )
            chat_service.add_message(db, assistant_msg)
        
        return QueryResponse(
            query=request.query,
            answer=answer,
            session_id=request.session_id,
            source_documents=source_docs,
            model_used=llm_service.llm.model
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")
