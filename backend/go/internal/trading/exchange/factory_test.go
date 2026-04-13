package exchange

import (
	"testing"
)

func TestFactoryCreateBinance(t *testing.T) {
	f := NewFactory()
	adapter, err := f.CreateAdapter("binance", AdapterConfig{APIKey: "key", APISecret: "secret"})
	if err != nil {
		t.Fatalf("expected no error, got %v", err)
	}
	if adapter == nil {
		t.Fatal("expected non-nil adapter")
	}
}

func TestFactoryCreateOKX(t *testing.T) {
	f := NewFactory()
	adapter, err := f.CreateAdapter("okx", AdapterConfig{APIKey: "key", APISecret: "secret", Passphrase: "pass"})
	if err != nil {
		t.Fatalf("expected no error, got %v", err)
	}
	if adapter == nil {
		t.Fatal("expected non-nil adapter")
	}
}

func TestFactoryAllSupportedExchanges(t *testing.T) {
	f := NewFactory()
	supported := f.SupportedExchanges()
	if len(supported) == 0 {
		t.Fatal("expected at least one supported exchange")
	}

	cfg := AdapterConfig{APIKey: "key", APISecret: "secret", Passphrase: "pass"}
	for _, name := range supported {
		adapter, err := f.CreateAdapter(name, cfg)
		if err != nil {
			t.Errorf("CreateAdapter(%q) error: %v", name, err)
		}
		if adapter == nil {
			t.Errorf("CreateAdapter(%q) returned nil", name)
		}
	}
}

func TestFactoryUnsupportedExchange(t *testing.T) {
	f := NewFactory()
	_, err := f.CreateAdapter("unknown_exchange_xyz", AdapterConfig{APIKey: "key", APISecret: "secret"})
	if err == nil {
		t.Error("expected error for unknown exchange")
	}
}
