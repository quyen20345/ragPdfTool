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
## [Type hints cheat sheet](https://mypy.readthedocs.io/en/latest/cheat_sheet_py3.html)
```python
# Variables
age: int = 22
salary: int 
...

# Useful built-in types
# collections
x: List[int] = [1]
x: Set[int] = {6,7}
x: Dict[str, float] = {"field": 3.0}
x: Tuple[int, str, float] = (3, "yes", 8.0)
x: Tuple[int, ...] = (1, 2, 3)

# Union vs Optional
Uinon[int, str] mean a variable maybe "int" or "str"
Optional[int] mean a variable maybe "int" or "None"
Optional[int] similar Union[int, None]

# Functions
def stringify(num: int) -> str:
   return str(num)

def show_name(name: str) -> None:
   print(f"my name is {name}")
```
---

## 🛠 Xử lý lỗi cổng (port)

```bash
sudo lsof -i :8000        # Kiểm tra tiến trình chiếm cổng
sudo kill -9 <PID>        # Dừng tiến trình chiếm cổng
```
---
## [Building Full Stack Applications With Python and ReactJS](https://www.youtube.com/watch?v=Jx39roFmTNg)
```text
- sử dụng docker để connect giữa frontend và backend
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
* 🔗 [ollama](https://ollama.readthedocs.io/en/api/)
---

## 🤖 Mô hình tải từ Hugging Face

* [`vinallama-7b-chat_q5_0.gguf`](https://huggingface.co/duyv/ChatBot-GGUF-VietNam/blob/main/vinallama-7b-chat_q5_0.gguf)
* [`all-MiniLM-L6-v2-f16.gguf`](https://huggingface.co/caliex/all-MiniLM-L6-v2-f16.gguf)

---