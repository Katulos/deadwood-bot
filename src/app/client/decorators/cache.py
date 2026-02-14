from cashews import Cache

from app.core.config import settings

cache = Cache()
cache.setup(
    settings.get("cache_url"),
)
