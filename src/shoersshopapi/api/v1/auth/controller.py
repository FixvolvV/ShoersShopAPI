from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from shoersshopapi.core.database import database
from shoersshopapi.core.database.models import User

from shoersshopapi.api.v1.users.crud import UserCrud
from shoersshopapi.api.v1.schemas import UserSchema, UserWithId

from shoersshopapi.api.v1.schemas.jwt_schemas import JWTCreateSchema, TokenInfo
from shoersshopapi.api.v1.schemas.auth_schemas import RegisterSchema

from shoersshopapi.api.v1.auth.jwtgen import create_access_token, create_refresh_token

from shoersshopapi.api.v1.validators.http import (
    validate_auth_user,
    get_current_auth_user,
    get_current_auth_user_for_refresh,
)


router = APIRouter(tags=["Auth"])


#  REGISTER

@router.post(
    "/register/",
    response_model=UserWithId,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    data: RegisterSchema,
    session: Annotated[AsyncSession, Depends(database.get_session)],
):

    user = await UserCrud.create_user(session, data)
    return user


#  LOGIN

@router.post(
    "/login/",
    response_model=TokenInfo,
    summary="Авторизация",
)
async def login(
    user: Annotated[User, Depends(validate_auth_user)],
):

    jwt_user = JWTCreateSchema(
        id=user.id,
        role=user.role,
    )

    access_token = create_access_token(jwt_user)
    refresh_token = create_refresh_token(jwt_user)

    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
    )


#  REFRESH

@router.post(
    "/refresh/",
    response_model=TokenInfo,
    summary="Обновить токен",
)
async def refresh_token(
    user: Annotated[User, Depends(get_current_auth_user_for_refresh)],
):
    """
    Обновить access токен по refresh токену.
    """
    jwt_user = JWTCreateSchema(
        id=user.id,
        role=user.role,
    )

    access_token = create_access_token(jwt_user)
    refresh_token = create_refresh_token(jwt_user)

    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
    )


#  ME

@router.get(
    "/me/",
    response_model=UserWithId,
    summary="Текущий пользователь",
)
async def get_me(
    user: Annotated[User, Depends(get_current_auth_user)],
):

    return user