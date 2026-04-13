.PHONY: help dev build test lint clean install

help: ## Show this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n\nTargets:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

install: ## Install all dependencies
	cd frontend && pnpm install
	cd backend-go && go mod download
	cd backend-python && pip install -r requirements.txt

dev: ## Start all services in development mode
	docker compose up -d postgres redis
	@echo "Starting development servers..."
	@echo "  Frontend:  http://localhost:3000"
	@echo "  Go API:    http://localhost:8080"
	@echo "  Python API:http://localhost:8000"

up: ## Start all services via Docker Compose
	docker compose up -d

down: ## Stop all Docker Compose services
	docker compose down

build: ## Build all services
	cd frontend && pnpm build
	cd backend-go && go build ./...
	cd backend-python && python -m py_compile app/main.py

test: ## Run all tests
	cd frontend && pnpm lint
	cd backend-go && go test ./... -v
	cd backend-python && pytest tests/ -v

lint: ## Lint all code
	cd frontend && pnpm lint
	cd backend-go && go vet ./...
	cd backend-python && ruff check app/

clean: ## Remove build artifacts
	cd frontend && rm -rf .next out
	cd backend-go && rm -f cryptohub-api cryptohub-worker cryptohub-ws
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

logs: ## Tail Docker Compose logs
	docker compose logs -f

ps: ## Show running containers
	docker compose ps

migrate-go: ## Run Go database migrations
	cd backend-go && migrate -path migrations -database "$$DATABASE_URL" up

migrate-python: ## Run Python (Alembic) migrations
	cd backend-python && alembic upgrade head
