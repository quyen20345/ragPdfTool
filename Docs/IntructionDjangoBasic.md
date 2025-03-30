# Hướng dẫn tạo webapp cơ bản với Django

Tài liệu này mô tả các bước cơ bản để tạo một ứng dụng web (webapp) sử dụng Django framework.

## Bước 1: Khởi tạo dự án Django

```bash
django-admin startproject config backend
cd backend
```

Lệnh này sẽ tạo một dự án Django với cấu trúc thư mục như sau:
- `backend/` - thư mục gốc chứa toàn bộ dự án
  - `config/` - chứa cấu hình dự án Django
  - `manage.py` - công cụ quản lý Django

## Bước 2: Tạo ứng dụng Django

```bash
python manage.py startapp app
```

Lệnh này tạo một ứng dụng Django mới với tên "app" trong dự án của bạn.

## Bước 3: Cấu hình ứng dụng

Mở file `config/settings.py` và thêm ứng dụng vào danh sách `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',  # Thêm ứng dụng của bạn vào đây
]
```

## Bước 4: Tạo mô hình dữ liệu (Models)

Chỉnh sửa file `app/models.py` để định nghĩa mô hình dữ liệu:

```python
from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
```

## Bước 5: Tạo views

Chỉnh sửa file `app/views.py`:

```python
from django.shortcuts import render
from .models import Item

def home(request):
    items = Item.objects.all()
    return render(request, 'home.html', {'items': items})
```

## Bước 6: Tạo URLs

Tạo file mới `app/urls.py`:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
]
```

Sau đó, kết nối URLs của ứng dụng với URLs chính trong `config/urls.py`:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
]
```

## Bước 7: Tạo templates

Tạo thư mục templates và file HTML:

```bash
mkdir -p app/templates
```

Tạo file `app/templates/home.html`:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Webapp Django Cơ Bản</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        .item {
            border: 1px solid #ddd;
            padding: 10px;
            margin-bottom: 10px;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <h1>Chào mừng đến với Webapp Django!</h1>
    
    <h2>Danh sách các mục:</h2>
    {% if items %}
        {% for item in items %}
            <div class="item">
                <h3>{{ item.name }}</h3>
                <p>{{ item.description }}</p>
                <small>Tạo lúc: {{ item.created_at }}</small>
            </div>
        {% endfor %}
    {% else %}
        <p>Chưa có mục nào.</p>
    {% endif %}
</body>
</html>
```

## Bước 8: Đăng ký model trong Admin

Chỉnh sửa file `app/admin.py`:

```python
from django.contrib import admin
from .models import Item

admin.site.register(Item)
```

## Bước 9: Tạo và áp dụng migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## Bước 10: Tạo tài khoản quản trị viên

```bash
python manage.py createsuperuser
```

Làm theo hướng dẫn để tạo tên người dùng, email và mật khẩu.

## Bước 11: Chạy server phát triển

```bash
python manage.py runserver
```

Sau khi chạy lệnh này, bạn có thể truy cập:
- http://127.0.0.1:8000/ - trang chủ của ứng dụng
- http://127.0.0.1:8000/admin/ - giao diện quản trị

## Cấu trúc thư mục hoàn chỉnh

```
backend/
├── app/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   ├── models.py
│   ├── templates/
│   │   └── home.html
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── config/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── manage.py
```

## Phát triển tiếp theo

Sau khi hoàn thành các bước cơ bản, bạn có thể tiếp tục phát triển bằng cách:
- Thêm CSS và JavaScript để cải thiện giao diện người dùng
- Tạo thêm các models, views và templates mới
- Thêm chức năng xác thực người dùng
- Tích hợp các thư viện Django bên thứ ba