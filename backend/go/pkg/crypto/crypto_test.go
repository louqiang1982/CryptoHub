package crypto

import (
	"testing"
)

func TestEncryptDecrypt(t *testing.T) {
	passphrase := "test-secret-key"
	plaintext := "my-api-key-12345"

	encrypted, err := Encrypt(plaintext, passphrase)
	if err != nil {
		t.Fatalf("Encrypt error: %v", err)
	}
	if encrypted == plaintext {
		t.Error("encrypted text should differ from plaintext")
	}

	decrypted, err := Decrypt(encrypted, passphrase)
	if err != nil {
		t.Fatalf("Decrypt error: %v", err)
	}
	if decrypted != plaintext {
		t.Errorf("got %q, want %q", decrypted, plaintext)
	}
}

func TestDecryptWrongPassphrase(t *testing.T) {
	encrypted, _ := Encrypt("secret", "correct-pass")
	_, err := Decrypt(encrypted, "wrong-pass")
	if err == nil {
		t.Error("expected error when decrypting with wrong passphrase")
	}
}

func TestDecryptInvalidInput(t *testing.T) {
	_, err := Decrypt("not-valid-base64!!!", "pass")
	if err == nil {
		t.Error("expected error for invalid base64")
	}
}
