# 🐳 Docker & Docker Compose Cheat Sheet

## ✨ Build & Run Docker Container (Without Compose)

```bash
# Build image from Dockerfile
sudo docker build -t rag_tool .

# Run container from built image
sudo docker run -p 5000:5000 rag_tool

# Access running container
sudo docker exec -it <container_id_or_name> /bin/bash

# Stop running container
sudo docker stop <container_id>

# Remove stopped container
sudo docker rm <container_id>

# Remove image (careful!)
sudo docker rmi <image_name_or_id>

# List running containers
sudo docker ps

# List all containers (including stopped)
sudo docker ps -a

# List all images
sudo docker images

# Clean up unused data (containers, images, networks)
sudo docker system prune -a

```
##  Docker Compose Commands
### Manage Services
```bash

# Start all services in background
sudo docker compose up -d

# Start services and show logs
sudo docker compose up

# Stop running containers without removing them
sudo docker compose stop

# Stop and remove containers, networks, and volumes
sudo docker compose down
```
### 🔹 Build & Rebuild Images
```bash
# Build images from docker-compose.yml
sudo docker compose build

# Rebuild and start containers
sudo docker compose up --build -d
🔹 Check & Debug Containers

# Show container status
sudo docker compose ps

# View logs in real time
sudo docker compose logs -f

# Access container via service name
sudo docker compose exec <service_name> bash
```
### 🔹 Manage Volumes & Data
```bash
# List all volumes
sudo docker volume ls

# Remove specific volume
sudo docker volume rm <volume_name>
