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
)

router = APIRouter(tags=["Cart"])

ITEMNOTFOUND = HTTPException(status_code=404, detail="Item not found")

@router.get(
    "/{user_id}",
)
async def get_cart(
    session: Annotated[
        AsyncSession,
        Depends(database.get_session)
    ],
    user_id: str,  # потом из JWT
):
    cart = await CartCrud.get_cart_with_items(session, user_id)

    if not cart:
        return {"id": None, "user_id": user_id, "items": [], "total_amount": 0}

    # Формируем ответ с информацией о товарах
    items = []
    total_amount = 0

    for cart_item in cart.cart_items:
        product = cart_item.product
        item_total = product.price * cart_item.quantity
        total_amount += item_total

        items.append({
            "id": cart_item.id,
            "product_id": product.id,
            "quantity": cart_item.quantity,
            "title": product.title,
            "price": product.price,
            "color": product.color,
            "brand_logo": product.brand.brand_logo if product.brand else None,
        })

    return {
        "id": cart.id,
        "user_id": cart.user_id,
        "items": items,
        "total_amount": total_amount,
    }


@router.post(
    "/{user_id}/items",
    response_model=CartItemResponse,
    status_code=status.HTTP_201_CREATED,
)
async def add_to_cart(
    session: Annotated[
        AsyncSession,
        Depends(database.get_session)
    ],
    user_id: str,  # потом из JWT
    data: CartItemAdd,
):
    item = await CartCrud.add_item(session, user_id, data)
    return item


@router.patch(
    "/{user_id}/items/{item_id}",
    response_model=CartItemResponse | None,
)
async def update_cart_item(
    session: Annotated[
        AsyncSession,
        Depends(database.get_session)
    ],
    user_id: str,
    item_id: str,
    data: CartItemUpdate,
):
    item = await CartCrud.update_item(session, user_id, item_id, data)

    if item is None and data.quantity > 0:
        raise ITEMNOTFOUND

    return item


@router.delete(
    "/{user_id}/items/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_from_cart(
    session: Annotated[
        AsyncSession,
        Depends(database.get_session)
    ],
    user_id: str,
    item_id: str,
):
    removed = await CartCrud.remove_item(session, user_id, item_id)

    if not removed:
        raise ITEMNOTFOUND


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def clear_cart(
    session: Annotated[
        AsyncSession,
        Depends(database.get_session)
    ],
    user_id: str,
):
    await CartCrud.clear_cart(session, user_id)