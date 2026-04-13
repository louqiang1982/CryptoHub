# Руководство по установке

В этом документе описывается настройка локальной среды разработки и продакшн-развёртывание CryptoHub.

## Предварительные требования

| Инструмент | Версия | Назначение |
|------------|--------|-----------|
| Docker & Docker Compose | 24+ / v2+ | Оркестрация контейнеров |
| Node.js | 22 LTS | Сборка фронтенда |
| pnpm | 10+ | Менеджер пакетов фронтенда |
| Go | 1.24+ | Go бэкенд |
| Python | 3.12+ | Python бэкенд |
| PostgreSQL | 17 | База данных |
| Redis | 7 | Кэш и брокер сообщений |

## 1 · Клонирование репозитория

```bash
git clone https://github.com/louqiang1982/CryptoHub.git
cd CryptoHub
cp .env.example .env
```

Отредактируйте `.env` и укажите как минимум:

```dotenv
OPENAI_API_KEY=sk-...
SECRET_KEY=<случайная строка>
```

## 2 · Запуск через Docker (рекомендуется)

```bash
docker compose up -d
```

## 3 · Запуск сервисов по отдельности

### Фронтенд

```bash
cd frontend
pnpm install
pnpm dev
```

### Go бэкенд

```bash
cd backend-go
go mod download
go run cmd/server/main.go
```

### Python бэкенд

```bash
cd backend-python
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Celery воркер

```bash
cd backend-python
celery -A app.workers.celery_app worker --loglevel=info
```

## 4 · Миграции базы данных

```bash
cd backend-python
alembic upgrade head
```

## 5 · Запуск тестов

```bash
# Фронтенд
cd frontend && pnpm lint && pnpm build

# Go
cd backend-go && go test ./... -v

# Python
cd backend-python && ruff check app/ && pytest tests/ -v
```

## 6 · Справочник переменных окружения

| Переменная | Значение по умолчанию | Описание |
|------------|----------------------|----------|
| `DATABASE_URL` | `postgresql+asyncpg://...` | Асинхронная строка подключения PostgreSQL |
| `REDIS_URL` | `redis://localhost:6379/0` | Строка подключения Redis |
| `CELERY_BROKER_URL` | `redis://localhost:6379/1` | Брокер Celery |
| `OPENAI_API_KEY` | (пусто) | API-ключ OpenAI |
| `SECRET_KEY` | `change-me-in-production` | Ключ подписи JWT |
| `GRPC_PORT` | `50051` | Порт gRPC-сервера Python |
