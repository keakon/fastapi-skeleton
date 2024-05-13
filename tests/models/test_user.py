import pytest
from argon2.exceptions import VerifyMismatchError
from sqlmodel import col, delete

from app.clients.mysql import async_session
from app.models.user import User, get_current_user_id
from app.utils.exception import HTTPError


class TestUser:
    def test_hash_and_verify_password(self):
        password1 = '123'
        hashed_password1 = User.hash_password(password1)
        assert len(hashed_password1) == 66
        assert User.verify_password(hashed_password1, password1)

        hashed_password2 = User.hash_password(password1)
        assert len(hashed_password2) == 66
        assert hashed_password1 != hashed_password2
        assert User.verify_password(hashed_password2, password1)

        password3 = ''
        hashed_password3 = User.hash_password(password3)
        assert len(hashed_password3) == 66
        assert hashed_password1 != hashed_password3
        assert User.verify_password(hashed_password3, password3)

        with pytest.raises(VerifyMismatchError):
            User.verify_password(hashed_password3, password1)

        with pytest.raises(VerifyMismatchError):
            User.verify_password(hashed_password1, password3)

    @pytest.mark.asyncio(scope='session')
    async def test_get_verified_user_id(self):
        async with async_session() as session:
            if (await session.execute(delete(User).where(col(User.id) > 1))).rowcount > 0:
                await session.commit()

            assert await User.get_verified_user_id(session, 'admin', 'admin') == 1
            assert await User.get_verified_user_id(session, 'admin', '123') == 0
            assert await User.get_verified_user_id(session, '123', '456') == 0

    def test_generate_token(self):
        token1 = User.generate_token(1)
        token2 = User.generate_token(1)
        assert token1 != token2

        token3 = User.generate_token(2)
        assert token1 != token3

    @pytest.mark.asyncio(scope='session')
    async def test_delete_by_name(self):
        async with async_session() as session:
            if (await session.execute(delete(User).where(col(User.id) > 1))).rowcount > 0:
                await session.commit()

            assert await User.delete_by_name(session, 'test') == 0

            session.add(User(name='test', password='123'))
            await session.commit()
            assert await User.delete_by_name(session, 'test') == 1
            assert await User.delete_by_name(session, 'test') == 0


def test_get_current_user_id():
    with pytest.raises(HTTPError):
        get_current_user_id('')
    with pytest.raises(HTTPError):
        get_current_user_id('1')

    token = User.generate_token(1)
    assert get_current_user_id(token) == 1

    token = User.generate_token(2)
    assert get_current_user_id(token) == 2
