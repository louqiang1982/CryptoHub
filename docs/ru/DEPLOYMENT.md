# Руководство по развёртыванию

Развёртывание CryptoHub в продакшн-среде с использованием Docker и CI/CD-пайплайнов.

## Docker Compose (один сервер)

```bash
docker compose up -d --build
docker compose ps
docker compose logs -f backend-python
```

### Переопределения для продакшн

Создайте `docker-compose.prod.yml`:

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

## Реестр контейнеров

Рабочий процесс `docker-build.yml` автоматически собирает и публикует образы в GitHub Container Registry (ghcr.io).

## Переменные окружения

| Переменная | Описание |
|------------|----------|
| `SECRET_KEY` | Надёжная случайная строка (≥ 32 символа) |
| `OPENAI_API_KEY` | API-ключ OpenAI |
| `DATABASE_URL` | Строка подключения к продакшн PostgreSQL |
| `REDIS_URL` | Строка подключения к продакшн Redis |

## Миграции базы данных

```bash
docker compose exec backend-python alembic upgrade head
```

## Обратный прокси (Nginx)

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

## CI/CD-пайплайны

| Рабочий процесс | Файл | Триггер |
|-----------------|------|---------|
| CI | `ci.yml` | Push в `main`/`develop`, PR |
| Сборка Docker | `docker-build.yml` | Push в `main`, теги |
| Деплой документации | `docs-deploy.yml` | Изменения в `docs/` |

## Масштабирование

- Горизонтальное масштабирование: несколько инстансов за балансировщиком нагрузки
- Celery воркеры: независимое масштабирование реплик
- База данных: реплики чтения PostgreSQL
- Redis: кластер Redis
