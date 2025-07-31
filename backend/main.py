from fastapi import FastAPI
from pydantic import BaseModel
from app.schema import ChatRequest
from app.db import *

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.utilities import SQLDatabase

from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.caches import InMemoryCache
from langchain_core.globals import set_llm_cache
from langchain_core.output_parsers import StrOutputParser

from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize FastAPI
app = FastAPI()

# Paths
base_dir = Path(__file__).resolve().parent
path_faiss_index = base_dir / "faiss_pdf_rag" / "vectorstores" / "db_faiss"

# Load embedding model from Hugging Face
embedding_model = HuggingFaceEmbeddings(
    model_name=os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
)

# Load FAISS vector database
vector_db = FAISS.load_local("faiss_pdf_rag/db_faiss", embedding_model, allow_dangerous_deserialization=True)

# vector_db = FAISS.load_local(
#     str(path_faiss_index), 
#     embedding_model, 
#     allow_dangerous_deserialization=True
# )
retriever = vector_db.as_retriever(search_kwargs={"k": 3})

# Initialize Ollama LLM
try:
    llm = OllamaLLM(
        model=os.getenv("OLLAMA_MODEL"),
        base_url=os.getenv("OLLAMA_HOST"),
        temperature=0,
    )
    print("LLM initialized successfully.")
except Exception as e:
    print("Error initializing LLM:", e)
    llm = None

# Set up cache
set_llm_cache(InMemoryCache())

# Prompt template
template = PromptTemplate.from_template(
    """
    Bạn là một chatbot trả lời câu hỏi dựa vào ngữ cảnh dưới. 
    Trả lời bằng tiếng việt.
    Dữ liệu từ file pdf:
    {context}
    Lịch sử chat:
    {context_db}
    Câu hỏi của người dùng:
    {question}
    """
)

# LangChain LLM chain
llm_chain = template | llm | StrOutputParser()

# SQL Database (for storing chat logs)
db = SQLDatabase(engine=engine)

# App startup: Create tables
@app.on_event("startup")
def startup_event():
    create_db_and_tables()

# Chat endpoint
@app.post("/prompt")
def prompt(chat_request: ChatRequest, session_db: SessionDeps) -> dict:
    if llm is None:
        return {"error": "LLM not initialized."}
    
    try:
        # Get context from FAISS
        docs = retriever.invoke(chat_request.prompt)
        context_vector = "\n".join([doc.page_content for doc in docs])

        # SQL schema info as context
        context_db = f"You are a helpful assistant. You can answer questions based on the context provided.\n{db.get_table_info(db.get_usable_table_names())}"
        
        # Generate response
        result = llm_chain.invoke({
            "context": chat_request.context or context_vector,
            "context_db": context_db,
            "question": chat_request.prompt
        })

        # Save to database
        session_db.add(
            DataChat(prompt=chat_request.prompt, result=result)
        )
        session_db.commit()

        return {
            "received_prompt": chat_request.prompt,
            "result": result
        }

    except Exception as e:
        print("Error:", e)
        return {"error": str(e)}

# Health check
@app.get("/")
def read_root():
    return {"message": "Hello world!"}
