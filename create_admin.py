import asyncio
import sys

from app.clients.mysql import get_session
from app.models.user import User


async def create_admin(password: str) -> None:
    async with get_session() as session:
        session.add(User(name='admin', password=password))
        await session.commit()


if __name__ == '__main__':
    password = sys.argv[1]
    asyncio.run(create_admin(password))
