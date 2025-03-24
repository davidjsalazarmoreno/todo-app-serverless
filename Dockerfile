FROM python:3.12-bookworm

WORKDIR /app

ENV PYTHONPATH=/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["chalice", "local", "--host", "0.0.0.0", "--port", "8000"]
