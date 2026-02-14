from tortoise import BaseDBAsyncClient, fields
from tortoise.models import Model
from tortoise.signals import post_save


class Chat(Model):
    id = fields.BigIntField(pk=True)
    chat_id = fields.BigIntField(unique=True)
    chat_title = fields.CharField(default=False, max_length=128)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    flags: fields.OneToOneRelation["ChatFlag"]

    class Meta:
        table = "chat"


class ChatFlag(Model):
    id = fields.BigIntField(pk=True)
    enabled = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    chat = fields.OneToOneField(
        model_name="app.Chat",
        related_name="flags",
        on_delete=fields.CASCADE,
    )

    class Meta:
        table = "chat_flag"


@post_save(Chat)
async def chat_post_save(
    sender: type[Chat],
    instance: Chat,
    created: bool,
    using_db: BaseDBAsyncClient | None,
    update_fields: list[str],
) -> None:
    # pylint: disable=unused-argument
    await ChatFlag.update_or_create(chat_id=instance.id)
