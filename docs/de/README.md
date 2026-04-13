# CryptoHub

Eine professionelle Kryptowährungs-Handelsplattform mit KI-gestützter Analyse, automatisierten Handelsstrategien und umfassendem Portfoliomanagement.

## Übersicht

CryptoHub kombiniert modernste künstliche Intelligenz mit quantitativem Handel, um Tradern einen Wettbewerbsvorteil zu verschaffen. Die Plattform unterstützt Echtzeit-Analysen für Kryptowährungen, Aktien und Devisenmärkte – alles in einer einheitlichen Benutzeroberfläche.

### Hauptfunktionen

- **KI-Analyse** — Machine-Learning-Modelle analysieren Marktdaten, generieren Handelssignale und liefern bewertete Empfehlungen.
- **Strategie-Engine** — Erstellen, Kompilieren, Backtesten und Bereitstellen von Handelsstrategien mit der Python-Scripting-Engine und vollständigem ereignisgesteuertem Lebenszyklus (`on_init` / `on_bar`).
- **Echtzeit-Handel** — WebSocket-Verbindung zu großen Börsen für Live-Orderausführung und Portfolio-Tracking.
- **Backtest-Engine** — Strategiesimulation auf historischen Daten mit Kommissions- und Slippage-Modellierung; Berechnung von Sharpe Ratio, Sortino Ratio, Maximum Drawdown und weiteren Metriken.
- **Multi-Markt-Daten** — Integrierte Datenanbieter für Kryptowährungen (ccxt/Binance), Aktien (Yahoo Finance) und Forex.
- **Portfoliomanagement** — Risikoüberwachung, Tracking unrealisierter Gewinne/Verluste und Benachrichtigungen bei Überschreitung von Drawdown-Schwellenwerten.
- **Prognosemärkte** — Integration von Polymarket-Daten für sentimentbasierte Analysen.
- **Internationalisierung** — Vollständige i18n-Unterstützung in 8 Sprachen: Englisch, Vereinfachtes Chinesisch, Traditionelles Chinesisch, Japanisch, Koreanisch, Arabisch, Russisch und Deutsch.

## Architektur

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│    Frontend      │    │   Go-Backend     │    │ Python-Backend  │
│   (Next.js 15)  │◄──►│   (API / WS)     │◄──►│   (AI / ML)     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │                        │
                       ┌──────┴──────┐          ┌──────┴──────┐
                       │ PostgreSQL  │          │   Redis     │
                       └─────────────┘          └─────────────┘
```

## Schnellstart

```bash
git clone https://github.com/louqiang1982/CryptoHub.git
cd CryptoHub
cp .env.example .env   # API-Schlüssel eintragen
docker compose up -d
```

| Dienst | URL |
|--------|-----|
| Frontend | http://localhost:3000 |
| Go API | http://localhost:8080 |
| Python API | http://localhost:8000 |

## Dokumentation

- [Installationsanleitung](./SETUP.md)
- [API-Referenz](./API.md)
- [Architektur](./ARCHITECTURE.md)
- [Mitwirken](./CONTRIBUTING.md)
- [Deployment](./DEPLOYMENT.md)

## Lizenz

MIT-Lizenz — siehe [LICENSE](../../LICENSE) für Details.
