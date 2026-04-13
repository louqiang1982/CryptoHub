package exchange

import (
	"errors"
	"strings"
)

type Factory struct {
	adapters map[string]ExchangeAdapter
}

func NewFactory() *Factory {
	return &Factory{
		adapters: make(map[string]ExchangeAdapter),
	}
}

func (f *Factory) RegisterAdapter(name string, adapter ExchangeAdapter) {
	f.adapters[strings.ToLower(name)] = adapter
}

// CreateAdapter creates an exchange adapter by name.
// For exchanges that require a passphrase (OKX, Bitget, KuCoin), pass it
// as the optional fourth argument.
func (f *Factory) CreateAdapter(name, apiKey, apiSecret string, extra ...string) (ExchangeAdapter, error) {
	passphrase := ""
	if len(extra) > 0 {
		passphrase = extra[0]
	}

	switch strings.ToLower(name) {
	case "binance":
		return NewBinanceAdapter(apiKey, apiSecret), nil
	case "okx":
		return NewOKXAdapter(apiKey, apiSecret, passphrase), nil
	case "bybit":
		return NewBybitAdapter(apiKey, apiSecret), nil
	case "bitget":
		return NewBitgetAdapter(apiKey, apiSecret, passphrase), nil
	case "coinbase":
		return NewCoinbaseAdapter(apiKey, apiSecret), nil
	case "kraken":
		return NewKrakenAdapter(apiKey, apiSecret), nil
	case "kucoin":
		return NewKuCoinAdapter(apiKey, apiSecret, passphrase), nil
	case "gate", "gateio":
		return NewGateAdapter(apiKey, apiSecret), nil
	case "deepcoin":
		return NewDeepcoinAdapter(apiKey, apiSecret), nil
	case "htx", "huobi":
		return NewHTXAdapter(apiKey, apiSecret), nil
	default:
		return nil, errors.New("unsupported exchange: " + name)
	}
}

// SupportedExchanges returns the list of exchange names this factory supports.
func (f *Factory) SupportedExchanges() []string {
	return []string{
		"binance", "okx", "bybit", "bitget", "coinbase",
		"kraken", "kucoin", "gate", "deepcoin", "htx",
	}
}

func (f *Factory) GetAdapter(name string) (ExchangeAdapter, error) {
	adapter, exists := f.adapters[strings.ToLower(name)]
	if !exists {
		return nil, errors.New("exchange adapter not found: " + name)
	}
	return adapter, nil
}

func (f *Factory) ListSupportedExchanges() []string {
	return []string{"binance"}
}