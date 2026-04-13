"""Tests for the strategy engine API endpoints."""

import pytest


class TestStrategyAPI:
    """Strategy engine API endpoint tests."""

    def test_compile_endpoint_exists(self):
        from app.api.strategy_engine import router

        routes = [r.path for r in router.routes]
        assert "/compile" in routes

    def test_start_endpoint_exists(self):
        from app.api.strategy_engine import router

        routes = [r.path for r in router.routes]
        assert "/start" in routes

    def test_stop_endpoint_exists(self):
        from app.api.strategy_engine import router

        routes = [r.path for r in router.routes]
        assert "/stop/{strategy_id}" in routes

    def test_status_endpoint_exists(self):
        from app.api.strategy_engine import router

        routes = [r.path for r in router.routes]
        assert "/{strategy_id}/status" in routes
