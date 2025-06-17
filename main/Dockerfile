# Dựa trên Python 3
FROM python:3.10-slim

# Work directory in Image
WORKDIR /app

# Copy the codes into container
COPY . .

# install libraries
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# run the app with gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:create_app()"]
