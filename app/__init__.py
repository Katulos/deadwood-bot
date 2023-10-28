from __future__ import annotations

import gettext
import logging
import os.path
from pathlib import Path

import dotenv
from cashews import Cache
from importlib_metadata import version

from .config import shared

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

locale_dir = os.path.join(Path(__file__).resolve().parent.parent, "locale")

t = gettext.translation(
    "messages",
    localedir=locale_dir,
    languages=[shared.settings.LOCALE],
    fallback=True,
)
t.install()

_ = t.gettext


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


__version__ = version(__package__ or __name__)
