# shoersshopapi/api/v1/order/crud.py

from typing import Union, Sequence
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status

from shoersshopapi.api.v1.basecrud import BaseCrud
from shoersshopapi.api.v1.utils import gen_uuid
from shoersshopapi.api.v1.carts.crud import CartCrud

from shoersshopapi.core.database.models import Order, OrderItem, Address, Size
from shoersshopapi.core.utils.enum import Status
from shoersshopapi.core.minio.image_service import image_service

from  shoersshopapi.api.v1.schemas import OrderCreate, OrderWithId, OrderUpdate, OrderFilter

ADDRESSNOTFOUND = HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Address not found",
)

NOTYOUADDRESS = HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not your address",
)


class OrderCrud(BaseCrud[Order]):
    model = Order

    # === CREATE (из корзины) ===

    @classmethod
    async def create_order(
        cls,
        session: AsyncSession,
        user_id: str,
        data: OrderCreate,
    ) -> Union[Order, None]:

        # Проверяем адрес
        address = await session.get(Address, data.address_id)
        if not address:
            raise ADDRESSNOTFOUND

        if address.user_id != user_id:
            raise NOTYOUADDRESS

        # Получаем товары из корзины
        cart_items = await CartCrud.get_cart_items(session, user_id)

        if not cart_items:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cart is empty",
            )

        # Считаем сумму
        total_amount = 0
        for inst in cart_items:
            total_amount += int(inst.items.product.price * inst.quantity)

        # Создаём заказ
        order_id = gen_uuid()

        order_data = OrderWithId(
            id=order_id,
            user_id=user_id,
            address_id=data.address_id,
            order_date=datetime.now().replace(tzinfo=None),
            total_amount=total_amount,
            status=Status.confirmation,
        )

        order = await cls.add(session, order_data)

        # Создаём элементы заказа из корзины
        for cart_item in cart_items:
            order_item = OrderItem(
                id=gen_uuid(),
                order_id=order_id,
                size_id=cart_item.size_id,
                quantity=cart_item.quantity,
            )
            session.add(order_item)

        await session.flush()

        # Очищаем корзину
        await CartCrud.clear_cart(session, user_id)

        await session.commit()

        return order

    # === READ ===

    @classmethod
    async def get_by_id(
        cls,
        session: AsyncSession,
        order_id: str,
    ):
        stmt = (
            select(Order)
            .where(Order.id == order_id)
            .options(
                selectinload(Order.order_items)
                .selectinload(OrderItem.items),
                selectinload(Order.address),
            )
        )
        
        result = await cls.find_all(session, stmt)

        if result is None:
            raise

        for item in result:
            if item.product.logo is None:
                continue
            
            item.product.logo = await image_service.get_image_url(item.product.logo)
        
            if item.product.brand.brand_logo is None:
                continue

            if not item.product.brand.brand_logo.startswith("http"):
                item.product.brand.brand_logo = await image_service.get_image_url(item.product.brand.brand_logo)

        return result

    @classmethod
    async def get_user_orders(
        cls,
        session: AsyncSession,
        user_id: str,
        filters: OrderFilter | None = None,
        limit: int = 20,
        offset: int = 0,
    ):
        query = (
            select(Order)
            .where(Order.user_id == user_id)
            .options(
                selectinload(Order.order_items)
                .selectinload(OrderItem.items)
                .selectinload(Size.product)
            )
            .order_by(Order.order_date.desc())
            .limit(limit)
            .offset(offset)
        )

        if filters and filters.status:
            query = query.where(Order.status == filters.status)

        result = await session.execute(query)
        return result.scalars().unique().all()

    @classmethod
    async def get_all_orders(
        cls,
        session: AsyncSession,
        filters: OrderFilter | None = None,
        limit: int = 20,
        offset: int = 0,
    ):
        """Для админа — все заказы"""
        stmt = (
            cls.stmt()
            .filters(filters)
            .order_by(Order.order_date, desc=True)
            .limit(limit)
            .offset(offset)
            .build()
        )
        return await cls.find_all(session, stmt)

    # === UPDATE ===

    @classmethod
    async def update_status(
        cls,
        session: AsyncSession,
        order_id: str,
        data: OrderUpdate,
    ):
        order = await cls.find_one_or_none_by_id(session, order_id)

        if not order:
            return None

        order.status = data.status #pyright: ignore
        await session.flush()
        await session.commit()

        return order

    # === CANCEL ===

    @classmethod
    async def cancel_order(
        cls,
        session: AsyncSession,
        order_id: str,
        user_id: str,
    ):
        order = await cls.find_one_or_none_by_id(session, order_id)

        if not order:
            return None

        if order.user_id != user_id:
            raise NOTYOUADDRESS

        if order.status not in (Status.confirmation,):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot cancel order with this status",
            )

        order.status = Status.cancelled
        await session.flush()
        await session.commit()

        return order