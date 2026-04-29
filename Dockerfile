FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# system dependencies (psycopg2 uchun kerak bo‘lishi mumkin)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# pip upgrade
RUN pip install --upgrade pip

# requirements
COPY requirements.txt .

RUN pip install -r requirements.txt

# project copy
COPY . .

# port
EXPOSE 8000

# entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]