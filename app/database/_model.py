from tortoise import Model, fields


class AbstractModel(Model):
    id = fields.BigIntField(pk=True)

    class Meta:
        abstract = True
