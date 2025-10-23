FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Код и вспомогательные скрипты
COPY src/ /app/src/
COPY wait_for_db.sh /app/
COPY start_prod.sh /app/

# На случай CRLF — починим и дадим права
RUN sed -i 's/\r$//' /app/wait_for_db.sh /app/start_prod.sh && \
    chmod +x /app/wait_for_db.sh /app/start_prod.sh

WORKDIR /app/src
ENV PYTHONPATH=/app

# По умолчанию (dev) — runserver:
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
