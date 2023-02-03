from __future__ import annotations

import asyncio
from collections import defaultdict
from datetime import datetime, timedelta
from string import Template
from time import time

from pyrogram import Client, enums, errors, filters, types
from pyrogram.types import ChatPermissions

from app import logger
from app.config import shared
from app.utils.admins import ADMINS

shared.BANNED_USERS = BANNED_USERS = filters.user()

MESSAGES, SECONDS, CB_SECONDS = (
    shared.settings.MESSAGES,
    shared.settings.SECONDS,
    shared.settings.CB_SECONDS,
)

_users = defaultdict(list)


async def is_flood(
    user: types.User,
    messages: int = 1,
    seconds: int = 6,
    users=None,
) -> bool | None:
    """Checks if a user is flooding"""

    if users is None:
        users = _users
    users[user.id].append(time())
    check = list(filter(lambda x: time() - int(x) < seconds, users[user.id]))
    if len(check) > messages:
        users[user.id] = check
        return True


@Client.on_message((filters.private | filters.group) & ~ADMINS)
@Client.on_callback_query(~ADMINS)
async def on_flood_handler(
    client: Client,
    update: types.Message | types.CallbackQuery,
):
    if not update.from_user:
        return
    is_callback = isinstance(update, types.CallbackQuery)
    if await is_flood(
        update.from_user,
        messages=MESSAGES,
        seconds=CB_SECONDS if is_callback else SECONDS,
    ):
        if is_callback:
            return await update.answer(
                Template("Stop flooding! 😡").substitute(
                    SEC=shared.settings.CB_SECONDS,
                ),
                show_alert=True,
            )
        try:
            if update.chat.type != enums.ChatType.PRIVATE:
                await client.restrict_chat_member(
                    chat_id=update.chat.id,
                    user_id=update.from_user.id,
                    permissions=ChatPermissions(),
                    until_date=datetime.now()
                    + timedelta(minutes=shared.settings.CB_SECONDS),
                )
            elif not client.me.is_bot:
                await client.block_user(update.from_user.id)
        except errors.ChatAdminRequired as e:
            logger.error(e)
        except errors.UserAdminInvalid as e:
            logger.error(e)
        return BANNED_USERS.add(update.from_user.id)
    if update.from_user.id in BANNED_USERS:
        try:
            if update.chat.type != enums.ChatType.PRIVATE:
                await client.restrict_chat_member(
                    chat_id=update.chat.id,
                    user_id=update.from_user.id,
                    permissions=ChatPermissions(can_send_messages=True),
                )
            elif not client.me.is_bot:
                await client.unblock_user(update.from_user.id)
        except errors.ChatAdminRequired as e:
            logger.error(e)
        except errors.UserAdminInvalid as e:
            logger.error(e)
        BANNED_USERS.remove(update.from_user.id)
    await update.continue_propagation()


async def cleaner(
    users: defaultdict,
    sleep: float = 30,
    seconds: int = SECONDS,
):
    while not await asyncio.sleep(sleep):
        for user, _ in users.copy().items():
            check = list(
                filter(lambda x: time() - int(x) < seconds, users[user]),
            )
            if not check:
                del users[user]


asyncio.create_task(cleaner(users=_users))
