from sqlalchemy.ext.asyncio import AsyncSession

from deadwood.adapters.db import models
from deadwood.adapters.db.dao import BaseDAO
from deadwood.core.models import dto


class ChatDao(BaseDAO[models.Chat]):
    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        super().__init__(
            models.Chat,
            session,
        )

    async def upsert(self, chat: dto.Chat) -> dto.Chat:
        kwargs = {
            "chat_id": chat.chat_id,
            "chat_title": chat.chat_title,
        }
        instance = await self.update_or_create(models.Chat, **kwargs)
        return instance.to_dto()

    async def delete_chat(self, chat: dto.Chat) -> bool:
        instance = await self.delete_by_key(
            models.Chat,
            key=models.Chat.chat_id,
            value=chat.chat_id,
        )
        if instance:
            return True
        else:
            return False
