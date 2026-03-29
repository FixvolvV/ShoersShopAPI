# shoersshopapi/api/v1/order/controller.py

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from shoersshopapi.core.database import database
from shoersshopapi.core.utils.enum import Status

from .crud import OrderCrud
from shoersshopapi.api.v1.schemas import (
    OrderSchema,
    OrderUpdate,
    OrderFilter,
    OrderWithId,
    OrderFull,
)

router = APIRouter(tags=["Orders"])

ORDERNOTFOUND = HTTPException(status_code=404, detail="Order not found")

# === CREATE ===

@router.post(
    "/",
    response_model=OrderWithId,
    status_code=status.HTTP_201_CREATED,
    summary="Создать заказ из корзины",
)
async def create_order(
    session: Annotated[
        AsyncSession,
        Depends(database.get_session)
    ],
    user_id: str,  # потом из JWT
    data: OrderSchema,
):

    order = await OrderCrud.create_order(session, user_id, data)
    return order


# === READ ===

@router.get(
    "/{order_id}",
    response_model=OrderFull,
    summary="Получить заказ по ID",
)
async def get_order(
    session: Annotated[
        AsyncSession,
        Depends(database.get_session)
    ],
    order_id: str,
):
    order = await OrderCrud.get_by_id(session, order_id)

    if not order:
        raise ORDERNOTFOUND

    # Формируем ответ с информацией о товарах
    items = []
    for order_item in order.order_items:
        items.append({
            "id": order_item.id,
            "product_id": order_item.product_id,
            "quantity": order_item.quantity,
            "title": order_item.product.title,
            "price": order_item.product.price,
        })

    return {
        "id": order.id,
        "user_id": order.user_id,
        "address_id": order.address_id,
        "order_date": order.order_date,
        "total_amount": order.total_amount,
        "status": order.status,
        "items": items,
        "address": order.address,
    }


@router.get(
    "/user/{user_id}",
    response_model=list[OrderWithId],
    summary="Получить заказы пользователя",
)
async def get_user_orders(
    session: Annotated[
        AsyncSession,
        Depends(database.get_session)
    ],
    user_id: str,
    order_status: Status | None = None,
    page: Annotated[int, Query(ge=1)] = 1,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
):
    filters = OrderFilter(status=order_status)

    orders = await OrderCrud.get_user_orders(
        session,
        user_id,
        filters=filters,
        limit=limit,
        offset=(page - 1) * limit,
    )

    return orders


# === UPDATE (admin) ===

@router.patch(
    "/{order_id}/status",
    response_model=OrderWithId,
    summary="Обновить статус заказа (admin)",
)
async def update_order_status(
    session: Annotated[
        AsyncSession,
        Depends(database.get_session)
    ],
    order_id: str,
    data: OrderUpdate,
):
    order = await OrderCrud.update_status(session, order_id, data)

    if not order:
        raise ORDERNOTFOUND

    return order


# === CANCEL ===

@router.post(
    "/{order_id}/cancel",
    response_model=OrderWithId,
    summary="Отменить заказ",
)
async def cancel_order(
    session: Annotated[
        AsyncSession,
        Depends(database.get_session)
    ],
    order_id: str,
    user_id: str,  # потом из JWT
):
    order = await OrderCrud.cancel_order(session, order_id, user_id)

    if not order:
        raise ORDERNOTFOUND

    return order