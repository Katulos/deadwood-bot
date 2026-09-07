import logging

from telethon import TelegramClient, events

from deadwood.adapters.db.dao import DAO
from deadwood.core.di.integrations.telethon import FromDishka
from deadwood.core.models import dto

load_priority = 2


async def init(client: TelegramClient) -> None:

    @client.on(events.NewMessage(func=lambda event: event.is_group))  # type: ignore[untyped-decorator]
    async def on_group_message_handler(
        event: events.NewMessage.Event,
        dao: FromDishka[DAO],
    ) -> None:
        await dao.chat.upsert(
            dto.Chat(
                chat_id=event.chat.id,
                chat_title=event.chat.title,
            ),
        )
        logging.info(
            f"Joined chat ID[{event.chat.id}]: {event.chat.title}",
        )
