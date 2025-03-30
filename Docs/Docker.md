### build image
docker build -t backend . 
### run container
docker run -p 8000:8000 backend