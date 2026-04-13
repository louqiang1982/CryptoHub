# Deployment Guide

This document covers deploying CryptoHub to production environments using Docker, Kubernetes, and CI/CD pipelines.

## Docker Compose (Single Server)

The simplest deployment method for small-to-medium workloads.

```bash
# Build and start all services
docker compose up -d --build

# Check status
docker compose ps

# View logs
docker compose logs -f backend-python
```

### Production Overrides

Create a `docker-compose.prod.yml` with production-specific settings:

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
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - SECRET_KEY=${SECRET_KEY}
```

Run with:

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## Container Registry

The `docker-build.yml` GitHub Actions workflow automatically builds and pushes images to GitHub Container Registry (ghcr.io) on every push to `main` or tagged release.

Images:

- `ghcr.io/<owner>/cryptohub/frontend`
- `ghcr.io/<owner>/cryptohub/backend-go`
- `ghcr.io/<owner>/cryptohub/backend-python`

## Environment Variables

See [SETUP.md](./SETUP.md) for the full list. In production, always set:

| Variable | Notes |
|----------|-------|
| `SECRET_KEY` | Strong random string (≥ 32 characters) |
| `OPENAI_API_KEY` | Your OpenAI API key |
| `DATABASE_URL` | Production PostgreSQL connection string |
| `REDIS_URL` | Production Redis connection string |

## Database Migrations

Run Alembic migrations before starting the Python backend:

```bash
cd backend/python
alembic upgrade head
```

Or inside a container:

```bash
docker compose exec backend-python alembic upgrade head
```

## Reverse Proxy (Nginx)

Example Nginx configuration:

```nginx
upstream frontend {
    server localhost:3000;
}

upstream go_api {
    server localhost:8080;
}

server {
    listen 80;
    server_name cryptohub.example.com;

    location / {
        proxy_pass http://frontend;
        proxy_set_header Host $host;
    }

    location /api/ {
        proxy_pass http://go_api;
        proxy_set_header Host $host;
    }

    location /ws/ {
        proxy_pass http://go_api;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

## CI/CD Pipelines

Three GitHub Actions workflows are provided:

| Workflow | File | Trigger |
|----------|------|---------|
| CI | `ci.yml` | Push to `main`/`develop`, PRs to `main` |
| Docker Build | `docker-build.yml` | Push to `main`, tags |
| Docs Deploy | `docs-deploy.yml` | Changes to `docs/` |

### CI Pipeline Steps

1. **Frontend** — `pnpm install` → `pnpm lint` → `pnpm build`
2. **Go Backend** — `go mod download` → `go vet` → `go build` → `go test`
3. **Python Backend** — `pip install` → `ruff check` → `pytest`
4. **Docker** — `docker compose build` (after all three pass)

## Monitoring

Recommended monitoring stack:

- **Prometheus** — Metrics collection
- **Grafana** — Dashboards and alerting
- **Sentry** — Error tracking for all three services

## Scaling

- **Horizontal** — Run multiple instances of Go and Python backends behind a load balancer.
- **Celery Workers** — Scale independently by increasing replicas of the `backend-python-worker` service.
- **Database** — Use PostgreSQL read replicas for read-heavy workloads.
- **Redis** — Use Redis Cluster for high-availability caching.
