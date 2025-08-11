#!/bin/bash

echo "🚀 Starting RAG PDF System..."

# Check Docker
if ! docker info > /dev/null 2>&1; then
  echo "❌ Docker is not running. Please start Docker first."
  exit 1
fi

# Create backend/.env if not exists
if [ ! -f ./backend/.env ]; then
  echo "📝 Creating ./backend/.env ..."
  cat > ./backend/.env << 'EOL'
# Database
POSTGRES_USER=raguser
POSTGRES_PASSWORD=ragpassword
POSTGRES_DB=ragdatabase
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

# Ollama
OLLAMA_MODEL=llama2
OLLAMA_BASE_URL=http://ollama:11434

# Qdrant
QDRANT_HOST=qdrant
QDRANT_PORT=6333
QDRANT_COLLECTION=pdf_documents

# Embeddings
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
EOL
  echo "✅ ./backend/.env created"
fi

# Create frontend/.env.development if not exists
if [ ! -f ./frontend/.env.development ]; then
  echo "📝 Creating ./frontend/.env.development ..."
  cat > ./frontend/.env.development << 'EOL'
REACT_APP_API_URL=http://backend:8000
EOL
  echo "✅ ./frontend/.env.development created"
fi

# Create frontend/.env.production if not exists
if [ ! -f ./frontend/.env.production ]; then
  echo "📝 Creating ./frontend/.env.production ..."
  cat > ./frontend/.env.production << 'EOL'
REACT_APP_API_URL=http://localhost:8000
EOL
  echo "✅ ./frontend/.env.production created"
fi

echo "📥 Pulling Docker images..."
docker compose pull

echo "🐳 Starting Docker containers..."
docker compose up -d

echo "⏳ Waiting for services to start..."
sleep 15

echo "🤖 Setting up Ollama model..."
# docker compose exec -T ollama ollama pull llama2
docker compose exec -T ollama ollama pull mrjacktung/phogpt-4b-chat-gguf

echo "📊 Checking service status..."
docker compose ps

echo ""
echo "🎉 RAG PDF System started successfully!"
echo "   🌐 Frontend: http://localhost:3000"
echo "   🔗 Backend API: http://localhost:8000"
echo "   📊 API Docs:   http://localhost:8000/docs"
echo "   🗄️ Qdrant UI:  http://localhost:6333/dashboard"
echo ""
echo "📝 To stop: docker compose down"
echo "🔧 Logs:   docker compose logs -f [service]"
