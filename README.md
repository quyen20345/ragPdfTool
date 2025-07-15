# 📘 ragPdfTool

Dự án này sử dụng kiến trúc microservice gồm **backend (FastAPI)** và **frontend (React)**. Docker được sử dụng để đóng gói và triển khai dễ dàng.

---

## 🔧 Python Virtual Environment

```bash
python -m venv venv         # tao moi truong ao
source venv/bin/activate    # kich hoat moi truong ao
deactivate                  # thoat khoi moi truong ao
pip freeze > requirements.txt  # cap nhap requirements
```

---

## 🐳 Docker & Docker Compose

### ✅ Build và chạy Docker Compose:

```bash
sudo docker compose up --build       # Build và chạy toàn bộ services
sudo docker compose down             # Dừng và xóa container, network
```

```bash
# Mở container frontend trong shell để kiểm tra thực tế
sudo docker run -it --rm -v $(pwd)/frontend:/app -w /app node:20-alpine sh
npm install
npm start
sudo docker compose down --volumes
sudo docker compose up --build

```

> Nhấn `Ctrl + C` để dừng nếu đang chạy foreground.

### ✅ Một số lệnh Docker cơ bản:

```bash
docker exec -it ollama-server /bin/sh
sudo docker compose down -v # xoa toan bo network, volume, ...
sudo docker build . -t backend       # Build image cho backend
sudo docker rmi -f $(sudo docker images -aq) # xoa sach docker images 
sudo docker rm -f $(sudo docker ps -aq) # xoa sach docker containers
sudo docker volume prune -f # Xoá toàn bộ volume
sudo docker network prune -f # Xoá toàn bộ network custom
sudo docker run --name backend --rm -p 8000:8000 backend 
sudo docker compose up --build frontend  # Build lại frontend
sudo docker logs frontend
docker ps                            # Xem các container đang chạy
docker rm -f <container_id_or_name> # Xóa container đang chạy
docker rmi <image_id_or_name>       # Xóa image
```

---

## 🛠 Xử lý lỗi cổng (port)

```bash
sudo lsof -i :8000        # Kiểm tra tiến trình chiếm cổng
sudo kill -9 <PID>        # Dừng tiến trình chiếm cổng
```

---

## 🌐 ReactJS Frontend

### Cài đặt và chạy ứng dụng React:

```bash
sudo apt install npm
npx create-react-app frontend
cd frontend
npm start
npm i axios       # Cài axios để gọi API
```

> 🔗 [Getting Started with React](https://create-react-app.dev/docs/getting-started/)

---

## 📦 Tài nguyên bổ trợ

* 🔗 [How-to guides with Langchain](https://python.langchain.com/docs/how_to/)
* 🔗 [Bootstrap 3.3 Getting Started](https://getbootstrap.com/docs/3.3/getting-started/#download)
* 🔗 [Custom Login/Registration/Forgot Password Snippets](https://bootsnipp.com/snippets/X04B0)

---

## 🤖 Mô hình tải từ Hugging Face

* [`vinallama-7b-chat_q5_0.gguf`](https://huggingface.co/duyv/ChatBot-GGUF-VietNam/blob/main/vinallama-7b-chat_q5_0.gguf)
* [`all-MiniLM-L6-v2-f16.gguf`](https://huggingface.co/caliex/all-MiniLM-L6-v2-f16.gguf)

---