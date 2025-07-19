from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain.chains import RetrievalQA
from pathlib import Path
from langchain_ollama import OllamaLLM

# Đường dẫn đến FAISS vector database
vector_db_path = "vectorstores/db_faiss"

# Đường dẫn đến mô hình embedding đã dùng để tạo DB
base_dir = Path(__file__).resolve().parent
model_path = base_dir / "models" / "models/all-MiniLM-L6-v2-f16.gguf"

# Load FAISS vector store
embedding_model = GPT4AllEmbeddings(
    model_file=model_path,
    allow_download=False
)
db = FAISS.load_local(
    vector_db_path,
    embeddings=embedding_model,
    allow_dangerous_deserialization=True
)


# Khởi tạo LLM từ Ollama
llm = OllamaLLM(
    model="qwen2.5-coder:0.5b",
    base_url="http://host.docker.internal:11434",  # chạy trong Docker
    temperature=0.0
)

# Tạo chain truy vấn RAG
qa = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=db.as_retriever(search_kwargs={"k": 2}),
    chain_type="stuff",  # có thể đổi thành "map_reduce", "refine" nếu cần
    return_source_documents=True
)

# Gửi truy vấn
query = "What are residual networks and how do they help deep learning models?"
result = qa({"query": query})

# In kết quả
print("🔍 Question:")
print(query)
print("\n🧠 Answer:")
print(result["result"])

print("\n📄 Source Documents:")
for doc in result["source_documents"]:
    print(f"- {doc.metadata}")
    print(doc.page_content[:200], "...\n")
