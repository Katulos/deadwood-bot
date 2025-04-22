from tortoise import fields

from app.database import AbstractModel, CreatedUpdatedAtMixin


class Chat(AbstractModel, CreatedUpdatedAtMixin):
    chat_id = fields.BigIntField(unique=True)
    enabled = fields.BooleanField(default=False)

    class Meta:
        table = "chat"
