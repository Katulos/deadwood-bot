from pyrogram import Client, filters
from pyrogram.types import Message

from app import logger
from app.models import Chat, ChatMember


@Client.on_message(filters.left_chat_member)
async def on_left_handler(client: Client, message: Message) -> None:
    try:
        if message.left_chat_member.id == client.me.id:
            chat = await Chat.filter(id=message.chat.id).get_or_none()
            await chat.delete()
            logger.info("Bot kicked")
        else:
            member = await ChatMember.filter(
                user_id=message.from_user.id,
                chat_id=message.chat.id,
            ).get_or_none()
            await member.delete()
            logger.info(
                "ID %s %s has left",
                message.from_user.id,
                message.from_user.username,
            )

    except BaseException as e:
        logger.error(e)
