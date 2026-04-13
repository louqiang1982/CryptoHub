# Multi-stage build
FROM golang:1.24-alpine AS builder

# Install build dependencies
RUN apk add --no-cache git ca-certificates

# Set working directory
WORKDIR /app

# Copy go mod files
COPY go.mod go.sum ./

# Download dependencies
RUN go mod download

# Copy source code
COPY . .

# Build the application
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o api ./cmd/api
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o ws ./cmd/ws
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o worker ./cmd/worker

# Final stage
FROM alpine:3.21

# Install ca-certificates
RUN apk --no-cache add ca-certificates

# Set working directory
WORKDIR /root/

# Copy the binaries from builder
COPY --from=builder /app/api .
COPY --from=builder /app/ws .
COPY --from=builder /app/worker .

# Copy config files
COPY --from=builder /app/configs ./configs
COPY --from=builder /app/migrations ./migrations

# Expose ports
EXPOSE 8080 8081

# Default command
CMD ["./api"]