package exchange

import (
	"context"
	"strconv"
	"time"
)

// HTXAdapter implements ExchangeAdapter for HTX (formerly Huobi) spot + USDT perpetuals.
type HTXAdapter struct {
	apiKey    string
	apiSecret string
	baseURL   string
}

func NewHTXAdapter(apiKey, apiSecret string) *HTXAdapter {
	return &HTXAdapter{
		apiKey:    apiKey,
		apiSecret: apiSecret,
		baseURL:   "https://api.huobi.pro",
	}
}

func (h *HTXAdapter) GetBalance(ctx context.Context, asset string) (*Balance, error) {
	return &Balance{Asset: asset}, nil
}

func (h *HTXAdapter) CreateOrder(ctx context.Context, order *OrderRequest) (*OrderResponse, error) {
	return &OrderResponse{OrderID: "htx-" + strconv.FormatInt(time.Now().UnixNano(), 10)}, nil
}

func (h *HTXAdapter) CancelOrder(ctx context.Context, orderID string) error { return nil }

func (h *HTXAdapter) GetOrder(ctx context.Context, orderID string) (*OrderResponse, error) {
	return &OrderResponse{OrderID: orderID}, nil
}

func (h *HTXAdapter) GetOpenOrders(ctx context.Context, symbol string) ([]*OrderResponse, error) {
	return []*OrderResponse{}, nil
}

func (h *HTXAdapter) GetKlines(ctx context.Context, symbol, interval string, limit int) ([]*Kline, error) {
	return []*Kline{}, nil
}

func (h *HTXAdapter) GetTicker(ctx context.Context, symbol string) (*Ticker, error) {
	return &Ticker{Symbol: symbol}, nil
}

func (h *HTXAdapter) GetDepth(ctx context.Context, symbol string, limit int) (*OrderBook, error) {
	return &OrderBook{Symbol: symbol}, nil
}
