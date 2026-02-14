from datetime import timedelta

from telethon import events
from tortoise import timezone

from app.adapters.db.models import Chat
from app.client.bot import client


@client.on(events.NewMessage(func=lambda event: event.is_group))
async def on_message_handler(event: events.NewMessage.Event):
    chat = await Chat.get_or_none(chat_id=event.chat.id)
    if chat:
        updated_at = chat.updated_at
        if timezone.now() - updated_at > timedelta(hours=1):
            await chat.update(updated_at=timezone.now())
    else:
        await Chat.update_or_create(
            chat_id=event.chat.id,
            chat_title=event.chat.title,
        )
