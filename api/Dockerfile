FROM python:3.12-slim-bookworm

WORKDIR /api

COPY reqs.txt .

RUN pip install --no-cache-dir -r reqs.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]