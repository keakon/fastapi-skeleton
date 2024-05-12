import logging
from datetime import datetime
from time import time

from argon2 import PasswordHasher
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text
from sqlmodel import Field, delete, select

from app.config import config
from app.schemas.token import TokenPayload
from app.utils.exception import (
    expired_token_error,
    internal_server_error,
    invalid_token_error,
)
from app.utils.token import decode_token, encode_token, oauth2_scheme

from . import BaseModel

HASHED_PASSWORD_PREFIX = '$argon2id$v=19$m=65536,t=3,p=4$'
HASHED_PASSWORD_PREFIX_LENGTH = len(HASHED_PASSWORD_PREFIX)
ph = PasswordHasher()


class UserBase(BaseModel):
    name: str


class User(UserBase, table=True):
    password: str
    created_at: datetime = Field(sa_column_kwargs={'server_default': text('CURRENT_TIMESTAMP')})
    updated_at: datetime = Field(
        sa_column_kwargs={'server_default': text('CURRENT_TIMESTAMP'), 'server_onupdate': text('CURRENT_TIMESTAMP')}
    )

    def __init__(self, name: str, password: str):
        self.name = name
        self.password = self.hash_password(password)

    @classmethod
    def hash_password(cls, password: str) -> str:
        return ph.hash(password)[HASHED_PASSWORD_PREFIX_LENGTH:]  # remove prefix to save space

    @classmethod
    def verify_password(cls, hashed_password: str, password: str) -> bool:
        return ph.verify(HASHED_PASSWORD_PREFIX + hashed_password, password)

    @classmethod
    async def get_verified_user_id(cls, session: AsyncSession, name: str, password: str) -> int:
        row = (await session.execute(select(cls.id, cls.password).where(cls.name == name))).first()
        if row:
            try:
                if cls.verify_password(row.password, password):
                    return row.id
            except Exception:
                return 0
        return 0

    @classmethod
    def generate_token(cls, user_id: int) -> bytes:
        now = int(time())
        token = TokenPayload(user_id=user_id, expire_at=now + config.TOKEN_EXPIRATION, not_before=now)
        return encode_token(token.model_dump())

    @classmethod
    async def delete_by_name(cls, session: AsyncSession, name: str) -> int:
        return (await session.execute(delete(cls).where(cls.name == name))).rowcount  # type: ignore


def get_current_user_id(token: str | bytes = Depends(oauth2_scheme)) -> int:
    paseto = decode_token(token)
    if not (paseto and isinstance(paseto.payload, bytes)):
        raise invalid_token_error
    try:
        payload = TokenPayload.model_validate_json(paseto.payload)
    except ValueError:
        raise invalid_token_error
    except Exception:
        logging.exception('')
        raise internal_server_error

    now = int(time())
    if now < payload.not_before:
        raise invalid_token_error
    if now > payload.expire_at:
        raise expired_token_error

    return payload.user_id
