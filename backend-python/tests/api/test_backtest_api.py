"""Tests for the backtest API endpoints."""

import pytest
from fastapi.testclient import TestClient


class TestBacktestAPI:
    """Backtest API endpoint tests."""

    def test_run_backtest_endpoint_exists(self):
        """POST /api/v1/backtest/run is registered."""
        # The endpoint is defined; full integration tests require DB
        from app.api.backtest import router

        routes = [r.path for r in router.routes]
        assert "/run" in routes

    def test_get_backtest_result_endpoint_exists(self):
        """GET /api/v1/backtest/{backtest_id} is registered."""
        from app.api.backtest import router

        routes = [r.path for r in router.routes]
        assert "/{backtest_id}" in routes

    def test_get_backtest_report_endpoint_exists(self):
        """GET /api/v1/backtest/{backtest_id}/report is registered."""
        from app.api.backtest import router

        routes = [r.path for r in router.routes]
        assert "/{backtest_id}/report" in routes
