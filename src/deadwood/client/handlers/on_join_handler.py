import logging

from telethon import TelegramClient, events

from deadwood.adapters.db.dao import DAO
from deadwood.core.di.integrations.telethon import FromDishka
from deadwood.core.models import dto


async def init(client: TelegramClient) -> None:
    @client.on(  # type: ignore[untyped-decorator]
        events.ChatAction(
            func=lambda event: (
                event.is_group
                and event.user_id == client.me.id
                and event.user_joined
                or event.user_added
            ),
        ),
    )
    async def on_join_handler(
        event: events.ChatAction.Event,
        dao: FromDishka[DAO],
    ) -> None:
        try:
            await dao.chat.delete_chat(dto.Chat(chat_id=event.chat.id))
            logging.info(
                f"Joined chat ID[{event.chat.id}]: {event.chat.title}",
            )
        except Exception as e:
            logging.error(e)
