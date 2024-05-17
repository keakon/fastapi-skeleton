import pytest
from sqlmodel import col, delete

from app.clients.mysql import get_session
from app.models.user import User

from . import async_client, client


def test_hello():
    response = client.get('/api/v1/hello/abc')
    assert response.status_code == 200
    assert response.json()['code'] == 0
    assert response.json()['msg'] == 'Hello, abc!'


@pytest.mark.asyncio(scope='session')
async def test_hello_to_self():
    async with get_session() as session:
        if (await session.execute(delete(User).where(col(User.id) > 1))).rowcount > 0:
            await session.commit()

    async with async_client() as client:
        response = await client.post('/api/v1/login', data={'username': 'admin', 'password': 'admin'})
        assert response.status_code == 200
        access_token = response.json()['access_token']

        response = await client.get('/api/v1/hello')
        assert response.status_code == 401

        response = await client.get('/api/v1/hello', headers={'Authorization': 'Bearer 123'})
        assert response.status_code == 401

        response = await client.get('/api/v1/hello', headers={'Authorization': f'Bearer {access_token}'})
        assert response.status_code == 200
        assert response.json()['msg'] == 'Hello, admin!'
