from tortoise import fields

from app.database import AbstractModel, CreatedUpdatedAtMixin


class Member(AbstractModel, CreatedUpdatedAtMixin):
    chat_id = fields.BigIntField(unique=True)

    class Meta:
        table = "member"
