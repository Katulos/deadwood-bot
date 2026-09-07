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
                and event.user_kicked
                or event.user_left
            ),
        ),
    )
    async def on_left_handler(
        event: events.ChatAction.Event,
        dao: FromDishka[DAO],
    ) -> None:
        try:
            # chat = await Chat.get_or_none(chat_id=event.chat.id)
            # if chat:
            #     await chat.delete()
            chat = await dao.chat.if_exists(
                dto.Chat(
                    chat_id=event.chat.id,
                ),
            )
            if chat:
                logging.info("chat exists")

                # await dao.chat.delete()

            logging.info(f"Left chat ID[{event.chat.id}]: {event.chat.title}")
        except Exception as e:
            logging.error(e)
