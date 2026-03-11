from typing import Annotated

from fastapi import APIRouter, Depends, Response
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession

from shoersshopapi.api.v1.schemas import (
    User,
    UserWithId
)

from shoersshopapi.core.database import database

from .utils import (
    check_user_data,
    create_user
)

router = APIRouter(
    tags=["User"]
)


@router.post(
    "/"
    )
async def addUser(
    user_data: Annotated[
        User,
        Depends(check_user_data)
    ],
    session: Annotated[
        AsyncSession,
        Depends(database.GetSession)
    ],
    response: Response
):

    user: UserWithId = await create_user(data=user_data, session=session)

    return {
        "status": "OK",
        "user": user
    }
