package exchange

import (
	"context"
	"strconv"
	"time"
)

// BitgetAdapter implements ExchangeAdapter for Bitget (futures + spot + copy trading).
type BitgetAdapter struct {
	apiKey     string
	apiSecret  string
	passphrase string
	baseURL    string
}

func NewBitgetAdapter(apiKey, apiSecret, passphrase string) *BitgetAdapter {
	return &BitgetAdapter{
		apiKey:     apiKey,
		apiSecret:  apiSecret,
		passphrase: passphrase,
		baseURL:    "https://api.bitget.com",
	}
}

func (b *BitgetAdapter) GetBalance(ctx context.Context, asset string) (*Balance, error) {
	return &Balance{Asset: asset}, nil
}

func (b *BitgetAdapter) CreateOrder(ctx context.Context, order *OrderRequest) (*OrderResponse, error) {
	return &OrderResponse{OrderID: "bitget-" + strconv.FormatInt(time.Now().UnixNano(), 10)}, nil
}

func (b *BitgetAdapter) CancelOrder(ctx context.Context, orderID string) error { return nil }

func (b *BitgetAdapter) GetOrder(ctx context.Context, orderID string) (*OrderResponse, error) {
	return &OrderResponse{OrderID: orderID}, nil
}

func (b *BitgetAdapter) GetOpenOrders(ctx context.Context, symbol string) ([]*OrderResponse, error) {
	return []*OrderResponse{}, nil
}

func (b *BitgetAdapter) GetKlines(ctx context.Context, symbol, interval string, limit int) ([]*Kline, error) {
	return []*Kline{}, nil
}

func (b *BitgetAdapter) GetTicker(ctx context.Context, symbol string) (*Ticker, error) {
	return &Ticker{Symbol: symbol}, nil
}

func (b *BitgetAdapter) GetDepth(ctx context.Context, symbol string, limit int) (*OrderBook, error) {
	return &OrderBook{Symbol: symbol}, nil
}
