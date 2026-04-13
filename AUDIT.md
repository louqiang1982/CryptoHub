# CryptoHub 主分支全量审计报告

> 审计时间：2026-04-13  
> 审计范围：`main` 分支当前提交内容  
> 参考文档：README.md、docs/、.github/workflows/、任务讨论设计方案

---

## 一、总体概况

| 层级 | 文件/模块数 | 已完成（有实质实现） | 仅骨架/Stub | 完全缺失 |
|------|------------|-------------------|------------|---------|
| 前端（Next.js） | ~42 文件 | 基础框架、i18n、主题、API请求层、WebSocket Hook、Polymarket页面、10个 shadcn/ui 组件 | 各页面（Mock数据/Placeholder图表）、认证页面（UI无session集成） | 图表组件库（lightweight-charts/klinecharts） |
| Go 后端 | ~64 文件 | Auth/User/Notification/Billing/Settings/Admin/Market(depth/ticker/kline)/Exchange(10个适配器)/Community/Credentials/Crypto加密/WebSocket/3个测试文件 | Portfolio(handler/service)、Risk(engine) | OAuth认证、gRPC客户端、Turnstile中间件 |
| Python 后端 | ~84 文件 | AI服务(含Web搜索)、Backtest、Strategy(含代码质量检查)、Data Providers(9个含A股/港股/期货/腾讯)、数据层基础设施(factory/cache/circuit_breaker/rate_limiter)、Workers、Alembic、Experiment(5子模块)、IBKR/MT5实盘、Polymarket研究、USDT支付、符号解析 | gRPC servicer（框架在，方法未实现） | Proto文件 |
| 基础设施 | ~12 文件 | docker-compose(8服务+healthcheck)、CI/CD(4个workflow含deploy)、Docker构建(3个Dockerfile)、Nginx反向代理、Makefile、文档部署 | — | — |
| 文档 | 48 文件 | 全部8语言×6份文档存在，根README链接正确 | 部分内容待细化 | — |

---

## 二、分层详细审计

### 2.1 前端（Frontend — Next.js/shadcn/ui）

#### ✅ 已完成

| 项目 | 文件/目录 | 说明 |
|------|----------|------|
| 项目基础配置 | `frontend/package.json`、`next.config.ts`、`tsconfig.json` | Next.js 15 + React 19 + TypeScript + Tailwind CSS + shadcn/ui + pnpm |
| 国际化框架（8语言） | `src/i18n/`、`src/middleware.ts` | next-intl，支持 en/zh-CN/zh-TW/ja/ko/ar/ru/de，全量翻译文件 |
| RTL 支持（阿拉伯语） | `src/app/[locale]/layout.tsx`、`src/i18n/config.ts` | `dir="rtl"` 动态切换，`isRtlLocale()` 工具函数，逻辑属性（`me-/ms-`） |
| 主题系统 | `src/components/providers/ThemeProvider.tsx`、`src/components/layout/ThemeCustomizer.tsx` | 暗/亮/自适应三种模式 + 8种预设色 + 自定义取色器（HSL转换） |
| 响应式布局 | `src/components/layout/Sidebar.tsx`、`TopBar.tsx`、`BottomTabBar.tsx` | 侧边栏折叠 + 顶栏语言/主题切换 + 移动端底部Tab栏 |
| 全部页面路由 | `src/app/[locale]/(main)/`（9个页面） | dashboard、ai-analysis、indicator、indicator-market、trading、portfolio、profile、membership、admin |
| 认证页面路由 | `src/app/[locale]/(auth)/login/`、`/register/` | 登录/注册界面框架存在（UI有表单和OAuth按钮） |
| API 请求层 | `src/lib/api/client.ts` | 封装了 auth/market/strategy/AI/polymarket 等后端 API 的类型化 fetch 请求 |
| WebSocket 客户端 Hook | `src/hooks/useWebSocket.ts` | 自定义 React Hook，支持自动重连、消息处理、状态追踪，连接 `NEXT_PUBLIC_WS_URL` |
| Polymarket 页面 | `src/app/[locale]/(main)/polymarket/page.tsx` | Polymarket 预测市场页面路由和布局文件 |
| shadcn/ui 组件 | `src/components/ui/` | Badge、Button、Card、Dialog、Input、Select、Skeleton、Table、Tabs、Tooltip（共10个组件） |
| i18n 翻译完整 | `src/i18n/messages/*.json` | 8语言均包含：common/nav/topbar/theme/dashboard/aiAnalysis/indicator/indicatorMarket/trading/portfolio/profile/membership/admin/auth/errors |

#### ❌ 未完成 / 缺失

| # | 项目 | 文件/目录 | 严重程度 | 说明 |
|---|------|----------|---------|------|
| F-1 | **图表组件全部为占位符** | `dashboard/page.tsx`、`ai-analysis/page.tsx`、`indicator/page.tsx` | 🔴 **阻断上线** | Dashboard的收益日历、策略分布饼图、回撤曲线、交易时段热力图均为 `"XXX Placeholder"` 字符串；AI分析的机会雷达图、K线图表均无实现，需集成 `lightweight-charts` 或 `klinecharts` |
| F-2 | **K线图表组件缺失** | `src/components/charts/`（不存在） | 🔴 **阻断上线** | `indicator/page.tsx` 中 "KLineChart Component Placeholder"，未引入 KLineCharts 库，无真实交互式蜡烛图 |
| F-3 | **认证 session 集成未实现** | `src/app/[locale]/(auth)/login/page.tsx` | 🔴 **阻断上线** | 登录/注册表单UI和OAuth按钮已存在，但无 `next-auth` session 管理、无 JWT token 集成、OAuth 按钮无实际跳转逻辑 |
| F-6 | **财经日历组件缺失** | `ai-analysis/page.tsx` | 🟡 **影响体验** | 设计方案中 AI 资产分析页包含财经日历，当前未实现 |
| F-7 | **闪电交易（Quick Trade）面板缺失** | `indicator/page.tsx` | 🟡 **影响体验** | 指标分析页面有 "Quick Trade" 按钮但无弹出面板实现 |
| F-10 | **移动端响应式未验证** | 全部页面 | 🟡 **影响体验** | 部分页面使用固定 `lg:grid-cols-4` 等，未系统性验证小屏幕布局；BottomTabBar 存在但各页面无移动优先适配 |
| F-11 | **用户中心页面（profile）为基础骨架** | `profile/page.tsx` | 🟡 **影响体验** | 仅包含静态展示，无 API 密钥管理表单、无通知偏好设置、无真实用户数据展示 |
| F-12 | **暗色模式硬编码 HSL 变量问题** | 全部页面 | 🟢 **优化项** | 大量使用 `text-[hsl(var(--muted-foreground))]` 内联写法，应使用 shadcn/ui 语义类（`text-muted-foreground`），存在与 Tailwind CSS 4 不兼容风险 |

---

### 2.2 Go 后端（backend/go — Gin/GORM/Redis）

#### ✅ 已完成

| 模块 | 目录/文件 | 说明 |
|------|----------|------|
| 认证服务 | `internal/auth/` | JWT 生成验证（handler/service/jwt/jwt_test.go），登录/注册/Token刷新路由 |
| 用户服务 | `internal/user/` | CRUD、角色、Repository 模式完整实现 |
| 仪表盘服务 | `internal/dashboard/` | 聚合数据 handler/service |
| 策略服务 | `internal/strategy/` | 策略 model/handler/service |
| 通知服务 | `internal/notification/` | 通知 handler/service（含邮件/Telegram/Discord接口结构） |
| 计费服务 | `internal/billing/` | 会员计划/积分 handler/service |
| 设置服务 | `internal/settings/` | 系统设置 handler/service |
| 管理后台 | `internal/admin/` | 用户管理/角色/系统日志 handler/service |
| 订单服务 | `internal/trading/order/` | 订单 model/handler/service（CreateOrder/ListOrders/GetOrder/CancelOrder/UpdateOrder/GetActiveOrders/GetOrderHistory） |
| 仓位服务 | `internal/trading/position/` | 仓位 model/handler/service |
| 组合模型 | `internal/trading/portfolio/` | Portfolio model + handler/service 骨架 |
| 交易所适配器（10个） | `internal/trading/exchange/` | 适配器接口（adapter.go）+ Binance/OKX/Bitget/Bybit/Coinbase/Kraken/KuCoin/Gate/DeepCoin/HTX 全部实现 + 工厂模式（factory.go + factory_test.go） |
| 市场数据（行情/K线/深度） | `internal/market/kline/`、`ticker/`、`depth/` | kline/ticker/depth 三个独立包，各含 handler.go + service.go，完整实现 |
| 全球市场数据 | `internal/market/global/` | 全球指数数据（S&P500/NASDAQ/DXY等）handler |
| 市场数据采集 | `internal/market/collector/` | 市场数据采集器 |
| 风控引擎 | `internal/trading/risk/engine.go` | 风控引擎骨架（HandleRiskCheckTask，含日志，逻辑待充实） |
| 社区模块 | `internal/community/` | 社区功能 handler（指标市场分享/评论/评分） |
| 凭证管理 | `internal/credentials/` | 交易所 API Key 加密存储（Create/List/Update/Delete/Verify），完整实现 |
| API Key 加密 | `pkg/crypto/` | AES 加密/解密实现（crypto.go + crypto_test.go） |
| WebSocket Hub | `pkg/ws/hub.go` | WS 连接管理（Register/Unregister/Broadcast），含 Message 结构体（Type/Channel/Data/UserID）、Room 管理、读写泵 |
| 中间件 | `pkg/middleware/` | auth/cors/logger/ratelimit/request_id 全部实现 |
| 数据库迁移 | `migrations/000001_init_schema.up.sql` | 初始 schema 建表语句 |
| 主服务入口 | `cmd/api/main.go` | Gin 路由注册、优雅关闭、Redis/DB 初始化 |
| 单元测试（3个） | `internal/auth/jwt_test.go`、`internal/trading/exchange/factory_test.go`、`pkg/crypto/crypto_test.go` | JWT、交易所工厂、加密模块测试 |

#### ❌ 未完成 / 缺失

| # | 项目 | 文件/目录 | 严重程度 | 说明 |
|---|------|----------|---------|------|
| G-3 | **组合服务/Handler 为 Stub** | `internal/trading/portfolio/` | 🔴 **阻断上线** | Portfolio model 完整，handler/service 存在但为最小实现（`ListPortfolios` 返回空数组）；无真实持仓聚合逻辑 |
| G-5 | **OAuth 认证未实现** | `internal/auth/service.go` | 🔴 **阻断上线** | Auth handler 无 Google/GitHub OAuth 路由；`GOOGLE_CLIENT_ID`/`GITHUB_CLIENT_ID` 在 `.env.example` 存在但代码未接入 |
| G-7 | **gRPC 客户端缺失** | `internal/grpc/`（不存在） | 🔴 **阻断上线** | 设计方案中 Go↔Python 通过 gRPC 通信；当前无 `.proto` 文件，无生成代码，Go 侧无 gRPC Client（docker-compose 已映射 gRPC 端口 50051） |
| G-10 | **快速交易（Quick Trade）Handler 无专用实现** | `internal/trading/order/handler.go` | 🟡 **影响体验** | 订单 handler 有完整 CRUD，但无闪电交易专用逻辑（市价单快速确认流程） |
| G-11 | **实验模块缺失** | `internal/experiment/`（不存在） | 🟢 **优化项** | 设计方案包含 experiment 模块（策略进化/评分/市场体制），Go 后端无对应模块（Python 端已实现） |
| G-12 | **风控规则配置 API 待完善** | `internal/trading/risk/engine.go` | 🟡 **影响体验** | 风控引擎骨架存在（HandleRiskCheckTask），但无 HTTP API 层（风控规则 CRUD 接口），业务逻辑仅有日志打印 |
| G-13 | **Cloudflare Turnstile 验证缺失** | `pkg/middleware/`（无 turnstile 文件） | 🟡 **影响体验** | 设计方案中注册/登录有 Turnstile 人机验证，当前中间件层无此实现 |

---

### 2.3 Python 后端（backend/python — FastAPI/Celery/gRPC）

#### ✅ 已完成

| 模块 | 目录/文件 | 说明 |
|------|----------|------|
| FastAPI 主程序 | `app/main.py` | 路由注册、lifespan 管理 |
| AI 分析服务 | `app/services/ai/` | fast_analysis、llm_service（多LLM支持）、analysis_memory（RAG）、ai_calibration、reflection、code_generator、ensemble |
| AI Web 搜索 | `app/services/ai/search.py` | 多后端 Web 搜索服务（Serper/Brave/DuckDuckGo），含 fallback 逻辑和 search_news() |
| 回测引擎 | `app/services/backtest/` | engine（181行完整实现）、metrics（197行夏普/最大回撤等）、report（76行报告生成） |
| 策略服务 | `app/services/strategy/` | compiler（沙箱编译）、runtime（策略运行时）、script_strategy（脚本策略）、indicator_strategy（指标策略）、snapshot（持久化） |
| 指标代码质量检查 | `app/services/strategy/code_quality.py` | AST 分析引擎：安全检查（禁止导入/调用）、方法验证、代码风格、性能提示，返回 QualityReport（评分+问题列表） |
| 数据提供器（9个） | `app/services/data/providers/` | base（抽象基类）、crypto（ccxt Binance/多交易所）、stock（Yahoo Finance，含美港股）、forex（httpx）、cn_stock（A股独立）、hk_stock（港股独立）、futures（期货）、tencent（腾讯行情源）、cn_hk_fundamentals（中港基本面） |
| 数据层基础设施 | `app/services/data/` | factory.py（数据源工厂模式）、cache_manager.py（数据缓存层）、circuit_breaker.py（熔断器）、rate_limiter.py（速率限制） |
| 实验模块（5子模块） | `app/services/experiment/` | evolution（策略进化）、regime（市场体制检测）、scoring（实验评分）、prompts（AI Prompt管理）、runner（实验运行器） |
| IBKR 交易服务 | `app/services/trading/live_trading/ibkr.py` | Interactive Brokers 美股实盘交易接入 |
| MT5 交易服务 | `app/services/trading/live_trading/mt5.py` | MetaTrader 5 外汇实盘交易接入 |
| Polymarket 研究服务 | `app/services/research/polymarket.py` | 预测市场研究分析服务 |
| 符号名称解析 | `app/services/symbol_name.py` | SymbolNameResolver：多资产类别（crypto/forex/futures/美股/A股/港股）符号识别、标准化和映射 |
| USDT TRC20 支付 | `app/services/billing/usdt_payment.py` | USDT TRC20 支付会员服务 |
| Celery Workers | `app/workers/` | celery_app（配置）、market_data_collector、pending_orders、portfolio_monitor、polymarket_worker、reflection_worker |
| 数据库配置 | `app/core/database.py`、`app/core/config.py` | SQLAlchemy async + Alembic 迁移 |
| Alembic 迁移 | `alembic/`、`alembic/versions/0001_initial.py` | 初始 schema 迁移文件 |
| 数据模型 | `app/models/` | analysis、backtest、indicator、strategy 完整 SQLAlchemy 模型 |
| API 路由 | `app/api/` | ai_analysis、backtest、strategy_engine、indicator、polymarket、code_gen |
| 测试覆盖 | `tests/` | api（3个）、core（1个）、services（6个），共约 11 个测试模块 |
| gRPC 服务端框架 | `app/core/grpc_server.py` | gRPC server 基础设施（serve/start_grpc_server），servicer 方法待实现 |

#### ❌ 未完成 / 缺失

| # | 项目 | 文件/目录 | 严重程度 | 说明 |
|---|------|----------|---------|------|
| P-5 | **gRPC Proto 文件缺失** | `proto/`（不存在） | 🔴 **阻断上线** | `grpc_server.py` 存在但未定义任何 `.proto` 服务契约；无 protobuf 生成代码；Go↔Python gRPC 通信无法建立（docker-compose 已映射 50051 端口） |
| P-6 | **gRPC 服务未绑定实际方法** | `app/core/grpc_server.py` | 🔴 **阻断上线** | `AnalysisServicer.GetAnalysis` 仅有 `pass`；`serve()` 未向 server 注册任何 servicer；gRPC server 启动后无法处理任何请求 |
| P-7 | **Polymarket 数据提供器缺失** | `app/services/data/providers/` | 🟢 **优化项** | 数据提供器目录已有9个提供器，但缺少 Polymarket 专用数据提供器（polymarket.py）；Polymarket 研究服务（`research/polymarket.py`）已存在 |

---

### 2.4 基础设施（Infrastructure）

#### ✅ 已完成

| 项目 | 文件 | 说明 |
|------|------|------|
| Docker Compose | `docker-compose.yml` | 全栈编排（nginx/frontend/backend-go/backend-go-worker/backend-python/backend-python-worker/postgres/redis），共8服务，全部配置 healthcheck |
| Nginx 反向代理 | `docker/nginx/nginx.conf` | 统一入口，反向代理 frontend(3000)/go-api(8080)/python-api(8000) |
| 环境变量模板 | `.env.example` | 包含 DB/Redis/JWT/LLM/Exchange/Notification/OAuth/Frontend 等关键变量 |
| CI 工作流 | `.github/workflows/ci.yml` | Frontend(pnpm lint+build) + Go(vet+build+test) + Python(ruff+pytest) + Docker build |
| CD 部署工作流 | `.github/workflows/deploy.yml` | 生产环境自动部署 |
| Docker 构建推送 | `.github/workflows/docker-build.yml` | 三个镜像构建推送到 GHCR，支持 tag/sha/branch 标签 |
| 文档部署 | `.github/workflows/docs-deploy.yml` | 自动部署 8 语言文档到 GitHub Pages |
| Dockerfile（3个） | `backend/go/Dockerfile`、`backend/python/Dockerfile`、`frontend/Dockerfile` | 三个服务独立 Dockerfile，frontend 使用 Node 22-alpine + pnpm 多阶段构建 |
| 根目录 Makefile | `Makefile` | 统一 `make install`/`make dev`/`make build`/`make test`/`make lint`/`make clean`/`make up`/`make down`/`make logs`/`make migrate-*` 命令 |

#### ❌ 未完成 / 缺失

> **注意：** 此前标记为缺失的 I-1（deploy.yml）、I-2（nginx.conf）、I-3（healthcheck）、I-4（Makefile）、I-5（README链接）、I-6（frontend/Dockerfile）、I-7（gRPC端口映射）均已实现，基础设施层当前无阻断上线问题。

---

### 2.5 文档（docs/）

#### ✅ 已完成

| 项目 | 目录 | 说明 |
|------|------|------|
| 8语言完整文档集 | `docs/en/`、`docs/zh-CN/`、`docs/zh-TW/`、`docs/ja/`、`docs/ko/`、`docs/ar/`、`docs/ru/`、`docs/de/` | 每种语言均包含 README、SETUP、API、ARCHITECTURE、CONTRIBUTING、DEPLOYMENT 共 6 份文档，合计 48 份 |
| 根目录 README | `README.md` | 包含多语言切换链接、功能概览、架构图、快速启动命令 |
| 文档自动部署 | `.github/workflows/docs-deploy.yml` | 推送 main 分支后自动部署到 GitHub Pages |

#### ❌ 未完成 / 缺失

| # | 项目 | 文件/目录 | 严重程度 | 说明 |
|---|------|----------|---------|------|
| D-2 | **docs/en/SETUP.md 中部分内容待同步** | `docs/en/SETUP.md` | 🟢 **优化项** | 文档中的构建步骤应与当前实际的 `frontend/Dockerfile`（多阶段构建）保持一致 |
| D-3 | **阿拉伯语文档 RTL 渲染未测试** | `docs/ar/*.md` | 🟢 **优化项** | 文档内容以阿拉伯语书写，但 GitHub Pages 部署后 Markdown 渲染是否正确显示 RTL 待验证 |

---

## 三、未完成清单（按优先级排序）

### 🔴 P0 — 阻断上线（必须完成才能正常运行）

| 编号 | 层级 | 问题描述 | 目录/文件 |
|------|------|---------|----------|
| 1 | 前端 | **图表组件全为占位符**，Dashboard/K线/AI雷达图无实现 | `frontend/src/components/charts/` |
| 2 | 前端 | **认证 session 集成缺失**（next-auth session管理），UI已有但无实际登录逻辑 | `frontend/src/app/[locale]/(auth)/` |
| 3 | Go 后端 | **OAuth 认证未实现**（Google/GitHub），用户无法第三方登录 | `internal/auth/oauth.go` |
| 4 | Go 后端 | **gRPC 客户端缺失**，Go↔Python 服务间通信无法建立 | `internal/grpc/` |
| 5 | Python 后端 | **Proto 文件及 gRPC 服务注册缺失**，gRPC Server 启动但无法响应 | `proto/*.proto`、`app/core/grpc_server.py` |
| 6 | Go 后端 | **组合服务为 Stub**（返回空数组），持仓/组合功能不可用 | `internal/trading/portfolio/` |

### 🟡 P1 — 影响体验（主要功能不完整）

| 编号 | 层级 | 问题描述 | 目录/文件 |
|------|------|---------|----------|
| 7 | 前端 | **闪电交易面板未实现**，指标分析页的核心交易功能缺失 | `indicator/page.tsx` |
| 8 | 前端 | **财经日历组件缺失**，AI分析页面功能不完整 | `ai-analysis/page.tsx` |
| 9 | 前端 | **用户中心（profile）为基础骨架**，无API密钥管理和通知偏好 | `profile/page.tsx` |
| 10 | 前端 | **移动端响应式未验证** | 各页面 |
| 11 | Go 后端 | **快速交易逻辑未独立**，无闪电交易专用流程 | `internal/trading/order/` |
| 12 | Go 后端 | **风控规则 API 待完善**，仅有骨架无业务逻辑 | `internal/trading/risk/engine.go` |
| 13 | Go 后端 | **Cloudflare Turnstile 验证缺失**，注册/登录有安全隐患 | `pkg/middleware/turnstile.go` |

### 🟢 P2 — 优化项（不影响核心功能）

| 编号 | 层级 | 问题描述 | 目录/文件 |
|------|------|----------|----------|
| 14 | 前端 | 大量 `hsl(var(--xxx))` 内联写法应改为语义 Tailwind 类 | 所有页面 `.tsx` |
| 15 | Go 后端 | 实验模块（experiment）未实现（Python 端已实现） | `internal/experiment/` |
| 16 | Python 后端 | Polymarket 数据提供器缺失（数据层，非研究服务） | `app/services/data/providers/polymarket.py` |
| 17 | 文档 | SETUP.md 构建步骤待同步 | `docs/en/SETUP.md` |
| 18 | 文档 | 阿拉伯语文档 RTL 渲染待验证 | `docs/ar/` |

---

## 四、总结

**当前主分支完成度评估：**

| 维度 | 完成度 | 状态 |
|------|--------|------|
| 项目骨架/架构 | 98% | ✅ 基础结构完整，技术选型正确，Docker/CI/CD/Nginx/Makefile 齐备 |
| 前端页面（结构/i18n/主题） | 85% | ✅ 结构完整，API层/WebSocket/Polymarket页面已实现，shadcn组件扩展至10个 |
| 前端功能（认证/图表） | 25% | ⚠️ API请求层和WebSocket已实现，但图表组件为占位符、认证session未集成 |
| Go 后端（服务结构） | 90% | ✅ 所有核心模块实现，10个交易所适配器完整，市场数据/社区/凭证/加密模块就绪 |
| Go 后端（测试/gRPC） | 20% | ⚠️ 有3个测试文件覆盖关键模块，但 OAuth 和 gRPC 客户端仍缺失 |
| Python 后端（AI/回测/策略） | 90% | ✅ 核心 AI 链路完整可用，含Web搜索、实验模块、代码质量检查、符号解析 |
| Python 后端（数据/交易/实验） | 85% | ✅ 9个数据提供器、数据层基础设施、IBKR/MT5实盘、Polymarket研究、USDT支付均已实现 |
| Python 后端（gRPC） | 15% | ❌ gRPC Server 框架存在但 Proto 文件缺失、servicer 方法未实现 |
| 基础设施（Docker/CI/CD） | 95% | ✅ 完整的构建流水线、部署工作流、Nginx反向代理、healthcheck 配置 |
| 文档 | 97% | ✅ 48份文档完整，README链接正确，仅 SETUP.md 待同步 |

**最高优先级行动项（建议执行顺序）：**

1. 集成图表组件（lightweight-charts 或 klinecharts）到 dashboard 和 indicator 页面 — 核心用户体验（F-1/F-2）
2. 完成 next-auth 认证 session 集成 — 核心安全功能（F-3）
3. 实现 OAuth 登录（Google/GitHub）— 提升登录体验（G-5）
4. 完成 proto 定义 + gRPC 双端接入 — 解除 Go↔Python 通信阻断（G-7/P-5/P-6）
5. 充实 Portfolio 组合服务业务逻辑 — 持仓管理核心功能（G-3）
6. 实现 Cloudflare Turnstile 中间件 — 安全加固（G-13）
7. 完善风控引擎业务逻辑和 API — 风险管理核心功能（G-12）
