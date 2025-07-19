from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_milvus import Milvus
from langchain.schema import Document
from uuid import uuid4
import os

# Cấu hình
pdf_data_path = "data"  # chứa các file PDF
milvus_uri = "http://localhost:19530"
collection_name = "pdf_collection"

def create_db_from_files():
    # 1. Load toàn bộ file PDF
    loader = DirectoryLoader(pdf_data_path, glob="*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()

    # 2. Chia nhỏ đoạn văn bản
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=50)
    split_docs = text_splitter.split_documents(documents)

    # 3. Khởi tạo embeddings với Ollama (model đã được pull)
    embedding_model = OllamaEmbeddings(model="qwen2.5-coder:0.5b")

    # 4. Tạo vector database Milvus
    uuids = [str(uuid4()) for _ in range(len(split_docs))]
    vectorstore = Milvus(
        embedding_function=embedding_model,
        connection_args={"uri": milvus_uri},
        collection_name=collection_name,
        drop_old=True
    )
    vectorstore.add_documents(documents=split_docs, ids=uuids)
    print("✅ Vector DB đã tạo trong Milvus.")

    return vectorstore

if __name__ == "__main__":
    create_db_from_files()
