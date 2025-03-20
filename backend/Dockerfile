# Sử dụng Python 3.9 làm base image
FROM python:3.9-slim

# Thiết lập biến môi trường
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Cài đặt các gói phụ thuộc
RUN pip install --upgrade pip
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Sao chép mã nguồn vào container
COPY . /app/

# Mở cổng để truy cập ứng dụng
EXPOSE 8000

# Chạy migrations và khởi động server
CMD ["sh", "-c", "cd backend && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]