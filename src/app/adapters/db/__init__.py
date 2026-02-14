from __future__ import annotations

import logging

from app.core.config import settings

TORTOISE_ORM = {
    "connections": {"default": settings.get("database_url")},
    "apps": {
        "app": {
            "models": ["app.adapters.db.models", "aerich.models"],
            "default_connection": "default",
        },
    },
    "use_tz": True,
}
