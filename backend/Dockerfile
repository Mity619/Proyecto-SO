FROM python:3.11-slim

WORKDIR /app

# Copiamos primero requirements para aprovechar la caché de capas
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5000

# 1 worker para que prometheus_client funcione correctamente
CMD ["gunicorn", "--bind", "0.0.0.0:5000", \
     "--worker-class", "gthread", \
     "--workers", "1", \
     "--threads", "8", \
     "--access-logfile", "-", \
     "app:app"]