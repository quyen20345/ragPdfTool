from langchain_community.llms import CTransformers
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_community.vectorstores import FAISS
import os
from pathlib import Path
from .rag_utils import load_vector_db

# Base dir: thư mục hiện tại chứa file đang chạy (vd: qabot.py)
base_dir = Path(__file__).resolve().parent

# Trỏ tới file model
model_file = base_dir / "models" / "vinallama-7b-chat_q5_0.gguf"

vector_db_path = "vectorstores/db_faiss"

# Load LLM
def load_llm(model_file: str) -> CTransformers:
    llm = CTransformers(
        model=model_file,
        model_type="llama",
        max_new_tokens=1024,
        temperature=0.01
    )
    return llm

# Tao prompt template
def creat_prompt(template: str) -> PromptTemplate:
    prompt = PromptTemplate(template=template, input_variables=["context", "question"])
    return prompt


# Tao simple chain
def create_qa_chain(prompt: PromptTemplate, llm: CTransformers, db: FAISS) -> RetrievalQA:
    llm_chain = RetrievalQA.from_chain_type(
        llm = llm,
        chain_type= "stuff",
        retriever = db.as_retriever(search_kwargs = {"k":3}, max_tokens_limit=1024),
        return_source_documents = False,
        chain_type_kwargs= {'prompt': prompt}

    )
    return llm_chain

db = load_vector_db()
llm = load_llm(str(model_file))

#Tao Prompt
template = """<|im_start|>system\nUse the following information to answer the question. If you don't know the answer, say you don't know, don't try to make up the answer.\n
    {context}<|im_end|>\n<|im_start|>user\n{question}<|im_end|>\n<|im_start|>assistant"""
prompt = creat_prompt(template=template)

llm_chain  = create_qa_chain(prompt=prompt, llm=llm, db=db)

# chay khi run truc tiep file
if __name__ == "__main__":
    question = "What is the Attention?"
    response = llm_chain.invoke({"query": question})
    print(response)