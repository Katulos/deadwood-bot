import asyncio
import logging
import random

from telethon import TelegramClient, functions
from telethon.errors import (
    MessageDeleteForbiddenError,
)
from telethon.tl.custom import Message
from telethon.tl.types import SendMessageTypingAction

from deadwood.client.decorators import command

id_command = "id"


async def init(client: TelegramClient) -> None:
    @command(id_command)  # type: ignore[untyped-decorator]
    async def id_command_handler(event: Message) -> None:
        # TODO: implement this
        # chat = (
        #     await Chat.filter(chat_id=event.chat.id)
        #     .prefetch_related("flags")
        #     .get_or_none()
        # )
        # if not chat.flags.enabled:
        #     return
        try:
            await client(
                functions.messages.SetTypingRequest(
                    peer=event.chat.id,
                    action=SendMessageTypingAction(),
                ),
            )
            await asyncio.sleep(random.randint(3, 6))

            msg = await event.reply(
                f"Your ID: `{event.from_id.user_id}`",
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
