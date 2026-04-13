# 설치 가이드

CryptoHub의 로컬 개발 환경 및 프로덕션 배포 설정 절차를 안내합니다.

## 사전 요구 사항

| 도구 | 버전 | 용도 |
|------|------|------|
| Docker & Docker Compose | 24+ / v2+ | 컨테이너 오케스트레이션 |
| Node.js | 22 LTS | 프론트엔드 빌드 |
| pnpm | 10+ | 프론트엔드 패키지 매니저 |
| Go | 1.24+ | Go 백엔드 |
| Python | 3.12+ | Python 백엔드 |
| PostgreSQL | 17 | 데이터베이스 |
| Redis | 7 | 캐시 & 메시지 브로커 |

## 1 · 저장소 클론

```bash
git clone https://github.com/louqiang1982/CryptoHub.git
cd CryptoHub
cp .env.example .env
```

`.env` 파일을 편집하여 최소한 다음을 설정합니다:

```dotenv
OPENAI_API_KEY=sk-...
SECRET_KEY=<랜덤 문자열>
```

## 2 · Docker로 실행 (권장)

```bash
docker compose up -d
```

## 3 · 개별 서비스 실행

### 프론트엔드

```bash
cd frontend
pnpm install
pnpm dev
```

### Go 백엔드

```bash
cd backend/go
go mod download
go run cmd/server/main.go
```

### Python 백엔드

```bash
cd backend/python
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Celery 워커

```bash
cd backend/python
celery -A app.workers.celery_app worker --loglevel=info
```

## 4 · 데이터베이스 마이그레이션

```bash
cd backend/python
alembic upgrade head
```

## 5 · 테스트 실행

```bash
# 프론트엔드
cd frontend && pnpm lint && pnpm build

# Go
cd backend/go && go test ./... -v

# Python
cd backend/python && ruff check app/ && pytest tests/ -v
```

## 6 · 환경 변수 참조

| 변수 | 기본값 | 설명 |
|------|--------|------|
| `DATABASE_URL` | `postgresql+asyncpg://...` | 비동기 PostgreSQL 연결 문자열 |
| `REDIS_URL` | `redis://localhost:6379/0` | Redis 연결 문자열 |
| `CELERY_BROKER_URL` | `redis://localhost:6379/1` | Celery 브로커 |
| `OPENAI_API_KEY` | (비어 있음) | OpenAI API 키 |
| `SECRET_KEY` | `change-me-in-production` | JWT 서명 키 |
| `GRPC_PORT` | `50051` | Python gRPC 서버 포트 |
