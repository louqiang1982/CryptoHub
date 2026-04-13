# Architektur

Beschreibung der Gesamtarchitektur von CryptoHub: Verantwortlichkeiten der Dienste, Datenflüsse und Technologiewahl.

## Systemübersicht

CryptoHub folgt einer **Microservice-Architektur** mit drei Hauptdiensten, die über gRPC und REST kommunizieren. PostgreSQL für die Datenpersistenz, Redis für Caching und Aufgabenverteilung.

## Verantwortlichkeiten der Dienste

### Frontend (Next.js 15 + React 19)

- Serverseitiges Rendering mit App Router
- Internationalisierung in 8 Sprachen über `next-intl`
- Theme-Wechsel (Hell / Dunkel / System) über `next-themes`
- Professionelle Charts mit KLineCharts und ECharts
- Responsives Layout (Mobil, Tablet, Desktop, große Bildschirme)

### Go-Backend

- API-Gateway, Benutzerverwaltung, JWT-Authentifizierung
- WebSocket-Echtzeit-Streaming
- gRPC-Client für Aufrufe an das Python-Backend

### Python-Backend (FastAPI)

- KI-Analyse (LangChain + OpenAI), Reflexionsschleifen, Ensemble
- Strategie-Engine (Kompilierung, Validierung, Sandbox-Ausführung)
- Backtest-Engine (Sharpe, Sortino, Max. Drawdown, Profitfaktor)
- Datenanbieter (Kryptowährungen, Aktien, Forex)

### Celery Worker

| Worker | Zweck |
|--------|-------|
| `pending_orders` | Ausstehende Orders verarbeiten |
| `portfolio_monitor` | Risikoüberwachung und Warnungen |
| `market_data_collector` | Periodische Marktdatenerfassung |
| `reflection_worker` | Asynchrone KI-Reflexion |
| `polymarket_worker` | Prognosemarktdaten aktualisieren |

## Datenbankschema

Verwaltet durch Alembic-Migrationen. Haupttabellen:

| Tabelle | Beschreibung |
|---------|-------------|
| `strategies` | Benutzerdefinierte Handelsstrategien |
| `backtest_results` | Backtestergebnisse und Metriken |
| `indicators` | Benutzerdefinierte und Marktplatz-Indikatoren |
| `ai_analyses` | KI-Analysedatensätze |

## Sicherheit

- JWT-Authentifizierung (HS256)
- Sandbox für Strategiecode
- CORS-Middleware
- Geheimnisverwaltung über Umgebungsvariablen
