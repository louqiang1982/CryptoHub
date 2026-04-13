package main

import (
	"context"
	"fmt"
	"log"
	"os"
	"os/signal"
	"syscall"

	"github.com/hibiken/asynq"
	"github.com/redis/go-redis/v9"
	"github.com/spf13/viper"
	"go.uber.org/zap"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"

	"github.com/louqiang1982/CryptoHub/backend-go/internal/market/collector"
	"github.com/louqiang1982/CryptoHub/backend-go/internal/notification"
	"github.com/louqiang1982/CryptoHub/backend-go/internal/trading/risk"
)

const (
	TypeMarketData     = "market_data"
	TypeNotification   = "notification"
	TypeRiskCheck      = "risk_check"
	TypeStrategySignal = "strategy_signal"
)

func main() {
	// Load configuration
	if err := loadConfig(); err != nil {
		log.Fatal("Failed to load config:", err)
	}

	// Initialize logger
	logger, err := initLogger()
	if err != nil {
		log.Fatal("Failed to initialize logger:", err)
	}
	defer logger.Sync()

	// Initialize database
	db, err := initDatabase()
	if err != nil {
		logger.Fatal("Failed to connect to database", zap.Error(err))
	}

	// Initialize Redis
	rdb, err := initRedis()
	if err != nil {
		logger.Fatal("Failed to connect to Redis", zap.Error(err))
	}

	// Create Asynq server
	srv := asynq.NewServer(
		asynq.RedisClientOpt{Addr: viper.GetString("redis.host") + ":" + viper.GetString("redis.port")},
		asynq.Config{
			Concurrency: 10,
			Queues: map[string]int{
				"critical": 6,
				"default":  3,
				"low":      1,
			},
		},
	)

	// Initialize services
	marketCollector := collector.NewCollector(db, rdb, logger)
	notificationService := notification.NewService(db)
	riskEngine := risk.NewEngine(db, rdb, logger)

	// Create multiplexer
	mux := asynq.NewServeMux()

	// Register task handlers
	mux.HandleFunc(TypeMarketData, marketCollector.HandleMarketDataTask)
	mux.HandleFunc(TypeNotification, handleNotificationTask(notificationService, logger))
	mux.HandleFunc(TypeRiskCheck, riskEngine.HandleRiskCheckTask)
	mux.HandleFunc(TypeStrategySignal, handleStrategySignalTask(db, logger))

	// Start the server
	go func() {
		logger.Info("Worker server starting")
		if err := srv.Run(mux); err != nil {
			logger.Fatal("Could not start worker server", zap.Error(err))
		}
	}()

	// Graceful shutdown
	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	<-quit

	logger.Info("Worker server shutting down...")
	srv.Shutdown()
	logger.Info("Worker server exited")
}

func handleNotificationTask(service *notification.Service, logger *zap.Logger) asynq.HandlerFunc {
	return func(ctx context.Context, t *asynq.Task) error {
		logger.Info("Processing notification task", zap.String("type", t.Type()))
		// Implementation for notification processing
		return service.ProcessNotificationTask(ctx, t.Payload())
	}
}

func handleStrategySignalTask(db *gorm.DB, logger *zap.Logger) asynq.HandlerFunc {
	return func(ctx context.Context, t *asynq.Task) error {
		logger.Info("Processing strategy signal task", zap.String("type", t.Type()))
		// Implementation for strategy signal processing
		return nil
	}
}

func loadConfig() error {
	viper.SetConfigName("config")
	viper.SetConfigType("yaml")
	viper.AddConfigPath("./configs")
	viper.AddConfigPath(".")
	return viper.ReadInConfig()
}

func initLogger() (*zap.Logger, error) {
	config := zap.NewProductionConfig()
	config.Level = zap.NewAtomicLevelAt(zap.InfoLevel)
	return config.Build()
}

func initDatabase() (*gorm.DB, error) {
	dsn := fmt.Sprintf("host=%s user=%s password=%s dbname=%s port=%s sslmode=disable",
		viper.GetString("database.host"),
		viper.GetString("database.user"),
		viper.GetString("database.password"),
		viper.GetString("database.name"),
		viper.GetString("database.port"))

	return gorm.Open(postgres.Open(dsn), &gorm.Config{})
}

func initRedis() (*redis.Client, error) {
	rdb := redis.NewClient(&redis.Options{
		Addr:     viper.GetString("redis.host") + ":" + viper.GetString("redis.port"),
		Password: viper.GetString("redis.password"),
		DB:       viper.GetInt("redis.db"),
	})

	ctx := context.Background()
	_, err := rdb.Ping(ctx).Result()
	return rdb, err
}