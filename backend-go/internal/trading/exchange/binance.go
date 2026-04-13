package exchange

import (
	"context"
	"crypto/hmac"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"net/http"
	"net/url"
	"strconv"
	"time"

	"github.com/shopspring/decimal"
)

type BinanceAdapter struct {
	apiKey    string
	apiSecret string
	baseURL   string
	client    *http.Client
}

func NewBinanceAdapter(apiKey, apiSecret string) *BinanceAdapter {
	return &BinanceAdapter{
		apiKey:    apiKey,
		apiSecret: apiSecret,
		baseURL:   "https://api.binance.com",
		client:    &http.Client{Timeout: 30 * time.Second},
	}
}

func (b *BinanceAdapter) GetBalance(ctx context.Context, asset string) (*Balance, error) {
	endpoint := "/api/v3/account"
	params := url.Values{}
	params.Set("timestamp", strconv.FormatInt(time.Now().UnixMilli(), 10))

	signature := b.sign(params.Encode())
	params.Set("signature", signature)

	req, err := http.NewRequestWithContext(ctx, "GET", b.baseURL+endpoint+"?"+params.Encode(), nil)
	if err != nil {
		return nil, err
	}

	req.Header.Set("X-MBX-APIKEY", b.apiKey)

	resp, err := b.client.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	var account struct {
		Balances []struct {
			Asset  string `json:"asset"`
			Free   string `json:"free"`
			Locked string `json:"locked"`
		} `json:"balances"`
	}

	if err := json.NewDecoder(resp.Body).Decode(&account); err != nil {
		return nil, err
	}

	for _, balance := range account.Balances {
		if balance.Asset == asset {
			free, _ := decimal.NewFromString(balance.Free)
			locked, _ := decimal.NewFromString(balance.Locked)
			return &Balance{
				Asset:  balance.Asset,
				Free:   free,
				Locked: locked,
			}, nil
		}
	}

	return &Balance{
		Asset:  asset,
		Free:   decimal.Zero,
		Locked: decimal.Zero,
	}, nil
}

func (b *BinanceAdapter) CreateOrder(ctx context.Context, order *OrderRequest) (*OrderResponse, error) {
	endpoint := "/api/v3/order"
	params := url.Values{}
	params.Set("symbol", order.Symbol)
	params.Set("side", order.Side)
	params.Set("type", order.Type)
	params.Set("quantity", order.Quantity.String())
	
	if !order.Price.IsZero() {
		params.Set("price", order.Price.String())
	}
	if order.TimeInForce != "" {
		params.Set("timeInForce", order.TimeInForce)
	}
	params.Set("timestamp", strconv.FormatInt(time.Now().UnixMilli(), 10))

	signature := b.sign(params.Encode())
	params.Set("signature", signature)

	req, err := http.NewRequestWithContext(ctx, "POST", b.baseURL+endpoint, nil)
	if err != nil {
		return nil, err
	}

	req.Header.Set("X-MBX-APIKEY", b.apiKey)
	req.Header.Set("Content-Type", "application/x-www-form-urlencoded")
	req.Body = http.NoBody

	// Add params to URL since it's a POST with query params
	req.URL.RawQuery = params.Encode()

	resp, err := b.client.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	var orderResp struct {
		OrderID       int64  `json:"orderId"`
		ClientOrderID string `json:"clientOrderId"`
		Symbol        string `json:"symbol"`
		Side          string `json:"side"`
		Type          string `json:"type"`
		Quantity      string `json:"origQty"`
		Price         string `json:"price"`
		ExecutedQty   string `json:"executedQty"`
		Status        string `json:"status"`
		TimeInForce   string `json:"timeInForce"`
		TransactTime  int64  `json:"transactTime"`
	}

	if err := json.NewDecoder(resp.Body).Decode(&orderResp); err != nil {
		return nil, err
	}

	quantity, _ := decimal.NewFromString(orderResp.Quantity)
	price, _ := decimal.NewFromString(orderResp.Price)
	executedQty, _ := decimal.NewFromString(orderResp.ExecutedQty)

	return &OrderResponse{
		OrderID:       strconv.FormatInt(orderResp.OrderID, 10),
		ClientOrderID: orderResp.ClientOrderID,
		Symbol:        orderResp.Symbol,
		Side:          orderResp.Side,
		Type:          orderResp.Type,
		Quantity:      quantity,
		Price:         price,
		ExecutedQty:   executedQty,
		Status:        orderResp.Status,
		TimeInForce:   orderResp.TimeInForce,
		CreatedAt:     orderResp.TransactTime,
		UpdatedAt:     orderResp.TransactTime,
	}, nil
}

func (b *BinanceAdapter) CancelOrder(ctx context.Context, orderID string) error {
	// Implementation for cancel order
	return nil
}

func (b *BinanceAdapter) GetOrder(ctx context.Context, orderID string) (*OrderResponse, error) {
	// Implementation for get order
	return nil, nil
}

func (b *BinanceAdapter) GetOpenOrders(ctx context.Context, symbol string) ([]*OrderResponse, error) {
	// Implementation for get open orders
	return nil, nil
}

func (b *BinanceAdapter) GetKlines(ctx context.Context, symbol, interval string, limit int) ([]*Kline, error) {
	// Implementation for get klines
	return nil, nil
}

func (b *BinanceAdapter) GetTicker(ctx context.Context, symbol string) (*Ticker, error) {
	// Implementation for get ticker
	return nil, nil
}

func (b *BinanceAdapter) GetDepth(ctx context.Context, symbol string, limit int) (*OrderBook, error) {
	// Implementation for get order book
	return nil, nil
}

func (b *BinanceAdapter) sign(message string) string {
	h := hmac.New(sha256.New, []byte(b.apiSecret))
	h.Write([]byte(message))
	return hex.EncodeToString(h.Sum(nil))
}