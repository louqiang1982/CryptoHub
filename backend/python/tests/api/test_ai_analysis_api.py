"""Tests for the AI analysis API endpoints."""

import pytest


class TestAIAnalysisAPI:
    """AI analysis API endpoint tests."""

    def test_analyze_endpoint_exists(self):
        from app.api.ai_analysis import router

        routes = [r.path for r in router.routes]
        assert "/analyze" in routes

    def test_get_analysis_result_endpoint_exists(self):
        from app.api.ai_analysis import router

        routes = [r.path for r in router.routes]
        assert "/analyze/{analysis_id}" in routes

    def test_fast_analyze_endpoint_exists(self):
        from app.api.ai_analysis import router

        routes = [r.path for r in router.routes]
        assert "/fast-analyze" in routes
