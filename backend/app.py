import os
import time
import random
from flask import Flask, jsonify, Response, request
from prometheus_client import (
    Counter,
    Histogram,
    generate_latest,
    CONTENT_TYPE_LATEST,
)

app = Flask(__name__)

# Identificador de la instancia (se pasa por variable de entorno)
INSTANCE_ID = os.getenv("INSTANCE_ID", "unknown")

# ----- Métricas de Prometheus -----
REQUEST_COUNT = Counter(
    "backend_http_requests_total",
    "Total de peticiones HTTP recibidas por el backend",
    ["method", "endpoint", "status", "instance"],
)

REQUEST_LATENCY = Histogram(
    "backend_http_request_duration_seconds",
    "Latencia de las peticiones HTTP en segundos",
    ["endpoint", "instance"],
    buckets=(0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1.0, 2.5, 5.0),
)

# Evitamos instrumentar el propio endpoint /metrics para no contaminar las métricas
EXCLUDED_PATHS = {"/metrics"}


@app.before_request
def start_timer():
    request._start_time = time.time()


@app.after_request
def record_metrics(response):
    if request.path in EXCLUDED_PATHS:
        return response
    latency = time.time() - request._start_time
    REQUEST_LATENCY.labels(
        endpoint=request.path, instance=INSTANCE_ID
    ).observe(latency)
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.path,
        status=response.status_code,
        instance=INSTANCE_ID,
    ).inc()
    return response


# ----- Endpoints -----
@app.route("/")
def index():
    """Devuelve el número de instancia: sirve para demostrar el balanceo."""
    return jsonify({
        "instance": INSTANCE_ID,
        "message": f"Hello from backend instance {INSTANCE_ID}",
    })


@app.route("/work")
def work():
    """Simula trabajo con latencia variable: útil para las pruebas de carga."""
    delay = random.uniform(0.05, 0.4)
    time.sleep(delay)
    return jsonify({
        "instance": INSTANCE_ID,
        "status": "ok",
        "processing_time": round(delay, 3),
    })


@app.route("/health")
def health():
    return jsonify({"status": "ok", "instance": INSTANCE_ID})


@app.route("/metrics")
def metrics():
    """Endpoint que Prometheus va a scrapear."""
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    # Solo para pruebas locales: en Docker se ejecuta con gunicorn
    app.run(host="0.0.0.0", port=5000)