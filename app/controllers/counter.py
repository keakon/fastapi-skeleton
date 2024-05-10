from app.clients.redis import redis_client
from app.router import router


@router.get('/count')
async def get_count():
    count = await redis_client.incr('count')
    return {'count': count}
