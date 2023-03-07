import asyncio
import random
import re
from typing import Any

import pyrogram
from pyrogram import Client, enums, filters
from pyrogram.types import Message

from app import cache, logger
from app.bot import command
from app.utils.reddit import RedditException, RedditWrapper

r_command = "r"


# pylint: disable=no-member
@Client.on_message(
    command([r_command]) & (filters.group | filters.private),
)
async def r_command_handler(client: Client, message: Message) -> None:
    pattern = rf"(?i)^[/!\\.]{r_command} (.*?)$"
    if re.match(pattern, message.text):
        s = message.text[3:]
        try:
            data = await fetch(s)
            media = random.choice(tuple(data))
            await client.send_chat_action(
                message.chat.id,
                enums.ChatAction.TYPING,
            )
            await asyncio.sleep(random.randint(3, 6))
            msg = await message.reply(
                media[0],  # url
                reply_to_message_id=(
                    message.reply_to_message_id
                    if message.reply_to_message
                    else message.id
                ),
                protect_content=True,
            )
            await asyncio.sleep(random.randint(10, 20))
            await client.delete_messages(
                chat_id=message.chat.id,
                message_ids=[msg.id, message.id],
            )
        except RedditException as e:
            await message.reply(e)
        except pyrogram.errors.MessageDeleteForbidden as e:
            logger.error(e)


@cache.failover(ttl="1h")
@cache(ttl="24h")
async def fetch(request) -> Any:
    reddit = RedditWrapper()
    media = await reddit.fetch(request)
    if not media:
        raise RedditException("Use another tag, Luke")
    return media
