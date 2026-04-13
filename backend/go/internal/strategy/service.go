package strategy

import (
	"context"

	"github.com/google/uuid"
	"github.com/redis/go-redis/v9"
	"gorm.io/gorm"
)

type Service struct {
	db  *gorm.DB
	rdb *redis.Client
}

func NewService(db *gorm.DB, rdb *redis.Client) *Service {
	return &Service{
		db:  db,
		rdb: rdb,
	}
}

func (s *Service) ListStrategies(ctx context.Context, userID string) ([]*Strategy, error) {
	var strategies []*Strategy
	err := s.db.WithContext(ctx).Where("user_id = ?", userID).Find(&strategies).Error
	return strategies, err
}

func (s *Service) CreateStrategy(ctx context.Context, userID, name, description, strategyType, config, riskConfig string) (*Strategy, error) {
	strategy := &Strategy{
		UserID:      uuid.MustParse(userID),
		Name:        name,
		Description: description,
		Type:        strategyType,
		Status:      "draft",
		Config:      config,
		RiskConfig:  riskConfig,
	}

	err := s.db.WithContext(ctx).Create(strategy).Error
	return strategy, err
}

func (s *Service) GetStrategy(ctx context.Context, userID, strategyID string) (*Strategy, error) {
	var strategy Strategy
	err := s.db.WithContext(ctx).Where("id = ? AND user_id = ?", strategyID, userID).First(&strategy).Error
	return &strategy, err
}

func (s *Service) UpdateStrategy(ctx context.Context, userID, strategyID, name, description, config, riskConfig string) (*Strategy, error) {
	var strategy Strategy
	if err := s.db.WithContext(ctx).Where("id = ? AND user_id = ?", strategyID, userID).First(&strategy).Error; err != nil {
		return nil, err
	}

	if name != "" {
		strategy.Name = name
	}
	if description != "" {
		strategy.Description = description
	}
	if config != "" {
		strategy.Config = config
	}
	if riskConfig != "" {
		strategy.RiskConfig = riskConfig
	}

	err := s.db.WithContext(ctx).Save(&strategy).Error
	return &strategy, err
}

func (s *Service) DeleteStrategy(ctx context.Context, userID, strategyID string) error {
	return s.db.WithContext(ctx).Where("id = ? AND user_id = ?", strategyID, userID).Delete(&Strategy{}).Error
}

func (s *Service) StartStrategy(ctx context.Context, userID, strategyID string) error {
	return s.updateStrategyStatus(ctx, userID, strategyID, "running")
}

func (s *Service) StopStrategy(ctx context.Context, userID, strategyID string) error {
	return s.updateStrategyStatus(ctx, userID, strategyID, "stopped")
}

func (s *Service) PauseStrategy(ctx context.Context, userID, strategyID string) error {
	return s.updateStrategyStatus(ctx, userID, strategyID, "paused")
}

func (s *Service) updateStrategyStatus(ctx context.Context, userID, strategyID, status string) error {
	return s.db.WithContext(ctx).Model(&Strategy{}).
		Where("id = ? AND user_id = ?", strategyID, userID).
		Update("status", status).Error
}