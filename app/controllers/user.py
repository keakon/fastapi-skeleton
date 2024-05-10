from typing import Annotated

from fastapi import Body, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import Row

from app.clients.mysql import async_session
from app.models import all_is_instance
from app.models.user import User, UserBase, get_current_user_id
from app.router import router
from app.schemas.resp import Resp
from app.schemas.user import UserRequest
from app.utils.exception import HTTPError
from app.utils.format import models_dump, row_dump


@router.post('/user', response_model=Resp, response_model_exclude_none=True, status_code=201)
async def create_user(req: UserRequest):
    async with async_session() as session:
        user = User(**req.model_dump())
        session.add(user)
        await session.commit()
    return Resp()


@router.post('/login')
async def login(req: OAuth2PasswordRequestForm = Depends()):
    async with async_session() as session:
        user_id = await User.get_verified_user_id(session, req.username, req.password)
        if user_id:
            token = User.generate_token(user_id)
            return {'access_token': token, 'token_type': 'bearer'}
    raise HTTPError(400, msg='login failed')


@router.get('/user/{user_id}', response_model=UserBase)
async def get_user(user_id: int, current_user_id: int = Depends(get_current_user_id)):
    async with async_session() as session:
        user = await User.get_by_id(session, user_id, (User.id, User.name))
    if user:
        return user
    raise HTTPError(404)


@router.put('/user/{user_id}', response_model=Resp, response_model_exclude_none=True)
async def update_user(user_id: int, req: UserRequest, current_user_id: int = Depends(get_current_user_id)):
    if current_user_id == 1:
        req.password = User.hash_password(req.password)
        async with async_session() as session:
            if await User.update_by_id(session, user_id, req.model_dump()):
                await session.commit()
                return Resp()
        raise HTTPError(404)
    raise HTTPError(403)


@router.get('/user/{user_id}/name', response_model=Resp, response_model_exclude_none=True)
async def get_user_name(user_id: int, current_user_id: int = Depends(get_current_user_id)):
    async with async_session() as session:
        user_name = await User.get_by_id(session, user_id, User.name)  # type: ignore
    if user_name:
        return Resp(data={'name': user_name})
    raise HTTPError(404)


@router.patch('/user/{user_id}/name', response_model=Resp, response_model_exclude_none=True)
async def set_user_name(
    user_id: int, name: Annotated[str, Body(embed=True)], current_user_id: int = Depends(get_current_user_id)
):
    async with async_session() as session:
        if await User.update_by_id(session, user_id, {'name': name}):
            await session.commit()
            return Resp()
    raise HTTPError(404)


@router.get('/user/{user_id}/time', response_model=Resp, response_model_exclude_none=True)
async def get_user_time(user_id: int, current_user_id: int = Depends(get_current_user_id)):
    async with async_session() as session:
        row = await User.get_by_id(session, user_id, (User.created_at, User.updated_at))
    if row:
        assert isinstance(row, Row)
        return Resp(data=row_dump(row))
    raise HTTPError(404)


@router.get('/users', response_model=Resp, response_model_exclude_none=True)
async def get_user_list(current_user_id: int = Depends(get_current_user_id)):
    if current_user_id == 1:
        async with async_session() as session:
            users = await User.get_all(session)
        assert all_is_instance(users, User)
        return Resp(data={'users': models_dump(users, exclude=set(['password']))})
    raise HTTPError(403)
