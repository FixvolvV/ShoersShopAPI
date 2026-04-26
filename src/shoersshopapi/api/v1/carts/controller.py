# shoersshopapi/api/v1/cart/controller.py

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from shoersshopapi.core.database import database
from .crud import CartCrud

from shoersshopapi.api.v1.schemas import (
    CartItemAdd,
    CartItemUpdate,
    CartItemResponse,
    UserWithId,
    ProductWithBrand
)

from shoersshopapi.api.v1.validators.http import (
    oauth2_scheme,
    get_current_auth_user
)

router = APIRouter(
    tags=["Cart"],
    dependencies=[Depends(oauth2_scheme)]
)

ITEMNOTFOUND = HTTPException(status_code=404, detail="Item not found")

@router.get(
    "/",
)
async def get_cart(
    user: Annotated[
        UserWithId,
        Depends(get_current_auth_user)
    ],
    session: Annotated[
        AsyncSession,
        Depends(database.get_session)
    ],
):
    cart = await CartCrud.get_cart_with_items(session, user.id)

    if not cart:
        return {"id": None, "user_id": user.id, "items": [], "total_amount": 0}

    # Формируем ответ с информацией о товарах
    items = []
    total_amount = 0 

    for cart_item in cart.cart_items: #pyright: ignore
        size = cart_item.items
        product = size.product
        item_total = product.price * cart_item.quantity
        total_amount += item_total

        items.append({
            "id": cart_item.id,
            "quantity": cart_item.quantity,
            "size_id": size.id,
            "size": size.size,
            "product_id": product.id,
            "article": product.article,
            "logo": product.logo,
            "price": product.price,
            "title": product.title
        })

    return {
        "id": cart.id, #pyright: ignore
        "user_id": cart.user_id, #pyright: ignore
        "items": items,
        "total_amount": total_amount,
    }


@router.post(
    "/items",
    response_model=CartItemResponse,
    status_code=status.HTTP_201_CREATED,
)
async def add_to_cart(
    user: Annotated[
        UserWithId,
        Depends(get_current_auth_user)
    ],
    session: Annotated[
        AsyncSession,
        Depends(database.get_session)
    ],
    data: CartItemAdd,
):
    item = await CartCrud.add_item(session, user.id, data)
    return item


@router.patch(
    "/items/{item_id}",
    response_model=CartItemResponse | None,
)
async def update_cart_item(
    user: Annotated[
        UserWithId,
        Depends(get_current_auth_user)
    ],
    session: Annotated[
        AsyncSession,
        Depends(database.get_session)
    ],
    item_id: str,
    data: CartItemUpdate,
):
    item = await CartCrud.update_item(session, user.id, item_id, data)

    if item is None and data.quantity > 0:
        raise ITEMNOTFOUND

    return item


@router.delete(
    "/items/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_from_cart(
    user: Annotated[
        UserWithId,
        Depends(get_current_auth_user)
    ],
    session: Annotated[
        AsyncSession,
        Depends(database.get_session)
    ],
    item_id: str,
):
    removed = await CartCrud.remove_item(session, user.id, item_id)

    if not removed:
        raise ITEMNOTFOUND


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def clear_cart(
    user: Annotated[
        UserWithId,
        Depends(get_current_auth_user)
    ],
    session: Annotated[
        AsyncSession,
        Depends(database.get_session)
    ],
):
    await CartCrud.clear_cart(session, user.id)