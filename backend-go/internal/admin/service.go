package admin

import (
	"context"
	"gorm.io/gorm"
)

type Service struct {
	db *gorm.DB
}

type SystemStats struct {
	TotalUsers     int64 `json:"total_users"`
	ActiveUsers    int64 `json:"active_users"`
	TotalOrders    int64 `json:"total_orders"`
	TotalTrades    int64 `json:"total_trades"`
	TotalVolume    string `json:"total_volume"`
}

func NewService(db *gorm.DB) *Service {
	return &Service{db: db}
}

func (s *Service) GetSystemStats(ctx context.Context) (*SystemStats, error) {
	stats := &SystemStats{}
	
	// Count users
	s.db.WithContext(ctx).Model(&struct{ TableName string `gorm:"tableName:users"`}{}).Count(&stats.TotalUsers)
	s.db.WithContext(ctx).Model(&struct{ TableName string `gorm:"tableName:users"`}{}).
		Where("status = ?", "active").Count(&stats.ActiveUsers)
	
	// Count orders
	s.db.WithContext(ctx).Model(&struct{ TableName string `gorm:"tableName:orders"`}{}).Count(&stats.TotalOrders)
	
	stats.TotalTrades = 0
	stats.TotalVolume = "0"
	
	return stats, nil
}