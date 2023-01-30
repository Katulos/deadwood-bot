from __future__ import annotations

from tortoise import BaseDBAsyncClient, Model, fields
from tortoise.signals import post_delete


class Chat(Model):
    id = fields.BigIntField(pk=True)
    name = fields.CharField(default=False, max_length=128)
    last_admins_update = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "chat"

    def __str__(self):
        return self.name


@post_delete(Chat)
async def chat_post_delete(
    sender: type[Chat],
    instance: Chat,
    using_db: BaseDBAsyncClient | None,
) -> None:
    # pylint: disable=unused-argument
    await ChatMember.filter(chat_id=instance.id).delete()


class ChatMember(Model):
    user_id = fields.BigIntField(pk=True)
    chat_id = fields.BigIntField()
    is_admin = fields.BooleanField(default=False)
    is_bot = fields.BooleanField(default=False)
    is_banned = fields.BooleanField(default=False)

    class Meta:
        table = "chat_member"
