# 架構說明

本文件描述 CryptoHub 的高層架構，包括服務職責、資料流和技術選型。

## 系統概覽

CryptoHub 採用**微服務架構**，三個主要服務透過 gRPC 和 REST 通訊，由 PostgreSQL 提供持久化儲存，Redis 負責快取和工作排程。

```
        ┌────────────────┐  ┌───────────────┐  ┌────────────────┐
        │     前端        │  │   Go 後端      │  │  Python 後端    │
        │  (Next.js 15)  │  │  (Gin + WS)   │  │  (FastAPI)     │
        └───────┬────────┘  └──────┬────────┘  └──────┬─────────┘
                │                  │  gRPC            │
                │                  └────────┬─────────┘
                │                           │
           ┌────▼─────┐  ┌────────▼────┐  ┌─▼────────────┐
           │PostgreSQL │  │   Redis     │  │Celery Workers│
           └──────────┘  └─────────────┘  └──────────────┘
```

## 服務職責

### 前端（Next.js 15 + React 19）

- App Router 伺服器端渲染
- `next-intl` 國際化（8 種語言）
- `next-themes` 主題切換（亮色 / 暗色 / 跟隨系統）
- KLineCharts 和 ECharts 專業圖表
- 響應式佈局（手機、平板、桌面、大螢幕）

### Go 後端

- API 閘道、使用者管理、JWT 驗證
- WebSocket 即時推送
- gRPC 客戶端呼叫 Python 後端

### Python 後端（FastAPI）

- AI 分析（LangChain + OpenAI）、反思迴圈、集成共識
- 策略引擎（編譯、驗證、沙箱執行）
- 回測引擎（夏普、索提諾、最大回撤、獲利因子）
- 資料提供者（加密貨幣、股票、外匯）
- gRPC 伺服器

### Celery Workers

| 工人 | 用途 |
|------|------|
| `pending_orders` | 處理掛單 |
| `portfolio_monitor` | 風險監控與警示 |
| `market_data_collector` | 定期抓取市場數據 |
| `reflection_worker` | 非同步 AI 反思 |
| `polymarket_worker` | 更新預測市場資料 |

## 資料庫結構

透過 Alembic 遷移管理。主要表格：

| 表格 | 說明 |
|------|------|
| `strategies` | 使用者定義的交易策略 |
| `backtest_results` | 回測結果與指標 |
| `indicators` | 自訂和市場指標 |
| `ai_analyses` | AI 分析紀錄 |

## 安全性

- JWT 驗證（HS256）
- 策略程式碼沙箱化
- CORS 中介軟體
- 環境變數金鑰管理
