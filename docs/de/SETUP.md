# Installationsanleitung

Diese Anleitung beschreibt die Einrichtung der lokalen Entwicklungsumgebung und das Produktions-Deployment von CryptoHub.

## Voraussetzungen

| Werkzeug | Version | Zweck |
|----------|---------|-------|
| Docker & Docker Compose | 24+ / v2+ | Container-Orchestrierung |
| Node.js | 22 LTS | Frontend-Build |
| pnpm | 10+ | Frontend-Paketmanager |
| Go | 1.24+ | Go-Backend |
| Python | 3.12+ | Python-Backend |
| PostgreSQL | 17 | Datenbank |
| Redis | 7 | Cache & Nachrichtenbroker |

## 1 · Repository klonen

```bash
git clone https://github.com/louqiang1982/CryptoHub.git
cd CryptoHub
cp .env.example .env
```

Bearbeite `.env` und setze mindestens:

```dotenv
OPENAI_API_KEY=sk-...
SECRET_KEY=<zufällige Zeichenfolge>
```

## 2 · Mit Docker starten (empfohlen)

```bash
docker compose up -d
```

## 3 · Dienste einzeln starten

### Frontend

```bash
cd frontend
pnpm install
pnpm dev
```

### Go-Backend

```bash
cd backend-go
go mod download
go run cmd/server/main.go
```

### Python-Backend

```bash
cd backend-python
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Celery Worker

```bash
cd backend-python
celery -A app.workers.celery_app worker --loglevel=info
```

## 4 · Datenbank-Migrationen

```bash
cd backend-python
alembic upgrade head
```

## 5 · Tests ausführen

```bash
# Frontend
cd frontend && pnpm lint && pnpm build

# Go
cd backend-go && go test ./... -v

# Python
cd backend-python && ruff check app/ && pytest tests/ -v
```

## 6 · Umgebungsvariablen-Referenz

| Variable | Standard | Beschreibung |
|----------|----------|-------------|
| `DATABASE_URL` | `postgresql+asyncpg://...` | Asynchrone PostgreSQL-Verbindungszeichenfolge |
| `REDIS_URL` | `redis://localhost:6379/0` | Redis-Verbindungszeichenfolge |
| `CELERY_BROKER_URL` | `redis://localhost:6379/1` | Celery-Broker |
| `OPENAI_API_KEY` | (leer) | OpenAI-API-Schlüssel |
| `SECRET_KEY` | `change-me-in-production` | JWT-Signaturschlüssel |
| `GRPC_PORT` | `50051` | Python-gRPC-Serverport |
