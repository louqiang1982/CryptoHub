# 배포 가이드

Docker와 CI/CD 파이프라인을 사용한 CryptoHub 프로덕션 환경 배포 방법을 안내합니다.

## Docker Compose (단일 서버)

```bash
docker compose up -d --build
docker compose ps
docker compose logs -f backend-python
```

### 프로덕션 환경 오버라이드

`docker-compose.prod.yml` 생성:

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

## 컨테이너 레지스트리

`docker-build.yml` 워크플로우가 `main` 브랜치로의 푸시나 태그 생성 시 자동으로 이미지를 빌드하고 GitHub Container Registry(ghcr.io)에 푸시합니다.

## 환경 변수

| 변수 | 설명 |
|------|------|
| `SECRET_KEY` | 강력한 랜덤 문자열 (32자 이상) |
| `OPENAI_API_KEY` | OpenAI API 키 |
| `DATABASE_URL` | 프로덕션 PostgreSQL 연결 문자열 |
| `REDIS_URL` | 프로덕션 Redis 연결 문자열 |

## 데이터베이스 마이그레이션

```bash
docker compose exec backend-python alembic upgrade head
```

## 리버스 프록시 (Nginx)

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

## CI/CD 파이프라인

| 워크플로우 | 파일 | 트리거 |
|-----------|------|--------|
| CI | `ci.yml` | `main`/`develop` 푸시, PR |
| Docker 빌드 | `docker-build.yml` | `main` 푸시, 태그 |
| 문서 배포 | `docs-deploy.yml` | `docs/` 변경 |

## 스케일링

- 수평 확장: 로드 밸런서 뒤에 다중 인스턴스 배치
- Celery 워커: 레플리카 수 독립 조정
- 데이터베이스: PostgreSQL 읽기 복제본
- Redis: Redis 클러스터
