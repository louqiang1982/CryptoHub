# API-Referenz

CryptoHub bietet zwei Backend-APIs: **Go API** (Haupt-Gateway) und **Python API** (KI- und quantitative Engine).

## Basis-URLs

| Dienst | URL | Präfix |
|--------|-----|--------|
| Go API | `http://localhost:8080` | `/api/v1` |
| Python API | `http://localhost:8000` | `/api/v1` |

## Python-API-Endpunkte

### Health Check

```
GET /health
```

### KI-Analyse

#### Streaming-KI-Analyse (SSE)

```
POST /api/v1/ai/analyze
```

| Feld | Typ | Beschreibung |
|------|-----|-------------|
| `symbol` | string | Handelssymbol (z.B. `BTC/USDT`) |
| `analysis_type` | string | `comprehensive`, `technical`, `fundamental` |
| `timeframe` | string | `1D`, `4H`, `1H` usw. |

#### Analyseergebnis abrufen

```
GET /api/v1/ai/analyze/{analysis_id}
```

#### Schnelle Multifaktor-Analyse

```
POST /api/v1/ai/fast-analyze
```

### Backtesting

#### Backtest ausführen

```
POST /api/v1/backtest/run
```

| Feld | Typ | Standard | Beschreibung |
|------|-----|----------|-------------|
| `strategy_id` | string | erforderlich | Strategie-ID |
| `symbol` | string | erforderlich | Handelspaar |
| `timeframe` | string | `1H` | Kerzen-Zeitrahmen |
| `start_date` | string | erforderlich | ISO-Datum |
| `end_date` | string | erforderlich | ISO-Datum |
| `initial_capital` | number | `10000` | Startkapital |

#### Ergebnis abrufen

```
GET /api/v1/backtest/{backtest_id}
```

#### Bericht abrufen

```
GET /api/v1/backtest/{backtest_id}/report
```

### Strategie-Engine

```
POST /api/v1/strategy/compile
POST /api/v1/strategy/start
POST /api/v1/strategy/stop/{strategy_id}
GET  /api/v1/strategy/{strategy_id}/status
```

### Indikatoren

```
POST /api/v1/indicator/calculate
GET  /api/v1/indicator/list
```

### Code-Generierung

```
POST /api/v1/codegen/generate
```

### Polymarket

```
GET /api/v1/polymarket/markets
```

## Authentifizierung

Geschützte Endpunkte erfordern ein Bearer-Token im `Authorization`-Header:

```
Authorization: Bearer <jwt_token>
```

## Fehlerantworten

```json
{ "code": 400, "message": "Validierung fehlgeschlagen", "detail": "Feld 'symbol' ist erforderlich" }
```
