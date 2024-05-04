import redis.asyncio as redis

from app.config import config


pool = redis.ConnectionPool.from_url(str(config.REDIS_DSN))
redis_client = redis.Redis(connection_pool=pool)
