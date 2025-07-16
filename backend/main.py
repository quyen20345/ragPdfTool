# from fastapi import FastAPI
# from typing import List, Union # thu vien cung cap cac kieu du lieu
# from pydantic import BaseModel # pydantic: thu vien anh xa du lieu
# from app.schema import (
#     ChatRequest # import schema
# )

# from langchain_ollama import OllamaLLM # thu vien langchain ollama du su dung llm

# app = FastAPI() # khoi tao app

# llm = OllamaLLM( # khoi tao llm
#     # host="http://localhost:11434", # dia chi cua llm
#     # host="http://ollama:11434",
#     host="http://host.docker.internal:11434",
#     model="qwen2.5-coder:0.5b"
# ) 

# @app.post("/prompt")
# def prompt(chat_request: ChatRequest):
#     print("Received prompt:", chat_request.prompt)

#     try:
#         result = llm.invoke(str(chat_request.prompt))
#     except Exception as e:
#         print("Error invoking LLM:", e)
#         return {"error": str(e)}

#     return {
#         "result": result
#     }


# class Person(BaseModel):
#     name: str
#     age: int
#     age: int

# DB: List[Person] = [
#     Person(name="Alice", age=30),
#     Person(name="Bob", age=25)
# ]

# @app.get("/api")
# def read_root()-> List[Person]:
#     return DB

from fastapi import FastAPI
from langchain_ollama import OllamaLLM
from pydantic import BaseModel

app = FastAPI()


class ChatRequest(BaseModel):
    prompt: str

try:
    llm = OllamaLLM(
        host="http://host.docker.internal:11434",
        model="qwen2.5-coder:0.5b"
    )
    print("LLM initialized successfully.")
except Exception as e:
    print("Error initializing LLM:", e)
    llm = None

@app.post("/prompt")
def prompt(chat_request: ChatRequest):
    print("Received prompt:", chat_request.prompt)

    if llm is None:
        return {"error": "LLM not initialized."}

    try:
        result = llm.invoke(chat_request.prompt)
        return {
            "received_prompt": chat_request.prompt,
            "result": result
        }
    except Exception as e:
        print("Error invoking LLM:", e)
        return {"error": str(e)}
