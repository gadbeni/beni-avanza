# Usa una imagen base oficial de Python
FROM python:3.11-slim

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    default-mysql-client \
    libmariadb3 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar requirements primero (para cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código de la aplicación
COPY . .

# Configurar variables de entorno para static files
ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=reportbump.settings

# Verificar la configuración
RUN echo "Verificando configuración Django:" && \
    python -c "from django.conf import settings; print('DEBUG:', settings.DEBUG); print('STATIC_URL:', settings.STATIC_URL); print('STATIC_ROOT:', settings.STATIC_ROOT)"

# Recopilar archivos estáticos
RUN python manage.py collectstatic --noinput

# Verificar que los archivos se copiaron (CORREGIDO)
RUN ls -la /app/static/ && \
    ls -la /app/static/reportbump/images/ || true

# Crear usuario no root por seguridad
RUN useradd --create-home --shell /bin/bash appuser && \
    chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

# Usar Gunicorn para ejecutar la aplicación
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "reportbump.wsgi:application"]