import logging
import sys

from telethon import TelegramClient, functions, types
from telethon.errors import (
    AccessTokenInvalidError,
    AuthKeyUnregisteredError,
    BotCommandInvalidError,
    TokenInvalidError,
)
from tortoise import Tortoise, run_async

from deadwood.adapters.db import TORTOISE_ORM
from deadwood.core import settings

client = TelegramClient(
    session=settings.get("session"),
    api_id=settings.get("api_id"),
    api_hash=settings.get("api_hash"),
    device_model=settings.get("device_model"),
    system_version=settings.get("system_version"),
    app_version=settings.get("app_version"),
    lang_code=settings.get("lang_code"),
    system_lang_code=settings.get("system_lang_code"),
)

try:
    from . import commands, handlers
except ImportError:
    logging.error(
        "Could not load the plugins module, does the directory exist in the correct location?",
    )
    sys.exit(1)


async def _start() -> None:
    try:
        await client.connect()
        await Tortoise.init(TORTOISE_ORM)
        await Tortoise.generate_schemas()
        if settings.get("phone"):
            phone_number = settings.get("phone")
            if not await client.is_user_authorized():
                await client.send_code_request(phone_number)
                client.me = await client.sign_in(
                    phone_number,
                    input("Enter code: "),
                )
            else:
                client.me = await client.get_me()
        elif settings.get("bot_token"):
            client.me = await client.sign_in(
                bot_token=settings.get("bot_token"),
            )
            await _set_bot_commands()
            logging.info("Auth as bot")

        if settings.get("admins") == []:
            logging.warning("Admins are not set!")

        await handlers.init(client)
        await commands.init(client)

        await client.run_until_disconnected()

    except TokenInvalidError:
        logging.error("Token is invalid")
    except AuthKeyUnregisteredError:
        logging.error("Auth key is unregistered")
    except AccessTokenInvalidError:
        logging.error("Access token is invalid")


async def _set_bot_commands() -> None:
    await client(
        functions.bots.ResetBotCommandsRequest(
            scope=types.BotCommandScopeDefault(),
            lang_code="en",
        ),
    )
    try:
        await client(
            functions.bots.SetBotCommandsRequest(
                scope=types.BotCommandScopeDefault(),
                lang_code="en",
                commands=[],
            ),
        )
    except BotCommandInvalidError:
        logging.error("Bot command is invalid")
    result = await client(
        functions.bots.GetBotCommandsRequest(
            scope=types.BotCommandScopeDefault(),
            lang_code="en",
        ),
    )
    for x in result:
        logging.debug(f"Set {x}")


def run() -> None:
    try:
        client.loop.run_until_complete(_start())
    finally:
        run_async(Tortoise.close_connections())
