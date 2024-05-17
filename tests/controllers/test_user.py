import pytest
from sqlalchemy.exc import IntegrityError
from sqlmodel import col, delete

from app.clients.mysql import get_session
from app.models.user import User
from app.schemas.token import TokenPayload
from app.schemas.user import UserRequest
from app.utils.token import decode_token

from . import async_client


@pytest.mark.asyncio(scope='session')
async def test_create_user():
    async with get_session() as session:
        if await User.delete_by_name(session, 'test') > 0:
            await session.commit()

    async with async_client() as client:
        response = await client.post('/api/v1/user', json=UserRequest(name='test', password='test').model_dump())
        assert response.status_code == 201
        assert response.json()['code'] == 0

        with pytest.raises(IntegrityError):
            await client.post('/api/v1/user', json=UserRequest(name='test', password='test').model_dump())


@pytest.mark.asyncio(scope='session')
async def test_login():
    async with get_session() as session:
        if await User.delete_by_name(session, 'test') > 0:
            await session.commit()

    async with async_client() as client:
        response = await client.post('/api/v1/login', data={'username': 'test', 'password': 'test'})
        assert response.status_code == 400

        response = await client.post('/api/v1/user', json=UserRequest(name='test', password='test').model_dump())
        assert response.status_code == 201
        assert response.json()['code'] == 0

        response = await client.post('/api/v1/login', data={'username': 'test', 'password': 'test'})
        assert response.status_code == 200
        assert response.json()['access_token']


@pytest.mark.asyncio(scope='session')
async def test_get_user():
    async with async_client() as client:
        response = await client.post('/api/v1/login', data={'username': 'admin', 'password': 'admin'})
        assert response.status_code == 200
        access_token = response.json()['access_token']

        response = await client.get('/api/v1/user/1', headers={'Authorization': f'Bearer {access_token}'})
        assert response.status_code == 200
        assert response.json()['name'] == 'admin'

        response = await client.get('/api/v1/user/0', headers={'Authorization': f'Bearer {access_token}'})
        assert response.status_code == 404


@pytest.mark.asyncio(scope='session')
async def test_update_user():
    async with get_session() as session:
        if (await session.execute(delete(User).where(col(User.id) > 1))).rowcount > 0:
            await session.commit()

    async with async_client() as client:
        response = await client.post('/api/v1/user', json=UserRequest(name='test', password='test').model_dump())
        assert response.status_code == 201
        assert response.json()['code'] == 0

        response = await client.post('/api/v1/login', data={'username': 'test', 'password': 'test'})
        assert response.status_code == 200
        access_token = response.json()['access_token']

        token = decode_token(access_token)
        assert token and isinstance(token.payload, bytes)
        payload = TokenPayload.model_validate_json(token.payload)
        user_id = payload.user_id

        data = UserRequest(name='test2', password='test2').model_dump()
        response = await client.put(
            f'/api/v1/user/{user_id}', headers={'Authorization': f'Bearer {access_token}'}, json=data
        )
        assert response.status_code == 403

        response = await client.post('/api/v1/login', data={'username': 'admin', 'password': 'admin'})
        assert response.status_code == 200
        access_token = response.json()['access_token']

        response = await client.put(
            f'/api/v1/user/{user_id}', headers={'Authorization': f'Bearer {access_token}'}, json=data
        )
        assert response.status_code == 200

        response = await client.post('/api/v1/login', data={'username': 'test', 'password': 'test'})
        assert response.status_code == 400

        response = await client.post('/api/v1/login', data={'username': 'test2', 'password': 'test2'})
        assert response.status_code == 200

        response = await client.put('/api/v1/user/0', headers={'Authorization': f'Bearer {access_token}'}, json=data)
        assert response.status_code == 404


@pytest.mark.asyncio(scope='session')
async def test_get_user_name():
    async with get_session() as session:
        if (await session.execute(delete(User).where(col(User.id) > 1))).rowcount > 0:
            await session.commit()

    async with async_client() as client:
        response = await client.post('/api/v1/user', json=UserRequest(name='test', password='test').model_dump())
        assert response.status_code == 201
        assert response.json()['code'] == 0

        response = await client.post('/api/v1/login', data={'username': 'test', 'password': 'test'})
        assert response.status_code == 200
        access_token = response.json()['access_token']

        token = decode_token(access_token)
        assert token and isinstance(token.payload, bytes)
        payload = TokenPayload.model_validate_json(token.payload)
        user_id = payload.user_id

        response = await client.get(f'/api/v1/user/{user_id}/name', headers={'Authorization': f'Bearer {access_token}'})
        assert response.status_code == 200
        assert response.json()['data']['name'] == 'test'

        response = await client.get('/api/v1/user/1/name', headers={'Authorization': f'Bearer {access_token}'})
        assert response.status_code == 200
        assert response.json()['data']['name'] == 'admin'

        response = await client.get('/api/v1/user/0/name', headers={'Authorization': f'Bearer {access_token}'})
        assert response.status_code == 404


@pytest.mark.asyncio(scope='session')
async def test_set_user_name():
    async with get_session() as session:
        if (await session.execute(delete(User).where(col(User.id) > 1))).rowcount > 0:
            await session.commit()

    async with async_client() as client:
        response = await client.post('/api/v1/user', json=UserRequest(name='test', password='test').model_dump())
        assert response.status_code == 201
        assert response.json()['code'] == 0

        response = await client.post('/api/v1/login', data={'username': 'test', 'password': 'test'})
        assert response.status_code == 200
        access_token = response.json()['access_token']

        token = decode_token(access_token)
        assert token and isinstance(token.payload, bytes)
        payload = TokenPayload.model_validate_json(token.payload)
        user_id = payload.user_id

        response = await client.patch(
            f'/api/v1/user/{user_id}/name', headers={'Authorization': f'Bearer {access_token}'}, json={'name': 'test2'}
        )
        assert response.status_code == 200

        response = await client.post('/api/v1/login', data={'username': 'test', 'password': 'test'})
        assert response.status_code == 400

        response = await client.post('/api/v1/login', data={'username': 'test2', 'password': 'test'})
        assert response.status_code == 200

        response = await client.patch(
            '/api/v1/user/0/name', headers={'Authorization': f'Bearer {access_token}'}, json={'name': 'test2'}
        )
        assert response.status_code == 404


@pytest.mark.asyncio(scope='session')
async def test_get_user_time():
    async with get_session() as session:
        if (await session.execute(delete(User).where(col(User.id) > 1))).rowcount > 0:
            await session.commit()

    async with async_client() as client:
        response = await client.post('/api/v1/user', json=UserRequest(name='test', password='test').model_dump())
        assert response.status_code == 201
        assert response.json()['code'] == 0

        response = await client.post('/api/v1/login', data={'username': 'test', 'password': 'test'})
        assert response.status_code == 200
        access_token = response.json()['access_token']

        token = decode_token(access_token)
        assert token and isinstance(token.payload, bytes)
        payload = TokenPayload.model_validate_json(token.payload)
        user_id = payload.user_id

        response = await client.get(f'/api/v1/user/{user_id}/time', headers={'Authorization': f'Bearer {access_token}'})
        assert response.status_code == 200
        data = response.json()['data']
        created_at = data['created_at']
        updated_at = data['updated_at']
        assert created_at == updated_at

        response = await client.patch(
            f'/api/v1/user/{user_id}/name', headers={'Authorization': f'Bearer {access_token}'}, json={'name': 'test2'}
        )
        assert response.status_code == 200

        response = await client.get(f'/api/v1/user/{user_id}/time', headers={'Authorization': f'Bearer {access_token}'})
        assert response.status_code == 200
        data = response.json()['data']
        created_at2 = data['created_at']
        updated_at2 = data['updated_at']
        assert created_at == created_at2
        assert updated_at2 >= updated_at

        response = await client.get('/api/v1/user/0/time', headers={'Authorization': f'Bearer {access_token}'})
        assert response.status_code == 404


@pytest.mark.asyncio(scope='session')
async def test_get_user_list():
    async with get_session() as session:
        if (await session.execute(delete(User).where(col(User.id) > 1))).rowcount > 0:
            await session.commit()

    async with async_client() as client:
        response = await client.post('/api/v1/login', data={'username': 'admin', 'password': 'admin'})
        assert response.status_code == 200
        access_token = response.json()['access_token']

        response = await client.get('/api/v1/users', headers={'Authorization': f'Bearer {access_token}'})
        assert response.status_code == 200
        users = response.json()['data']['users']
        assert len(users) == 1
        user = users[0]
        assert user['id'] == 1
        assert user['name'] == 'admin'
        assert user['created_at'] > 0
        assert user['updated_at'] > 0

        response = await client.post('/api/v1/user', json=UserRequest(name='test', password='test').model_dump())
        assert response.status_code == 201
        assert response.json()['code'] == 0

        response = await client.get('/api/v1/users', headers={'Authorization': f'Bearer {access_token}'})
        assert response.status_code == 200
        users = response.json()['data']['users']
        assert len(users) == 2
        user = users[1]
        assert user['name'] == 'test'

        response = await client.post('/api/v1/login', data={'username': 'test', 'password': 'test'})
        assert response.status_code == 200
        access_token = response.json()['access_token']

        response = await client.get('/api/v1/users', headers={'Authorization': f'Bearer {access_token}'})
        assert response.status_code == 403
