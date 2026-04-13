package kline

import (
	"context"
	"gorm.io/gorm"
)

type Service struct{ db *gorm.DB }

func NewService(db *gorm.DB) *Service { return &Service{db} }

func (s *Service) GetKlines(ctx context.Context, symbol, interval string) ([]interface{}, error) {
	return []interface{}{}, nil
}
