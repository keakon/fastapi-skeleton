from pydantic import AnyUrl, MySQLDsn, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    MYSQL_DSN: MySQLDsn = AnyUrl('mysql+asyncmy://root@127.0.0.1:3306/test?charset=utf8mb4')
    MYSQL_POOL_SIZE: int = 10
    MYSQL_MAX_OVERFLOW: int = 0
    MYSQL_POOL_TIMEOUT: int = 0

    REDIS_DSN: RedisDsn = AnyUrl('redis://127.0.0.1:6379/0?protocol=3')

    TOKEN_KEY: str = 'test'
    TOKEN_EXPIRATION: int = 60 * 60 * 24 * 7


config = Settings()
