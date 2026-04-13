# API 参考

CryptoHub 提供两个后端 API：**Go API**（主网关）和 **Python API**（AI 与量化引擎）。两者通过 gRPC 内部通信，对外提供 REST/HTTP 接口。

## 基础地址

| 服务 | 地址 | 前缀 |
|------|------|------|
| Go API | `http://localhost:8080` | `/api/v1` |
| Python API | `http://localhost:8000` | `/api/v1` |

---

## Python API 端点

### 健康检查

```
GET /health
```

响应：
```json
{ "status": "healthy", "service": "CryptoHub Python Backend" }
```

### AI 分析

#### 流式 AI 分析（SSE）

```
POST /api/v1/ai/analyze
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `symbol` | string | 交易品种（如 `BTC/USDT`） |
| `analysis_type` | string | `comprehensive`、`technical`、`fundamental` |
| `timeframe` | string | `1D`、`4H`、`1H` 等 |

#### 获取分析结果

```
GET /api/v1/ai/analyze/{analysis_id}
```

#### 快速多因子分析

```
POST /api/v1/ai/fast-analyze
```

### 回测

#### 运行回测

```
POST /api/v1/backtest/run
```

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `strategy_id` | string | 必填 | 策略标识符 |
| `symbol` | string | 必填 | 交易对 |
| `timeframe` | string | `1H` | K线时间周期 |
| `start_date` | string | 必填 | ISO 日期 |
| `end_date` | string | 必填 | ISO 日期 |
| `initial_capital` | number | `10000` | 初始资金 |

#### 获取回测结果

```
GET /api/v1/backtest/{backtest_id}
```

#### 获取回测报告

```
GET /api/v1/backtest/{backtest_id}/report
```

### 策略引擎

#### 编译策略

```
POST /api/v1/strategy/compile
```

#### 启动策略

```
POST /api/v1/strategy/start
```

#### 停止策略

```
POST /api/v1/strategy/stop/{strategy_id}
```

### 指标

#### 计算指标

```
POST /api/v1/indicator/calculate
```

#### 列出可用指标

```
GET /api/v1/indicator/list
```

### 代码生成

```
POST /api/v1/codegen/generate
```

### Polymarket

```
GET /api/v1/polymarket/markets
```

## 认证

受保护的端点需要在 `Authorization` 请求头中携带 Bearer 令牌：

```
Authorization: Bearer <jwt_token>
```

## 错误响应

```json
{
  "code": 400,
  "message": "验证失败",
  "detail": "字段 'symbol' 为必填项"
}
```
