import logging
import typing as t

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute, selectinload

from deadwood.adapters.db.models import Base

T = t.TypeVar("T", bound=Base, covariant=True, contravariant=False)


class BaseDAO[T: Base]:
    def __init__(self, model: type[T], session: AsyncSession) -> None:
        self.model = model
        self.session = session

    async def commit(self) -> None:
        await self.session.commit()

    async def all(
        self,
        cls: type[T],
        join_tables: t.Any | list[t.Any] | None = None,
    ) -> t.Sequence[T]:
        statement = select(cls)
        if join_tables is not None:
            if not isinstance(join_tables, list):
                join_tables = [join_tables]
            statement = statement.options(selectinload(*join_tables))
        result = await self.session.execute(statement)
        return result.scalars().all()

    async def all_by_filter(
        self,
        cls: type[T],
        join_tables: t.Any | list[t.Any] | None = None,
        **kwargs: t.Any,
    ) -> t.Sequence[T]:
        statement = select(cls).filter_by(**kwargs)
        if join_tables is not None:
            if not isinstance(join_tables, list):
                join_tables = [join_tables]
            statement = statement.options(selectinload(*join_tables))
        result = await self.session.execute(statement)
        return result.scalars().all()

    async def get(
        self,
        cls: type[T],
        pk: t.Any,
        join_tables: t.Any | list[t.Any] | None = None,
    ) -> T | None:
        pk_name = cls._get_primary_key()
        pk_column = getattr(cls, pk_name)
        statement = select(cls).where(pk_column == pk)
        if join_tables is not None:
            if not isinstance(join_tables, list):
                join_tables = [join_tables]
            statement = statement.options(selectinload(*join_tables))
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def get_by_filter(
        self,
        cls: type[T],
        join_tables: t.Any | list[t.Any] | None = None,
        **kwargs: t.Any,
    ) -> T | None:
        statement = select(cls).filter_by(**kwargs)
        if join_tables is not None:
            if not isinstance(join_tables, list):
                join_tables = [join_tables]
            statement = statement.options(selectinload(*join_tables))
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def create(
        self,
        cls: type[T],
        **kwargs: t.Any,
    ) -> T:
        instance: T = cls(**kwargs)
        try:
            self.session.add(instance)
            await self.commit()
        except Exception as e:
            await self.session.rollback()
            logging.exception(e)
            raise
        return instance

    async def update(
        self,
        cls: type[T],
        pk: t.Any,
        **kwargs: t.Any,
    ) -> T:
        instance = await self.get(cls, pk)
        if instance is None:
            raise ValueError(f"Object with primary key {pk} not found")

        for key, value in kwargs.items():
            if hasattr(instance, key):
                setattr(instance, key, value)

        try:
            await self.commit()
        except Exception as e:
            await self.session.rollback()
            logging.exception(e)
            raise
        return instance

    async def delete(
        self,
        cls: type[T],
        pk: t.Any,
    ) -> None:
        instance = await self.get(cls, pk)
        if instance is None:
            raise ValueError(f"Object with primary key {pk} not found")

        try:
            await self.session.delete(instance)
            await self.commit()
        except Exception as e:
            await self.session.rollback()
            logging.exception(e)
            raise

    async def delete_by_key(
        self,
        cls: type[T],
        key: InstrumentedAttribute[t.Any],
        value: t.Any,
    ) -> T | None:
        instance = await self.get_by_key(cls, key, value)
        if instance:
            try:
                await self.session.delete(instance)
                await self.commit()
            except Exception as e:
                logging.exception(e)

        return instance

    async def get_by_key(
        self,
        cls: type[T],
        key: InstrumentedAttribute[t.Any],
        value: t.Any,
    ) -> T | None:
        statement = select(cls).filter_by(
            **{cls._get_column(cls, key): value},
        )
        result = await self.session.execute(statement)

        return result.scalars().first()

    async def update_or_create(
        self,
        cls: type[T],
        **kwargs: t.Any,
    ) -> T:
        instance = await self.get_by_filter(cls, **kwargs)

        if instance is not None:
            for key, value in kwargs.items():
                if hasattr(instance, key):
                    setattr(instance, key, value)
            try:
                await self.commit()
                return instance
            except Exception as e:
                await self.session.rollback()
                logging.exception(e)
                raise

        return await self.create(cls, **kwargs)
