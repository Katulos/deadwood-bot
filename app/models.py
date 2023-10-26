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
    await ChatStatistic.filter(chat_id=instance.id).delete()


class ChatMember(Model):
    user_id = fields.BigIntField(pk=True)
    chat_id = fields.BigIntField()
    is_admin = fields.BooleanField(default=False)
    is_bot = fields.BooleanField(default=False)
    is_banned = fields.BooleanField(default=False)

    class Meta:
        table = "chat_member"


@post_delete(ChatMember)
async def member_post_delete(
    sender: type[ChatMember],
    instance: ChatMember,
    using_db: BaseDBAsyncClient | None,
) -> None:
    # pylint: disable=unused-argument
    await ChatStatistic.filter(
        chat_id=instance.chat_id,
        user_id=instance.user_id,
    ).delete()


class ChatStatistic(Model):
    user_id = fields.BigIntField()
    chat_id = fields.BigIntField()
    animation_count = fields.BigIntField(default=0)
    audio_count = fields.BigIntField(default=0)
    command_count = fields.BigIntField(default=0)
    contact_count = fields.BigIntField(default=0)
    dice_count = fields.BigIntField(default=0)
    document_count = fields.BigIntField(default=0)
    forward_count = fields.BigIntField(default=0)
    location_count = fields.BigIntField(default=0)
    photo_count = fields.BigIntField(default=0)
    pinned_message_count = fields.BigIntField(default=0)
    poll_count = fields.BigIntField(default=0)
    reaction_count = fields.BigIntField(default=0)
    sticker_count = fields.BigIntField(default=0)
    video_count = fields.BigIntField(default=0)
    voice_count = fields.BigIntField(default=0)
    message_count = fields.BigIntField(default=0)
    word_count = fields.BigIntField(default=0)
    letter_count = fields.BigIntField(default=0)

    class Meta:
        table = "chat_statistic"
