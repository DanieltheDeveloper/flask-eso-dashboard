"""Cache for FastAPI routes."""

from cachetools import TTLCache

# Create a cache with a maximum size and time-to-live (TTL)
cache = TTLCache(maxsize=5, ttl=60)  # Cache size of 5 items, expires after 1 minute
cacheLong = TTLCache(maxsize=1, ttl=300)  # Cache size of 1 item, expires after 5 minutes
