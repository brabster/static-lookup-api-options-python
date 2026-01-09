FROM python:3.12-slim

WORKDIR /app

COPY ./serve .

RUN pip install --no-cache-dir -r requirements.txt


COPY uncommitted/recommendations_dataset.compressed.dbm.db /app/data/recommendations_dataset.compressed.dbm.db

ENV DB_PATH="/app/data/recommendations_dataset.compressed.dbm"
ENV PORT=8080

CMD ["gunicorn", "--bind", ":8080", "--workers", "2", "--threads", "4", "app:app"]