
from fastapi import FastAPI
from pydantic import BaseModel
from app.schema import (ChatRequest, Person)
from typing import List
# from langchain_community.llms import Ollama
from langchain_ollama import OllamaLLM # thu vien langchain ollama du su dung llm
from langchain_core.prompts import PromptTemplate
from langchain_core.caches import InMemoryCache
from langchain_core.globals import set_llm_cache
from langchain_core.output_parsers import StrOutputParser

from app.db import *
from langchain.sql_database import SQLDatabase

# thu vien de load vector database
from langchain.vectorstores import FAISS
from langchain_community.embeddings import GPT4AllEmbeddings
from pathlib import Path
import os

# Initialize FastAPI App
app = FastAPI()

# load the vector database
path_faiss_index = "app/faiss_pdf_rag/vectorstores/db_faiss"
# Base dir
base_dir = Path(__file__).resolve().parent
model_path = base_dir / "app" / "faiss_pdf_rag" / "models" / "models/all-MiniLM-L6-v2-f16.gguf"
# embedding
embedding_model = GPT4AllEmbeddings(model_file=model_path, allow_download=False) 
vector_db = FAISS.load_local(path_faiss_index, embedding_model, allow_dangerous_deserialization=True)
retriever = vector_db.as_retriever(search_kwargs={"k": 3})

# Load the model
try:
    # llm = Ollama(
    #     base_url="http://host.docker.internal:11434", # the request go to outside the ollama container, so the ollama model can be handled the request
    #     # base_url="http://localhost:11434", # error: Connection refused - backend container failed to connect to host, so the resquest couldn't be handled by the ollama model 
    #     model="qwen2.5-coder:0.5b",
    #     temperature=0,
    # )
    llm = OllamaLLM(
        model="qwen2.5-coder:0.5b",
        base_url="http://host.docker.internal:11434",
        temperature=0,
    )
    print("LLM initialized successfully.")
except Exception as e:
    print("Error initializing LLM:", e)
    llm = None


# Initialize the in-memory cache for LLMs
cache = InMemoryCache()
set_llm_cache(cache)

# Define the prompt template
# https://mirascope.com/blog/langchain-prompt-template#prompttemplate-simple-string-based-prompts:~:text=a%20conversation%20history).-,PromptTemplate,%3A%20Simple%20String%2DBased%20Prompts,-This%20generates%20prompts
template = PromptTemplate.from_template( 
    """
    {context}

    {context_db}

    User's question:
    {question}
    """
)

db = SQLDatabase(engine=engine)

# Create the LLM chain with the prompt template
# https://python.langchain.com/api_reference/langchain/chains/langchain.chains.llm.LLMChain.html
llm_chain = (
    template | llm | StrOutputParser()
)

# Startup event to create the database and tables before the app starts.
# https://fastapi.tiangolo.com/advanced/events/#alternative-events-deprecated:~:text=.-,startup,event,-%C2%B6
@app.on_event("startup")
def connect_db():
    create_db_and_tables() # create the database and tables.

@app.post("/prompt")
def prompt(chat_request: ChatRequest, session_db: SessionDeps)-> dict:
    print("chat_request:", chat_request.prompt)

    if llm is None:
        return {"error": "LLM not initialized."}

    try:
        # Truy vấn vector DB
        docs = retriever.invoke(chat_request.prompt)
        context_vector = "\n".join([doc.page_content for doc in docs])

        context_db = f"You are a helpful assistant. You can answer questions based on the context provided.{db.get_table_info(db.get_usable_table_names())}"
        print("context_db:", context_db)
        result = llm_chain.invoke({
            "context": chat_request.context or context_vector,
            "context_db": context_db,
            "question": chat_request.prompt
        })

        # add the rows to the database with the session
        # https://sqlmodel.tiangolo.com/tutorial/insert/#create-data-with-python-and-sqlmodel:~:text=to%20the%20database-,Create%20a%20Model%20Instance,-%C2%B6
        session_db.add(
            DataChat(
                prompt=chat_request.prompt,
                result=result
            )
        )
        # commit the changes to the database
        # https://sqlmodel.tiangolo.com/tutorial/insert/#add-model-instances-to-the-session:~:text=a%20broken%20state.-,Commit%20the%20Session%20Changes,-%C2%B6
        session_db.commit()
        return {
            "received_prompt": chat_request.prompt,
            "result": result
        }
    except Exception as e:
        print("Error invoking LLM:", e)
        return {"error": str(e)}


# test
@app.get("/api")
def read_root()-> List[Person]:
    DB = [
       Person(id=1, name="Alice", age=25),
       Person(id=2, name="Bob", age=30),
       Person(id=3, name="Charlie", age=22)
  ]
    return DB
