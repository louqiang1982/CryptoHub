package risk

import (
	"context"

	"github.com/hibiken/asynq"
	"github.com/redis/go-redis/v9"
	"go.uber.org/zap"
	"gorm.io/gorm"
)

type Engine struct {
	db     *gorm.DB
	rdb    *redis.Client
	logger *zap.Logger
}

func NewEngine(db *gorm.DB, rdb *redis.Client, logger *zap.Logger) *Engine {
	return &Engine{db: db, rdb: rdb, logger: logger}
}

func (e *Engine) HandleRiskCheckTask(ctx context.Context, t *asynq.Task) error {
	e.logger.Info("Processing risk check task")
	return nil
}
