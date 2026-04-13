# API Reference

CryptoHub exposes two backend APIs: a **Go API** (primary gateway) and a **Python API** (AI & quantitative engine). Both communicate internally via gRPC and are accessible through REST/HTTP.

## Base URLs

| Service | URL | Prefix |
|---------|-----|--------|
| Go API | `http://localhost:8080` | `/api/v1` |
| Python API | `http://localhost:8000` | `/api/v1` |

---

## Python API Endpoints

### Health Check

```
GET /health
```

Response:

```json
{ "status": "healthy", "service": "CryptoHub Python Backend" }
```

---

### AI Analysis

#### Stream AI Analysis (SSE)

```
POST /api/v1/ai/analyze
```

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Trading symbol (e.g. `BTC/USDT`) |
| `analysis_type` | string | `comprehensive`, `technical`, `fundamental` |
| `timeframe` | string | `1D`, `4H`, `1H`, etc. |

Returns a `text/event-stream` with chunks:

```
data: {"chunk": "Based on current market conditions..."}
data: {"status": "complete"}
```

#### Get Analysis Result

```
GET /api/v1/ai/analyze/{analysis_id}
```

#### Fast Multi-Factor Analysis

```
POST /api/v1/ai/fast-analyze
```

---

### Backtest

#### Run Backtest

```
POST /api/v1/backtest/run
```

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `strategy_id` | string | required | Strategy identifier |
| `symbol` | string | required | Trading pair |
| `timeframe` | string | `1H` | Candle timeframe |
| `start_date` | string | required | ISO date |
| `end_date` | string | required | ISO date |
| `initial_capital` | number | `10000` | Starting capital |

#### Get Backtest Result

```
GET /api/v1/backtest/{backtest_id}
```

#### Get Backtest Report

```
GET /api/v1/backtest/{backtest_id}/report
```

Returns full performance report with equity curve, trade list, monthly returns, and drawdown series.

---

### Strategy Engine

#### Compile Strategy

```
POST /api/v1/strategy/compile
```

| Field | Type | Description |
|-------|------|-------------|
| `code` | string | Python strategy source code |
| `strategy_type` | string | `script` or `indicator` |

#### Start Strategy

```
POST /api/v1/strategy/start
```

#### Stop Strategy

```
POST /api/v1/strategy/stop/{strategy_id}
```

#### Get Strategy Status

```
GET /api/v1/strategy/{strategy_id}/status
```

---

### Indicators

#### Calculate Indicators

```
POST /api/v1/indicator/calculate
```

#### List Available Indicators

```
GET /api/v1/indicator/list
```

Returns: `SMA`, `EMA`, `RSI`, `MACD`, `BB`, and more.

---

### Code Generation

#### Generate Strategy Code

```
POST /api/v1/codegen/generate
```

| Field | Type | Description |
|-------|------|-------------|
| `description` | string | Natural language description |
| `strategy_type` | string | `technical`, `momentum`, etc. |
| `complexity` | string | `simple`, `medium`, `advanced` |

---

### Polymarket

#### List Prediction Markets

```
GET /api/v1/polymarket/markets
```

---

## Authentication

All protected endpoints require a Bearer token in the `Authorization` header:

```
Authorization: Bearer <jwt_token>
```

Tokens are issued by the Go backend's auth endpoints and verified using HS256.

## Error Responses

All errors follow a consistent format:

```json
{
  "code": 400,
  "message": "Validation failed",
  "detail": "Field 'symbol' is required"
}
```
