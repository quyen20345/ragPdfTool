## Dừng tiến trình đang chiếm cổng 8000
sudo lsof -i :8000
sudo kill -9 PID

## xet template cho frontend
echo settings.py
edit on TEMPLATES : 'DIRS': [
            "../frontend", 
        ],