from pydantic import BaseModel, Field
from typing import Optional, List


# ----------------------------
# Request body for chat input
# ----------------------------
class ChatRequest(BaseModel):
    prompt: str = Field(
        default="Tóm tắt context cho tôi?",
        description="đây là câu hỏi hoặc yêu cầu của người dùng"
    )
    context: Optional[str] = Field(
        default=None,
        description="Ngữ cảnh tùy chọn cho mô hình"
    )


# ----------------------------
# Optional response schema (useful if frontend uses it)
# ----------------------------
class ChatResponse(BaseModel):
    response: str
    model: str


# ----------------------------
# Generic chat message (for future extensions like chat history)
# ----------------------------
class Message(BaseModel):
    role: str  # e.g., "user" or "assistant"
    content: str


# ----------------------------
# For schema testing/demo
# ----------------------------
class Person(BaseModel):
    id: int
    name: str
    age: int
