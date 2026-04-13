package position

import (
	"context"
	"strconv"
	"time"

	"github.com/shopspring/decimal"
	"gorm.io/gorm"
)

type Service struct {
	db *gorm.DB
}

type PositionSummary struct {
	TotalPositions    int64           `json:"total_positions"`
	OpenPositions     int64           `json:"open_positions"`
	TotalUnrealizedPL decimal.Decimal `json:"total_unrealized_pl"`
	TotalRealizedPL   decimal.Decimal `json:"total_realized_pl"`
	TotalMarketValue  decimal.Decimal `json:"total_market_value"`
}

func NewService(db *gorm.DB) *Service {
	return &Service{db: db}
}

func (s *Service) ListPositions(ctx context.Context, userID, pageStr, limitStr, symbol, status string) ([]*Position, int64, error) {
	page, err := strconv.Atoi(pageStr)
	if err != nil {
		page = 1
	}

	limit, err := strconv.Atoi(limitStr)
	if err != nil {
		limit = 20
	}

	offset := (page - 1) * limit

	query := s.db.WithContext(ctx).Where("user_id = ?", userID)

	if symbol != "" {
		query = query.Where("symbol = ?", symbol)
	}
	if status != "" {
		query = query.Where("status = ?", status)
	}

	var positions []*Position
	err = query.Order("created_at DESC").Limit(limit).Offset(offset).Find(&positions).Error
	if err != nil {
		return nil, 0, err
	}

	var total int64
	countQuery := s.db.WithContext(ctx).Model(&Position{}).Where("user_id = ?", userID)
	if symbol != "" {
		countQuery = countQuery.Where("symbol = ?", symbol)
	}
	if status != "" {
		countQuery = countQuery.Where("status = ?", status)
	}

	err = countQuery.Count(&total).Error
	return positions, total, err
}

func (s *Service) GetPosition(ctx context.Context, userID, positionID string) (*Position, error) {
	var position Position
	err := s.db.WithContext(ctx).Where("id = ? AND user_id = ?", positionID, userID).First(&position).Error
	return &position, err
}

func (s *Service) ClosePosition(ctx context.Context, userID, positionID string) error {
	var position Position
	if err := s.db.WithContext(ctx).Where("id = ? AND user_id = ?", positionID, userID).First(&position).Error; err != nil {
		return err
	}

	now := time.Now()
	position.Status = "CLOSED"
	position.ClosedAt = &now

	return s.db.WithContext(ctx).Save(&position).Error
}

func (s *Service) GetOpenPositions(ctx context.Context, userID string) ([]*Position, error) {
	var positions []*Position
	err := s.db.WithContext(ctx).
		Where("user_id = ? AND status = ?", userID, "OPEN").
		Order("created_at DESC").
		Find(&positions).Error
	return positions, err
}

func (s *Service) GetPositionSummary(ctx context.Context, userID string) (*PositionSummary, error) {
	var summary PositionSummary

	// Count total and open positions
	s.db.WithContext(ctx).Model(&Position{}).Where("user_id = ?", userID).Count(&summary.TotalPositions)
	s.db.WithContext(ctx).Model(&Position{}).Where("user_id = ? AND status = ?", userID, "OPEN").Count(&summary.OpenPositions)

	// Calculate totals
	var unrealizedPL, realizedPL, marketValue decimal.Decimal
	
	rows, err := s.db.WithContext(ctx).Model(&Position{}).
		Select("SUM(unrealized_pl) as total_unrealized, SUM(realized_pl) as total_realized, SUM(market_value) as total_market").
		Where("user_id = ?", userID).Rows()
	
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	if rows.Next() {
		var totalUnrealized, totalRealized, totalMarket interface{}
		rows.Scan(&totalUnrealized, &totalRealized, &totalMarket)
		
		if totalUnrealized != nil {
			unrealizedPL, _ = decimal.NewFromString(totalUnrealized.(string))
		}
		if totalRealized != nil {
			realizedPL, _ = decimal.NewFromString(totalRealized.(string))
		}
		if totalMarket != nil {
			marketValue, _ = decimal.NewFromString(totalMarket.(string))
		}
	}

	summary.TotalUnrealizedPL = unrealizedPL
	summary.TotalRealizedPL = realizedPL
	summary.TotalMarketValue = marketValue

	return &summary, nil
}