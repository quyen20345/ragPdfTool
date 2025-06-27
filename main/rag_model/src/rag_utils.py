# main/rag_model/src/rag_utils.py

from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_community.vectorstores import FAISS
from pathlib import Path
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
import os

# vector_db_path = "vectorstores/db_faiss"
# pdf_data_path = "data"
vector_db_path = os.path.join(os.path.dirname(__file__), "vectorstores", "db_faiss")
pdf_data_path = os.path.join(os.path.dirname(__file__), "data")

def create_db_from_files():
    print(f"---folder pdf path: {pdf_data_path}--")
    print(f"---folder pdf path: {vector_db_path}--")
    # declare loader to scan entire data directory for pdf files
    loader = DirectoryLoader(pdf_data_path, glob="*.pdf", loader_cls = PyPDFLoader)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=50)
    chunks = text_splitter.split_documents(documents)
    base_dir = Path(__file__).resolve().parent
    model_path = base_dir / "models" / "models/all-MiniLM-L6-v2-f16.gguf"
    # Embeding
    embedding_model = GPT4AllEmbeddings(model_file=model_path, allow_download=False)
    db = FAISS.from_documents(chunks, embedding_model)
    db.save_local(vector_db_path)
    return db

def load_vector_db():
    base_dir = Path(__file__).resolve().parent
    vector_db_path = base_dir / "vectorstores" / "db_faiss"
    embedding_model_path = base_dir / "models" / "models/all-MiniLM-L6-v2-f16.gguf"

    embedding_model = GPT4AllEmbeddings(model_file=embedding_model_path, allow_download=False)
    db = FAISS.load_local(vector_db_path, embedding_model, allow_dangerous_deserialization=True)
    return db

if __name__ == "__main__":
    # create_db_from_text()
    create_db_from_files()
    print("preparing vectorDB done !!!")
