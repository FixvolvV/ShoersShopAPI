from typing import Annotated
from fastapi import (
    Depends,
    HTTPException
)

from starlette import status

from sqlalchemy.ext.asyncio import AsyncSession

from shoersshopapi.api.v1.schemas import (
    UserUnique,
    User
)

from shoersshopapi.api.v1.users.crud import UserCrud
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