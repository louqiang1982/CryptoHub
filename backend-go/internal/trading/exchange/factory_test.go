package exchange

import (
	"testing"
)

func TestFactoryCreateBinance(t *testing.T) {
	f := NewFactory()
	adapter, err := f.CreateAdapter("binance", "key", "secret")
	if err != nil {
		t.Fatalf("expected no error, got %v", err)
	}
	if adapter == nil {
		t.Fatal("expected non-nil adapter")
	}
}

func TestFactoryCreateOKX(t *testing.T) {
	f := NewFactory()
	adapter, err := f.CreateAdapter("okx", "key", "secret", "passphrase")
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

	for _, name := range supported {
		adapter, err := f.CreateAdapter(name, "key", "secret", "pass")
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
	_, err := f.CreateAdapter("unknown_exchange_xyz", "key", "secret")
	if err == nil {
		t.Error("expected error for unknown exchange")
	}
}
