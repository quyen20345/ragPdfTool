from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from app.schema import ChatRequest
from app.db import *

from langchain_qdrant import Qdrant
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.utilities import SQLDatabase
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.caches import InMemoryCache
from langchain_core.globals import set_llm_cache
from langchain_core.output_parsers import StrOutputParser

from qdrant_client.models import Filter, FieldCondition, MatchValue

from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
base_dir = Path(__file__).resolve().parent

embedding_model = HuggingFaceEmbeddings(
    model_name=os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
)

qdrant_host = os.getenv("QDRANT_HOST", "qdrant-container")
qdrant_port = int(os.getenv("QDRANT_PORT", "6333"))
collection_name = os.getenv("QDRANT_COLLECTION", "rag_pdf")

qdrant_client = QdrantClient(host=qdrant_host, port=qdrant_port)

# ==== AUTO CREATE QDRANT COLLECTION IF NOT EXISTS ====
def ensure_collection_exists():
    collections = qdrant_client.get_collections().collections
    exists = any(c.name == collection_name for c in collections)
    if not exists:
        print(f"[!] Collection '{collection_name}' chưa tồn tại. Đang tạo mới...")
        # Chỉnh dimension đúng với model embedding!
        qdrant_client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE),
        )
        print(f"[✓] Đã tạo collection '{collection_name}'.")
    else:
        print(f"[✓] Collection '{collection_name}' đã tồn tại.")

# ==== Qdrant LangChain wrapper ====
vector_db = Qdrant(
    client=qdrant_client,
    collection_name=collection_name,
    embeddings=embedding_model,
)
retriever = vector_db.as_retriever(search_kwargs={"k": 3})

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

set_llm_cache(InMemoryCache())
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
llm_chain = template | llm | StrOutputParser()

db = SQLDatabase(engine=engine)

# ==== Helper: Split & add PDF với metadata ====
def split_and_add_pdf_to_qdrant(file_path, vector_db, embedding_model, filename):
    loader = PyPDFLoader(str(file_path))
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=50)
    chunks = splitter.split_documents(docs)
    for c in chunks:
        c.metadata = {"filename": filename}
    vector_db.add_documents(chunks)
    return len(chunks)

def batch_import_pdfs_to_qdrant(pdf_data_path, vector_db, embedding_model):
    loader = DirectoryLoader(pdf_data_path, glob="*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()
    if not documents:
        print(f"[!] No PDF found in {pdf_data_path}")
        return 0
    splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=50)
    chunks = splitter.split_documents(documents)
    for c in chunks:
        c.metadata = {"filename": c.metadata.get("source", "unknown")}
    vector_db.add_documents(chunks)
    print(f"[✓] Imported {len(chunks)} chunks from folder '{pdf_data_path}'.")
    return len(chunks)

@app.on_event("startup")
def startup_event():
    create_db_and_tables()
    ensure_collection_exists()
    # batch_import_pdfs_to_qdrant(base_dir / "vectordb" / "data", vector_db, embedding_model)

# ==== UPLOAD PDF ====
@app.post("/documents")
async def upload_document(session_db: SessionDeps, file: UploadFile = File(...)):
    ensure_collection_exists()  # Bổ sung đảm bảo collection luôn tồn tại trước khi upload
    data_dir = base_dir / "vectordb" / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    file_path = data_dir / file.filename
    with open(file_path, "wb") as f:
        f.write(await file.read())
    chunks_added = split_and_add_pdf_to_qdrant(file_path, vector_db, embedding_model, file.filename)
    session_db.add(
        Document(
            filename=file.filename,
            file_path=str(file_path),
            vector_path=collection_name,
        )
    )
    session_db.commit()
    return {"filename": file.filename, "chunks_added": chunks_added}

# ==== IMPORT ALL PDF FOLDER (BATCH) ====
@app.post("/import_folder")
def import_folder(session_db: SessionDeps):
    ensure_collection_exists()
    data_dir = base_dir / "vectordb" / "data"
    chunks_added = batch_import_pdfs_to_qdrant(data_dir, vector_db, embedding_model)
    return {"folder": str(data_dir), "chunks_added": chunks_added}

# ==== DELETE 1 FILE PDF + VECTOR ====

@app.delete("/documents/{filename}")
def delete_pdf_and_vectors(filename: str, session_db: SessionDeps):
    ensure_collection_exists()
    filter_condition = Filter(
        must=[
            FieldCondition(
                key="filename",
                match=MatchValue(value=filename)
            )
        ]
    )
    # Scroll lấy id
    hits, _ = vector_db.client.scroll(
        collection_name=collection_name,
        scroll_filter=filter_condition,
        limit=1000  # Nếu file lớn thì cần lặp hoặc tăng limit
    )
    point_ids = [point.id for point in hits]
    if point_ids:
        vector_db.client.delete(
            collection_name=collection_name,
            points_selector=point_ids,
            wait=True
        )
    # Xóa file vật lý và metadata như cũ
    data_dir = base_dir / "vectordb" / "data"
    file_path = data_dir / filename
    if file_path.exists():
        os.remove(file_path)
    doc = session_db.query(Document).filter(Document.filename == filename).first()
    if doc:
        session_db.delete(doc)
        session_db.commit()
    return {"message": f"Deleted {filename} from PDF folder and Qdrant."}

# ==== RESET VECTOR DB + XÓA HẾT PDF ====
@app.delete("/reset_vectordb")
def reset_vectordb(session_db: SessionDeps):
    try:
        vector_db.client.delete_collection(collection_name=collection_name)
    except Exception:
        pass
    data_dir = base_dir / "vectordb" / "data"
    for file in data_dir.glob("*.pdf"):
        file.unlink()
    session_db.query(Document).delete()
    session_db.commit()
    ensure_collection_exists()  # Tạo lại collection sau khi reset
    return {"message": "Vector DB & PDF files reset (deleted) successfully."}

# ==== UPDATE (REPLACE) PDF + VECTOR ====
@app.put("/documents/{filename}")
async def update_pdf_and_vectors(filename: str, session_db: SessionDeps, file: UploadFile = File(...)):
    delete_pdf_and_vectors(filename, session_db)
    ensure_collection_exists()
    data_dir = base_dir / "vectordb" / "data"
    file_path = data_dir / file.filename
    with open(file_path, "wb") as f:
        f.write(await file.read())
    chunks_added = split_and_add_pdf_to_qdrant(file_path, vector_db, embedding_model, file.filename)
    session_db.add(
        Document(
            filename=file.filename,
            file_path=str(file_path),
            vector_path=collection_name,
        )
    )
    session_db.commit()
    return {"filename": file.filename, "chunks_added": chunks_added}

# ==== CHAT ENDPOINT ====
@app.post("/prompt")
def prompt(chat_request: ChatRequest, session_db: SessionDeps) -> dict:
    if llm is None:
        return {"error": "LLM not initialized."}
    ensure_collection_exists()
    try:
        docs = retriever.invoke(chat_request.prompt)
        if not docs:
            return {"error": "Chưa có dữ liệu nào trong hệ thống! Vui lòng upload file PDF trước khi hỏi."}
        context_vector = "\n".join([doc.page_content for doc in docs])
        context_db = f"Bạn là một trợ lý chatbot. Bạn hãy trả lời câu hỏi dựa vào ngữ cảnh mà tôi cung cấp.\n{db.get_table_info(db.get_usable_table_names())}"
        result = llm_chain.invoke({
            "context": chat_request.context or context_vector,
            "context_db": context_db,
            "question": chat_request.prompt
        })
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

@app.get("/")
def read_root():
    return {"message": "Hello world!"}
