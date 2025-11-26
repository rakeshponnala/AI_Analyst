"""Rate limiting middleware for API endpoints."""
from slowapi import Limiter
from slowapi.util import get_remote_address

# Create limiter instance
limiter = Limiter(key_func=get_remote_address)


def get_limiter():
    """Get limiter instance."""
    return limiter
