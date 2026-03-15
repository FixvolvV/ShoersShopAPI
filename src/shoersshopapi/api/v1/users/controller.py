from typing import Annotated

from fastapi import APIRouter, Depends, Response
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession

from shoersshopapi.api.v1.schemas import (
    UserSchema,
    UserWithId
)

from shoersshopapi.api.v1.users.crud import UserCrud
from shoersshopapi.core.database import database

router = APIRouter(
    tags=["User"]
)


@router.post(
    "/",
    response_class=JSONResponse
    )
async def addUser(
    user_data: UserSchema,
    session: Annotated[
        AsyncSession,
        Depends(database.GetSession)
    ],
    response: Response
):

    user = await UserCrud.create_user(data=user_data, session=session)

    return {
        "status": "OK",
        "user": user
    }
