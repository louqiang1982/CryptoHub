# 📈 CryptoHub --- Crypto AI Trading Platform

🌐 **Multi-Language Documentation**: [English](./docs/en/) | [中文简体](./docs/zh-CN/) | [中文繁體](./docs/zh-TW/) | [日本語](./docs/ja/) | [한국어](./docs/ko/) | [العربية](./docs/ar/) | [Русский](./docs/ru/) | [Deutsch](./docs/de/)

![Go](https://img.shields.io/badge/Go-1.24-00ADD8?style=flat-square&logo=go) ![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python) ![TypeScript](https://img.shields.io/badge/TypeScript-Next.js-007ACC?style=flat-square&logo=typescript) ![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat-square&logo=docker)

## Overview

CryptoHub is a professional cryptocurrency trading platform featuring AI-powered analytics, automated trading strategies, and comprehensive portfolio management. Built with modern microservices architecture combining Go, Python, and TypeScript.

### 🚀 Key Features

- **Real-time Trading** - WebSocket connections to major exchanges
- **AI Analytics** - Machine learning powered market analysis
- **Strategy Engine** - Automated trading strategies with backtesting
- **Portfolio Management** - Multi-exchange portfolio tracking
- **Risk Management** - Advanced risk assessment and alerts
- **Social Trading** - Follow and copy successful traders

### 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Go Backend     │    │ Python Backend  │
│   (Next.js)     │◄───┤   (API/WS)       │◄───┤   (AI/ML)       │
│                 │    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         └───────────────────────▼───────────────────────┘
                            ┌──────────────┐
                            │  PostgreSQL  │
                            │    Redis     │
                            └──────────────┘
```

### 🚀 Quick Start

```bash
# Clone and setup
git clone https://github.com/louqiang1982/CryptoHub.git
cd CryptoHub
cp .env.example .env

# Run with Docker
docker compose up -d

# Access
# Frontend: http://localhost:3000
# Go API: http://localhost:8080
# Python API: http://localhost:8000
```

### 📖 Documentation

- [Setup Guide](./docs/en/SETUP.md)
- [API Reference](./docs/en/API.md)
- [Architecture](./docs/en/ARCHITECTURE.md)
- [Contributing](./docs/en/CONTRIBUTING.md)
- [Deployment](./docs/en/DEPLOYMENT.md)

## License

MIT License - see [LICENSE](LICENSE) for details.
Crypto AI Trading Platform
