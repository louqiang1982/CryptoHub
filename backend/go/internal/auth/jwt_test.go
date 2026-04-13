package auth

import (
	"strings"
	"testing"
	"time"
)

func TestGenerateAndParseAccessToken(t *testing.T) {
	userID := "user-123"
	token, err := GenerateAccessToken(userID)
	if err != nil {
		t.Fatalf("GenerateAccessToken error: %v", err)
	}
	if token == "" {
		t.Fatal("expected non-empty token")
	}
	if !strings.Contains(token, ".") {
		t.Error("token should be JWT (contains dots)")
	}

	claims, err := ParseAccessToken(token)
	if err != nil {
		t.Fatalf("ParseAccessToken error: %v", err)
	}
	if claims.UserID != userID {
		t.Errorf("got UserID %q, want %q", claims.UserID, userID)
	}
}

func TestGenerateRefreshToken(t *testing.T) {
	token, err := GenerateRefreshToken("user-456")
	if err != nil {
		t.Fatalf("GenerateRefreshToken error: %v", err)
	}
	if token == "" {
		t.Fatal("expected non-empty refresh token")
	}
}

func TestParseInvalidToken(t *testing.T) {
	_, err := ParseAccessToken("not.a.valid.token")
	if err == nil {
		t.Error("expected error for invalid token")
	}
}

func TestTokenExpiry(t *testing.T) {
	token, err := GenerateAccessToken("user-789")
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	claims, err := ParseAccessToken(token)
	if err != nil {
		t.Fatalf("unexpected parse error: %v", err)
	}
	// Token should expire roughly 24 h from now
	expiresIn := time.Until(claims.ExpiresAt.Time)
	if expiresIn < 23*time.Hour || expiresIn > 25*time.Hour {
		t.Errorf("unexpected expiry: %v (want ~24h)", expiresIn)
	}
}
