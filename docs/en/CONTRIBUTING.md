# Contributing to CryptoHub

Thank you for your interest in contributing to CryptoHub! This guide explains the process for contributing code, documentation, and bug reports.

## Getting Started

1. **Fork** the repository on GitHub.
2. **Clone** your fork locally and create a feature branch:

   ```bash
   git clone https://github.com/<you>/CryptoHub.git
   cd CryptoHub
   git checkout -b feature/my-change
   ```

3. **Set up** the development environment — see [SETUP.md](./SETUP.md).

## Development Workflow

### Branch Naming

| Prefix | Usage |
|--------|-------|
| `feature/` | New features |
| `fix/` | Bug fixes |
| `docs/` | Documentation changes |
| `refactor/` | Code refactoring |
| `test/` | Adding or improving tests |

### Commit Messages

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
feat: add Bollinger Band indicator support
fix: correct Sharpe ratio calculation for empty data
docs: update API reference with new endpoints
test: add backtest engine edge case tests
```

## Code Standards

### Python (backend/python)

- Formatter / linter: **Ruff**
- Run before committing: `ruff check app/ --fix`
- Tests: `pytest tests/ -v`
- Type hints are encouraged for all public APIs.

### Go (backend/go)

- Follow standard `go fmt` and `go vet`.
- Run tests: `go test ./... -v`

### TypeScript / React (frontend)

- Linter: **ESLint** with the project config.
- Run: `pnpm lint`
- Build check: `pnpm build`

## Testing

- Write tests for all new functionality.
- Place Python tests in `backend/python/tests/` mirroring the `app/` structure.
- Use `pytest.mark.asyncio` for async tests.
- Aim for at least 80 % coverage on new code.

## Pull Request Process

1. Ensure CI passes — the repository runs frontend lint/build, Go vet/test, Python ruff/pytest, and Docker build.
2. Fill in the PR template with a clear description.
3. Request a review from at least one maintainer.
4. Address review feedback promptly.
5. Squash-merge once approved.

## Internationalisation (i18n)

- Documentation exists in 8 languages under `docs/{lang}/`.
- When updating English docs, please note in the PR so translators can update other languages.
- Frontend translations live in `frontend/src/i18n/messages/`.

## Reporting Issues

- Use GitHub Issues with a clear title and reproduction steps.
- Label with `bug`, `enhancement`, `documentation`, or `question`.
- Include environment details (OS, browser, Docker version).

## Code of Conduct

Be respectful, inclusive, and constructive. We follow the [Contributor Covenant](https://www.contributor-covenant.org/) code of conduct.

## License

By contributing you agree that your contributions will be licensed under the MIT License.
