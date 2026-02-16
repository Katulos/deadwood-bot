import asyncio
import logging
import random

from telethon import TelegramClient, functions
from telethon.errors import (
    MessageDeleteForbiddenError,
)
from telethon.tl.custom import Message
from telethon.tl.types import SendMessageTypingAction

from app.client.decorators import command

start_command = "start"


async def init(client: TelegramClient):
    @command(start_command)
    async def start_command_handler(event: Message):
        try:
            await client(
                functions.messages.SetTypingRequest(
                    peer=event.chat.id,
                    action=SendMessageTypingAction(),
                ),
            )
            await asyncio.sleep(random.randint(3, 6))
            msg = await event.reply(
                "Start your anus, dog",
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
        except MessageDeleteForbiddenError:
            logging.warning("Grant permission can_delete_messages!")
