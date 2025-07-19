# 📘 ragPdfTool

Dự án này sử dụng kiến trúc microservice gồm **backend (FastAPI)** và **frontend (React)**. Docker được sử dụng để đóng gói và triển khai dễ dàng.
---
## Hướng dẫn chạy dự án.
- cài đặt sẵn docker vs docker compose.
- clone dự án trên github về.
- cd vào thư mục song song với docker-compose.yml
- sudo docker compose up

---

---
## [Building Full Stack Applications With Python and ReactJS](https://www.youtube.com/watch?v=Jx39roFmTNg)
```text
- sử dụng docker để connect giữa frontend và backend
```

---

## ReactJS Frontend

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
### [langchain milvus](https://python.langchain.com/docs/integrations/vectorstores/milvus/) vs docker milvus
```text
- Langchain milvus: xu ly cac tac vu client
- docker milvus: server cua milvus duoc trien khai bang docker
```

---

## 📦 Tài nguyên bổ trợ
#### [Milvus docker](https://milvus.io/docs/install_standalone-docker.md#Install-Milvus-standalone-using-Docker-Compose)
* https://github.com/milvus-io/milvus/releases/download/v2.5.14/milvus-standalone-docker-compose.yml

#### [langchain milvus](https://python.langchain.com/docs/integrations/vectorstores/milvus/)

#### [Explore Attu, an open-source GUI tool for intuitive Milvus management.](https://milvus.io/docs/install_standalone-docker-compose.md#:~:text=Explore%20Attu%2C%20an%20open%2Dsource%20GUI%20tool%20for%20intuitive%20Milvus%20management.)
* https://github.com/zilliztech/attu

#### [How-to guides with Langchain](https://python.langchain.com/docs/how_to/)

#### [ollama](https://ollama.readthedocs.io/en/api/)

---

## 🤖 Mô hình tải từ Hugging Face

* [`vinallama-7b-chat_q5_0.gguf`](https://huggingface.co/duyv/ChatBot-GGUF-VietNam/blob/main/vinallama-7b-chat_q5_0.gguf)
* [`all-MiniLM-L6-v2-f16.gguf`](https://huggingface.co/caliex/all-MiniLM-L6-v2-f16.gguf)

---