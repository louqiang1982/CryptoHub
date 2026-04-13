# 部署指南

本文件介紹如何使用 Docker 和 CI/CD 管線將 CryptoHub 部署到生產環境。

## Docker Compose（單一伺服器）

```bash
docker compose up -d --build
docker compose ps
docker compose logs -f backend-python
```

### 生產環境覆寫

建立 `docker-compose.prod.yml`：

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

## 容器映像檔倉庫

`docker-build.yml` 工作流程會自動建置並推送映像檔到 GitHub Container Registry（ghcr.io）。

## 環境變數

| 變數 | 說明 |
|------|------|
| `SECRET_KEY` | 強隨機字串（≥ 32 字元） |
| `OPENAI_API_KEY` | OpenAI API 金鑰 |
| `DATABASE_URL` | 生產 PostgreSQL 連線字串 |
| `REDIS_URL` | 生產 Redis 連線字串 |

## 資料庫遷移

```bash
docker compose exec backend-python alembic upgrade head
```

## 反向代理（Nginx）

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

## CI/CD 管線

| 工作流程 | 檔案 | 觸發條件 |
|----------|------|----------|
| CI | `ci.yml` | 推送到 `main`/`develop`、PR |
| Docker 建置 | `docker-build.yml` | 推送到 `main`、標籤 |
| 文件部署 | `docs-deploy.yml` | `docs/` 變更 |

## 擴容

- 水平擴展：負載均衡器後方多實例
- Celery Worker：獨立增加副本
- 資料庫：PostgreSQL 讀取副本
- Redis：Redis 叢集
