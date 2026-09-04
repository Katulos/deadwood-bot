import logging

from telethon import TelegramClient, events

load_priority = 1


async def init(client: TelegramClient) -> None:
    @client.on(events.Raw)  # type: ignore[untyped-decorator]
    async def on_raw_update_handler(event: events.Raw) -> None:
        logging.debug(event)
