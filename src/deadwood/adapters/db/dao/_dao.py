from sqlalchemy.ext.asyncio import AsyncSession

from deadwood.adapters.db.dao.chat import ChatDao


class DAO:
    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self.session = session
        self.chat = ChatDao(session)

    async def commit(self) -> None:
        await self.session.commit()
