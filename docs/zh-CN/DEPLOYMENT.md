# 部署指南

本文档介绍如何使用 Docker、Kubernetes 和 CI/CD 流水线将 CryptoHub 部署到生产环境。

## Docker Compose（单服务器）

适用于中小规模工作负载的最简部署方式。

```bash
# 构建并启动所有服务
docker compose up -d --build

# 查看状态
docker compose ps

# 查看日志
docker compose logs -f backend-python
```

### 生产环境覆盖配置

创建 `docker-compose.prod.yml`：

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

运行：

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## 容器镜像仓库

`docker-build.yml` GitHub Actions 工作流会在每次推送到 `main` 分支或创建标签时，自动构建并推送镜像到 GitHub Container Registry（ghcr.io）。

镜像：

- `ghcr.io/<owner>/cryptohub/frontend`
- `ghcr.io/<owner>/cryptohub/backend-go`
- `ghcr.io/<owner>/cryptohub/backend-python`

## 环境变量

完整列表参见 [SETUP.md](./SETUP.md)。生产环境务必设置：

| 变量 | 说明 |
|------|------|
| `SECRET_KEY` | 强随机字符串（≥ 32 字符） |
| `OPENAI_API_KEY` | OpenAI API 密钥 |
| `DATABASE_URL` | 生产 PostgreSQL 连接字符串 |
| `REDIS_URL` | 生产 Redis 连接字符串 |

## 数据库迁移

启动 Python 后端前运行 Alembic 迁移：

```bash
cd backend/python
alembic upgrade head
```

或在容器内执行：

```bash
docker compose exec backend-python alembic upgrade head
```

## 反向代理（Nginx）

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

## CI/CD 流水线

提供三个 GitHub Actions 工作流：

| 工作流 | 文件 | 触发条件 |
|--------|------|----------|
| CI | `ci.yml` | 推送到 `main`/`develop`，PR 到 `main` |
| Docker 构建 | `docker-build.yml` | 推送到 `main`，标签 |
| 文档部署 | `docs-deploy.yml` | `docs/` 目录变更 |

## 扩容

- **水平扩展** — 在负载均衡器后面运行多个 Go 和 Python 后端实例。
- **Celery Worker** — 通过增加 `backend-python-worker` 服务副本独立扩展。
- **数据库** — 使用 PostgreSQL 读副本处理高读取负载。
- **Redis** — 使用 Redis 集群实现高可用缓存。
