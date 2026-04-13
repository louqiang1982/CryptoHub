# 安裝指南

本文件介紹如何建立 CryptoHub 的本機開發環境和生產部署。

## 前置條件

| 工具 | 版本 | 用途 |
|------|------|------|
| Docker & Docker Compose | 24+ / v2+ | 容器編排 |
| Node.js | 22 LTS | 前端建置 |
| pnpm | 10+ | 前端套件管理員 |
| Go | 1.24+ | Go 後端 |
| Python | 3.12+ | Python 後端 |
| PostgreSQL | 17 | 資料庫 |
| Redis | 7 | 快取與訊息佇列 |

## 1 · 複製儲存庫

```bash
git clone https://github.com/louqiang1982/CryptoHub.git
cd CryptoHub
cp .env.example .env
```

編輯 `.env` 檔案，至少設定：

```dotenv
OPENAI_API_KEY=sk-...
SECRET_KEY=<隨機字串>
```

## 2 · 使用 Docker 執行（建議）

```bash
docker compose up -d
```

## 3 · 個別執行各服務

### 前端

```bash
cd frontend
pnpm install
pnpm dev
```

### Go 後端

```bash
cd backend/go
go mod download
go run cmd/server/main.go
```

### Python 後端

```bash
cd backend/python
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Celery Worker

```bash
cd backend/python
celery -A app.workers.celery_app worker --loglevel=info
```

## 4 · 資料庫遷移

```bash
cd backend/python
alembic upgrade head
```

## 5 · 執行測試

```bash
# 前端
cd frontend && pnpm lint && pnpm build

# Go
cd backend/go && go test ./... -v

# Python
cd backend/python && ruff check app/ && pytest tests/ -v
```

## 6 · 環境變數參考

| 變數 | 預設值 | 說明 |
|------|--------|------|
| `DATABASE_URL` | `postgresql+asyncpg://...` | 非同步 PostgreSQL 連線字串 |
| `REDIS_URL` | `redis://localhost:6379/0` | Redis 連線字串 |
| `CELERY_BROKER_URL` | `redis://localhost:6379/1` | Celery 訊息佇列 |
| `OPENAI_API_KEY` | （空） | OpenAI API 金鑰 |
| `SECRET_KEY` | `change-me-in-production` | JWT 簽署金鑰 |
| `GRPC_PORT` | `50051` | Python gRPC 伺服器連接埠 |
