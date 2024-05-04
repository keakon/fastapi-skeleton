from typing import Any, Sequence, TypeGuard

from sqlalchemy import Column, Row
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.sql import func, text
from sqlalchemy.sql.elements import TextClause
from sqlmodel import delete, Field, insert, SQLModel, select, update


Values = dict[str, Any]


def is_sql_models(vals) -> TypeGuard[Sequence[SQLModel]]:
    return isinstance(vals, Sequence) and all(isinstance(val, SQLModel) for val in vals)


class BaseModel(SQLModel, table=False):
    id: int | None = Field(default=None, primary_key=True)

    @classmethod
    async def get_by_id(
        cls,
        session: AsyncSession,
        id: int,
        columns: list | tuple | InstrumentedAttribute | TextClause | Column | None = None,
        for_update: bool = False,
        for_read: bool = False
    ) -> 'BaseModel | Row | None':
        if columns is None:
            query = select(cls)
            scalar = True
        else:
            if isinstance(columns, (list, tuple)):
                query = select(*columns)
                scalar = False
            else:
                query = select(columns)
                scalar = True
        query = query.where(cls.id == id)
        if for_update:
            query = query.with_for_update()
        elif for_read:
            query = query.with_for_update(read=True)
        if scalar:
            return (await session.scalars(query)).first()
        else:
            return (await session.execute(query)).first()

    @classmethod
    async def get_by_ids(
        cls,
        session: AsyncSession,
        ids: Sequence[int],
        columns: list | tuple | InstrumentedAttribute | TextClause | Column | None = None,
        for_update: bool = False,
        for_read: bool = False
    ) -> 'Sequence[BaseModel | Row]':
        if not ids:
            return []
        if columns is None:
            query = select(cls)
            scalar = True
        else:
            if isinstance(columns, (list, tuple)):
                query = select(*columns)
                scalar = False
            else:
                query = select(columns)
                scalar = True
        query = query.where(cls.id.in_(ids))  # type: ignore
        if for_update:
            query = query.with_for_update()
        elif for_read:
            query = query.with_for_update(read=True)
        if scalar:
            return (await session.scalars(query)).all()
        else:
            return (await session.execute(query)).all()

    @classmethod
    async def exsit(
        cls,
        session: AsyncSession,
        id: int,
        for_update: bool = False,
        for_read: bool = False
    ) -> bool:
        query = select(text('1')).select_from(cls).where(cls.id == id)
        if for_update:
            query = query.with_for_update()
        elif for_read:
            query = query.with_for_update(read=True)
        return (await session.scalars(query)).first() is not None

    @classmethod
    async def get_all(
        cls,
        session: AsyncSession,
        columns: list | tuple | InstrumentedAttribute | None = None,
        for_update: bool = False,
        for_read: bool = False
    ) -> 'Sequence[BaseModel | Row]':
        if columns is None:
            query = select(cls)
            scalar = True
        else:
            if isinstance(columns, (list, tuple)):
                query = select(*columns)
                scalar = False
            else:
                query = select(columns)
                scalar = True
        if for_update:
            query = query.with_for_update()
        elif for_read:
            query = query.with_for_update(read=True)
        if scalar:
            return (await session.scalars(query)).all()
        else:
            return (await session.execute(query)).all()

    @classmethod
    async def count_all(cls, session: AsyncSession) -> int:
        return (await session.scalars(select(func.count()).select_from(cls))).first()  # type: ignore

    @classmethod
    async def update_by_id(cls, session: AsyncSession, id: int, values: Values) -> int:
        return (await session.execute(update(cls).where(cls.id == id).values(**values))).rowcount  # type: ignore

    @classmethod
    async def delete_by_id(cls, session: AsyncSession, id: int) -> int:
        return (await session.execute(delete(cls).where(cls.id == id))).rowcount  # type: ignore

    @classmethod
    async def delete_by_ids(cls, session: AsyncSession, ids: Sequence[int]) -> int:
        return (await session.execute(delete(cls).where(cls.id.in_(ids)))).rowcount  # type: ignore

    @classmethod
    async def insert(cls, session: AsyncSession, values: Values) -> int:
        return (await session.execute(insert(cls).values(**values))).rowcount

    @classmethod
    async def batch_insert(cls, session: AsyncSession, values: list[Values | tuple]) -> int:
        return (await session.execute(insert(cls).values(values))).rowcount
