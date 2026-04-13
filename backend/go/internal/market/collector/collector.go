package collector

import (
	"context"

	"github.com/hibiken/asynq"
	"github.com/redis/go-redis/v9"
	"go.uber.org/zap"
	"gorm.io/gorm"
)

type Collector struct {
	db     *gorm.DB
	rdb    *redis.Client
	logger *zap.Logger
}

func NewCollector(db *gorm.DB, rdb *redis.Client, logger *zap.Logger) *Collector {
	return &Collector{db: db, rdb: rdb, logger: logger}
}

func (c *Collector) HandleMarketDataTask(ctx context.Context, t *asynq.Task) error {
	c.logger.Info("Processing market data task")
	return nil
}
