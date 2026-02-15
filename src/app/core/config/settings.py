import logging
import os

from dynaconf import Dynaconf, ValidationError, Validator

_BASE_DIR = os.getcwd()


settings = Dynaconf(
    settings_files=[
        "?/etc/deadwood/settings.yml",
        "?/etc/deadwood/.secrets.yml",
        "?~/.config/deadwood/settings.yml",
        "?~/.config/deadwood/.secrets.yml",
        os.path.join(_BASE_DIR, "settings.yml"),
        os.path.join(_BASE_DIR, ".secrets.yml"),
    ],
)

settings.validators.register(
    # Client
    Validator(
        "api_id",
        apply_default_on_none=True,
        default=2040,
        is_type_of=int,
        required=True,
    ),
    Validator(
        "api_hash",
        apply_default_on_none=True,
        default="b18441a1ff607e10a989891a5462e627",
        required=True,
    ),
    Validator(
        "app_version",
        apply_default_on_none=True,
        default="5.12.1 x64",
        required=True,
    ),
    Validator(
        "device_model",
        apply_default_on_none=True,
        default="B75M-D3H-BT",
        required=True,
    ),
    Validator(
        "lang_code",
        apply_default_on_none=True,
        default="en",
        required=True,
    ),
    Validator(
        "system_lang_code",
        apply_default_on_none=True,
        default="en-US",
        required=True,
    ),
    Validator(
        "system_version",
        apply_default_on_none=True,
        default="Windows 10",
        required=True,
    ),
    Validator("bot_token", apply_default_on_none=False),
    Validator("phone", apply_default_on_none=False),
    Validator(
        "admins",
        apply_default_on_none=True,
        default=[],
        is_type_of=list,
        required=True,
    ),
    Validator(
        "session",
        default=os.path.join(_BASE_DIR, "data/session"),
        required=True,
    ),
    # Database
    # like a postgres://postgres:postgres@db:5432/postgres
    Validator(
        "database_url",
        default="sqlite://" + os.path.join(_BASE_DIR, "data/db.sqlite3"),
        required=True,
    ),
    # debug
    Validator("debug", default=False, is_type_of=bool),
    # static
    Validator(
        "static_path",
        apply_default_on_none=True,
        default=os.path.join(_BASE_DIR, "static"),
    ),
    # Reddit
    Validator("reddit_client_id", apply_default_on_none=False),
    Validator("reddit_client_secret", apply_default_on_none=False),
    Validator(
        "reddit_user_agent",
        apply_default_on_none=True,
        default="Trenddit/0.0.2",
    ),
    # Cache
    Validator(
        "cache_url",
        apply_default_on_none=True,
        default=f"disk://?directory={os.path.join(_BASE_DIR, 'data/cache')}",
    ),
)

try:
    settings.validators.validate_all()
except ValidationError as e:
    logging.error(e.message)
