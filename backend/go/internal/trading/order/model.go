package order

import (
	"time"

	"github.com/google/uuid"
	"github.com/shopspring/decimal"
	"gorm.io/gorm"
)

type Order struct {
	ID              uuid.UUID       `gorm:"type:uuid;primaryKey;default:gen_random_uuid()" json:"id"`
	UserID          uuid.UUID       `gorm:"type:uuid;not null;index" json:"user_id"`
	StrategyID      uuid.UUID       `gorm:"type:uuid;index" json:"strategy_id"`
	ExchangeOrderID string          `gorm:"size:100;index" json:"exchange_order_id"`
	ClientOrderID   string          `gorm:"size:100;index" json:"client_order_id"`
	Exchange        string          `gorm:"size:20;not null;index" json:"exchange"`
	Symbol          string          `gorm:"size:20;not null;index" json:"symbol"`
	Side            string          `gorm:"size:10;not null" json:"side"` // BUY, SELL
	Type            string          `gorm:"size:20;not null" json:"type"` // MARKET, LIMIT, STOP_LOSS, etc.
	Status          string          `gorm:"size:20;not null;index" json:"status"` // NEW, PARTIALLY_FILLED, FILLED, CANCELED, REJECTED
	TimeInForce     string          `gorm:"size:10" json:"time_in_force"` // GTC, IOC, FOK
	Quantity        decimal.Decimal `gorm:"type:decimal(20,8);not null" json:"quantity"`
	Price           decimal.Decimal `gorm:"type:decimal(20,8)" json:"price"`
	StopPrice       decimal.Decimal `gorm:"type:decimal(20,8)" json:"stop_price"`
	ExecutedQty     decimal.Decimal `gorm:"type:decimal(20,8);default:0" json:"executed_qty"`
	ExecutedValue   decimal.Decimal `gorm:"type:decimal(20,8);default:0" json:"executed_value"`
	Commission      decimal.Decimal `gorm:"type:decimal(20,8);default:0" json:"commission"`
	CommissionAsset string          `gorm:"size:10" json:"commission_asset"`
	CreatedAt       time.Time       `json:"created_at"`
	UpdatedAt       time.Time       `json:"updated_at"`
	DeletedAt       gorm.DeletedAt  `gorm:"index" json:"-"`
}

type OrderFill struct {
	ID            uuid.UUID       `gorm:"type:uuid;primaryKey;default:gen_random_uuid()" json:"id"`
	OrderID       uuid.UUID       `gorm:"type:uuid;not null;index" json:"order_id"`
	TradeID       string          `gorm:"size:100;not null" json:"trade_id"`
	Price         decimal.Decimal `gorm:"type:decimal(20,8);not null" json:"price"`
	Quantity      decimal.Decimal `gorm:"type:decimal(20,8);not null" json:"quantity"`
	Commission    decimal.Decimal `gorm:"type:decimal(20,8);default:0" json:"commission"`
	CommissionAsset string        `gorm:"size:10" json:"commission_asset"`
	CreatedAt     time.Time       `json:"created_at"`
}

func (Order) TableName() string {
	return "orders"
}

func (OrderFill) TableName() string {
	return "order_fills"
}