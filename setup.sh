#!/bin/bash

# Setup script for RAG PDF System

echo "🔧 Setting up RAG PDF System..."

# Check requirements
# 1) Docker must be installed
# 2) Docker Compose plugin or standalone must be available

echo "🔍 Checking requirements..."

# Ensure docker is present
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Ensure docker-compose (binary) or docker compose (plugin) is present
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install the Docker Compose plugin or standalone."
    exit 1
fi

# Create necessary directories

echo "📁 Creating directories..."
mkdir -p backend/vectordb/data
mkdir -p backend/alembic/versions

# Set permissions for start/stop scripts
chmod +x start.sh
chmod +x stop.sh

# Initialize Alembic migrations directory if missing

echo "🗄️ Initializing database migration..."
cd backend
if [ ! -d "alembic" ]; then
    alembic init alembic
fi
cd ..

echo "✅ Setup completed successfully!"
echo ""
echo "🚀 To start the system, run:"
echo "   docker compose up -d"
