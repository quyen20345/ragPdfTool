# RAG PDF System

Hệ thống hỏi đáp thông minh với tài liệu PDF sử dụng RAG (Retrieval-Augmented Generation).

## Tính năng

- 📄 **Quản lý tài liệu PDF**: Upload, xử lý và quản lý tài liệu PDF
- 💬 **Hỏi đáp thông minh**: Sử dụng RAG để trả lời câu hỏi dựa trên tài liệu
- 💾 **Lưu trữ lịch sử chat**: Quản lý các cuộc trò chuyện với PostgreSQL
- 🔍 **Vector Search**: Tìm kiếm ngữ nghĩa với Qdrant
- 🤖 **LLM tự host**: Sử dụng Ollama để chạy LLM cục bộ
- 🌐 **Giao diện thân thiện**: React frontend với Tailwind CSS

## Công nghệ sử dụng

### Backend
- **FastAPI**: Web framework
- **PostgreSQL**: Database chính
- **Qdrant**: Vector database
- **Ollama**: Local LLM server
- **LangChain**: RAG framework
- **SQLAlchemy**: ORM

### Frontend
- **React**: Frontend framework
- **Tailwind CSS**: UI styling
- **Axios**: HTTP client
- **React Router**: Navigation

## Cài đặt và chạy

### Yêu cầu hệ thống
- Docker & Docker Compose
- 8GB RAM trở lên (để chạy LLM)
- 10GB dung lượng trống

### Cài đặt nhanh

1. **Clone repository**
   ```bash
   git clone <repository-url>
   cd ragPdfTool
   ```

2. **Setup**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

3. **Khởi động hệ thống**
   ```bash
   ./start.sh
   ```

4. **Truy cập ứng dụng**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs
   - Qdrant Dashboard: http://localhost:6333/dashboard

### Sử dụng thủ công

1. **Tạo file .env**
   ```bash
   cp .env.example .env
   # Chỉnh sửa cấu hình nếu cần
   ```

2. **Khởi động services**
   ```bash
   docker-compose up -d
   ```

3. **Cài đặt Ollama model**
   ```bash
   docker exec ollama-server-container ollama pull llama2
   ```

## Cách sử dụng

### 1. Upload tài liệu
- Vào tab "Quản lý tài liệu"
- Click để chọn file PDF
- Đợi hệ thống xử lý tài liệu

### 2. Tạo cuộc trò chuyện
- Vào tab "Trò chuyện" 
- Click "Cuộc trò chuyện mới"
- Bắt đầu đặt câu hỏi về tài liệu

### 3. Giám sát hệ thống
- Vào tab "Trạng thái hệ thống"
- Xem trạng thái các service
- Theo dõi thống kê

## API Endpoints

### Documents
- `POST /api/documents/` - Upload PDF
- `GET /api/documents/` - List documents
- `GET /api/documents/{id}` - Get document
- `DELETE /api/documents/{id}` - Delete document

### Chat
- `POST /api/chat/sessions` - Create session
- `GET /api/chat/sessions` - List sessions
- `DELETE /api/chat/sessions/{id}` - Delete session
- `GET /api/chat/sessions/{id}/messages` - Get messages
- `POST /api/chat/query` - Send query

### System
- `GET /health` - Health check

## Cấu hình

### Environment Variables
```bash
# Database
POSTGRES_USER=raguser
POSTGRES_PASSWORD=ragpassword
POSTGRES_DB=ragdatabase

# Ollama
OLLAMA_MODEL=llama2
OLLAMA_BASE_URL=http://ollama-server-container:11434

# Qdrant
QDRANT_HOST=qdrant-container
QDRANT_PORT=6333

# Embeddings
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

### Thay đổi LLM Model
1. Vào container Ollama:
   ```bash
   docker exec -it ollama-server-container bash
   ```

2. Pull model mới:
   ```bash
   ollama pull <model-name>
   ```

3. Cập nhật .env:
   ```bash
   OLLAMA_MODEL=<model-name>
   ```

4. Restart backend:
   ```bash
   docker-compose restart backend
   ```

## Development

### Backend Development
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development
```bash
cd frontend
npm install
npm start
```

### Database Migration
```bash
cd backend
alembic revision --autogenerate -m "description"
alembic upgrade head
```

## Troubleshooting

### Lỗi thường gặp

1. **Container không start**
   ```bash
   # Kiểm tra logs
   docker-compose logs [service-name]
   
   # Restart service
   docker-compose restart [service-name]
   ```

2. **Ollama không respond**
   ```bash
   # Kiểm tra Ollama
   docker exec ollama-server-container ollama list
   
   # Pull lại model
   docker exec ollama-server-container ollama pull llama2
   ```

3. **Database connection error**
   ```bash
   # Kiểm tra PostgreSQL
   docker-compose logs postgres
   
   # Reset database
   docker-compose down -v
   docker-compose up -d
   ```

4. **Qdrant không kết nối được**
   ```bash
   # Kiểm tra Qdrant
   curl http://localhost:6333/health
   
   # Restart Qdrant
   docker-compose restart qdrant
   ```

### Performance Tuning

1. **Tăng memory cho container**
   ```yaml
   # Trong docker-compose.yaml
   services:
     ollama:
       deploy:
         resources:
           limits:
             memory: 4G
   ```

2. **Tối ưu chunk size**
   ```python
   # Trong backend/app/services/vector_service.py
   text_splitter = RecursiveCharacterTextSplitter(
       chunk_size=500,  # Giảm để tăng độ chính xác
       chunk_overlap=100,
   )
   ```

3. **Điều chỉnh temperature**
   ```python
   # Temperature thấp hơn = câu trả lời ít sáng tạo hơn
   llm.temperature = 0.3
   ```

## Contributing

1. Fork repository
2. Tạo feature branch
3. Commit changes
4. Push to branch
5. Tạo Pull Request

## License

MIT License

## Support

Nếu gặp vấn đề, hãy tạo issue trên GitHub repository.

## Changelog

### v1.0.0
- Triển khai RAG system cơ bản
- Upload và quản lý PDF
- Chat interface với lưu trữ lịch sử
- Health monitoring
- Docker containerization

---

**Made with ❤️ using FastAPI, React, Ollama, Qdrant, and PostgreSQL**
