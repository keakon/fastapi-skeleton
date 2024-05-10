
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient

from app.main import app


client = TestClient(app)
transport = ASGITransport(app=app)  # type: ignore


def async_client():
    return AsyncClient(transport=transport, base_url="http://test")
