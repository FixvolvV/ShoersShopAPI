from typing import Annotated
from fastapi import (
    Depends,
    HTTPException
)
from pydantic import BaseModel
from starlette import status

from sqlalchemy.ext.asyncio import AsyncSession

from shoersshopapi.api.v1.schemas import (
    UserUnique,
    User,
    Users
)

from shoersshopapi.api.v1.schemas.user_schemas import UserWithId
from shoersshopapi.api.v1.users.crud import UserCrud
from shoersshopapi.api.v1.utils import gen_uuid, hash_password
from shoersshopapi.core.database import database


# Функция проверяющая уникальные данные при попытке добавления в базу данных
async def check_user_data(
    data: User,
    session: Annotated[
        AsyncSession,
        Depends(database.GetSession)
    ]
) -> User:

    exception = HTTPException (
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this username or mail already exists"
        )

    filters: UserUnique = UserUnique.model_validate(
        data.model_dump(include=set(UserUnique.model_fields))
    )

    if await UserCrud.find_all(session=session, filters=filters):
        raise exception

    return data

# Функция добавляющая пользователя в DB. 
async def create_user(
    data: User,
    session: AsyncSession
) -> UserWithId:

    user: UserWithId = UserWithId(**data.model_dump(), id=gen_uuid())

    user.password = hash_password(
        password=str(user.password)
    )

    await UserCrud.add(session=session, values=user)
    await session.commit()

    return user