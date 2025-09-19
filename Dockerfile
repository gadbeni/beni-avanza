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

# Copiar e instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código de la aplicación
COPY . .

# Recopilar archivos estáticos de Django
# Esto asume que tienes un directorio STATIC_ROOT configurado en settings.py
RUN python manage.py collectstatic --noinput

# Crear usuario no root por seguridad
RUN useradd --create-home --shell /bin/bash appuser
USER appuser

EXPOSE 8000

# Usar Gunicorn para ejecutar la aplicación
# Ahora gunicorn sabrá dónde encontrar los archivos estáticos
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "reportbump.wsgi:application"]