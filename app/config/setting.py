import logging
import pathlib
import sys
from typing import Optional

from pydantic import BaseModel, Field, ValidationError
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    YamlConfigSettingsSource,
)

from app.utils import logging as logger

_logger = logger.setup_logger().bind(type="business")

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent.parent

config = BASE_DIR / "config.yaml"

if config.is_file():
    _logger.info("Using config file: %s", config)
else:
    _logger.critical("Can't find config file: %s", config)
    _logger.critical("The application is shutting down")
    sys.exit(1)


class AbstractSettings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=True,
        extra="ignore",
        env_nested_delimiter=".",
        yaml_file=config,
        yaml_file_encoding="utf-8",
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (YamlConfigSettingsSource(settings_cls),)


class AppConfig(BaseModel):
    debug: bool = Field(default=False)

    @property
    def logging_level(self) -> int:
        return logging.DEBUG if self.debug else logging.INFO


class BotConfig(BaseModel):
    api_id: int
    api_hash: str
    phone: Optional[str] = None
    token: Optional[str] = None
    session_url: pathlib.Path = Field(default=BASE_DIR / "data" / "session")
    blacklist: list[int] = Field(default=[])
    whitelist: list[int] = Field(default=[])


class DbConfig(BaseModel):
    dsn: str = Field(
        default=str("sqlite://" / BASE_DIR / "data" / "deadwood.db"),
    )


class Settings(AbstractSettings):
    app: AppConfig
    bot: BotConfig
    db: DbConfig


try:
    settings = Settings()
    _logger.info("Configuration loaded")
except (ValueError, ValidationError) as e:
    _logger.critical("Configuration file validation error: %s", e)
    sys.exit(0)
