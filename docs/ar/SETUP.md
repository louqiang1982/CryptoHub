# دليل الإعداد

يوضح هذا المستند كيفية إعداد بيئة التطوير المحلية والنشر الإنتاجي لـ CryptoHub.

## المتطلبات الأساسية

| الأداة | الإصدار | الغرض |
|--------|---------|-------|
| Docker & Docker Compose | 24+ / v2+ | تنسيق الحاويات |
| Node.js | 22 LTS | بناء الواجهة الأمامية |
| pnpm | 10+ | مدير حزم الواجهة الأمامية |
| Go | 1.24+ | خادم Go الخلفي |
| Python | 3.12+ | خادم Python الخلفي |
| PostgreSQL | 17 | قاعدة البيانات |
| Redis | 7 | التخزين المؤقت ووسيط الرسائل |

## 1 · استنساخ المستودع

```bash
git clone https://github.com/louqiang1982/CryptoHub.git
cd CryptoHub
cp .env.example .env
```

عدّل ملف `.env` واضبط على الأقل:

```dotenv
OPENAI_API_KEY=sk-...
SECRET_KEY=<سلسلة عشوائية>
```

## 2 · التشغيل باستخدام Docker (مُوصى)

```bash
docker compose up -d
```

## 3 · تشغيل الخدمات بشكل فردي

### الواجهة الأمامية

```bash
cd frontend
pnpm install
pnpm dev
```

### خادم Go الخلفي

```bash
cd backend/go
go mod download
go run cmd/server/main.go
```

### خادم Python الخلفي

```bash
cd backend/python
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### عامل Celery

```bash
cd backend/python
celery -A app.workers.celery_app worker --loglevel=info
```

## 4 · ترحيل قاعدة البيانات

```bash
cd backend/python
alembic upgrade head
```

## 5 · تشغيل الاختبارات

```bash
# الواجهة الأمامية
cd frontend && pnpm lint && pnpm build

# Go
cd backend/go && go test ./... -v

# Python
cd backend/python && ruff check app/ && pytest tests/ -v
```

## 6 · مرجع المتغيرات البيئية

| المتغير | القيمة الافتراضية | الوصف |
|---------|-------------------|-------|
| `DATABASE_URL` | `postgresql+asyncpg://...` | سلسلة اتصال PostgreSQL غير متزامنة |
| `REDIS_URL` | `redis://localhost:6379/0` | سلسلة اتصال Redis |
| `CELERY_BROKER_URL` | `redis://localhost:6379/1` | وسيط Celery |
| `OPENAI_API_KEY` | (فارغ) | مفتاح OpenAI API |
| `SECRET_KEY` | `change-me-in-production` | مفتاح توقيع JWT |
| `GRPC_PORT` | `50051` | منفذ خادم gRPC لـ Python |
