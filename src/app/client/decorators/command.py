import logging

from telethon import events
from telethon.errors import ChatAdminRequiredError
from telethon.tl.custom import Message

from app.client.bot import client
from app.core.config import settings


def par_command(command: str):
    def decorator(func):
        pattern = f"(?i)^[/!]{command} (.*?)$"

        @client.on(
            events.NewMessage(
                pattern=pattern,
                func=lambda event: event.is_group,
            ),
        )
        async def handle(event: Message):
            try:
                await func(event)
            except ChatAdminRequiredError as e:
                logging.error(e.message)

    return decorator


def admin_command(command: str):
    def decorator(func):
        pattern = f"(?i)^[/!]{command}$"

        @client.on(
            events.NewMessage(
                pattern=pattern,
                func=lambda event: event.is_group,
            ),
        )
        async def handle(event: Message):
            if not await _is_admin(event.sender.id):
                return
            try:
                await func(event)
            except ChatAdminRequiredError as e:
                logging.error(e.message)
            return handle

    return decorator


async def _is_admin(user_id: int):
    if user_id in settings.get("admins"):
        return True
    else:
        return False
