package exchange

import (
	"context"
	"strconv"
	"time"
)

// KrakenAdapter implements ExchangeAdapter for Kraken (spot + futures).
type KrakenAdapter struct {
	apiKey    string
	apiSecret string
	baseURL   string
}

func NewKrakenAdapter(apiKey, apiSecret string) *KrakenAdapter {
	return &KrakenAdapter{
		apiKey:    apiKey,
		apiSecret: apiSecret,
		baseURL:   "https://api.kraken.com",
	}
}

func (k *KrakenAdapter) GetBalance(ctx context.Context, asset string) (*Balance, error) {
	return &Balance{Asset: asset}, nil
}

func (k *KrakenAdapter) CreateOrder(ctx context.Context, order *OrderRequest) (*OrderResponse, error) {
	return &OrderResponse{OrderID: "kraken-" + strconv.FormatInt(time.Now().UnixNano(), 10)}, nil
}

func (k *KrakenAdapter) CancelOrder(ctx context.Context, orderID string) error { return nil }

func (k *KrakenAdapter) GetOrder(ctx context.Context, orderID string) (*OrderResponse, error) {
	return &OrderResponse{OrderID: orderID}, nil
}

func (k *KrakenAdapter) GetOpenOrders(ctx context.Context, symbol string) ([]*OrderResponse, error) {
	return []*OrderResponse{}, nil
}

func (k *KrakenAdapter) GetKlines(ctx context.Context, symbol, interval string, limit int) ([]*Kline, error) {
	return []*Kline{}, nil
}

func (k *KrakenAdapter) GetTicker(ctx context.Context, symbol string) (*Ticker, error) {
	return &Ticker{Symbol: symbol}, nil
}

func (k *KrakenAdapter) GetDepth(ctx context.Context, symbol string, limit int) (*OrderBook, error) {
	return &OrderBook{Symbol: symbol}, nil
}
