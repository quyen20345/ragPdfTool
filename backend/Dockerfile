FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive

# 1. Cài đặt các tiện ích cần thiết
RUN apt-get update && apt-get install -y \
    curl git wget unzip nano vim libgl1 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# 2. Thư mục làm việc
WORKDIR /home/backend

# 3. Copy file requirements và cài đặt thư viện Python
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# 4. Copy toàn bộ mã nguồn vào container
COPY . .

# 5. Biến môi trường hỗ trợ log rõ ràng
ENV PYTHONUNBUFFERED=1 \
    UVICORN_CMD="uvicorn main:app --host 0.0.0.0 --port 8000 --reload"

# 6. Khởi chạy FastAPI server
CMD ["sh", "-c", "$UVICORN_CMD"]
