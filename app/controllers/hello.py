from fastapi import Depends
from sqlmodel import col

from app.clients.mysql import async_session
from app.models.user import User, get_current_user_id
from app.router import router
from app.schemas.resp import Resp


@router.get('/hello/{user_name}', response_model=Resp, response_model_exclude_none=True)
def hello(user_name: str):
    return Resp(msg=f'Hello, {user_name}!')


@router.get('/hello', response_model=Resp, response_model_exclude_none=True)
async def hello_to_self(current_user_id: int = Depends(get_current_user_id)):
    async with async_session() as session:
        user_name = await User.get_by_id(session, current_user_id, col(User.name))
    return Resp(msg=f'Hello, {user_name}!')
