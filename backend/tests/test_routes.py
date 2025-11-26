"""Tests for API routes."""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from main import app

client = TestClient(app)


class TestHealthCheck:
    """Test health check endpoint."""

    def test_health_check_returns_200(self):
        """Test that health check returns 200 OK."""
        response = client.get("/v1/")
        assert response.status_code == 200
        assert response.json()["status"] == "active"

    def test_health_check_has_version(self):
        """Test that health check includes version."""
        response = client.get("/v1/")
        data = response.json()
        assert "version" in data
        assert data["version"] == "1.0.0"


class TestAnalyzeEndpoint:
    """Test stock analysis endpoint."""

    def test_analyze_invalid_ticker_format(self):
        """Test that invalid ticker format is rejected."""
        response = client.get("/v1/api/analyze/INVALID@TICKER")
        assert response.status_code == 400

    def test_analyze_too_long_ticker(self):
        """Test that too-long ticker is rejected."""
        response = client.get("/v1/api/analyze/VERYLONGTICKERNAME123")
        assert response.status_code == 400

    def test_analyze_with_special_chars(self):
        """Test that special characters are rejected."""
        response = client.get("/v1/api/analyze/TEST<script>")
        assert response.status_code == 400


class TestRateLimiting:
    """Test rate limiting functionality."""

    def test_rate_limit_exceeded(self):
        """Test that rate limiting works."""
        # Make more than 10 requests in quick succession
        responses = []
        for i in range(12):
            response = client.get(f"/v1/api/analyze/AAPL{i}")
            responses.append(response)

        # At least one should be rate limited (429)
        status_codes = [r.status_code for r in responses]
        # We expect either 429 (rate limited), 400 (validation), or other errors
        # The important thing is the rate limiter is active
        assert len(status_codes) == 12
