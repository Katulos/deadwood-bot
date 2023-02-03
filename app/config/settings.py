import os
from pathlib import Path
from typing import Optional

from pydantic import BaseSettings, Field

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
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
    )
    LOCALE: str = Field(env="LOCALE", default="en_US")
    SESSION_URL: str = Field(
        default=os.path.join(BASE_DIR, "data/session"),
        env="SESSION_URL",
    )
    TEST_ENV: bool = Field(default=False, env="TEST_ENV")

    ADMIN: Optional[int]  # pylint: disable=consider-alternative-union-syntax

    # Antiflood
    MESSAGES = Field(3)
    # Rate limit (N) messages every x seconds
    SECONDS = Field(15)
    # Rate limit x messages every (N) seconds
    CB_SECONDS = Field(15)
    # Rate limit x callback queries every (N) seconds

    # Database
    DATABASE_URL: str = Field(env="DATABASE_URL")
    # redis
    REDIS_URL: str = Field(default="redis://redis:6379", env="REDIS_URL")

    ROOT_PATH = Path(__file__).resolve().parent.parent.parent

    STATIC_PATH = os.path.join(ROOT_PATH, "static")

    class Config:
        case_sensitive: bool = True
        env_file = (
            ".env",
            ".env.prod",
            ".env.production",
            ".env.dev",
            ".env.develop",
        )
        env_file_encoding = "utf-8"
        fields = {
            x[0]: {"env": x}
            for x in (
                ["ADMIN"],
                ["API_ID"],
                ["API_HASH"],
                ["BOT_TOKEN"],
                ["PHONE"],
                ["LOCALE"],
                ["SESSION_URL"],
                ["TEST_ENV"],
                ["MESSAGES"],
                ["SECONDS"],
                ["CB_SECONDS"],
                ["DATABASE_URL"],
                ["REDIS_URL"],
                ["ROOT_PATH"],
                ["STATIC_PATH"],
            )
        }
