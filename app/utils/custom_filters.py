from pyrogram import filters
from pyrogram.types import Update

from app.utils import utils


async def _admin_right(_, __, update: Update) -> bool:
    if not await utils.is_admin(update.chat.id, update.from_user.id):
        is_admin = False
    else:
        is_admin = True
    return is_admin


admin_right = filters.create(_admin_right)
