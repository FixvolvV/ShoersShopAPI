from typing import Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status

from shoersshopapi.api.v1.basecrud import BaseCrud
from shoersshopapi.api.v1.utils import gen_uuid
from shoersshopapi.core.database.models import Cart, CartItem, Product, Size

from  shoersshopapi.api.v1.schemas import (
    CartItemAdd,
    CartItemUpdate,
    CartCreate,
    CartItemCreate
)


CARTNOTFOUND = HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cart not found"
            )

class CartCrud(BaseCrud[Cart]):
    model = Cart

    # === Получить или создать корзину ===

    @classmethod
    async def get_or_create(cls, session: AsyncSession, user_id: str) -> Union[Cart, None]:
        
        query = select(Cart).where(Cart.user_id == user_id)
        result = await session.execute(query)
        cart = result.scalar_one_or_none()

        if not cart:
            cart_data = CartCreate(id=gen_uuid(), user_id=user_id)
            cart = await cls.add(session, cart_data)
            await session.flush()

        return cart

    # === Получить корзину с товарами ===

    @classmethod
    async def get_cart_with_items(cls, session: AsyncSession, user_id: str):

        query = (
            select(Cart)
            .where(Cart.user_id == user_id)
            .options(
                selectinload(Cart.cart_items)
                .selectinload(CartItem.items)
                .selectinload(Size.product) 
                .selectinload(Product.brand)
            )
        )

        result = await session.execute(query)
        cart = result.scalar_one_or_none()

        return cart

    # === Добавить товар ===

    @classmethod
    async def add_item(
        cls,
        session: AsyncSession,
        user_id: str,
        data: CartItemAdd,
    ) -> CartItem:
        cart = await cls.get_or_create(session, user_id)

        if not cart:
            raise CARTNOTFOUND

        query = (
            select(CartItem)
            .where(
                CartItem.cart_id == cart.id,
                CartItem.size_id == data.size_id,
            )
        )
        result = await session.execute(query)
        existing_item = result.scalar_one_or_none()

        if existing_item:
            # Увеличиваем количество
            existing_item.quantity += data.quantity
            await session.flush()
            await session.commit()
            return existing_item

        # Создаём новый элемент
        item_data = CartItemCreate(
            id=gen_uuid(),
            cart_id=cart.id,
            size_id=data.size_id,
            quantity=data.quantity,
        )

        item = CartItem(**item_data.model_dump())
        session.add(item)
        await session.flush()
        await session.commit()

        return item

    # === Обновить количество ===

    @classmethod
    async def update_item(
        cls,
        session: AsyncSession,
        user_id: str,
        item_id: str,
        data: CartItemUpdate,
    ) -> CartItem | None:
        cart = await cls.get_or_create(session, user_id)

        if not cart:
            raise CARTNOTFOUND

        query = (
            select(CartItem)
            .where(
                CartItem.id == item_id,
                CartItem.cart_id == cart.id,
            )
        )
        result = await session.execute(query)
        item = result.scalar_one_or_none()

        if not item:
            return None

        if data.quantity <= 0:
            await session.delete(item)
            await session.flush()
            await session.commit()
            return None

        item.quantity = data.quantity
        await session.flush()
        await session.commit()

        return item

    # === Удалить товар из корзины ===

    @classmethod
    async def remove_item(
        cls,
        session: AsyncSession,
        user_id: str,
        item_id: str,
    ) -> bool:
        cart = await cls.get_or_create(session, user_id)

        if not cart:
            raise CARTNOTFOUND


        query = (
            select(CartItem)
            .where(
                CartItem.id == item_id,
                CartItem.cart_id == cart.id,
            )
        )
        result = await session.execute(query)
        item = result.scalar_one_or_none()

        if not item:
            return False

        await session.delete(item)
        await session.flush()
        await session.commit()

        return True

    # === Очистить корзину ===

    @classmethod
    async def clear_cart(
        cls,
        session: AsyncSession,
        user_id: str,
    ) -> bool:
        cart = await cls.get_or_create(session, user_id)

        if not cart:
            raise CARTNOTFOUND


        query = select(CartItem).where(CartItem.cart_id == cart.id)
        result = await session.execute(query)
        items = result.scalars().all()

        for item in items:
            await session.delete(item)

        await session.flush()
        await session.commit()

        return True

    # === Получить элементы корзины (для создания заказа) ===

    @classmethod
    async def get_cart_items(
        cls,
        session: AsyncSession,
        user_id: str,
    ) -> list[CartItem]:
        cart = await cls.get_or_create(session, user_id)

        if not cart:
            raise CARTNOTFOUND


        query = (
            select(CartItem)
            .where(CartItem.cart_id == cart.id)
            .options(selectinload(CartItem.size_id))
        )
        result = await session.execute(query)
        return list(result.scalars().all())