from typing import Annotated

from fastapi import APIRouter, Depends, Response
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession

from shoersshopapi.api.v1.schemas import (
    UserSchema,
    UserWithId
)

from shoersshopapi.core.database import database

from .utils import (
    check_user_data
)
from .crud import (
    add_user
)

router = APIRouter(
    tags=["User"]
)


@router.post(
    "/",
    response_class=JSONResponse
    )
async def addUser(
    user_data: Annotated[
        UserSchema,
        Depends(check_user_data)
    ],
    session: Annotated[
        AsyncSession,
        Depends(database.GetSession)
    ],
    response: Response
):

    user: UserWithId = await add_user(data=user_data, session=session)

    return {
        "status": "OK",
        "user": user
    }
