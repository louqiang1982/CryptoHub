# Setup Guide

This document walks you through setting up CryptoHub for local development and production deployment.

## Prerequisites

| Tool | Version | Purpose |
|------|---------|---------|
| Docker & Docker Compose | 24+ / v2+ | Container orchestration |
| Node.js | 22 LTS | Frontend build |
| pnpm | 10+ | Frontend package manager |
| Go | 1.24+ | Go backend |
| Python | 3.12+ | Python backend |
| PostgreSQL | 17 | Database (or use the Docker service) |
| Redis | 7 | Cache & message broker |

## 1 · Clone the Repository

```bash
git clone https://github.com/louqiang1982/CryptoHub.git
cd CryptoHub
cp .env.example .env
```

Edit `.env` and set at minimum:

```dotenv
OPENAI_API_KEY=sk-...        # Required for AI analysis
SECRET_KEY=<random-string>   # Used for JWT signing
```

## 2 · Run with Docker (Recommended)

```bash
docker compose up -d
```

This starts all services: frontend, Go backend, Python backend, PostgreSQL, and Redis.

## 3 · Run Services Individually

### Frontend

```bash
cd frontend
pnpm install
pnpm dev          # http://localhost:3000
```

### Go Backend

```bash
cd backend/go
go mod download
go run cmd/server/main.go    # http://localhost:8080
```

### Python Backend

```bash
cd backend/python
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload   # http://localhost:8000
```

### Celery Worker

```bash
cd backend/python
celery -A app.workers.celery_app worker --loglevel=info
```

## 4 · Database Migrations

```bash
cd backend/python
alembic upgrade head
```

To create a new migration after model changes:

```bash
alembic revision --autogenerate -m "describe change"
```

## 5 · Running Tests

```bash
# Frontend
cd frontend && pnpm lint && pnpm build

# Go
cd backend/go && go test ./... -v

# Python
cd backend/python
pip install ruff pytest pytest-asyncio
ruff check app/
pytest tests/ -v
```

## 6 · Environment Variables Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `postgresql+asyncpg://postgres:postgres@localhost:5432/cryptohub` | Async PostgreSQL connection string |
| `REDIS_URL` | `redis://localhost:6379/0` | Redis connection string |
| `CELERY_BROKER_URL` | `redis://localhost:6379/1` | Celery broker |
| `OPENAI_API_KEY` | (empty) | OpenAI API key for AI features |
| `SECRET_KEY` | `change-me-in-production` | JWT signing secret |
| `GRPC_PORT` | `50051` | Python gRPC server port |
