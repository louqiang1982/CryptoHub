package position

import (
	"time"

	"github.com/google/uuid"
	"github.com/shopspring/decimal"
	"gorm.io/gorm"
)

type Position struct {
	ID           uuid.UUID       `gorm:"type:uuid;primaryKey;default:gen_random_uuid()" json:"id"`
	UserID       uuid.UUID       `gorm:"type:uuid;not null;index" json:"user_id"`
	StrategyID   uuid.UUID       `gorm:"type:uuid;index" json:"strategy_id"`
	Exchange     string          `gorm:"size:20;not null;index" json:"exchange"`
	Symbol       string          `gorm:"size:20;not null;index" json:"symbol"`
	Side         string          `gorm:"size:10;not null" json:"side"` // LONG, SHORT
	Size         decimal.Decimal `gorm:"type:decimal(20,8);not null" json:"size"`
	EntryPrice   decimal.Decimal `gorm:"type:decimal(20,8);not null" json:"entry_price"`
	CurrentPrice decimal.Decimal `gorm:"type:decimal(20,8)" json:"current_price"`
	MarketValue  decimal.Decimal `gorm:"type:decimal(20,8)" json:"market_value"`
	UnrealizedPL decimal.Decimal `gorm:"type:decimal(20,8);default:0" json:"unrealized_pl"`
	RealizedPL   decimal.Decimal `gorm:"type:decimal(20,8);default:0" json:"realized_pl"`
	Status       string          `gorm:"size:20;not null;default:open" json:"status"` // OPEN, CLOSED
	OpenedAt     time.Time       `gorm:"not null" json:"opened_at"`
	ClosedAt     *time.Time      `json:"closed_at,omitempty"`
	CreatedAt    time.Time       `json:"created_at"`
	UpdatedAt    time.Time       `json:"updated_at"`
	DeletedAt    gorm.DeletedAt  `gorm:"index" json:"-"`
}

func (Position) TableName() string {
	return "positions"
}