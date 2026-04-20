# router name: "favorites"

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from shoersshopapi.api.v1.schemas.product_schemas import ProductWithAll
from shoersshopapi.core.database import database
from shoersshopapi.api.v1.schemas import (
    FavoriteAdd,
    FavoriteListResponse,
    FavoriteProductResponse,
    FavoriteWithId,
    UserWithId
)

from .crud import FavoriteCrud

from shoersshopapi.api.v1.validators.http import (
    oauth2_scheme,
    get_current_auth_user
)


router = APIRouter(
    tags=["Favorites"],
    dependencies=[Depends(oauth2_scheme)]
)

PRODUCT_NOT_FOUND_IN_FAVORITES = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Product not found in favorites"
)


# === Получить все избранные товары ===

@router.get(
    "/",
    response_model=FavoriteListResponse,
)
async def get_favorites(
    user: Annotated[
        UserWithId,
        Depends(get_current_auth_user)
    ],
    session: Annotated[
        AsyncSession,
        Depends(database.get_session)
    ],
):
    favorites = await FavoriteCrud.get_favorites(session, user.id)

    items = []
    for favorite in favorites:
        product = favorite.product
        items.append(
            FavoriteProductResponse(
                id=favorite.id,
                product=ProductWithAll.model_validate(product)
                )
        )

    return FavoriteListResponse(
        user_id=user.id,
        items=items,
        total=len(items),
    )


# === Добавить товар в избранное ===

@router.post(
    "/",
    response_model=FavoriteWithId,
    status_code=status.HTTP_201_CREATED,
)
async def add_to_favorites(
    user: Annotated[
        UserWithId,
        Depends(get_current_auth_user)
    ],
    session: Annotated[
        AsyncSession,
        Depends(database.get_session)
    ],
    data: Annotated[
        FavoriteAdd,
        Query(...)
    ],
):
    favorite = await FavoriteCrud.add_favorite(session, user.id, data.product_id)
    return favorite


# === Проверить, в избранном ли товар ===

@router.get(
    "/{product_id}/check",
    response_model=dict,
)
async def check_favorite(
    user: Annotated[
        UserWithId,
        Depends(get_current_auth_user)
    ],
    session: Annotated[
        AsyncSession,
        Depends(database.get_session)
    ],
    product_id: str,
):
    is_fav = await FavoriteCrud.is_favorite(session, user.id, product_id)
    return {"product_id": product_id, "is_favorite": is_fav}


# === Удалить товар из избранного ===

@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_from_favorites(
    user: Annotated[
        UserWithId,
        Depends(get_current_auth_user)
    ],
    session: Annotated[
        AsyncSession,
        Depends(database.get_session)
    ],
    product_id: str,
):
    removed = await FavoriteCrud.remove_favorite(session, user.id, product_id)

    if not removed:
        raise PRODUCT_NOT_FOUND_IN_FAVORITES


# === Очистить всё избранное ===

@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def clear_favorites(
    user: Annotated[
        UserWithId,
        Depends(get_current_auth_user)
    ],
    session: Annotated[
        AsyncSession,
        Depends(database.get_session)
    ],
):
    await FavoriteCrud.clear_favorites(session, user.id)