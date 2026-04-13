# CryptoHub

专业的加密货币交易平台，集成 AI 智能分析、自动化交易策略和全方位投资组合管理。

## 概述

CryptoHub 将前沿人工智能与量化交易深度结合，为交易者提供竞争优势。平台支持加密货币、股票和外汇市场的实时分析，统一在一个界面中呈现。

### 核心功能

- **AI 智能分析** — 机器学习模型分析市场数据、生成交易信号，并提供带置信度评分的建议。
- **策略引擎** — 使用 Python 脚本引擎编写、编译、回测和部署交易策略，支持完整的事件驱动生命周期（`on_init` / `on_bar`）。
- **实时交易** — 通过 WebSocket 连接主流交易所，实现实时下单和组合跟踪。
- **回测引擎** — 在历史数据上模拟策略执行，包含佣金和滑点建模，查看夏普比率、索提诺比率、最大回撤等多项指标。
- **多市场数据** — 内置加密货币（ccxt/Binance）、股票（Yahoo Finance）和外汇数据提供者。
- **投资组合管理** — 监控风险、跟踪未实现盈亏，当回撤阈值被突破时发送告警。
- **预测市场** — 集成 Polymarket 数据，用于情绪感知分析。
- **国际化** — 完整 i18n 支持，涵盖英文、简体中文、繁体中文、日文、韩文、阿拉伯文、俄文和德文。

## 架构

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   前端           │    │   Go 后端         │    │  Python 后端     │
│   (Next.js 15)  │◄──►│   (API / WS)     │◄──►│   (AI / ML)     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │                        │
                       ┌──────┴──────┐          ┌──────┴──────┐
                       │ PostgreSQL  │          │   Redis     │
                       └─────────────┘          └─────────────┘
```

| 层 | 技术栈 | 用途 |
|---|--------|------|
| 前端 | Next.js 15、React 19、Ant Design 5、Tailwind CSS 4 | 用户界面、图表、国际化 |
| Go 后端 | Go 1.24、Gin、gRPC、WebSocket | 高性能 API 网关和实时推送 |
| Python 后端 | FastAPI、Celery、pandas、ccxt、LangChain | AI 分析、回测、策略执行 |
| 数据库 | PostgreSQL 17 | 策略、分析、交易持久化存储 |
| 缓存/消息队列 | Redis 7 | 会话缓存、Celery 任务队列、实时数据缓存 |

## 快速开始

```bash
git clone https://github.com/louqiang1982/CryptoHub.git
cd CryptoHub
cp .env.example .env   # 编辑并填入你的 API 密钥
docker compose up -d
```

| 服务 | 地址 |
|------|------|
| 前端 | http://localhost:3000 |
| Go API | http://localhost:8080 |
| Python API | http://localhost:8000 |

详细安装指南请参阅 [SETUP.md](./SETUP.md)。

## 文档

- [安装指南](./SETUP.md)
- [API 参考](./API.md)
- [架构说明](./ARCHITECTURE.md)
- [贡献指南](./CONTRIBUTING.md)
- [部署指南](./DEPLOYMENT.md)

## 许可证

MIT 许可证 — 详见 [LICENSE](../../LICENSE)。
