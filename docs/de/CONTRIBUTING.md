# Mitwirken

Vielen Dank für Ihr Interesse an der Mitarbeit an CryptoHub!

## Erste Schritte

1. **Forken** Sie das Repository auf GitHub.
2. **Klonen** Sie Ihren Fork lokal und erstellen Sie einen Feature-Branch:

   ```bash
   git clone https://github.com/<you>/CryptoHub.git
   cd CryptoHub
   git checkout -b feature/my-change
   ```

3. Richten Sie die Entwicklungsumgebung ein — siehe [SETUP.md](./SETUP.md).

## Branch-Benennung

| Präfix | Verwendung |
|--------|-----------|
| `feature/` | Neue Funktionen |
| `fix/` | Fehlerbehebungen |
| `docs/` | Dokumentationsänderungen |
| `refactor/` | Code-Refactoring |
| `test/` | Tests hinzufügen oder verbessern |

## Commit-Nachrichten

Folgen Sie der Conventional-Commits-Spezifikation:

```
feat: Bollinger-Bänder-Indikator hinzufügen
fix: Sharpe-Ratio-Berechnung bei leeren Daten korrigieren
docs: API-Referenz aktualisieren
```

## Code-Standards

- **Python**: Ruff für Formatierung/Linting, `pytest` für Tests
- **Go**: `go fmt`, `go vet`, `go test`
- **TypeScript**: ESLint, `pnpm lint`, `pnpm build`

## Tests

- Schreiben Sie Tests für alle neuen Funktionen.
- Python-Tests gehören nach `backend/python/tests/`.
- Verwenden Sie `pytest.mark.asyncio` für asynchrone Tests.
- Streben Sie mindestens 80 % Abdeckung für neuen Code an.

## Pull-Request-Prozess

1. Stellen Sie sicher, dass CI erfolgreich durchläuft.
2. Füllen Sie die PR-Vorlage mit einer klaren Beschreibung aus.
3. Fordern Sie ein Review von mindestens einem Maintainer an.
4. Nach Genehmigung: Squash-Merge.

## Internationalisierung

- Die Dokumentation wird in 8 Sprachen unter `docs/{lang}/` gepflegt.
- Bei Aktualisierung der englischen Dokumentation bitte im PR vermerken.

## Fehler melden

Verwenden Sie GitHub Issues mit einem klaren Titel und Reproduktionsschritten.

## Lizenz

Durch Mitwirken stimmen Sie zu, dass Ihre Beiträge unter der MIT-Lizenz lizenziert werden.
