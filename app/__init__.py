from __future__ import annotations

import gettext
import logging
import os.path
from pathlib import Path

import dotenv
from cashews import Cache

from .config import shared

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

locale_dir = os.path.join(Path(__file__).resolve().parent.parent, "locales")

t = gettext.translation(
    domain="messages",
    localedir=locale_dir,
    languages=[shared.settings.LOCALE],
    fallback=True,
)

_ = t.gettext
_n = t.ngettext


# Load env variables from file
dotenv_file = Path(__file__).resolve().parent.parent / ".env"
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

cache = Cache()
cache.setup("disk://?directory=" + shared.settings.CACHE_URL)

TORTOISE_ORM = {
    "connections": {"default": shared.settings.DATABASE_URL},
    "apps": {
        "app": {
            "models": ["app.models", "aerich.models"],
            "default_connection": "default",
        },
    },
    "use_tz": True,
}


__version__ = "0.0.4"
