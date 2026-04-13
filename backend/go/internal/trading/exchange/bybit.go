package exchange

import (
	"context"
	"strconv"
	"time"
)

// BybitAdapter implements ExchangeAdapter for Bybit (spot + linear futures).
type BybitAdapter struct {
	apiKey    string
	apiSecret string
	baseURL   string
}

func NewBybitAdapter(apiKey, apiSecret string) *BybitAdapter {
	return &BybitAdapter{
		apiKey:    apiKey,
		apiSecret: apiSecret,
		baseURL:   "https://api.bybit.com",
	}
}

func (b *BybitAdapter) GetBalance(ctx context.Context, asset string) (*Balance, error) {
	return &Balance{Asset: asset}, nil
}

func (b *BybitAdapter) CreateOrder(ctx context.Context, order *OrderRequest) (*OrderResponse, error) {
	return &OrderResponse{OrderID: "bybit-" + strconv.FormatInt(time.Now().UnixNano(), 10)}, nil
}

func (b *BybitAdapter) CancelOrder(ctx context.Context, orderID string) error { return nil }

func (b *BybitAdapter) GetOrder(ctx context.Context, orderID string) (*OrderResponse, error) {
	return &OrderResponse{OrderID: orderID}, nil
}

func (b *BybitAdapter) GetOpenOrders(ctx context.Context, symbol string) ([]*OrderResponse, error) {
	return []*OrderResponse{}, nil
}

func (b *BybitAdapter) GetKlines(ctx context.Context, symbol, interval string, limit int) ([]*Kline, error) {
	return []*Kline{}, nil
}

func (b *BybitAdapter) GetTicker(ctx context.Context, symbol string) (*Ticker, error) {
	return &Ticker{Symbol: symbol}, nil
}

func (b *BybitAdapter) GetDepth(ctx context.Context, symbol string, limit int) (*OrderBook, error) {
	return &OrderBook{Symbol: symbol}, nil
}
