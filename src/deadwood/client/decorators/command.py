import logging
from collections.abc import Callable
from typing import Any, cast

from telethon import events
from telethon.errors import ChatAdminRequiredError
from telethon.tl.custom import Message

from deadwood.client import client
from deadwood.core import settings


def command(
    command: str,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        pattern = f"(?i)^[/!]{command}$"

        @client.on(  # type: ignore[untyped-decorator]
            events.NewMessage(
                pattern=pattern,
                func=lambda event: event.is_group,
            ),
        )
        async def handle(event: Message) -> None:
            try:
                await func(event)
            except ChatAdminRequiredError as e:
                logging.error(e.message)

        return cast(Callable[..., Any], handle)

    return decorator


def par_command(
    command: str,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        pattern = f"(?i)^[/!]{command} (.*?)$"

        @client.on(  # type: ignore[untyped-decorator]
            events.NewMessage(
                pattern=pattern,
                func=lambda event: event.is_group,
            ),
        )
        async def handle(event: Message) -> None:
            try:
                await func(event)
            except ChatAdminRequiredError as e:
                logging.error(e.message)

        return cast(Callable[..., Any], handle)

    return decorator


def admin_command(
    command: str,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        pattern = f"(?i)^[/!]{command}$"

        @client.on(  # type: ignore[untyped-decorator]
            events.NewMessage(
                pattern=pattern,
                func=lambda event: event.is_group,
            ),
        )
        async def handle(event: Message) -> None:
            if not await _is_admin(event.sender.id):
                return
            try:
                await func(event)
            except ChatAdminRequiredError as e:
                logging.error(e.message)

        return cast(Callable[..., Any], handle)

    return decorator


async def _is_admin(user_id: int) -> bool:
    if user_id in settings.get("admins"):
        return True
    else:
        return False
