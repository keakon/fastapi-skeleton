import pytest

from . import async_client


@pytest.mark.asyncio
async def test_get_count():
    async with async_client() as client:
        response = await client.get('/api/v1/count')
        assert response.status_code == 200
        count = response.json()['count']
        assert count > 0

        response = await client.get('/api/v1/count')
        assert response.status_code == 200
        new_count = response.json()['count']
        assert new_count == count + 1
