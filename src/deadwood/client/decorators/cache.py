from cashews import Cache

from deadwood.core.config import settings

cache = Cache()
cache.setup(
    settings.get("cache_url"),
)
