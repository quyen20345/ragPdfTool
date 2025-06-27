# import getpass
# import os
# from langchain_core.messages import HumanMessage

# if not os.environ.get("GOOGLE_API_KEY"):
#     os.environ["GOOGLE_API_KEY"] = "AIzaSyDaOTajq9YRNRvNE7bIPYOv568CP4WNO0A" # getpass.getpass("Nhập API key Google Gemini: ") 
#     # "AIzaSyDaOTajq9YRNRvNE7bIPYOv568CP4WNO0A"

# from langchain.chat_models import init_chat_model

# model = init_chat_model("gemini-2.0-flash", model_provider="google_genai")

# def ask_with_gemini(question: str):
#     response = model.invoke([HumanMessage(content=question)])
#     return {"result": response.content} 

# if __name__ == "__main__":
#     question = input("Nhập câu hỏi: ")
#     response = ask_with_gemini(question)
#     print(f"Trả lời từ Gemini: {response}")

# main/rag_model/src/geminiQA.py
import os
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from .rag_utils import load_vector_db, create_db_from_files  # import FAISS retriever

# API key
if not os.environ.get("GOOGLE_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = "AIzaSyDaOTajq9YRNRvNE7bIPYOv568CP4WNO0A"  # 

# Load Gemini model
model = init_chat_model("gemini-2.0-flash", model_provider="google_genai")

# Load FAISS
db = load_vector_db()

# Prompt template (giống như bên vinallama)
def build_prompt(context: str, question: str) -> str:
    return f"""<|im_start|>system
Use the following information to answer the question. 
If you don't know the answer, say you don't know, don't try to make up the answer.

{context}
<|im_end|>
<|im_start|>user
{question}
<|im_end|>
<|im_start|>assistant"""

# Hàm chính
def ask_with_gemini(question: str):
    retriever = db.as_retriever(search_kwargs={"k": 3})
    docs = retriever.get_relevant_documents(question)
    context = "\n\n".join([doc.page_content for doc in docs])

    prompt = build_prompt(context, question)
    response = model.invoke([HumanMessage(content=prompt)])
    return {"result": response.content}

# Test 
if __name__ == "__main__":
    q = input("Nhập câu hỏi: ")
    r = ask_with_gemini(q)
    print("Gemini trả lời:", r["result"])
