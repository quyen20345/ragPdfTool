from pydantic import BaseModel, Field
from typing import Optional, List


# ----------------------------
# Request body for chat input
# ----------------------------
class ChatRequest(BaseModel):
    prompt: str = Field(
        default="How to write a Python function?",
        description="User's input question"
    )
    context: Optional[str] = Field(
        default=None,
        description="Optional pre-context for the model"
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
