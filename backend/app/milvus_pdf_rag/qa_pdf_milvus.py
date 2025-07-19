from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_milvus import Milvus
from langchain_ollama.embeddings import OllamaEmbeddings

# Cấu hình
milvus_uri = "http://localhost:19530"
collection_name = "pdf_collection"

# 1. Load LLM từ Ollama
def load_llm():
    llm = Ollama(model="qwen2.5-coder:0.5b", temperature=0.01)
    return llm

# 2. Prompt template
def create_prompt():
    template = """<|im_start|>system
Use the following context to answer the question. If unsure, say you don't know.
{context}<|im_end|>
<|im_start|>user
{question}<|im_end|>
<|im_start|>assistant"""
    return PromptTemplate(template=template, input_variables=["context", "question"])

# 3. Kết nối tới Milvus
def connect_milvus():
    embeddings = OllamaEmbeddings(model="qwen2.5-coder:0.5b")
    vectorstore = Milvus(
        embedding_function=embeddings,
        connection_args={"uri": milvus_uri},
        collection_name=collection_name
    )
    return vectorstore

# 4. Tạo RetrievalQA Chain
def create_qa_chain():
    llm = load_llm()
    prompt = create_prompt()
    vectorstore = connect_milvus()

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
        return_source_documents=False,
        chain_type_kwargs={"prompt": prompt}
    )
    return qa_chain

# 5. Test
if __name__ == "__main__":
    qa = create_qa_chain()
    question = "Hồ Cảnh Quyền là ai?"
    result = qa.invoke({"query": question})
    print(result)
