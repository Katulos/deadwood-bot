from datetime import timedelta

from pyrogram import Client, filters
from pyrogram.types import Message
from tortoise import timezone

from app.models import Chat
from app.plugins.public.on_flood_handler import BANNED_USERS
from app.utils.utils import reload_admins, update_chat_member


@Client.on_message(filters.group & ~BANNED_USERS, group=1000)
async def on_group_message_handler(client: Client, message: Message) -> None:
    chat = await Chat.get_or_none(id=message.chat.id)
    if chat is None:
        await Chat.update_or_create(
            id=message.chat.id,
            name=message.chat.title,
        )
        await reload_admins(client, message.chat.id)
    else:
        await update_chat_member(
            chat_id=message.chat.id,
            user_id=message.from_user.id,
        )
        last_update = chat.last_admins_update
        if timezone.now() - last_update > timedelta(hours=1):
            await reload_admins(client, message.chat.id)
