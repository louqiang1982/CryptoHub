# API 레퍼런스

CryptoHub은 두 개의 백엔드 API를 제공합니다: **Go API**(메인 게이트웨이)와 **Python API**(AI 및 퀀트 엔진).

## 기본 URL

| 서비스 | URL | 접두사 |
|--------|-----|--------|
| Go API | `http://localhost:8080` | `/api/v1` |
| Python API | `http://localhost:8000` | `/api/v1` |

## Python API 엔드포인트

### 헬스 체크

```
GET /health
```

### AI 분석

#### 스트리밍 AI 분석 (SSE)

```
POST /api/v1/ai/analyze
```

| 필드 | 타입 | 설명 |
|------|------|------|
| `symbol` | string | 거래 종목 (예: `BTC/USDT`) |
| `analysis_type` | string | `comprehensive`, `technical`, `fundamental` |
| `timeframe` | string | `1D`, `4H`, `1H` 등 |

#### 분석 결과 조회

```
GET /api/v1/ai/analyze/{analysis_id}
```

#### 빠른 멀티팩터 분석

```
POST /api/v1/ai/fast-analyze
```

### 백테스트

#### 백테스트 실행

```
POST /api/v1/backtest/run
```

| 필드 | 타입 | 기본값 | 설명 |
|------|------|--------|------|
| `strategy_id` | string | 필수 | 전략 식별자 |
| `symbol` | string | 필수 | 거래 쌍 |
| `timeframe` | string | `1H` | 캔들 타임프레임 |
| `start_date` | string | 필수 | ISO 날짜 |
| `end_date` | string | 필수 | ISO 날짜 |
| `initial_capital` | number | `10000` | 초기 자본 |

#### 결과 조회

```
GET /api/v1/backtest/{backtest_id}
```

#### 리포트 조회

```
GET /api/v1/backtest/{backtest_id}/report
```

### 전략 엔진

```
POST /api/v1/strategy/compile
POST /api/v1/strategy/start
POST /api/v1/strategy/stop/{strategy_id}
GET  /api/v1/strategy/{strategy_id}/status
```

### 인디케이터

```
POST /api/v1/indicator/calculate
GET  /api/v1/indicator/list
```

### 코드 생성

```
POST /api/v1/codegen/generate
```

### Polymarket

```
GET /api/v1/polymarket/markets
```

## 인증

보호된 엔드포인트는 `Authorization` 헤더에 Bearer 토큰이 필요합니다:

```
Authorization: Bearer <jwt_token>
```

## 에러 응답

```json
{ "code": 400, "message": "유효성 검사 실패", "detail": "'symbol' 필드는 필수입니다" }
```
