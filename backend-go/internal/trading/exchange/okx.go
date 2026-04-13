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

// OKXAdapter implements ExchangeAdapter for OKX (spot + perpetual + options).
type OKXAdapter struct {
	apiKey     string
	apiSecret  string
	passphrase string
	baseURL    string
	client     *http.Client
}

func NewOKXAdapter(apiKey, apiSecret, passphrase string) *OKXAdapter {
	return &OKXAdapter{
		apiKey:     apiKey,
		apiSecret:  apiSecret,
		passphrase: passphrase,
		baseURL:    "https://www.okx.com",
		client:     &http.Client{Timeout: 30 * time.Second},
	}
}

func (o *OKXAdapter) sign(timestamp, method, path, body string) string {
	prehash := timestamp + method + path + body
	mac := hmac.New(sha256.New, []byte(o.apiSecret))
	mac.Write([]byte(prehash))
	return hex.EncodeToString(mac.Sum(nil))
}

func (o *OKXAdapter) GetBalance(ctx context.Context, asset string) (*Balance, error) {
	timestamp := time.Now().UTC().Format(time.RFC3339)
	path := "/api/v5/account/balance?ccy=" + asset
	sig := o.sign(timestamp, "GET", path, "")

	req, err := http.NewRequestWithContext(ctx, "GET", o.baseURL+path, nil)
	if err != nil {
		return nil, err
	}
	req.Header.Set("OK-ACCESS-KEY", o.apiKey)
	req.Header.Set("OK-ACCESS-SIGN", sig)
	req.Header.Set("OK-ACCESS-TIMESTAMP", timestamp)
	req.Header.Set("OK-ACCESS-PASSPHRASE", o.passphrase)

	resp, err := o.client.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	var result struct {
		Data []struct {
			Details []struct {
				Ccy     string `json:"ccy"`
				AvailBal string `json:"availBal"`
				FrozenBal string `json:"frozenBal"`
			} `json:"details"`
		} `json:"data"`
	}
	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		return nil, err
	}

	for _, d := range result.Data {
		for _, detail := range d.Details {
			if detail.Ccy == asset {
				free, _ := decimal.NewFromString(detail.AvailBal)
				locked, _ := decimal.NewFromString(detail.FrozenBal)
				return &Balance{Asset: asset, Free: free, Locked: locked}, nil
			}
		}
	}
	return &Balance{Asset: asset}, nil
}

func (o *OKXAdapter) CreateOrder(ctx context.Context, order *OrderRequest) (*OrderResponse, error) {
	// OKX order creation via POST /api/v5/trade/order
	return &OrderResponse{OrderID: "okx-stub-" + strconv.FormatInt(time.Now().UnixNano(), 10)}, nil
}

func (o *OKXAdapter) CancelOrder(ctx context.Context, orderID string) error {
	return nil
}

func (o *OKXAdapter) GetOrder(ctx context.Context, orderID string) (*OrderResponse, error) {
	return &OrderResponse{OrderID: orderID}, nil
}

func (o *OKXAdapter) GetOpenOrders(ctx context.Context, symbol string) ([]*OrderResponse, error) {
	return []*OrderResponse{}, nil
}

func (o *OKXAdapter) GetKlines(ctx context.Context, symbol, interval string, limit int) ([]*Kline, error) {
	params := url.Values{}
	params.Set("instId", symbol)
	params.Set("bar", interval)
	params.Set("limit", strconv.Itoa(limit))

	req, err := http.NewRequestWithContext(ctx, "GET",
		fmt.Sprintf("%s/api/v5/market/candles?%s", o.baseURL, params.Encode()), nil)
	if err != nil {
		return nil, err
	}

	resp, err := o.client.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	var result struct {
		Data [][]string `json:"data"`
	}
	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		return nil, err
	}

	klines := make([]*Kline, 0, len(result.Data))
	for _, row := range result.Data {
		if len(row) < 6 {
			continue
		}
		ts, _ := strconv.ParseInt(row[0], 10, 64)
		open, _ := decimal.NewFromString(row[1])
		high, _ := decimal.NewFromString(row[2])
		low, _ := decimal.NewFromString(row[3])
		close_, _ := decimal.NewFromString(row[4])
		vol, _ := decimal.NewFromString(row[5])
		klines = append(klines, &Kline{
			OpenTime:  ts,
			Open:      open,
			High:      high,
			Low:       low,
			Close:     close_,
			Volume:    vol,
		})
	}
	return klines, nil
}

func (o *OKXAdapter) GetTicker(ctx context.Context, symbol string) (*Ticker, error) {
	req, err := http.NewRequestWithContext(ctx, "GET",
		fmt.Sprintf("%s/api/v5/market/ticker?instId=%s", o.baseURL, symbol), nil)
	if err != nil {
		return nil, err
	}
	resp, err := o.client.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	var result struct {
		Data []struct {
			Last string `json:"last"`
			Bid1 string `json:"bidPx"`
			Ask1 string `json:"askPx"`
			Vol24h string `json:"vol24h"`
		} `json:"data"`
	}
	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		return nil, err
	}
	if len(result.Data) == 0 {
		return &Ticker{Symbol: symbol}, nil
	}
	d := result.Data[0]
	last, _ := decimal.NewFromString(d.Last)
	bid, _ := decimal.NewFromString(d.Bid1)
	ask, _ := decimal.NewFromString(d.Ask1)
	vol, _ := decimal.NewFromString(d.Vol24h)
	return &Ticker{Symbol: symbol, LastPrice: last, BidPrice: bid, AskPrice: ask, Volume: vol}, nil
}

func (o *OKXAdapter) GetDepth(ctx context.Context, symbol string, limit int) (*OrderBook, error) {
	return &OrderBook{Symbol: symbol}, nil
}
