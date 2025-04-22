from tortoise import fields


class CreatedAtMixin:
    created_at = fields.DatetimeField(auto_now_add=True)


class UpdatedAtMixin:
    updated_at = fields.DatetimeField(auto_now=True)


class CreatedUpdatedAtMixin(CreatedAtMixin, UpdatedAtMixin): ...
