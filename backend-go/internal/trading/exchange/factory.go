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

func (f *Factory) CreateAdapter(name, apiKey, apiSecret string) (ExchangeAdapter, error) {
	switch strings.ToLower(name) {
	case "binance":
		return NewBinanceAdapter(apiKey, apiSecret), nil
	default:
		return nil, errors.New("unsupported exchange: " + name)
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