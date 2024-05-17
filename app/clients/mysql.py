import typing
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import config

async_engine = create_async_engine(
    str(config.MYSQL_DSN),
    pool_size=config.MYSQL_POOL_SIZE,
    max_overflow=config.MYSQL_MAX_OVERFLOW,
    pool_timeout=config.MYSQL_POOL_TIMEOUT,
)
async_session: async_sessionmaker[AsyncSession] = async_sessionmaker(async_engine, expire_on_commit=False)


@asynccontextmanager
async def get_session() -> typing.AsyncGenerator[AsyncSession, typing.Any]:
    session = async_session()
    try:
        yield session
    finally:
        await session.close()
