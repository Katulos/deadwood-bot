import logging
from collections.abc import Callable

import click
from alembic import command
from alembic.config import Config

from deadwood.adapters.db.alembic.config import get_alembic_config_path
from deadwood.client import run
from deadwood.core import logging as logger
from deadwood.core import settings


def with_alembic_config(
    callback: Callable[[Config], None],
) -> None:
    alembic_path_gen = get_alembic_config_path()
    try:
        alembic_path = next(alembic_path_gen)
    except StopIteration:
        logging.error("Alembic config path not found")
        return

    alembic_cfg = Config(str(alembic_path))
    alembic_cfg.set_main_option(
        "sqlalchemy.url",
        settings.get("db.database_url"),
    )
    callback(alembic_cfg)


@click.group()
def cli() -> None:
    debug = settings.get("debug")

    if debug:
        logger.setup_logger(loglevel=logging.DEBUG)
    else:
        logger.setup_logger(loglevel=logging.INFO)


@cli.group()
def migrations() -> None:
    """Database migrations management."""
    pass


@cli.command()
def start() -> None:
    """Start client."""
    ctx = click.get_current_context()
    ctx.invoke(upgrade)
    run()


@migrations.command()
@click.argument("message", required=True)
def autogenerate(
    message: str,
) -> None:
    """Autogenerate new migration."""
    with_alembic_config(
        lambda cfg: command.revision(cfg, autogenerate=True, message=message),
    )


@migrations.command()
@click.argument("revision", default="head")
def upgrade(revision: str) -> None:
    """Upgrade database to specified revision."""
    with_alembic_config(lambda cfg: command.upgrade(cfg, revision))
