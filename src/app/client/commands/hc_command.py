import asyncio
import logging
import random
from typing import Any

from aiohttp import ClientSession
from telethon import TelegramClient, functions
from telethon.errors import (
    MessageDeleteForbiddenError,
)
from telethon.tl.custom import Message
from telethon.tl.types import SendMessageTypingAction

from app.client.decorators import cache, command
from app.core.services import reddit

hc_command = "hc"


async def init(client: TelegramClient):
    @command(hc_command)
    async def hc_command_handler(event: Message):
        # TODO: implement this
        # chat = (
        #     await Chat.filter(chat_id=event.chat.id)
        #     .prefetch_related("flags")
        #     .get_or_none()
        # )
        # if not chat.flags.enabled:
        #     return
        content = []
        async with ClientSession() as session:
            pages = await _fetch(session)
            for page in pages:
                for thread in page["threads"]:
                    if "ext" in thread:
                        content.append([thread["tim"], thread["ext"]])
                    if "last_replies" in thread:
                        for replies in thread["last_replies"]:
                            if "ext" in replies:
                                content.append(
                                    [replies["tim"], replies["ext"]],
                                )
        await session.close()
        url_parts = random.choice(tuple(content))

        try:
            await client(
                functions.messages.SetTypingRequest(
                    peer=event.chat.id,
                    action=SendMessageTypingAction(),
                ),
            )
            await asyncio.sleep(random.randint(3, 6))

            msg = await event.reply(
                f"https://i.4cdn.org/hc/{url_parts[0]}{url_parts[1]}",  # url
                reply_to=(
                    event.message.reply_to_msg_id
                    if event.message.reply_to_msg_id
                    else event.message.id
                ),
            )
            await asyncio.sleep(random.randint(10, 20))
            await client.delete_messages(
                event.chat.id,
                message_ids=[msg.id, event.message.id],
            )
        except reddit.RedditException as e:
            await event.reply(e)
        except MessageDeleteForbiddenError:
            logging.warning("Grant permission can_delete_messages!")

    @cache.failover(ttl="1h")
    @cache(ttl="24h")
    async def _fetch(client: ClientSession) -> Any:
        async with client.get("https://a.4cdn.org/hc/catalog.json") as resp:
            return await resp.json()
