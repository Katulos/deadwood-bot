import logging

from telethon import events

from app.client.bot import client


@client.on(events.Raw)
async def on_raw_update_handler(event: events.Raw):
    logging.debug(event)
