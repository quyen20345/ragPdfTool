
from fastapi import FastAPI
from langchain_ollama import OllamaLLM
from pydantic import BaseModel
from app.schema import (ChatRequest, Person)
from typing import List
# from langchain_community.llms import Ollama
from langchain_ollama import OllamaLLM # thu vien langchain ollama du su dung llm
from langchain_core.prompts import PromptTemplate
from langchain_core.caches import InMemoryCache
from langchain_core.globals import set_llm_cache
from langchain_core.output_parsers import StrOutputParser

# Initialize FastAPI App
app = FastAPI()

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
    User's question:
    {question}
    """
)

# Create the LLM chain with the prompt template
# https://python.langchain.com/api_reference/langchain/chains/langchain.chains.llm.LLMChain.html
llm_chain = (
    template | llm | StrOutputParser()
)


@app.post("/prompt")
def prompt(chat_request: ChatRequest)-> dict:
    print("chat_request:", chat_request.prompt)

    if llm is None:
        return {"error": "LLM not initialized."}

    try:
        result = llm_chain.invoke({
            "context": chat_request.context or "",
            "question": chat_request.prompt
        })
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
