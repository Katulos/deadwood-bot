import asyncio
import sys
from typing import NoReturn

import tenacity
from telethon import TelegramClient
from telethon.errors import TokenInvalidError

from app.config.setting import settings
from app.utils import connect_to_services, logging

_logger = logging.setup_logger(settings.app.logging_level).bind(
    type="business",
)


def _exit_with_error(message: str) -> NoReturn:
    _logger.error(message)
    sys.exit(1)


try:
    from . import plugins
except ImportError:
    _exit_with_error(
        "Could not load the plugins module. Does the directory exist in the correct location?",
    )


async def _handle_database_connection(connect: bool = True) -> None:
    logger = logging.setup_logger(settings.app.logging_level).bind(
        type="database",
    )
    operation = "connect" if connect else "disconnect"
    action_past = "connected" if connect else "disconnected"

    try:
        if connect:
            await connect_to_services.wait_db(
                logger=logger,
                dsn=settings.db.dsn,
            )
        else:
            await connect_to_services.wait_close_db(logger=logger)
    except tenacity.RetryError:
        logger.exception(f"Failed to {operation} from database")
        sys.exit(1)
    else:
        logger.info(f"Successfully {action_past} from database")


async def _on_startup() -> None:
    await _handle_database_connection(connect=True)


async def _on_shutdown() -> None:
    await _handle_database_connection(connect=False)


client = TelegramClient(
    session=settings.bot.session_url,
    api_id=settings.bot.api_id,
    api_hash=settings.bot.api_hash,
)
client.parse_mode = "HTML"


async def _authenticate() -> None:
    if settings.bot.phone:
        if not await client.is_user_authorized():
            await client.send_code_request(settings.bot.phone)
            client.me = await client.sign_in(
                settings.bot.phone,
                input("Enter verification code: "),
            )
        else:
            client.me = await client.get_me()
        _logger.info("Authenticated as user")
    elif settings.bot.token:
        client.me = await client.sign_in(bot_token=settings.bot.token)
        _logger.info("Authenticated as bot")


async def main() -> None:
    await _on_startup()

    try:
        await client.connect()
        await _authenticate()
        await plugins.init(client)
        await client.run_until_disconnected()
    except TokenInvalidError:
        _exit_with_error("Invalid authentication token")
    finally:
        await _on_shutdown()


def run() -> None:
    asyncio.run(main())
