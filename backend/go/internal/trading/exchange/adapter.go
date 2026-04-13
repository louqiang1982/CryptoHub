package exchange

import (
	"context"

	"github.com/shopspring/decimal"
)

type ExchangeAdapter interface {
	GetBalance(ctx context.Context, asset string) (*Balance, error)
	CreateOrder(ctx context.Context, order *OrderRequest) (*OrderResponse, error)
	CancelOrder(ctx context.Context, orderID string) error
	GetOrder(ctx context.Context, orderID string) (*OrderResponse, error)
	GetOpenOrders(ctx context.Context, symbol string) ([]*OrderResponse, error)
	GetKlines(ctx context.Context, symbol, interval string, limit int) ([]*Kline, error)
	GetTicker(ctx context.Context, symbol string) (*Ticker, error)
	GetDepth(ctx context.Context, symbol string, limit int) (*OrderBook, error)
}

type Balance struct {
	Asset  string          `json:"asset"`
	Free   decimal.Decimal `json:"free"`
	Locked decimal.Decimal `json:"locked"`
}

type OrderRequest struct {
	Symbol      string          `json:"symbol"`
	Side        string          `json:"side"` // BUY, SELL
	Type        string          `json:"type"` // MARKET, LIMIT, STOP_LOSS, etc.
	Quantity    decimal.Decimal `json:"quantity"`
	Price       decimal.Decimal `json:"price,omitempty"`
	StopPrice   decimal.Decimal `json:"stop_price,omitempty"`
	TimeInForce string          `json:"time_in_force,omitempty"` // GTC, IOC, FOK
}

type OrderResponse struct {
	OrderID       string          `json:"order_id"`
	ClientOrderID string          `json:"client_order_id"`
	Symbol        string          `json:"symbol"`
	Side          string          `json:"side"`
	Type          string          `json:"type"`
	Quantity      decimal.Decimal `json:"quantity"`
	Price         decimal.Decimal `json:"price"`
	ExecutedQty   decimal.Decimal `json:"executed_qty"`
	Status        string          `json:"status"`
	TimeInForce   string          `json:"time_in_force"`
	CreatedAt     int64           `json:"created_at"`
	UpdatedAt     int64           `json:"updated_at"`
}

type Kline struct {
	OpenTime  int64           `json:"open_time"`
	CloseTime int64           `json:"close_time"`
	Open      decimal.Decimal `json:"open"`
	High      decimal.Decimal `json:"high"`
	Low       decimal.Decimal `json:"low"`
	Close     decimal.Decimal `json:"close"`
	Volume    decimal.Decimal `json:"volume"`
}

type Ticker struct {
	Symbol             string          `json:"symbol"`
	PriceChange        decimal.Decimal `json:"price_change"`
	PriceChangePercent decimal.Decimal `json:"price_change_percent"`
	WeightedAvgPrice   decimal.Decimal `json:"weighted_avg_price"`
	PrevClosePrice     decimal.Decimal `json:"prev_close_price"`
	LastPrice          decimal.Decimal `json:"last_price"`
	LastQty            decimal.Decimal `json:"last_qty"`
	BidPrice           decimal.Decimal `json:"bid_price"`
	AskPrice           decimal.Decimal `json:"ask_price"`
	OpenPrice          decimal.Decimal `json:"open_price"`
	HighPrice          decimal.Decimal `json:"high_price"`
	LowPrice           decimal.Decimal `json:"low_price"`
	Volume             decimal.Decimal `json:"volume"`
	QuoteVolume        decimal.Decimal `json:"quote_volume"`
	OpenTime           int64           `json:"open_time"`
	CloseTime          int64           `json:"close_time"`
	Count              int64           `json:"count"`
}

type OrderBook struct {
	Symbol string      `json:"symbol"`
	Bids   []PriceLevel `json:"bids"`
	Asks   []PriceLevel `json:"asks"`
}

type PriceLevel struct {
	Price    decimal.Decimal `json:"price"`
	Quantity decimal.Decimal `json:"quantity"`
}