package portfolio

import (
	"context"

	"gorm.io/gorm"
)

type Service struct{ db *gorm.DB }

func NewService(db *gorm.DB) *Service { return &Service{db} }

func (s *Service) ListPortfolios(ctx context.Context, userID string) ([]Portfolio, error) {
	return []Portfolio{}, nil
}
