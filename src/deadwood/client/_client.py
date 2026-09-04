import asyncio
import logging
import sys

from telethon import TelegramClient, connection, functions, types
from telethon.errors import (
    AccessTokenInvalidError,
    AuthKeyUnregisteredError,
    BotCommandInvalidError,
    TokenInvalidError,
)
from tortoise import Tortoise

from deadwood.adapters.db import TORTOISE_ORM
from deadwood.core import settings

_client_kwargs = {
    "session": settings.get("session"),
    "api_id": settings.get("api_id"),
    "api_hash": settings.get("api_hash"),
    "device_model": settings.get("device_model"),
    "system_version": settings.get("system_version"),
    "app_version": settings.get("app_version"),
    "lang_code": settings.get("lang_code"),
    "system_lang_code": settings.get("system_lang_code"),
    "use_ipv6": settings.get("use_ipv6"),
}

if settings.get("use_proxy"):
    proxy_type = settings.get("proxy.proxy_type")
    proxy_config = settings.get("proxy")

    match proxy_type:
        case "mtproxy":
            logging.debug("Using mtproxy")
            _client_kwargs["connection"] = (
                connection.ConnectionTcpMTProxyRandomizedIntermediate
            )
            _client_kwargs["proxy"] = (
                proxy_config.get("addr"),
                proxy_config.get("port"),
                proxy_config.get("secret"),
            )
        case "socks5":
            logging.debug("Using socks5 proxy")
            _client_kwargs["proxy"] = proxy_config
        case _:
            raise ValueError(f"Unknown proxy type: {proxy_type}")

client: TelegramClient = TelegramClient(**_client_kwargs)

try:
    from . import commands, handlers
except ImportError:
    logging.error(
        "Could not load the plugins module. Does the directory exist in the correct location?",
        exc_info=True,
    )
    sys.exit(1)


async def _start() -> None:
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()

    try:
        await client.connect()

        if settings.get("phone"):
            phone_number = settings.get("phone")
            if not await client.is_user_authorized():
                logging.info(
                    "Authorization required. Sending code request...",
                )
                await client.send_code_request(phone_number)

                loop = asyncio.get_running_loop()
                try:
                    code = await loop.run_in_executor(
                        None,
                        input,
                        "Enter code: ",
                    )
                    client.me = await client.sign_in(phone_number, code)
                except asyncio.CancelledError:
                    logging.info("Authorization cancelled by user.")
                    return
            else:
                client.me = await client.get_me()
            logging.info("Authorized as user")

        elif settings.get("bot_token"):
            client.me = await client.sign_in(
                bot_token=settings.get("bot_token"),
            )
            await _set_bot_commands()
            logging.info("Authorized as bot")

        else:
            logging.error(
                "Neither 'phone' nor 'bot_token' is provided in settings.",
            )
            return

        if not settings.get("admins"):
            logging.warning("Admins are not set!")

        await handlers.init(client)
        await commands.init(client)

        logging.info("Client is running. Press Ctrl+C to stop.")

        await client.run_until_disconnected()

    except TokenInvalidError:
        logging.error("Token is invalid")
    except AuthKeyUnregisteredError:
        logging.error("Auth key is unregistered")
    except AccessTokenInvalidError:
        logging.error("Access token is invalid")
    except ConnectionError as e:
        logging.error(f"Connection error: {e}")
    except asyncio.CancelledError:
        logging.info("Async task was cancelled (normal shutdown).")
    except KeyboardInterrupt:
        logging.info("KeyboardInterrupt caught. Shutting down gracefully...")
    except Exception as e:
        logging.exception(f"An unexpected error occurred: {e}")
    finally:
        logging.info("Shutting down client and database connections...")
        try:
            if client.is_connected():
                await client.disconnect()
        except Exception as e:
            logging.warning(f"Error during client disconnect: {e}")

        try:
            await Tortoise.close_connections()
        except Exception as e:
            logging.warning(f"Error during database disconnect: {e}")

        logging.info("Shutdown complete.")


async def _set_bot_commands() -> None:
    scope = types.BotCommandScopeDefault()
    lang_code = "en"

    await client(
        functions.bots.ResetBotCommandsRequest(
            scope=scope,
            lang_code=lang_code,
        ),
    )

    try:
        await client(
            functions.bots.SetBotCommandsRequest(
                scope=scope,
                lang_code=lang_code,
                commands=[],
            ),
        )
    except BotCommandInvalidError:
        logging.error("Bot command is invalid")

    result = await client(
        functions.bots.GetBotCommandsRequest(
            scope=scope,
            lang_code=lang_code,
        ),
    )
    for cmd in result:
        logging.debug(f"Bot command registered: {cmd}")


def run() -> None:
    try:
        asyncio.run(_start())
    except KeyboardInterrupt:
        logging.info("Application terminated by user (run level).")
    except Exception as e:
        logging.exception(f"Fatal error during application execution: {e}")
    finally:
        logging.info("Application process exited.")
