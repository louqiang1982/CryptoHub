# CryptoHub

A professional cryptocurrency trading platform featuring AI-powered analytics, automated trading strategies, and comprehensive portfolio management.

## Overview

CryptoHub combines cutting-edge artificial intelligence with quantitative trading to give traders a competitive edge. The platform supports real-time market analysis across cryptocurrency, stock, and forex markets—all from one unified interface.

### Key Features

- **AI-Powered Analytics** — Machine learning models analyze market data, generate trading signals, and provide confidence-scored recommendations.
- **Strategy Engine** — Write, compile, back-test, and deploy trading strategies using a Python-based scripting engine with a full event-driven lifecycle (`on_init` / `on_bar`).
- **Real-Time Trading** — Connect to major exchanges via WebSocket for live order execution and portfolio tracking.
- **Backtest Engine** — Simulate strategies on historical data with commission and slippage modelling, then review Sharpe ratio, Sortino ratio, maximum drawdown, and dozens of other metrics.
- **Multi-Market Data** — Built-in providers for crypto (ccxt/Binance), equities (Yahoo Finance), and forex.
- **Portfolio Management** — Monitor risk, track unrealised PnL, and receive alerts when drawdown thresholds are breached.
- **Prediction Markets** — Integrate Polymarket data for sentiment-aware analysis.
- **Internationalisation** — Full i18n with support for English, Simplified Chinese, Traditional Chinese, Japanese, Korean, Arabic, Russian, and German.

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Go Backend     │    │ Python Backend  │
│   (Next.js 15)  │◄──►│   (API / WS)     │◄──►│   (AI / ML)     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │                        │
                       ┌──────┴──────┐          ┌──────┴──────┐
                       │ PostgreSQL  │          │   Redis     │
                       └─────────────┘          └─────────────┘
```

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | Next.js 15, React 19, Ant Design 5, Tailwind CSS 4 | User interface, charts, i18n |
| Go Backend | Go 1.24, Gin, gRPC, WebSocket | High-performance API gateway and real-time streaming |
| Python Backend | FastAPI, Celery, pandas, ccxt, LangChain | AI analysis, backtesting, strategy execution |
| Database | PostgreSQL 17 | Persistent storage for strategies, analyses, trades |
| Cache / Broker | Redis 7 | Session cache, Celery task broker, real-time data cache |

## Quick Start

```bash
git clone https://github.com/louqiang1982/CryptoHub.git
cd CryptoHub
cp .env.example .env   # edit with your API keys
docker compose up -d
```

| Service | URL |
|---------|-----|
| Frontend | http://localhost:3000 |
| Go API | http://localhost:8080 |
| Python API | http://localhost:8000 |

See [SETUP.md](./SETUP.md) for detailed installation instructions.

## Documentation

- [Setup Guide](./SETUP.md)
- [API Reference](./API.md)
- [Architecture](./ARCHITECTURE.md)
- [Contributing](./CONTRIBUTING.md)
- [Deployment](./DEPLOYMENT.md)

## License

MIT License — see [LICENSE](../../LICENSE) for details.
