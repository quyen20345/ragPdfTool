

import os
import json
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

# Tải biến môi trường từ .env (nếu có)
load_dotenv()

def crawl_single_page(url):
    """
    Crawl một trang web đơn (không đệ quy), trích xuất nội dung văn bản.
    """
    print(f"[+] Đang tải trang: {url}")
    loader = WebBaseLoader(url)
    docs = loader.load()
    print(f"[+] Số tài liệu tải được: {len(docs)}")

    # Chia nhỏ nội dung
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_documents(docs)
    print(f"[+] Số đoạn sau khi chia nhỏ: {len(chunks)}")

    return chunks

def save_to_json(documents, filename='output.json'):
    """
    Lưu kết quả crawl vào file JSON.
    """
    data = [{'page_content': doc.page_content, 'metadata': doc.metadata} for doc in documents]
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"[+] Đã lưu kết quả vào {filename}")

def main():
    # Thay đổi URL này nếu muốn crawl trang khác
    test_url = "https://flask.palletsprojects.com/en/stable/quickstart/#deploying-to-a-web-server"#"https://en.wikipedia.org/wiki/Artificial_intelligence"
    
    data = crawl_single_page(test_url)
    save_to_json(data, "output.json")

if __name__ == "__main__":
    main()

