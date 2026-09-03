import asyncio
import logging
import random
import re
from typing import Any

from telethon import TelegramClient, functions
from telethon.errors import (
    MessageDeleteForbiddenError,
)
from telethon.tl.custom import Message
from telethon.tl.types import SendMessageTypingAction

from deadwood.client.decorators import cache, par_command
from deadwood.core.services import reddit

r_command = "r"


async def init(client: TelegramClient):
    @par_command(r_command)
    async def r_command_handler(event: Message):
        # TODO: implement this
        # chat = (
        #     await Chat.filter(chat_id=event.chat.id)
        #     .prefetch_related("flags")
        #     .get_or_none()
        # )
        # if not chat.flags.enabled:
        #     return
        pattern = rf"(?i)^[/!\\.]{r_command} (.*?)$"
        if re.match(pattern, event.text):
            s = event.text[3:]
            try:
                data = await _fetch(s)
                media = random.choice(tuple(data))
                await client(
                    functions.messages.SetTypingRequest(
                        peer=event.chat.id,
                        action=SendMessageTypingAction(),
                    ),
                )
                await asyncio.sleep(random.randint(3, 6))

                msg = await event.reply(
                    media[0],
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
    async def _fetch(request) -> Any:
        _reddit = reddit.RedditWrapper()
        media = await _reddit.fetch(request)
        if not media:
            raise reddit.RedditException("Use another tag, Luke")
        return media
