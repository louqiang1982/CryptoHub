package exchange

import (
	"context"
	"strconv"
	"time"
)

// DeepcoinAdapter implements ExchangeAdapter for DeepCoin derivatives exchange.
type DeepcoinAdapter struct {
	apiKey    string
	apiSecret string
	baseURL   string
}

func NewDeepcoinAdapter(apiKey, apiSecret string) *DeepcoinAdapter {
	return &DeepcoinAdapter{
		apiKey:    apiKey,
		apiSecret: apiSecret,
		baseURL:   "https://api.deepcoin.com",
	}
}

func (d *DeepcoinAdapter) GetBalance(ctx context.Context, asset string) (*Balance, error) {
	return &Balance{Asset: asset}, nil
}

func (d *DeepcoinAdapter) CreateOrder(ctx context.Context, order *OrderRequest) (*OrderResponse, error) {
	return &OrderResponse{OrderID: "deepcoin-" + strconv.FormatInt(time.Now().UnixNano(), 10)}, nil
}

func (d *DeepcoinAdapter) CancelOrder(ctx context.Context, orderID string) error { return nil }

func (d *DeepcoinAdapter) GetOrder(ctx context.Context, orderID string) (*OrderResponse, error) {
	return &OrderResponse{OrderID: orderID}, nil
}

func (d *DeepcoinAdapter) GetOpenOrders(ctx context.Context, symbol string) ([]*OrderResponse, error) {
	return []*OrderResponse{}, nil
}

func (d *DeepcoinAdapter) GetKlines(ctx context.Context, symbol, interval string, limit int) ([]*Kline, error) {
	return []*Kline{}, nil
}

func (d *DeepcoinAdapter) GetTicker(ctx context.Context, symbol string) (*Ticker, error) {
	return &Ticker{Symbol: symbol}, nil
}

func (d *DeepcoinAdapter) GetDepth(ctx context.Context, symbol string, limit int) (*OrderBook, error) {
	return &OrderBook{Symbol: symbol}, nil
}
