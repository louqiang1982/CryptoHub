package exchange

import (
	"context"
	"strconv"
	"time"
)

// CoinbaseAdapter implements ExchangeAdapter for Coinbase Advanced Trade API.
type CoinbaseAdapter struct {
	apiKey    string
	apiSecret string
	baseURL   string
}

func NewCoinbaseAdapter(apiKey, apiSecret string) *CoinbaseAdapter {
	return &CoinbaseAdapter{
		apiKey:    apiKey,
		apiSecret: apiSecret,
		baseURL:   "https://api.coinbase.com",
	}
}

func (c *CoinbaseAdapter) GetBalance(ctx context.Context, asset string) (*Balance, error) {
	return &Balance{Asset: asset}, nil
}

func (c *CoinbaseAdapter) CreateOrder(ctx context.Context, order *OrderRequest) (*OrderResponse, error) {
	return &OrderResponse{OrderID: "coinbase-" + strconv.FormatInt(time.Now().UnixNano(), 10)}, nil
}

func (c *CoinbaseAdapter) CancelOrder(ctx context.Context, orderID string) error { return nil }

func (c *CoinbaseAdapter) GetOrder(ctx context.Context, orderID string) (*OrderResponse, error) {
	return &OrderResponse{OrderID: orderID}, nil
}

func (c *CoinbaseAdapter) GetOpenOrders(ctx context.Context, symbol string) ([]*OrderResponse, error) {
	return []*OrderResponse{}, nil
}

func (c *CoinbaseAdapter) GetKlines(ctx context.Context, symbol, interval string, limit int) ([]*Kline, error) {
	return []*Kline{}, nil
}

func (c *CoinbaseAdapter) GetTicker(ctx context.Context, symbol string) (*Ticker, error) {
	return &Ticker{Symbol: symbol}, nil
}

func (c *CoinbaseAdapter) GetDepth(ctx context.Context, symbol string, limit int) (*OrderBook, error) {
	return &OrderBook{Symbol: symbol}, nil
}
