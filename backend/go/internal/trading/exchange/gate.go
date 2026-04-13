package exchange

import (
	"context"
	"strconv"
	"time"
)

// GateAdapter implements ExchangeAdapter for Gate.io (spot + futures).
type GateAdapter struct {
	apiKey    string
	apiSecret string
	baseURL   string
}

func NewGateAdapter(apiKey, apiSecret string) *GateAdapter {
	return &GateAdapter{
		apiKey:    apiKey,
		apiSecret: apiSecret,
		baseURL:   "https://api.gateio.ws",
	}
}

func (g *GateAdapter) GetBalance(ctx context.Context, asset string) (*Balance, error) {
	return &Balance{Asset: asset}, nil
}

func (g *GateAdapter) CreateOrder(ctx context.Context, order *OrderRequest) (*OrderResponse, error) {
	return &OrderResponse{OrderID: "gate-" + strconv.FormatInt(time.Now().UnixNano(), 10)}, nil
}

func (g *GateAdapter) CancelOrder(ctx context.Context, orderID string) error { return nil }

func (g *GateAdapter) GetOrder(ctx context.Context, orderID string) (*OrderResponse, error) {
	return &OrderResponse{OrderID: orderID}, nil
}

func (g *GateAdapter) GetOpenOrders(ctx context.Context, symbol string) ([]*OrderResponse, error) {
	return []*OrderResponse{}, nil
}

func (g *GateAdapter) GetKlines(ctx context.Context, symbol, interval string, limit int) ([]*Kline, error) {
	return []*Kline{}, nil
}

func (g *GateAdapter) GetTicker(ctx context.Context, symbol string) (*Ticker, error) {
	return &Ticker{Symbol: symbol}, nil
}

func (g *GateAdapter) GetDepth(ctx context.Context, symbol string, limit int) (*OrderBook, error) {
	return &OrderBook{Symbol: symbol}, nil
}
