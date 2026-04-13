package exchange

import (
"errors"
"strings"
)

// AdapterConfig holds the credentials needed to instantiate an exchange adapter.
// Passphrase is required only for OKX, Bitget, and KuCoin.
type AdapterConfig struct {
APIKey     string
APISecret  string
Passphrase string // required for OKX, Bitget, KuCoin
}

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

// CreateAdapter creates an exchange adapter by name using the supplied config.
// Use AdapterConfig.Passphrase for OKX, Bitget, and KuCoin.
func (f *Factory) CreateAdapter(name string, cfg AdapterConfig) (ExchangeAdapter, error) {
switch strings.ToLower(name) {
case "binance":
return NewBinanceAdapter(cfg.APIKey, cfg.APISecret), nil
case "okx":
return NewOKXAdapter(cfg.APIKey, cfg.APISecret, cfg.Passphrase), nil
case "bybit":
return NewBybitAdapter(cfg.APIKey, cfg.APISecret), nil
case "bitget":
return NewBitgetAdapter(cfg.APIKey, cfg.APISecret, cfg.Passphrase), nil
case "coinbase":
return NewCoinbaseAdapter(cfg.APIKey, cfg.APISecret), nil
case "kraken":
return NewKrakenAdapter(cfg.APIKey, cfg.APISecret), nil
case "kucoin":
return NewKuCoinAdapter(cfg.APIKey, cfg.APISecret, cfg.Passphrase), nil
case "gate", "gateio":
return NewGateAdapter(cfg.APIKey, cfg.APISecret), nil
case "deepcoin":
return NewDeepcoinAdapter(cfg.APIKey, cfg.APISecret), nil
case "htx", "huobi":
return NewHTXAdapter(cfg.APIKey, cfg.APISecret), nil
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
return f.SupportedExchanges()
}
