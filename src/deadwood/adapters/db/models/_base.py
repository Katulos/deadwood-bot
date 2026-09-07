import typing as t

import sqlalchemy as sa
import sqlalchemy.schema as sh
from sqlalchemy import (
    Column,
)
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    InstrumentedAttribute,
)


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    __convention: dict[type[sh.Constraint | sh.Index], str] = {
        sh.Index: "ix__%(table_name)s__%(all_column_names)s",
        sh.UniqueConstraint: "uq__%(table_name)s__%(all_column_names)s",
        sh.CheckConstraint: "ck__%(table_name)s__%(constraint_name)s",
        sh.ForeignKeyConstraint: (
            "fk__%(table_name)s__%(all_column_names)s__"
            "%(referred_table_name)s"
        ),
        sh.PrimaryKeyConstraint: "pk__%(table_name)s",
    }

    __naming_convention = {  # type: ignore
        **__convention,
        "all_column_names": lambda constraint, table: "_".join(
            [column.name for column in constraint.columns.values()],
        ),
    }

    metadata = sa.MetaData(naming_convention=__naming_convention)

    @sa.event.listens_for(sa.engine.Engine, "connect")
    def _set_sqlite_pragma(dbapi, connection_record) -> None:  # type: ignore
        if hasattr(dbapi.dbapi, "sqlite"):  # type: ignore
            cursor = dbapi.cursor()  # type: ignore
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.execute("PRAGMA journal_mode=WAL")
            cursor.close()

    def to_dict(self) -> dict[str, t.Any]:
        return {
            f"{self.__tablename__}_{col.name}": getattr(self, col.name)
            for col in t.cast(list[Column[t.Any]], self.__table__.columns)
        }

    @staticmethod
    def _get_column(
        model: type["Base"],
        col: InstrumentedAttribute[t.Any],
    ) -> t.Any:
        name = col.name
        if name not in model.__table__.columns:
            raise ValueError(f"Column {name} not found in {model.__name__}")
        return name

    @classmethod
    def _get_primary_key(cls) -> t.Any:
        return list(cls.__table__.primary_key)[0].name
