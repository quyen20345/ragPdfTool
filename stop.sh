# =====================================
# stop.sh (create this file in root directory)
#!/bin/bash

echo "🛑 Stopping RAG PDF System..."

# Stop Docker containers
docker compose down

echo "✅ RAG PDF System stopped successfully!"
