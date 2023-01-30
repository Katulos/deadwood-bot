from __future__ import annotations

import logging
from functools import partial

from pyrogram import Client, filters
from tortoise import Tortoise

from app import TORTOISE_ORM, shared

command = partial(filters.command, prefixes=["!", "/", "."])


class Bot(Client):  # pylint: disable=too-many-ancestors
    def __init__(self):
        if shared.settings.PHONE:
            super().__init__(
                name=shared.settings.SESSION_URL,
                api_id=shared.settings.API_ID,
                api_hash=shared.settings.API_HASH,
                phone_number=shared.settings.PHONE,
                test_mode=shared.settings.TEST_ENV,
                plugins=dict(root="app.plugins"),
            )
            logging.info("Auth as user")
        elif shared.settings.BOT_TOKEN:
            super().__init__(
                name=shared.settings.SESSION_URL,
                api_id=shared.settings.API_ID,
                api_hash=shared.settings.API_HASH,
                bot_token=shared.settings.BOT_TOKEN,
                test_mode=shared.settings.TEST_ENV,
                plugins=dict(root="app.plugins"),
            )
            logging.info("Auth as bot")

    async def start(self):
        await Tortoise.init(config=TORTOISE_ORM)
        await super().start()  # pylint: disable=no-member

    async def stop(self):
        await Tortoise.close_connections()
        await super().stop()  # pylint: disable=no-member
