from datetime import timedelta

from telethon import TelegramClient, events
from tortoise import timezone

from deadwood.adapters.db.models import Chat

load_priority = 2


async def init(client: TelegramClient):
    @client.on(events.NewMessage(func=lambda event: event.is_group))
    async def on_group_message_handler(event: events.NewMessage.Event):
        chat = await Chat.get_or_none(chat_id=event.chat.id)
        if chat:
            updated_at = chat.updated_at
            if timezone.now() - updated_at > timedelta(hours=1):
                chat.updated_at = timezone.now()
                await chat.save()
        else:
            await Chat.update_or_create(
                chat_id=event.chat.id,
                chat_title=event.chat.title,
            )
