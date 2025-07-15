./bin/ollama serve &         # 1. Chạy Ollama server ở chế độ nền
pid=$!                       # 2. Lưu lại PID của server
sleep 5                      # 3. Chờ 5 giây để server khởi động xong
echo "Pulling qwen2.5-coder model"
ollama pull qwen2.5-coder:0.5b  # 4. Tải model qwen2.5-coder:0.5b về local
wait $pid                    # 5. Giữ script chạy cho đến khi server tắt
