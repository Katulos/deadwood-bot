from collections.abc import AsyncIterable, AsyncIterator

from dishka import Provider, Scope, provide
from sqlalchemy import make_url
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from deadwood.adapters.db import dao
from deadwood.adapters.db.dao import DAO
from deadwood.core import settings


class DbProvider(Provider):
    scope = Scope.APP

    @provide
    async def provide_async_engine(
        self,
    ) -> AsyncIterable[AsyncEngine]:
        connection_url = settings.get("db.database_url")
        engine = create_async_engine(
            url=make_url(connection_url),
            future=True,
            # echo=settings.get("db.echo"),
        )

        yield engine

        await engine.dispose()

    @provide
    async def provide_async_sessionmaker(
        self,
        engine: AsyncEngine,
    ) -> async_sessionmaker[AsyncSession]:
        session_factory = async_sessionmaker(
            bind=engine,
            expire_on_commit=False,
            autoflush=False,
            class_=AsyncSession,
        )

        return session_factory

    @provide
    async def provide_async_session(
        self,
        session_factory: async_sessionmaker[AsyncSession],
    ) -> AsyncIterator[AsyncSession]:
        async with session_factory() as session:
            yield session


class DAOProvider(Provider):
    scope = Scope.REQUEST

    @provide
    async def provide_dao(
        self,
        session: AsyncSession,
    ) -> DAO:
        return DAO(session=session)

    @provide
    async def provide_chat_dao(self, dao: DAO) -> dao.ChatDao:
        return dao.chat
