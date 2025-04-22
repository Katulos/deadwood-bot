import asyncio

from telethon import TelegramClient
from telethon.tl.custom import Message

from app.utils.decorators import user_command
from app.utils.i18n import _
from app.utils.tools import get_mention


async def init(client: TelegramClient) -> None:
    @user_command(["start"])
    async def handler(event: Message) -> None:
        chat = await event.get_chat()
        async with event.client.action(chat, "typing"):
            await asyncio.sleep(2)
            sender = await event.get_sender()
            await event.reply(_("hello", {"user": get_mention(sender)}))
