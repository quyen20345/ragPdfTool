# =====================================
# start.sh (create this file in root directory)
#!/bin/bash

# Start script for RAG PDF System

echo "🚀 Starting RAG PDF System..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cat > .env << EOL
# Database
POSTGRES_USER=raguser
POSTGRES_PASSWORD=ragpassword
POSTGRES_DB=ragdatabase
POSTGRES_HOST=postgres-container
POSTGRES_PORT=5432

# Ollama
OLLAMA_MODEL=llama2
OLLAMA_BASE_URL=http://ollama-server-container:11434

# Qdrant
QDRANT_HOST=qdrant-container
QDRANT_PORT=6333
QDRANT_COLLECTION=pdf_documents

# Embeddings
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
EOL
    echo "✅ .env file created"
fi

# Pull required Docker images
echo "📥 Pulling Docker images..."
docker compose pull

# Start services
echo "🐳 Starting Docker containers..."
docker compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 30

# Check if Ollama is ready and pull model
echo "🤖 Setting up Ollama model..."
docker exec ollama-server-container ollama pull llama2

# Show status
echo "📊 Checking service status..."
docker compose ps

echo ""
echo "🎉 RAG PDF System started successfully!"
echo ""
echo "📋 Access URLs:"
echo "   🌐 Frontend: http://localhost:3000"
echo "   🔗 Backend API: http://localhost:8000"
echo "   📊 API Documentation: http://localhost:8000/docs"
echo "   🗄️ Qdrant Dashboard: http://localhost:6333/dashboard"
echo ""
echo "📝 To stop the system, run:"
echo "   docker compose down"
echo ""
echo "🔧 To view logs, run:"
echo "   docker compose logs -f [service_name]"
