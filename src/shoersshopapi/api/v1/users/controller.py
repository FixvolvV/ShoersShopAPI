# shoersshopapi/api/v1/user/controller.py

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from shoersshopapi.core.database import database
from shoersshopapi.core.utils.enum import Role

from shoersshopapi.api.v1.schemas.user_schemas import UserWithId
from shoersshopapi.api.v1.users.crud import UserCrud
from shoersshopapi.api.v1.schemas import (
    UserSchema,
    UserUpdate,
    UserFilter,
    UserFull,
)


router = APIRouter(tags=["User"])


USERNOTFOUND = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )


#  CREATE

@router.post(
    "/",
    response_model=UserWithId,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    data: UserSchema,
    session: Annotated[
        AsyncSession,
        Depends(database.get_session)
    ]
):

    user = await UserCrud.create_user(session, data)
    return user


#  READ: один пользователь

@router.get(
    "/{user_id}",
    response_model=UserWithId,
    summary="Получить пользователя по ID",
)
async def get_user(
    user_id: str,
    session: Annotated[
        AsyncSession,
        Depends(database.get_session)
    ]
):
    user = await UserCrud.get_by_id(session, user_id)
    
    if not user:
        raise USERNOTFOUND
    
    return user


@router.get(
    "/{user_id}/full",
    response_model=UserFull,
    summary="Получить пользователя со всеми связями",
)
async def get_user_full(
    user_id: str,
    session: Annotated[
        AsyncSession,
        Depends(database.get_session)
    ]
):
    """Пользователь с адресами, заказами и отзывами"""
    user = await UserCrud.get_full(session, user_id)
    
    if not user:
        raise USERNOTFOUND
    
    return user


@router.get(
    "/{user_id}/orders",
    response_model=UserFull,
    summary="Получить пользователя с заказами",
)
async def get_user_orders(
    user_id: str,
    session: Annotated[
        AsyncSession,
        Depends(database.get_session)
    ]
):
    user = await UserCrud.get_with_orders(session, user_id)
    
    if not user:
        raise USERNOTFOUND
    
    return user


@router.get(
    "/{user_id}/reviews",
    response_model=UserFull,
    summary="Получить пользователя с отзывами",
)
async def get_user_reviews(
    user_id: str,
    session: Annotated[
        AsyncSession,
        Depends(database.get_session)
    ]
):
    user = await UserCrud.get_with_reviews(session, user_id)
    
    if not user:
        raise USERNOTFOUND
    
    return user


@router.get(
    "/{user_id}/addresses",
    response_model=UserFull,
    summary="Получить пользователя с адресами",
)
async def get_user_addresses(
    user_id: str,
    session: Annotated[
        AsyncSession,
        Depends(database.get_session)
    ]
):
    user = await UserCrud.get_with_addresses(session, user_id)
    
    if not user:
        raise USERNOTFOUND
    
    return user


#  READ: список пользователей

@router.get(
    "/",
    response_model=list[UserWithId],
    summary="Получить список пользователей",
)
async def get_users(
    session: Annotated[
        AsyncSession,
        Depends(database.get_session)
    ],
    # Фильтры
    phone: Annotated[str | None, Query(description="Фильтр по телефону")] = None,
    email: Annotated[str | None, Query(description="Фильтр по email")] = None,
    role: Annotated[Role | None, Query(description="Фильтр по роли")] = None,
    # Пагинация
    page: Annotated[int, Query(ge=1, description="Номер страницы")] = 1,
    limit: Annotated[int, Query(ge=1, le=100, description="Количество на странице")] = 20,
):
    """
    Получить список пользователей с фильтрами и пагинацией.
    """
    filters = UserFilter(
        phone=phone,
        email=email,
        role=role,
    )
    
    offset = (page - 1) * limit
    
    users = await UserCrud.get_all(
        session,
        filters=filters,
        limit=limit,
        offset=offset,
    )
    
    return users


#  UPDATE

@router.patch(
    "/{user_id}",
    response_model=UserWithId,
)
async def update_user(
    user_id: str,
    data: UserUpdate,
    session: Annotated[
        AsyncSession,
        Depends(database.get_session)
    ]
):

    user = await UserCrud.update_user(session, user_id, data)
    
    if not user:
        raise USERNOTFOUND
    
    return user


#  DELETE

@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(
    user_id: str,
    session: Annotated[
        AsyncSession,
        Depends(database.get_session)
    ]
):
    """Удалить пользователя по ID"""
    deleted = await UserCrud.delete_user(session, user_id)
    
    if not deleted:
        raise USERNOTFOUND