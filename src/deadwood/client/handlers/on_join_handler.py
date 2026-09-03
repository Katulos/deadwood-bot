import logging

from telethon import TelegramClient, events

from deadwood.adapters.db.models import Chat


async def init(client: TelegramClient):
    @client.on(
        events.ChatAction(
            func=lambda event: (
                event.is_group
                and event.user_id == client.me.id
                and event.user_joined
                or event.user_added
            ),
        ),
    )
    async def on_join_handler(event: events.ChatAction.Event):
        try:
            await Chat.update_or_create(
                chat_id=event.chat.id,
                chat_title=event.chat.title,
            )
            logging.info(
                f"Joined chat ID[{event.chat.id}]: {event.chat.title}",
            )
        except Exception as e:
            logging.error(e)
