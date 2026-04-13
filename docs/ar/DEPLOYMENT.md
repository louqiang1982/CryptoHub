# دليل النشر

يتناول هذا المستند نشر CryptoHub في بيئات الإنتاج باستخدام Docker وخطوط أنابيب CI/CD.

## Docker Compose (خادم واحد)

```bash
docker compose up -d --build
docker compose ps
docker compose logs -f backend-python
```

### تجاوزات بيئة الإنتاج

أنشئ `docker-compose.prod.yml`:

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

## سجل الحاويات

يقوم سير عمل `docker-build.yml` تلقائياً ببناء ودفع الصور إلى GitHub Container Registry (ghcr.io).

## المتغيرات البيئية

| المتغير | الوصف |
|---------|-------|
| `SECRET_KEY` | سلسلة عشوائية قوية (32 حرفاً على الأقل) |
| `OPENAI_API_KEY` | مفتاح OpenAI API |
| `DATABASE_URL` | سلسلة اتصال PostgreSQL للإنتاج |
| `REDIS_URL` | سلسلة اتصال Redis للإنتاج |

## ترحيل قاعدة البيانات

```bash
docker compose exec backend-python alembic upgrade head
```

## الوكيل العكسي (Nginx)

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

## خطوط أنابيب CI/CD

| سير العمل | الملف | المحفز |
|-----------|-------|--------|
| CI | `ci.yml` | دفع إلى `main`/`develop`، PR |
| بناء Docker | `docker-build.yml` | دفع إلى `main`، وسوم |
| نشر التوثيق | `docs-deploy.yml` | تغييرات في `docs/` |

## التوسع

- التوسع الأفقي: عدة نسخ خلف موازن الأحمال
- عمال Celery: توسيع عدد النسخ بشكل مستقل
- قاعدة البيانات: نسخ قراءة PostgreSQL
- Redis: عنقود Redis
