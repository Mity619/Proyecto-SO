# Proyecto Final — Infraestructura en Docker

## Requisitos
- Docker + Docker Compose
- (Opcional) k6 para pruebas de carga

## Levantar
docker compose up -d --build

## Accesos
- Nginx (proxy): http://localhost:8080
- Prometheus:    http://localhost:9090
- Grafana:       http://localhost:3000  (admin/admin)
- cAdvisor:      solo interno

## Verificar balanceo
for i in {1..9}; do curl -s http://localhost:8080/; echo; done
1..9 | ForEach-Object { curl.exe -s http://localhost:8080/ ; "" }

## Prueba de carga
k6 run load-test.js

## Detener
docker compose down