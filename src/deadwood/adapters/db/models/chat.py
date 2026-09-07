import sqlalchemy as sa
from sqlalchemy import orm

from deadwood.adapters.db.models import Base, CreatedUpdatedAtMixin
from deadwood.core.models import dto


class Chat(Base, CreatedUpdatedAtMixin):
    __tablename__ = "chats"

    id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer,
        primary_key=True,
    )

    chat_id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer,
        unique=True,
    )

    chat_title: orm.Mapped[str] = orm.mapped_column(
        sa.String(),
        nullable=True,
    )

    def to_dto(self) -> dto.Chat:
        return dto.Chat(
            chat_id=self.chat_id,
            chat_title=self.chat_title,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
