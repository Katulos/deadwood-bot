import asyncio

from pyrogram import Client, enums, errors, filters
from pyrogram.types import Message

from app import _, logger
from app.bot import command


# pylint: disable=no-member
@Client.on_message(command(["start"]) & (filters.group | filters.private))
async def start_command_handler(client: Client, message: Message) -> None:
    await client.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
    await asyncio.sleep(3)
    msg = await message.reply(_("Start your anus, dog"))
    try:
        await client.delete_messages(
            chat_id=message.chat.id,
            message_ids=[msg.id, message.id],
        )
    except errors.MessageDeleteForbidden as e:
        logger.error(e)
