"""Tests for core modules."""

import pytest

from app.core.config import Settings
from app.core.security import (
    create_access_token,
    verify_token,
    hash_password,
    verify_password,
)


class TestConfig:
    def test_default_settings(self):
        s = Settings()
        assert s.APP_NAME == "CryptoHub Python Backend"
        assert s.API_PREFIX == "/api/v1"
        assert s.GRPC_PORT == 50051

    def test_debug_default_false(self):
        s = Settings()
        assert s.DEBUG is False


class TestSecurity:
    def test_password_hash_and_verify(self):
        raw = "my-secret-password"
        hashed = hash_password(raw)
        assert hashed != raw
        assert verify_password(raw, hashed) is True
        assert verify_password("wrong", hashed) is False

    def test_create_and_verify_token(self):
        token = create_access_token({"sub": "user-123"})
        payload = verify_token(token)
        assert payload is not None
        assert payload["sub"] == "user-123"

    def test_invalid_token(self):
        result = verify_token("invalid-token")
        assert result is None
