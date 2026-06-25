FROM python:3.12-slim

# Evitar que Python genere archivos .pyc para no ensuciar el contenedor
ENV PYTHONDONTWRITEBYTECODE=1
# Forzar salida de logs sin buffer para ver errores en docker logs al instante
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .
