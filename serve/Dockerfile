FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY uncommitted/recommendations_dataset.compressed.dbm.db /app/data/recommendations_dataset.compressed.dbm.db

# Set the environment variable to point to the internal file
ENV DB_PATH="/app/data/recommendations_dataset.compressed.dbm"
ENV PORT=8080

# Use Gunicorn for production (Flask dev server is not safe for prod)
# Workers: 1 is often safer for legacy file-based DBs to avoid lock contention, 
# though read-only dbm usually handles concurrency fine.
CMD ["gunicorn", "--bind", ":8080", "--workers", "2", "--threads", "4", "app:app"]