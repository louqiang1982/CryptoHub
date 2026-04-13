package dashboard

import (
	"context"

	"github.com/redis/go-redis/v9"
	"github.com/shopspring/decimal"
	"gorm.io/gorm"
)

type Service struct {
	db  *gorm.DB
	rdb *redis.Client
}

type DashboardStats struct {
	TotalStrategies   int64           `json:"total_strategies"`
	ActiveStrategies  int64           `json:"active_strategies"`
	TotalPositions    int64           `json:"total_positions"`
	OpenPositions     int64           `json:"open_positions"`
	TotalPortfolio    decimal.Decimal `json:"total_portfolio_value"`
	UnrealizedPL      decimal.Decimal `json:"unrealized_pl"`
	RealizedPL        decimal.Decimal `json:"realized_pl"`
	TotalOrders       int64           `json:"total_orders"`
	PendingOrders     int64           `json:"pending_orders"`
	RecentTrades      int64           `json:"recent_trades"`
}

func NewService(db *gorm.DB, rdb *redis.Client) *Service {
	return &Service{
		db:  db,
		rdb: rdb,
	}
}

func (s *Service) GetDashboardStats(ctx context.Context, userID string) (*DashboardStats, error) {
	stats := &DashboardStats{}

	// Count strategies
	s.db.WithContext(ctx).Model(&struct{ TableName string `gorm:"tableName:strategies"`}{}).
		Where("user_id = ?", userID).Count(&stats.TotalStrategies)
	
	s.db.WithContext(ctx).Model(&struct{ TableName string `gorm:"tableName:strategies"`}{}).
		Where("user_id = ? AND status = ?", userID, "running").Count(&stats.ActiveStrategies)

	// Count positions
	s.db.WithContext(ctx).Model(&struct{ TableName string `gorm:"tableName:positions"`}{}).
		Where("user_id = ?", userID).Count(&stats.TotalPositions)
	
	s.db.WithContext(ctx).Model(&struct{ TableName string `gorm:"tableName:positions"`}{}).
		Where("user_id = ? AND status = ?", userID, "open").Count(&stats.OpenPositions)

	// Count orders
	s.db.WithContext(ctx).Model(&struct{ TableName string `gorm:"tableName:orders"`}{}).
		Where("user_id = ?", userID).Count(&stats.TotalOrders)
	
	s.db.WithContext(ctx).Model(&struct{ TableName string `gorm:"tableName:orders"`}{}).
		Where("user_id = ? AND status IN (?)", userID, []string{"NEW", "PARTIALLY_FILLED"}).Count(&stats.PendingOrders)

	// Default values for financial calculations
	stats.TotalPortfolio = decimal.Zero
	stats.UnrealizedPL = decimal.Zero
	stats.RealizedPL = decimal.Zero

	return stats, nil
}