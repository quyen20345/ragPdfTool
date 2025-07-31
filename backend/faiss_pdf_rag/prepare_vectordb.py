from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from pathlib import Path
import os

# Đường dẫn đến thư mục chứa PDF và nơi lưu VectorDB
pdf_data_path = "data"
vector_db_path = "vectorstores/db_faiss"

# Kiểm tra đường dẫn data
def check_data_path():
    if os.path.exists(pdf_data_path):
        print(f"[✓] Path '{pdf_data_path}' exists.")
    else:
        print(f"[!] Path '{pdf_data_path}' does NOT exist.")
        raise FileNotFoundError(f"'{pdf_data_path}' not found.")

# Tạo vector DB từ file PDF
def create_db_from_files():
    print("[*] Loading PDF files...")
    loader = DirectoryLoader(pdf_data_path, glob="*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()

    print(f"[✓] Loaded {len(documents)} documents.")

    # Tách nhỏ tài liệu thành đoạn
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=50)
    chunks = text_splitter.split_documents(documents)

    print(f"[✓] Split into {len(chunks)} chunks.")

    # Dùng mô hình Hugging Face để tạo embedding
    print("[*] Loading embedding model...")
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # Tạo FAISS vector store
    print("[*] Creating FAISS vector store...")
    db = FAISS.from_documents(chunks, embedding_model)
    db.save_local(vector_db_path)
    print(f"[✓] Vector DB saved at '{vector_db_path}'.")

    return db

if __name__ == "__main__":
    check_data_path()
    create_db_from_files()
    print("[✓] prepare_vectordb.py done.")
