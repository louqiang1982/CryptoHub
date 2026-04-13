# Architecture

This document describes the high-level architecture of CryptoHub, including service responsibilities, data flow, and technology choices.

## System Overview

CryptoHub follows a **microservices architecture** with three main services communicating through gRPC and REST, backed by PostgreSQL for persistence and Redis for caching and task brokering.

```
                        ┌────────────────────────────────┐
                        │        Load Balancer           │
                        └───────────┬────────────────────┘
                                    │
                 ┌──────────────────┼──────────────────┐
                 │                  │                   │
        ┌────────▼───────┐ ┌───────▼────────┐ ┌────────▼───────┐
        │   Frontend     │ │  Go Backend    │ │ Python Backend │
        │  (Next.js 15)  │ │  (Gin + WS)   │ │  (FastAPI)     │
        └────────────────┘ └───────┬────────┘ └────────┬───────┘
                                   │  gRPC             │
                                   └──────────┬────────┘
                                              │
                            ┌─────────────────┼─────────────────┐
                            │                 │                 │
                     ┌──────▼──────┐  ┌───────▼──────┐ ┌───────▼──────┐
                     │ PostgreSQL  │  │    Redis     │ │Celery Workers│
                     │   (v17)     │  │    (v7)      │ │              │
                     └─────────────┘  └──────────────┘ └──────────────┘
```

## Service Responsibilities

### Frontend (Next.js 15 + React 19)

- Server-side rendering with App Router
- Internationalisation via `next-intl` (8 languages)
- Theme switching (light / dark / system) via `next-themes`
- Professional charting with KLineCharts and ECharts
- Responsive layout for mobile, tablet, desktop, and large screens

### Go Backend

- **API Gateway** — REST endpoints for user management, authentication, and general CRUD
- **WebSocket Server** — Real-time price streaming and order updates
- **gRPC Client** — Calls the Python backend for AI analysis and strategy execution

### Python Backend (FastAPI)

- **AI Analysis** — LLM-powered analysis using LangChain and OpenAI, with reflection loops and ensemble consensus
- **Strategy Engine** — Compile, validate, and run user-written Python strategies in a sandboxed environment
- **Backtest Engine** — Simulate strategies on historical data with full metrics (Sharpe, Sortino, max drawdown, profit factor)
- **Data Providers** — Fetch market data from crypto exchanges (ccxt), stock markets (Yahoo Finance), and forex
- **gRPC Server** — Exposes services to the Go backend

### Celery Workers

Background tasks managed by Celery with Redis as broker:

| Worker | Purpose |
|--------|---------|
| `pending_orders` | Process pending limit/stop orders |
| `portfolio_monitor` | Check risk limits and generate alerts |
| `market_data_collector` | Periodically fetch and cache market data |
| `reflection_worker` | Run AI reflection loops asynchronously |
| `polymarket_worker` | Refresh prediction market data |

## Data Flow

### AI Analysis Flow

```
User Request → Go API → gRPC → Python FastAPI
                                     │
                              ┌──────▼──────┐
                              │ LLM Service │  (streaming SSE)
                              └──────┬──────┘
                                     │
                              ┌──────▼──────┐
                              │  Reflection │  (async via Celery)
                              │   Worker    │
                              └─────────────┘
```

### Backtest Flow

```
Strategy Code + Config → BacktestEngine.run()
                              │
                    ┌─────────▼─────────┐
                    │  Simulate trades  │
                    │  on historical    │
                    │  bar data         │
                    └─────────┬─────────┘
                              │
                    ┌─────────▼─────────┐
                    │ Calculate metrics │  (Sharpe, Sortino, etc.)
                    └─────────┬─────────┘
                              │
                    ┌─────────▼─────────┐
                    │ Generate report   │
                    └───────────────────┘
```

## Database Schema

Managed via Alembic migrations. Key tables:

| Table | Description |
|-------|-------------|
| `strategies` | User-defined trading strategies |
| `backtest_results` | Backtest run results with metrics |
| `indicators` | Custom and marketplace indicators |
| `ai_analyses` | AI analysis records |

## Security

- JWT authentication (HS256) managed by the Go backend
- Strategy code sandboxing with forbidden import detection
- CORS middleware on both backends
- Environment-based secret management
