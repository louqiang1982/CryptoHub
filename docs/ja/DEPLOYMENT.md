# デプロイガイド

Docker と CI/CD パイプラインを使用した CryptoHub の本番環境へのデプロイ方法を説明します。

## Docker Compose（シングルサーバー）

```bash
docker compose up -d --build
docker compose ps
docker compose logs -f backend-python
```

### 本番環境用オーバーライド

`docker-compose.prod.yml` を作成：

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

## コンテナレジストリ

`docker-build.yml` ワークフローが `main` ブランチへのプッシュやタグ作成時に自動でイメージをビルドし、GitHub Container Registry（ghcr.io）にプッシュします。

## 環境変数

| 変数 | 説明 |
|------|------|
| `SECRET_KEY` | 強力なランダム文字列（32 文字以上） |
| `OPENAI_API_KEY` | OpenAI API キー |
| `DATABASE_URL` | 本番 PostgreSQL 接続文字列 |
| `REDIS_URL` | 本番 Redis 接続文字列 |

## データベースマイグレーション

```bash
docker compose exec backend-python alembic upgrade head
```

## リバースプロキシ（Nginx）

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

## CI/CD パイプライン

| ワークフロー | ファイル | トリガー |
|------------|---------|---------|
| CI | `ci.yml` | `main`/`develop` へのプッシュ、PR |
| Docker ビルド | `docker-build.yml` | `main` へのプッシュ、タグ |
| ドキュメントデプロイ | `docs-deploy.yml` | `docs/` の変更 |

## スケーリング

- 水平スケール：ロードバランサー背後に複数インスタンスを配置
- Celery ワーカー：レプリカ数を独立にスケール
- データベース：PostgreSQL リードレプリカ
- Redis：Redis クラスター
