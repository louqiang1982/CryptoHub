package exchange

import (
	"context"
	"strconv"
	"time"
)

// KuCoinAdapter implements ExchangeAdapter for KuCoin (spot + futures).
type KuCoinAdapter struct {
	apiKey    string
	apiSecret string
	passphrase string
	baseURL   string
}

func NewKuCoinAdapter(apiKey, apiSecret, passphrase string) *KuCoinAdapter {
	return &KuCoinAdapter{
		apiKey:     apiKey,
		apiSecret:  apiSecret,
		passphrase: passphrase,
		baseURL:    "https://api.kucoin.com",
	}
}

func (k *KuCoinAdapter) GetBalance(ctx context.Context, asset string) (*Balance, error) {
	return &Balance{Asset: asset}, nil
}

func (k *KuCoinAdapter) CreateOrder(ctx context.Context, order *OrderRequest) (*OrderResponse, error) {
	return &OrderResponse{OrderID: "kucoin-" + strconv.FormatInt(time.Now().UnixNano(), 10)}, nil
}

func (k *KuCoinAdapter) CancelOrder(ctx context.Context, orderID string) error { return nil }

func (k *KuCoinAdapter) GetOrder(ctx context.Context, orderID string) (*OrderResponse, error) {
	return &OrderResponse{OrderID: orderID}, nil
}

func (k *KuCoinAdapter) GetOpenOrders(ctx context.Context, symbol string) ([]*OrderResponse, error) {
	return []*OrderResponse{}, nil
}

func (k *KuCoinAdapter) GetKlines(ctx context.Context, symbol, interval string, limit int) ([]*Kline, error) {
	return []*Kline{}, nil
}

func (k *KuCoinAdapter) GetTicker(ctx context.Context, symbol string) (*Ticker, error) {
	return &Ticker{Symbol: symbol}, nil
}

func (k *KuCoinAdapter) GetDepth(ctx context.Context, symbol string, limit int) (*OrderBook, error) {
	return &OrderBook{Symbol: symbol}, nil
}
