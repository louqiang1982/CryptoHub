module github.com/louqiang1982/CryptoHub/backend-go

go 1.24

require (
	github.com/gin-gonic/gin v1.10.0
	github.com/gin-contrib/cors v1.7.3
	gorm.io/gorm v1.25.12
	gorm.io/driver/postgres v1.5.11
	github.com/redis/go-redis/v9 v9.7.0
	github.com/gorilla/websocket v1.5.3
	github.com/golang-jwt/jwt/v5 v5.2.1
	go.uber.org/zap v1.27.0
	github.com/spf13/viper v1.19.0
	github.com/hibiken/asynq v0.25.1
	github.com/shopspring/decimal v1.4.0
	google.golang.org/grpc v1.69.4
	google.golang.org/protobuf v1.36.3
	github.com/google/uuid v1.6.0
	golang.org/x/crypto v0.32.0
)