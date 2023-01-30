from __future__ import annotations

import asyncio
import re
from datetime import timedelta

from pyrogram import enums
from pyrogram.errors import FloodWait
from tortoise import timezone

from app import logger
from app.models import Chat, ChatMember


async def update_chat_member(chat_id: int, user_id: int, **kwargs):
    """update chat member"""
    await ChatMember.update_or_create(
        chat_id=chat_id,
        user_id=user_id,
        defaults=kwargs,
    )


async def chat_admins(chat_id: int):
    users = await ChatMember.get_or_none(chat_id=chat_id, is_banned=False)
    return users


async def is_admin(chat_id: int, user_id: int):
    """is admin check"""
    member = await ChatMember.get_or_none(chat_id=chat_id, user_id=user_id)
    return member and member.is_admin


async def is_banned(chat_id: int, user_id: int):
    """is banned check"""
    member = await ChatMember.get_or_none(chat_id=chat_id, user_id=user_id)
    return member and member.is_banned


async def chat_banned_users(chat_id: int):
    users = await ChatMember.get_or_none(chat_id=chat_id, is_banned=True)
    return users


async def is_bot(chat_id: int, user_id: int):
    """is bot check"""
    member = await ChatMember.get_or_none(chat_id=chat_id, user_id=user_id)
    return member and member.is_bot


async def reload_admins(client, chat_id):
    """reload admins"""
    await ChatMember.filter(chat_id=chat_id, is_admin=True).update(
        is_admin=False,
    )
    try:
        admin = False
        participants = []
        async for m in client.get_chat_members(
            chat_id=chat_id,
            filter=enums.ChatMembersFilter.ADMINISTRATORS,
        ):
            participants.append(m)
        for participant in participants:
            if not participant.user.is_deleted:
                admin_rights = participant.privileges
                if admin_rights.can_restrict_members:
                    admin = True
            await update_chat_member(
                chat_id,
                participant.user.id,
                is_admin=admin,
                is_bot=participant.user.is_bot,
                is_deleted=participant.user.is_deleted,
            )
            await Chat.filter(id=chat_id).update(
                last_admins_update=timezone.now(),
            )
    except FloodWait as e:
        logger.error(e)
        await asyncio.sleep(e.value)


def parse_time(time_str: str) -> timedelta:
    """parse time"""
    parse_time_regex = re.compile(
        r"((?P<hours>\d+?)hr)?((?P<minutes>\d+?)m)?((?P<seconds>\d+?)s)?",
    )
    parts = parse_time_regex.match(time_str)
    if not parts:
        return None
    parts = parts.groupdict()
    time_params = {}
    for name, param in parts.items():
        if param:
            time_params[name] = int(param)
    return timedelta(**time_params)
