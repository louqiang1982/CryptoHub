# API リファレンス

CryptoHub は 2 つのバックエンド API を提供します：**Go API**（メインゲートウェイ）と **Python API**（AI・定量エンジン）。

## ベース URL

| サービス | URL | プレフィックス |
|---------|-----|--------------|
| Go API | `http://localhost:8080` | `/api/v1` |
| Python API | `http://localhost:8000` | `/api/v1` |

## Python API エンドポイント

### ヘルスチェック

```
GET /health
```

### AI 分析

#### ストリーミング AI 分析（SSE）

```
POST /api/v1/ai/analyze
```

| フィールド | 型 | 説明 |
|-----------|---|------|
| `symbol` | string | 取引銘柄（例：`BTC/USDT`） |
| `analysis_type` | string | `comprehensive`、`technical`、`fundamental` |
| `timeframe` | string | `1D`、`4H`、`1H` など |

#### 分析結果の取得

```
GET /api/v1/ai/analyze/{analysis_id}
```

#### 高速マルチファクター分析

```
POST /api/v1/ai/fast-analyze
```

### バックテスト

#### バックテスト実行

```
POST /api/v1/backtest/run
```

| フィールド | 型 | デフォルト | 説明 |
|-----------|---|-----------|------|
| `strategy_id` | string | 必須 | 戦略 ID |
| `symbol` | string | 必須 | 取引ペア |
| `timeframe` | string | `1H` | ローソク足の時間軸 |
| `start_date` | string | 必須 | ISO 日付 |
| `end_date` | string | 必須 | ISO 日付 |
| `initial_capital` | number | `10000` | 初期資金 |

#### 結果取得

```
GET /api/v1/backtest/{backtest_id}
```

#### レポート取得

```
GET /api/v1/backtest/{backtest_id}/report
```

### 戦略エンジン

```
POST /api/v1/strategy/compile
POST /api/v1/strategy/start
POST /api/v1/strategy/stop/{strategy_id}
GET  /api/v1/strategy/{strategy_id}/status
```

### インジケーター

```
POST /api/v1/indicator/calculate
GET  /api/v1/indicator/list
```

### コード生成

```
POST /api/v1/codegen/generate
```

### Polymarket

```
GET /api/v1/polymarket/markets
```

## 認証

保護されたエンドポイントには `Authorization` ヘッダーに Bearer トークンが必要です：

```
Authorization: Bearer <jwt_token>
```

## エラーレスポンス

```json
{ "code": 400, "message": "バリデーション失敗", "detail": "'symbol' フィールドは必須です" }
```
