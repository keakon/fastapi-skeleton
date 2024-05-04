import app.clients.mysql
import tests.clients.mysql


# monkeypatch for pytest-asyncio: https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#using-multiple-asyncio-event-loops
app.clients.mysql.async_session = tests.clients.mysql.async_session
