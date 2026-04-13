.PHONY: build run test lint migrate-up migrate-down proto docker-build clean

# Build the application
build:
	go build -o bin/api ./cmd/api
	go build -o bin/ws ./cmd/ws
	go build -o bin/worker ./cmd/worker

# Run the API server
run:
	go run ./cmd/api

# Run the WebSocket server
run-ws:
	go run ./cmd/ws

# Run the worker
run-worker:
	go run ./cmd/worker

# Run tests
test:
	go test -v ./...

# Run tests with coverage
test-cover:
	go test -v -coverprofile=coverage.out ./...
	go tool cover -html=coverage.out -o coverage.html

# Lint the code
lint:
	golangci-lint run

# Format the code
fmt:
	go fmt ./...

# Tidy go modules
tidy:
	go mod tidy

# Migrate database up
migrate-up:
	migrate -path migrations -database "postgres://cryptohub:password@localhost:5432/cryptohub?sslmode=disable" up

# Migrate database down
migrate-down:
	migrate -path migrations -database "postgres://cryptohub:password@localhost:5432/cryptohub?sslmode=disable" down

# Create new migration
migrate-create:
	migrate create -ext sql -dir migrations -seq $(name)

# Generate protobuf files
proto:
	protoc --go_out=. --go_opt=paths=source_relative \
		--go-grpc_out=. --go-grpc_opt=paths=source_relative \
		api/proto/*.proto

# Build Docker image
docker-build:
	docker build -t cryptohub-backend .

# Run with Docker Compose
docker-up:
	docker-compose up -d

# Stop Docker Compose
docker-down:
	docker-compose down

# Clean build artifacts
clean:
	rm -rf bin/
	rm -f coverage.out coverage.html

# Install tools
tools:
	go install github.com/golang-migrate/migrate/v4/cmd/migrate@latest
	go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest
	go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
	go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest

# Development server with hot reload
dev:
	air -c .air.toml

# Production build
build-prod:
	CGO_ENABLED=0 GOOS=linux go build -a -ldflags '-extldflags "-static"' -o bin/api ./cmd/api
	CGO_ENABLED=0 GOOS=linux go build -a -ldflags '-extldflags "-static"' -o bin/ws ./cmd/ws
	CGO_ENABLED=0 GOOS=linux go build -a -ldflags '-extldflags "-static"' -o bin/worker ./cmd/worker

# Initialize project
init:
	go mod download
	make tools
	make migrate-up

# Help
help:
	@echo "Available commands:"
	@echo "  build        Build the application"
	@echo "  run          Run the API server"
	@echo "  run-ws       Run the WebSocket server"
	@echo "  run-worker   Run the worker"
	@echo "  test         Run tests"
	@echo "  test-cover   Run tests with coverage"
	@echo "  lint         Lint the code"
	@echo "  fmt          Format the code"
	@echo "  tidy         Tidy go modules"
	@echo "  migrate-up   Run database migrations"
	@echo "  migrate-down Rollback database migrations"
	@echo "  proto        Generate protobuf files"
	@echo "  docker-build Build Docker image"
	@echo "  clean        Clean build artifacts"
	@echo "  tools        Install development tools"
	@echo "  dev          Start development server"
	@echo "  help         Show this help message"