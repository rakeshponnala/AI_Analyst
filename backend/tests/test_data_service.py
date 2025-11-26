"""Tests for data service."""
import pytest
from unittest.mock import Mock, patch, AsyncMock
from app.services.data_service import DataService


class TestDataService:
    """Test DataService functionality."""

    @patch('app.services.data_service.yf.Ticker')
    def test_get_stock_data_success(self, mock_ticker_class):
        """Test successful stock data fetch."""
        # Arrange
        mock_ticker = Mock()
        mock_ticker.info = {
            'shortName': 'Apple Inc.',
            'previousClose': 150.0,
            'marketCap': 2500000000000,
            'trailingPE': 25.5,
            'forwardPE': 24.0
        }
        mock_ticker.fast_info.last_price = 151.5
        mock_ticker.fast_info.last_volume = 50000000
        mock_ticker_class.return_value = mock_ticker

        # Act
        result = DataService.get_stock_data("AAPL")

        # Assert
        assert result["company_name"] == "Apple Inc."
        assert result["current_price"] == 151.5
        assert "market_cap" in result

    @patch('app.services.data_service.yf.Ticker')
    def test_get_stock_data_invalid_ticker(self, mock_ticker_class):
        """Test handling of invalid ticker."""
        # Arrange
        mock_ticker_class.side_effect = Exception("Invalid ticker")

        # Act
        result = DataService.get_stock_data("INVALID_TICKER_XYZ")

        # Assert
        assert result["current_price"] == "Unknown"
        assert result["company_name"] == "INVALID_TICKER_XYZ"

    @patch('app.services.data_service.DDGS')
    def test_get_news_with_sources(self, mock_ddgs_class):
        """Test news fetching."""
        # Arrange
        mock_ddgs = Mock()
        mock_ddgs.__enter__ = Mock(return_value=mock_ddgs)
        mock_ddgs.__exit__ = Mock(return_value=False)
        mock_ddgs.news.return_value = [
            {"title": "Test News", "source": "Test Source", "url": "http://test.com", "date": "2025-01-01"}
        ]
        mock_ddgs_class.return_value = mock_ddgs

        # Act
        result = DataService.get_news_with_sources("AAPL")

        # Assert
        assert len(result) > 0
        assert "title" in result[0]
        assert result[0]["title"] == "Test News"

    @pytest.mark.asyncio
    async def test_fetch_stock_data_async(self):
        """Test async fetch_stock_data."""
        with patch.object(DataService, 'get_stock_data', return_value={"company_name": "Test", "current_price": 100.0}):
            with patch.object(DataService, 'get_news_with_sources', return_value=[{"title": "News"}]):
                result = await DataService.fetch_stock_data("TEST")
                assert "company_name" in result
                assert "news" in result
