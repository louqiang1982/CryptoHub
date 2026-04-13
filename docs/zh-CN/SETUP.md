# 安装指南

本文档介绍如何搭建 CryptoHub 的本地开发环境和生产部署。

## 前置条件

| 工具 | 版本 | 用途 |
|------|------|------|
| Docker & Docker Compose | 24+ / v2+ | 容器编排 |
| Node.js | 22 LTS | 前端构建 |
| pnpm | 10+ | 前端包管理器 |
| Go | 1.24+ | Go 后端 |
| Python | 3.12+ | Python 后端 |
| PostgreSQL | 17 | 数据库（也可使用 Docker 服务） |
| Redis | 7 | 缓存与消息队列 |

## 1 · 克隆仓库

```bash
git clone https://github.com/louqiang1982/CryptoHub.git
cd CryptoHub
cp .env.example .env
```

编辑 `.env` 文件，至少设置以下内容：

```dotenv
OPENAI_API_KEY=sk-...        # AI 分析所需
SECRET_KEY=<随机字符串>        # JWT 签名使用
```

## 2 · 使用 Docker 运行（推荐）

```bash
docker compose up -d
```

将启动所有服务：前端、Go 后端、Python 后端、PostgreSQL 和 Redis。

## 3 · 单独运行各服务

### 前端

```bash
cd frontend
pnpm install
pnpm dev          # http://localhost:3000
```

### Go 后端

```bash
cd backend/go
go mod download
go run cmd/server/main.go    # http://localhost:8080
```

### Python 后端

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

## 4 · 数据库迁移

```bash
cd backend/python
alembic upgrade head
```

修改模型后创建新的迁移脚本：

```bash
alembic revision --autogenerate -m "描述变更"
```

## 5 · 运行测试

```bash
# 前端
cd frontend && pnpm lint && pnpm build

# Go
cd backend/go && go test ./... -v

# Python
cd backend/python
pip install ruff pytest pytest-asyncio
ruff check app/
pytest tests/ -v
```

## 6 · 环境变量参考

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `DATABASE_URL` | `postgresql+asyncpg://postgres:postgres@localhost:5432/cryptohub` | 异步 PostgreSQL 连接字符串 |
| `REDIS_URL` | `redis://localhost:6379/0` | Redis 连接字符串 |
| `CELERY_BROKER_URL` | `redis://localhost:6379/1` | Celery 消息队列 |
| `OPENAI_API_KEY` | （空） | OpenAI API 密钥 |
| `SECRET_KEY` | `change-me-in-production` | JWT 签名密钥 |
| `GRPC_PORT` | `50051` | Python gRPC 服务端口 |
