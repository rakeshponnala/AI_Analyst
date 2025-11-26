"""Simple in-memory caching service using TTL cache."""
from cachetools import TTLCache
from app.core.config import settings
from app.core.logging_config import get_logger

logger = get_logger(__name__)

# Create cache instances with TTL from config
stock_cache = TTLCache(maxsize=100, ttl=settings.STOCK_DATA_CACHE_TTL)
news_cache = TTLCache(maxsize=100, ttl=settings.NEWS_CACHE_TTL)


def get_cached_stock_data(ticker: str):
    """
    Get cached stock data if available.

    Args:
        ticker: Stock ticker symbol

    Returns:
        Cached stock data dict or None
    """
    cached = stock_cache.get(ticker)
    if cached:
        logger.info(f"[CacheService] Cache HIT for stock data: {ticker}")
    return cached


def set_cached_stock_data(ticker: str, data: dict):
    """
    Cache stock data with TTL.

    Args:
        ticker: Stock ticker symbol
        data: Stock data dictionary to cache
    """
    stock_cache[ticker] = data
    logger.info(f"[CacheService] Cached stock data for: {ticker}")


def get_cached_news(ticker: str):
    """
    Get cached news data if available.

    Args:
        ticker: Stock ticker symbol

    Returns:
        Cached news list or None
    """
    cached = news_cache.get(ticker)
    if cached:
        logger.info(f"[CacheService] Cache HIT for news: {ticker}")
    return cached


def set_cached_news(ticker: str, data: list):
    """
    Cache news data with TTL.

    Args:
        ticker: Stock ticker symbol
        data: News list to cache
    """
    news_cache[ticker] = data
    logger.info(f"[CacheService] Cached news for: {ticker}")


def clear_cache():
    """Clear all caches."""
    stock_cache.clear()
    news_cache.clear()
    logger.info("[CacheService] All caches cleared")
