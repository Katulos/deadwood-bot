import logging

from telethon import TelegramClient, events

load_priority = 1


async def init(client: TelegramClient):
    @client.on(events.Raw)
    async def on_raw_update_handler(event: events.Raw):
        logging.debug(event)
