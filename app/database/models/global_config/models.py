from tortoise import fields

from app.database import AbstractModel, CreatedAtMixin


class GlobalConfig(AbstractModel, CreatedAtMixin):
    chat_id = fields.BigIntField(unique=True)
    enabled = fields.BooleanField(default=False)

    class Meta:
        table = "global_config"
