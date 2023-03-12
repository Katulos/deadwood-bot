import asyncio
import random
from typing import Any

import aiohttp
import pyrogram
from aiohttp import ClientSession
from pyrogram import Client, enums
from pyrogram.types import Message

from app import cache, logger
from app.bot import command


@Client.on_message(command(["hc"]))
async def hc_command_handler(client: Client, message: Message) -> None:
    content = []
    async with aiohttp.ClientSession() as session:
        pages = await fetch(session)
        for page in pages:
            for thread in page["threads"]:
                if "ext" in thread:
                    content.append([thread["tim"], thread["ext"]])
                if "last_replies" in thread:
                    for replies in thread["last_replies"]:
                        if "ext" in replies:
                            content.append([replies["tim"], replies["ext"]])
    await session.close()
    url_parts = random.choice(tuple(content))
    try:
        await client.send_chat_action(
            message.chat.id,
            enums.ChatAction.TYPING,
        )
        await asyncio.sleep(random.randint(3, 6))
        msg = await message.reply(
            f"https://i.4cdn.org/hc/{url_parts[0]}{url_parts[1]}",  # url
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
    except pyrogram.errors.WebpageMediaEmpty:
        await client.delete_messages(
            chat_id=message.chat.id,
            message_ids=[message.id],
        )
    except pyrogram.errors.MessageDeleteForbidden as e:
        logger.error(e)


@cache.failover(ttl="1h")
@cache(ttl="24h")
async def fetch(client: ClientSession) -> Any:
    async with client.get("https://a.4cdn.org/hc/catalog.json") as resp:
        return await resp.json()
