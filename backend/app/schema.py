from pydantic import BaseModel, Field # pydantic: thu vien anh xa du lieu
from typing import * # thu vien cung cap cac kieu du lieu

class ChatRequest(BaseModel):
    prompt: str = Field(
        default="How to write a Python function?"
    )

class ChatResponse(BaseModel):
    response: str
    model: str

class Message(BaseModel):
    role: str
    content: str
