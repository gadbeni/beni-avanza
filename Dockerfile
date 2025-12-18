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

# Crear usuario no root por seguridad antes de que se ejecuten los siguientes comandos
RUN useradd --create-home --shell /bin/bash appuser

# Configurar variables de entorno para static files
ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=reportbump.settings

# Cambiar propietario de los archivos de la aplicación
RUN chown -R appuser:appuser /app

# Cambiar al usuario no root
USER appuser

# Recopilar archivos estáticos
RUN python manage.py collectstatic --noinput

EXPOSE 8000

# Usar Gunicorn para ejecutar la aplicación
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "reportbump.wsgi:application"]