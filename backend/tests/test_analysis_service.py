"""Tests for analysis service."""
import pytest
from unittest.mock import Mock, AsyncMock, patch
from app.services.analysis_service import AnalysisService


class TestAnalysisService:
    """Test AnalysisService functionality."""

    def test_initialization_without_api_key(self):
        """Test that service fails without API key."""
        with patch('app.services.analysis_service.settings.ANTHROPIC_API_KEY', ''):
            with pytest.raises(ValueError, match="Missing API Key"):
                AnalysisService()

    def test_extract_rating_bearish(self):
        """Test rating extraction for bearish analysis."""
        service = AnalysisService()
        analysis = "This stock is risky. **VERDICT: BEARISH** - too many concerns."

        rating = service._extract_rating(analysis)

        assert rating == "BEARISH"

    def test_extract_rating_neutral(self):
        """Test rating extraction for neutral analysis."""
        service = AnalysisService()
        analysis = "Mixed signals here. **VERDICT: NEUTRAL** - wait and see."

        rating = service._extract_rating(analysis)

        assert rating == "NEUTRAL"

    def test_extract_rating_default(self):
        """Test rating extraction defaults to NEUTRAL."""
        service = AnalysisService()
        analysis = "Some general analysis without clear verdict."

        rating = service._extract_rating(analysis)

        assert rating == "NEUTRAL"

    @pytest.mark.asyncio
    async def test_analyze_structure(self):
        """Test that analyze returns proper structure."""
        service = AnalysisService()

        # Mock data_service.fetch_stock_data
        mock_data = {
            "company_name": "Test Corp",
            "price": 100.0,
            "price_change": 2.5,
            "price_change_pct": 2.5,
            "prev_close": 97.5,
            "week_52_high": 120.0,
            "week_52_low": 80.0,
            "pct_from_high": -16.7,
            "market_cap": "$10B",
            "pe_ratio": 25.0,
            "forward_pe": 23.0,
            "volume_vs_avg": 110,
            "beta": 1.2,
            "short_percent": 5.0,
            "debt_to_equity": 50.0,
            "current_ratio": 1.5,
            "profit_margin": 15.0,
            "revenue_growth": 10.0,
            "earnings_growth": 12.0,
            "target_price": 110.0,
            "target_upside": 10.0,
            "recommendation": "buy",
            "news": "1. Test news - Source",
            "news_sources": [{"title": "Test", "source": "Source", "url": ""}]
        }

        # Mock Anthropic API response
        mock_response = Mock()
        mock_response.content = [Mock(text="Test analysis. **VERDICT: NEUTRAL**")]

        with patch.object(service.data_service, 'fetch_stock_data', new=AsyncMock(return_value=mock_data)):
            with patch.object(service.client.messages, 'create', return_value=mock_response):
                result = await service.analyze("TEST")

                # Verify structure
                assert "ticker" in result
                assert "company_name" in result
                assert "rating" in result
                assert "metrics" in result
                assert "news" in result
                assert "analysis" in result
                assert "generated_at" in result
                assert result["ticker"] == "TEST"
                assert result["rating"] in ["BEARISH", "NEUTRAL"]
