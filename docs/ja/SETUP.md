# セットアップガイド

CryptoHub のローカル開発環境と本番デプロイのセットアップ手順を説明します。

## 前提条件

| ツール | バージョン | 用途 |
|--------|-----------|------|
| Docker & Docker Compose | 24+ / v2+ | コンテナオーケストレーション |
| Node.js | 22 LTS | フロントエンドビルド |
| pnpm | 10+ | フロントエンドパッケージマネージャー |
| Go | 1.24+ | Go バックエンド |
| Python | 3.12+ | Python バックエンド |
| PostgreSQL | 17 | データベース |
| Redis | 7 | キャッシュ & メッセージブローカー |

## 1 · リポジトリのクローン

```bash
git clone https://github.com/louqiang1982/CryptoHub.git
cd CryptoHub
cp .env.example .env
```

`.env` を編集し、少なくとも以下を設定：

```dotenv
OPENAI_API_KEY=sk-...
SECRET_KEY=<ランダム文字列>
```

## 2 · Docker で実行（推奨）

```bash
docker compose up -d
```

## 3 · 個別サービスの実行

### フロントエンド

```bash
cd frontend
pnpm install
pnpm dev
```

### Go バックエンド

```bash
cd backend/go
go mod download
go run cmd/server/main.go
```

### Python バックエンド

```bash
cd backend/python
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Celery ワーカー

```bash
cd backend/python
celery -A app.workers.celery_app worker --loglevel=info
```

## 4 · データベースマイグレーション

```bash
cd backend/python
alembic upgrade head
```

## 5 · テストの実行

```bash
# フロントエンド
cd frontend && pnpm lint && pnpm build

# Go
cd backend/go && go test ./... -v

# Python
cd backend/python && ruff check app/ && pytest tests/ -v
```

## 6 · 環境変数リファレンス

| 変数 | デフォルト | 説明 |
|------|-----------|------|
| `DATABASE_URL` | `postgresql+asyncpg://...` | 非同期 PostgreSQL 接続文字列 |
| `REDIS_URL` | `redis://localhost:6379/0` | Redis 接続文字列 |
| `CELERY_BROKER_URL` | `redis://localhost:6379/1` | Celery ブローカー |
| `OPENAI_API_KEY` | （空） | OpenAI API キー |
| `SECRET_KEY` | `change-me-in-production` | JWT 署名キー |
| `GRPC_PORT` | `50051` | Python gRPC サーバーポート |
