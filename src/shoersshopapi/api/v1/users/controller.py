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

from shoersshopapi.api.v1.validators.http import (
    oauth2_scheme,
    get_current_auth_user,
    RoleRequired,
)

router = APIRouter(
    tags=["User"],
    dependencies=[Depends(oauth2_scheme)]
)


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
    user: Annotated[
        UserWithId,
        Depends(RoleRequired("admin"))
    ],
    session: Annotated[
        AsyncSession,
        Depends(database.get_session)
    ],
    data: UserSchema,
):

    user_data = await UserCrud.create_user(session, data)
    return user_data


#  READ: один пользователь

@router.get(
    "/{user_id}",
    response_model=UserWithId,
    summary="Получить пользователя по ID",
)
async def get_user(
    user: Annotated[
        UserWithId,
        Depends(RoleRequired("admin"))
    ],
    session: Annotated[
        AsyncSession,
        Depends(database.get_session)
    ],
    user_id: str,
):
    user_data = await UserCrud.get_by_id(session, user_id)
    
    if not user_data:
        raise USERNOTFOUND
    
    return user_data


@router.get(
    "/{user_id}/full",
    response_model=UserFull,
    summary="Получить пользователя со всеми связями",
)
async def get_user_full(
    user: Annotated[
        UserWithId,
        Depends(RoleRequired("admin"))
    ],
    session: Annotated[
        AsyncSession,
        Depends(database.get_session)
    ],
    user_id: str,
):
    """Пользователь с адресами, заказами и отзывами"""
    user_data = await UserCrud.get_full(session, user_id)
    
    if not user_data:
        raise USERNOTFOUND
    
    return user_data


@router.get(
    "/{user_id}/orders",
    response_model=UserFull,
    summary="Получить пользователя с заказами",
)
async def get_user_orders(
    user: Annotated[
        UserWithId,
        Depends(RoleRequired("admin"))
    ],
    session: Annotated[
        AsyncSession,
        Depends(database.get_session)
    ],
    user_id: str,
):
    user_data = await UserCrud.get_with_orders(session, user_id)
    
    if not user_data:
        raise USERNOTFOUND
    
    return user_data


@router.get(
    "/{user_id}/reviews",
    response_model=UserFull,
    summary="Получить пользователя с отзывами",
)
async def get_user_reviews(
    user: Annotated[
        UserWithId,
        Depends(RoleRequired("admin"))
    ],
    session: Annotated[
        AsyncSession,
        Depends(database.get_session)
    ],
    user_id: str,
):
    user_data = await UserCrud.get_with_reviews(session, user_id)
    
    if not user_data:
        raise USERNOTFOUND
    
    return user_data


@router.get(
    "/{user_id}/addresses",
    response_model=UserFull,
    summary="Получить пользователя с адресами",
)
async def get_user_addresses(
    user: Annotated[
        UserWithId,
        Depends(RoleRequired("admin"))
    ],
    session: Annotated[
        AsyncSession,
        Depends(database.get_session)
    ],
    user_id: str,
):
    user_data = await UserCrud.get_with_addresses(session, user_id)
    
    if not user_data:
        raise USERNOTFOUND
    
    return user_data


#  READ: список пользователей

@router.get(
    "/",
    response_model=list[UserWithId],
    summary="Получить список пользователей",
)
async def get_users(
    user: Annotated[
        UserWithId,
        Depends(RoleRequired("admin"))
    ],
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
    "/",
    response_model=UserWithId,
)
async def update_self(
    user: Annotated[
        UserWithId,
        Depends(get_current_auth_user)
    ],
    session: Annotated[
        AsyncSession,
        Depends(database.get_session)
    ],
    data: UserUpdate,
):

    user_data = await UserCrud.update_user(session, user.id, data)
    
    if not user_data:
        raise USERNOTFOUND
    
    return user_data


@router.patch(
    "/{user_id}",
    response_model=UserWithId,
)
async def update_user(
    user: Annotated[
        UserWithId,
        Depends(RoleRequired("admin"))
    ],
    session: Annotated[
        AsyncSession,
        Depends(database.get_session)
    ],
    user_id: str,
    data: UserUpdate,
):

    user_data = await UserCrud.update_user(session, user_id, data)
    
    if not user_data:
        raise USERNOTFOUND
    
    return user_data


#  DELETE

@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(
    user: Annotated[
        UserWithId,
        Depends(RoleRequired("admin"))
    ],
    session: Annotated[
        AsyncSession,
        Depends(database.get_session)
    ],
    user_id: str,
):
    """Удалить пользователя по ID"""
    deleted = await UserCrud.delete_user(session, user_id)
    
    if not deleted:
        raise USERNOTFOUND