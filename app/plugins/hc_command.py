import asyncio
import random
from typing import Any

import aiohttp
from aiohttp import ClientSession
from pyrogram import Client, errors
from pyrogram.types import Message

from app import cache
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
        msg = await client.send_photo(
            chat_id=message.chat.id,
            photo=f"https://i.4cdn.org/hc/{url_parts[0]}{url_parts[1]}",
            protect_content=True,
            has_spoiler=True,
            reply_to_message_id=message.reply_to_message_id
            if message.reply_to_message
            else message.id,
        )
        await asyncio.sleep(10)
        await client.delete_messages(
            chat_id=message.chat.id,
            message_ids=[message.id, msg.id],
        )
    except errors.WebpageMediaEmpty:
        await client.delete_messages(
            chat_id=message.chat.id,
            message_ids=[message.id],
        )


@cache.failover(ttl="1h")
@cache(ttl="24h")
async def fetch(client: ClientSession) -> Any:
    async with client.get("https://a.4cdn.org/hc/catalog.json") as resp:
        return await resp.json()
