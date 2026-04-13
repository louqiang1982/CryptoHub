# Справочник API

CryptoHub предоставляет два бэкенд-API: **Go API** (основной шлюз) и **Python API** (движок ИИ и количественного анализа).

## Базовые URL

| Сервис | URL | Префикс |
|--------|-----|---------|
| Go API | `http://localhost:8080` | `/api/v1` |
| Python API | `http://localhost:8000` | `/api/v1` |

## Эндпоинты Python API

### Проверка состояния

```
GET /health
```

### ИИ-анализ

#### Потоковый ИИ-анализ (SSE)

```
POST /api/v1/ai/analyze
```

| Поле | Тип | Описание |
|------|-----|----------|
| `symbol` | string | Торговый символ (напр. `BTC/USDT`) |
| `analysis_type` | string | `comprehensive`, `technical`, `fundamental` |
| `timeframe` | string | `1D`, `4H`, `1H` и т.д. |

#### Получение результата анализа

```
GET /api/v1/ai/analyze/{analysis_id}
```

#### Быстрый мультифакторный анализ

```
POST /api/v1/ai/fast-analyze
```

### Бэктестинг

#### Запуск бэктеста

```
POST /api/v1/backtest/run
```

| Поле | Тип | По умолчанию | Описание |
|------|-----|-------------|----------|
| `strategy_id` | string | обязательно | Идентификатор стратегии |
| `symbol` | string | обязательно | Торговая пара |
| `timeframe` | string | `1H` | Таймфрейм |
| `start_date` | string | обязательно | Дата ISO |
| `end_date` | string | обязательно | Дата ISO |
| `initial_capital` | number | `10000` | Начальный капитал |

#### Получение результата

```
GET /api/v1/backtest/{backtest_id}
```

#### Получение отчёта

```
GET /api/v1/backtest/{backtest_id}/report
```

### Движок стратегий

```
POST /api/v1/strategy/compile
POST /api/v1/strategy/start
POST /api/v1/strategy/stop/{strategy_id}
GET  /api/v1/strategy/{strategy_id}/status
```

### Индикаторы

```
POST /api/v1/indicator/calculate
GET  /api/v1/indicator/list
```

### Генерация кода

```
POST /api/v1/codegen/generate
```

### Polymarket

```
GET /api/v1/polymarket/markets
```

## Аутентификация

Защищённые эндпоинты требуют Bearer-токен в заголовке `Authorization`:

```
Authorization: Bearer <jwt_token>
```

## Ответы об ошибках

```json
{ "code": 400, "message": "Ошибка валидации", "detail": "Поле 'symbol' обязательно" }
```
