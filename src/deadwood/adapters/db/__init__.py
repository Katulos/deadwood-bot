from __future__ import annotations

import logging

from deadwood.core import settings

TORTOISE_ORM = {
    "connections": {"default": settings.get("database_url")},
    "apps": {
        "deadwood": {
            "models": ["deadwood.adapters.db.models", "aerich.models"],
            "default_connection": "default",
        },
    },
    "use_tz": True,
}
