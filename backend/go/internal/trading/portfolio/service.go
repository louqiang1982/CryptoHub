package portfolio

import (
	"context"
	"errors"

	"github.com/google/uuid"
	"github.com/shopspring/decimal"
	"gorm.io/gorm"
)

type Service struct {
	db *gorm.DB
}

func NewService(db *gorm.DB) *Service { return &Service{db: db} }

// CreateRequest contains the fields needed to create a portfolio.
type CreateRequest struct {
	Name         string `json:"name" binding:"required"`
	Type         string `json:"type"`
	Exchange     string `json:"exchange" binding:"required"`
	BaseCurrency string `json:"base_currency"`
}

// UpdateRequest contains the fields that can be updated.
type UpdateRequest struct {
	Name         string `json:"name"`
	Type         string `json:"type"`
	BaseCurrency string `json:"base_currency"`
}

// Summary provides aggregated statistics for a user's portfolios.
type Summary struct {
	TotalPortfolios int             `json:"total_portfolios"`
	TotalValue      decimal.Decimal `json:"total_value"`
	TotalUnrealized decimal.Decimal `json:"total_unrealized_pl"`
	TotalRealized   decimal.Decimal `json:"total_realized_pl"`
}

// ListPortfolios returns all portfolios belonging to a user.
func (s *Service) ListPortfolios(ctx context.Context, userID string) ([]Portfolio, error) {
	var portfolios []Portfolio
	if err := s.db.WithContext(ctx).Where("user_id = ?", userID).Order("created_at DESC").Find(&portfolios).Error; err != nil {
		return nil, err
	}
	return portfolios, nil
}

// GetPortfolio returns a single portfolio if it belongs to the user.
func (s *Service) GetPortfolio(ctx context.Context, userID, portfolioID string) (*Portfolio, error) {
	var p Portfolio
	if err := s.db.WithContext(ctx).Where("id = ? AND user_id = ?", portfolioID, userID).First(&p).Error; err != nil {
		if errors.Is(err, gorm.ErrRecordNotFound) {
			return nil, errors.New("portfolio not found")
		}
		return nil, err
	}
	return &p, nil
}

// CreatePortfolio creates a new portfolio for a user.
func (s *Service) CreatePortfolio(ctx context.Context, userID string, req *CreateRequest) (*Portfolio, error) {
	uid, err := uuid.Parse(userID)
	if err != nil {
		return nil, errors.New("invalid user ID")
	}

	baseCurrency := req.BaseCurrency
	if baseCurrency == "" {
		baseCurrency = "USDT"
	}
	pType := req.Type
	if pType == "" {
		pType = "live"
	}

	p := Portfolio{
		ID:           uuid.New(),
		UserID:       uid,
		Name:         req.Name,
		Type:         pType,
		Exchange:     req.Exchange,
		BaseCurrency: baseCurrency,
	}

	if err := s.db.WithContext(ctx).Create(&p).Error; err != nil {
		return nil, err
	}
	return &p, nil
}

// UpdatePortfolio updates an existing portfolio.
func (s *Service) UpdatePortfolio(ctx context.Context, userID, portfolioID string, req *UpdateRequest) (*Portfolio, error) {
	p, err := s.GetPortfolio(ctx, userID, portfolioID)
	if err != nil {
		return nil, err
	}

	updates := map[string]interface{}{}
	if req.Name != "" {
		updates["name"] = req.Name
	}
	if req.Type != "" {
		updates["type"] = req.Type
	}
	if req.BaseCurrency != "" {
		updates["base_currency"] = req.BaseCurrency
	}

	if len(updates) > 0 {
		if err := s.db.WithContext(ctx).Model(p).Updates(updates).Error; err != nil {
			return nil, err
		}
	}

	return s.GetPortfolio(ctx, userID, portfolioID)
}

// DeletePortfolio soft-deletes a portfolio.
func (s *Service) DeletePortfolio(ctx context.Context, userID, portfolioID string) error {
	result := s.db.WithContext(ctx).Where("id = ? AND user_id = ?", portfolioID, userID).Delete(&Portfolio{})
	if result.Error != nil {
		return result.Error
	}
	if result.RowsAffected == 0 {
		return errors.New("portfolio not found")
	}
	return nil
}

// GetSummary returns aggregated statistics across all portfolios for a user.
func (s *Service) GetSummary(ctx context.Context, userID string) (*Summary, error) {
	portfolios, err := s.ListPortfolios(ctx, userID)
	if err != nil {
		return nil, err
	}

	summary := &Summary{
		TotalPortfolios: len(portfolios),
		TotalValue:      decimal.Zero,
		TotalUnrealized: decimal.Zero,
		TotalRealized:   decimal.Zero,
	}

	for _, p := range portfolios {
		summary.TotalValue = summary.TotalValue.Add(p.TotalValue)
		summary.TotalUnrealized = summary.TotalUnrealized.Add(p.UnrealizedPL)
		summary.TotalRealized = summary.TotalRealized.Add(p.RealizedPL)
	}

	return summary, nil
}
