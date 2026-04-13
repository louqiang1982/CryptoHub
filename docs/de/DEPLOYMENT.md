# Deployment-Anleitung

Deployment von CryptoHub in Produktionsumgebungen mit Docker und CI/CD-Pipelines.

## Docker Compose (einzelner Server)

```bash
docker compose up -d --build
docker compose ps
docker compose logs -f backend-python
```

### Produktionsüberschreibungen

Erstellen Sie `docker-compose.prod.yml`:

```yaml
services:
  frontend:
    environment:
      - NODE_ENV=production
  backend-go:
    environment:
      - GIN_MODE=release
      - JWT_SECRET=${JWT_SECRET}
  backend-python:
    environment:
      - DEBUG=false
      - SECRET_KEY=${SECRET_KEY}
```

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## Container-Registry

Der `docker-build.yml`-Workflow baut und pusht Images automatisch bei Pushes auf `main` oder Tags in die GitHub Container Registry (ghcr.io).

## Umgebungsvariablen

| Variable | Beschreibung |
|----------|-------------|
| `SECRET_KEY` | Starke zufällige Zeichenfolge (≥ 32 Zeichen) |
| `OPENAI_API_KEY` | OpenAI-API-Schlüssel |
| `DATABASE_URL` | PostgreSQL-Verbindungszeichenfolge für Produktion |
| `REDIS_URL` | Redis-Verbindungszeichenfolge für Produktion |

## Datenbank-Migrationen

```bash
docker compose exec backend-python alembic upgrade head
```

## Reverse Proxy (Nginx)

```nginx
server {
    listen 80;
    server_name cryptohub.example.com;

    location / {
        proxy_pass http://localhost:3000;
    }
    location /api/ {
        proxy_pass http://localhost:8080;
    }
    location /ws/ {
        proxy_pass http://localhost:8080;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

## CI/CD-Pipelines

| Workflow | Datei | Auslöser |
|----------|-------|----------|
| CI | `ci.yml` | Push auf `main`/`develop`, PR |
| Docker Build | `docker-build.yml` | Push auf `main`, Tags |
| Docs Deploy | `docs-deploy.yml` | Änderungen in `docs/` |

## Skalierung

- Horizontale Skalierung: Mehrere Instanzen hinter einem Load Balancer
- Celery Worker: Unabhängige Replikatskalierung
- Datenbank: PostgreSQL-Lesereplikate
- Redis: Redis Cluster
