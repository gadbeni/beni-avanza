FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    default-mysql-client \
    libmariadb3 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Crear usuario no root por seguridad
RUN useradd --create-home --shell /bin/bash appuser
USER appuser

EXPOSE 8000

# CAMBIA ESTO: Usar Gunicorn en lugar de runserver
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "reportbump.wsgi:application"]