import os
from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=(
            ".env",
            ".env.prod",
            ".env.production",
            ".env.dev",
            ".env.develop",
        ),
        env_file_encoding="utf-8",
    )

    DEBUG: bool = Field(default=False, env="DEBUG")

    # Pyrogram
    API_ID: int = Field(env="API_ID")
    API_HASH: str = Field(env="API_HASH")
    # pylint: disable=consider-alternative-union-syntax
    BOT_TOKEN: Optional[str] = Field(
        env="BOT_TOKEN",
    )
    # pylint: disable=consider-alternative-union-syntax
    PHONE: Optional[str] = Field(
        env="PHONE",
        default="",
    )
    LOCALE: str = Field(env="LOCALE", default="en")
    SESSION_URL: str = Field(
        default=os.path.join(BASE_DIR, "data/session"),
        env="SESSION_URL",
    )
    TEST_ENV: bool = Field(default=False, env="TEST_ENV")

    ADMIN: Optional[str] = Field(
        env="ADMIN",
        default="",
    )

    # Antiflood
    MESSAGES: int = Field(3)
    # Rate limit (N) messages every x seconds
    SECONDS: int = Field(15)
    # Rate limit x messages every (N) seconds
    CB_SECONDS: int = Field(15)
    # Rate limit x callback queries every (N) seconds

    # Database
    DATABASE_URL: str = Field(env="DATABASE_URL")
    # redis
    REDIS_URL: str = Field(default="redis://redis:6379", env="REDIS_URL")

    ROOT_PATH: Path = Path(__file__).resolve().parent.parent.parent

    # Cache
    CACHE_URL: str = Field(
        default=os.path.join(ROOT_PATH, "data/cache"),
        env="CACHE_URL",
    )

    STATIC_PATH: str = os.path.join(ROOT_PATH, "static")

    # Reddit
    REDDIT_ID: str = Field(env="REDDIT_ID")
    REDDIT_SECRET: str = Field(env="REDDIT_SECRET")
    REDDIT_TOKEN: str = Field(env="REDDIT_TOKEN")
