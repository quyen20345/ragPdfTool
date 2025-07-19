FROM python:3.10-slim

# Cài curl bằng apt
RUN apt-get update && apt-get install -y curl && apt-get clean

WORKDIR /api

COPY ./requirements.txt /api/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /api/requirements.txt

COPY . /api

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
