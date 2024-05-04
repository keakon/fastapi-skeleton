from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.config import config


async_engine = create_async_engine(str(config.MYSQL_DSN), poolclass=NullPool)
async_session = async_sessionmaker(async_engine, expire_on_commit=False)
