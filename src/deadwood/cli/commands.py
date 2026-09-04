import logging

import click

from deadwood.client import run
from deadwood.core import logging as logger
from deadwood.core import settings


@click.group()
def cli() -> None:
    debug = settings.get("debug")

    if debug:
        logger.setup_logger(loglevel=logging.DEBUG)
    else:
        logger.setup_logger(loglevel=logging.INFO)


@cli.command()
def start() -> None:
    """Start client."""
    run()
