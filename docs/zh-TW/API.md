# API 參考

CryptoHub 提供兩個後端 API：**Go API**（主閘道）和 **Python API**（AI 與量化引擎）。

## 基礎位址

| 服務 | 位址 | 前綴 |
|------|------|------|
| Go API | `http://localhost:8080` | `/api/v1` |
| Python API | `http://localhost:8000` | `/api/v1` |

## Python API 端點

### 健康檢查

```
GET /health
```

### AI 分析

#### 串流 AI 分析（SSE）

```
POST /api/v1/ai/analyze
```

| 欄位 | 類型 | 說明 |
|------|------|------|
| `symbol` | string | 交易品種（如 `BTC/USDT`） |
| `analysis_type` | string | `comprehensive`、`technical`、`fundamental` |
| `timeframe` | string | `1D`、`4H`、`1H` 等 |

#### 取得分析結果

```
GET /api/v1/ai/analyze/{analysis_id}
```

#### 快速多因子分析

```
POST /api/v1/ai/fast-analyze
```

### 回測

#### 執行回測

```
POST /api/v1/backtest/run
```

| 欄位 | 類型 | 預設值 | 說明 |
|------|------|--------|------|
| `strategy_id` | string | 必填 | 策略識別碼 |
| `symbol` | string | 必填 | 交易對 |
| `timeframe` | string | `1H` | K線時間週期 |
| `start_date` | string | 必填 | ISO 日期 |
| `end_date` | string | 必填 | ISO 日期 |
| `initial_capital` | number | `10000` | 初始資金 |

#### 取得回測結果

```
GET /api/v1/backtest/{backtest_id}
```

#### 取得回測報告

```
GET /api/v1/backtest/{backtest_id}/report
```

### 策略引擎

```
POST /api/v1/strategy/compile
POST /api/v1/strategy/start
POST /api/v1/strategy/stop/{strategy_id}
GET  /api/v1/strategy/{strategy_id}/status
```

### 指標

```
POST /api/v1/indicator/calculate
GET  /api/v1/indicator/list
```

### 程式碼生成

```
POST /api/v1/codegen/generate
```

### Polymarket

```
GET /api/v1/polymarket/markets
```

## 驗證

受保護端點需在 `Authorization` 標頭攜帶 Bearer 權杖：

```
Authorization: Bearer <jwt_token>
```

## 錯誤回應

```json
{ "code": 400, "message": "驗證失敗", "detail": "欄位 'symbol' 為必填" }
```
