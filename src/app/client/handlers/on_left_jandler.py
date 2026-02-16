import logging

from telethon import TelegramClient, events

from app.adapters.db.models import Chat


async def init(client: TelegramClient):
    @client.on(
        events.ChatAction(
            func=lambda event: (
                event.is_group
                and event.user_id == client.me.id
                and event.user_kicked
                or event.user_left
            ),
        ),
    )
    async def on_left_handler(event: events.ChatAction.Event):
        try:
            chat = await Chat.get_or_none(chat_id=event.chat.id)
            if chat:
                await chat.delete()
            logging.info(f"Left chat ID[{event.chat.id}]: {event.chat.title}")
        except Exception as e:
            logging.error(e)
