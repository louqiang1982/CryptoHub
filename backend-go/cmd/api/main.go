package main

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
	"github.com/redis/go-redis/v9"
	"github.com/spf13/viper"
	"go.uber.org/zap"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"

	"github.com/louqiang1982/CryptoHub/backend-go/internal/auth"
	"github.com/louqiang1982/CryptoHub/backend-go/internal/user"
	"github.com/louqiang1982/CryptoHub/backend-go/internal/trading/order"
	"github.com/louqiang1982/CryptoHub/backend-go/internal/trading/position"
	"github.com/louqiang1982/CryptoHub/backend-go/internal/trading/portfolio"
	"github.com/louqiang1982/CryptoHub/backend-go/internal/market/kline"
	"github.com/louqiang1982/CryptoHub/backend-go/internal/market/ticker"
	"github.com/louqiang1982/CryptoHub/backend-go/internal/market/depth"
	"github.com/louqiang1982/CryptoHub/backend-go/internal/strategy"
	"github.com/louqiang1982/CryptoHub/backend-go/internal/notification"
	"github.com/louqiang1982/CryptoHub/backend-go/internal/billing"
	"github.com/louqiang1982/CryptoHub/backend-go/internal/settings"
	"github.com/louqiang1982/CryptoHub/backend-go/internal/dashboard"
	"github.com/louqiang1982/CryptoHub/backend-go/internal/admin"
	"github.com/louqiang1982/CryptoHub/backend-go/pkg/middleware"
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

	// Initialize services and handlers
	authService := auth.NewService(db, rdb)
	authHandler := auth.NewHandler(authService)

	userRepository := user.NewRepository(db)
	userService := user.NewService(userRepository)
	userHandler := user.NewHandler(userService)

	orderService := order.NewService(db, rdb)
	orderHandler := order.NewHandler(orderService)

	positionService := position.NewService(db)
	positionHandler := position.NewHandler(positionService)

	portfolioService := portfolio.NewService(db)
	portfolioHandler := portfolio.NewHandler(portfolioService)

	klineService := kline.NewService(db)
	klineHandler := kline.NewHandler(klineService)

	tickerService := ticker.NewService(rdb)
	tickerHandler := ticker.NewHandler(tickerService)

	depthService := depth.NewService(rdb)
	depthHandler := depth.NewHandler(depthService)

	strategyService := strategy.NewService(db, rdb)
	strategyHandler := strategy.NewHandler(strategyService)

	notificationService := notification.NewService(db)
	notificationHandler := notification.NewHandler(notificationService)

	billingService := billing.NewService(db)
	billingHandler := billing.NewHandler(billingService)

	settingsService := settings.NewService(db)
	settingsHandler := settings.NewHandler(settingsService)

	dashboardService := dashboard.NewService(db, rdb)
	dashboardHandler := dashboard.NewHandler(dashboardService)

	adminService := admin.NewService(db)
	adminHandler := admin.NewHandler(adminService)

	// Setup Gin router
	r := gin.New()

	// Setup middleware
	r.Use(gin.Recovery())
	r.Use(middleware.Logger(logger))
	r.Use(middleware.RequestID())
	r.Use(cors.New(cors.Config{
		AllowOrigins:     []string{"*"},
		AllowMethods:     []string{"GET", "POST", "PUT", "DELETE", "OPTIONS"},
		AllowHeaders:     []string{"*"},
		ExposeHeaders:    []string{"*"},
		AllowCredentials: true,
	}))
	r.Use(middleware.RateLimit(rdb))

	// API routes
	api := r.Group("/api/v1")

	// Public routes
	authHandler.RegisterRoutes(api)

	// Protected routes
	protected := api.Group("")
	protected.Use(middleware.Auth(authService))

	userHandler.RegisterRoutes(protected)
	orderHandler.RegisterRoutes(protected)
	positionHandler.RegisterRoutes(protected)
	portfolioHandler.RegisterRoutes(protected)
	klineHandler.RegisterRoutes(protected)
	tickerHandler.RegisterRoutes(protected)
	depthHandler.RegisterRoutes(protected)
	strategyHandler.RegisterRoutes(protected)
	notificationHandler.RegisterRoutes(protected)
	billingHandler.RegisterRoutes(protected)
	settingsHandler.RegisterRoutes(protected)
	dashboardHandler.RegisterRoutes(protected)

	// Admin routes
	adminGroup := protected.Group("/admin")
	adminGroup.Use(middleware.Admin())
	adminHandler.RegisterRoutes(adminGroup)

	// Start server
	port := viper.GetString("server.port")
	if port == "" {
		port = "8080"
	}

	srv := &http.Server{
		Addr:    ":" + port,
		Handler: r,
	}

	go func() {
		logger.Info("Server starting", zap.String("port", port))
		if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			logger.Fatal("Failed to start server", zap.Error(err))
		}
	}()

	// Graceful shutdown
	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	<-quit

	logger.Info("Server shutting down...")

	ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
	defer cancel()

	if err := srv.Shutdown(ctx); err != nil {
		logger.Fatal("Server forced to shutdown", zap.Error(err))
	}

	logger.Info("Server exited")
}

func loadConfig() error {
	viper.SetConfigName("config")
	viper.SetConfigType("yaml")
	viper.AddConfigPath("./configs")
	viper.AddConfigPath(".")

	viper.SetDefault("server.port", "8080")
	viper.SetDefault("database.host", "localhost")
	viper.SetDefault("database.port", "5432")
	viper.SetDefault("redis.host", "localhost")
	viper.SetDefault("redis.port", "6379")

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