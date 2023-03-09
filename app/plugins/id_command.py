import asyncio
import random

from pyrogram import Client, enums, errors
from pyrogram.types import Message

from app import _, logger
from app.bot import command


@Client.on_message(command(["id"]))
async def id_command_handler(client: Client, message: Message) -> None:
    try:
        await client.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
        await asyncio.sleep(random.randint(3, 6))
        msg = await message.reply(
            _("Your ID: <pre>%(id)s</pre>")
            % {"id": str(message.from_user.id)},
            protect_content=True,
        )
        await asyncio.sleep(random.randint(10, 20))
        await client.delete_messages(
            chat_id=message.chat.id,
            message_ids=[msg.id, message.id],
        )
    except errors.MessageDeleteForbidden as e:
        logger.error(e)
