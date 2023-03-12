from pyrogram import Client, filters
from pyrogram.types import Message

from app import logger
from app.models import Chat
from app.utils.utils import reload_admins, update_chat_member


# pylint: disable=no-member
@Client.on_message(filters.new_chat_members)
async def on_join_handler(client: Client, message: Message) -> None:
    await Chat.update_or_create(id=message.chat.id, name=message.chat.title)
    await update_chat_member(
        chat_id=message.chat.id,
        user_id=message.from_user.id,
    )
    logger.info(
        "ID %s %s has join",
        message.from_user.id,
        message.from_user.username,
    )
    await reload_admins(client, message.chat.id)
