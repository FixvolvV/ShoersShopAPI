from typing import Union
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from shoersshopapi.api.v1.basecrud import BaseCrud
from shoersshopapi.api.v1.utils import gen_uuid
from shoersshopapi.core.database.models import Size

from shoersshopapi.api.v1.schemas import (
    SizeSchema,
    SizeWithId,
    SizeUpdate,
    SizeFilter
)
from shoersshopapi.core.utils.enum import ASizes

class SizeCrud(BaseCrud[Size]):
    model = Size

    # === CREATE ===

    @classmethod
    async def create_size(
        cls,
        session: AsyncSession,
        data: SizeSchema,
    ) -> Union[Size, None]:
        # Проверяем дубликат size для product
        stmt = (
            cls.stmt()
            .filters(SizeFilter(product_id=data.product_id, size=data.size))
            .build()
        )
        existing = await cls.find_one_or_none(session, stmt)

        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Size {data.size} already exists for this product",
            )

        size_data = SizeWithId(
            id=gen_uuid(),
            **data.model_dump(),
        )

        size = await cls.add(session, size_data)
        await session.commit()

        return size

    # === READ ===

    @classmethod
    async def get_by_id(cls, session: AsyncSession, size_id: str):
        stmt = cls.stmt().filters(SizeFilter(id=size_id)).build()
        return await cls.find_one_or_none(session, stmt)

    @classmethod
    async def get_by_product(
        cls,
        session: AsyncSession,
        product_id: str,
    ):
        stmt = (
            cls.stmt()
            .filters(SizeFilter(product_id=product_id))
            .order_by(Size.size)
            .build()
        )
        return await cls.find_all(session, stmt)

    @classmethod
    async def get_available_by_product(
        cls,
        session: AsyncSession,
        product_id: str,
    ):
        """Только размеры в наличии (count > 0)"""
        stmt = (
            cls.stmt()
            .filters(SizeFilter(product_id=product_id, count_min=1))
            .order_by(Size.size)
            .build()
        )
        return await cls.find_all(session, stmt)

    # === UPDATE ===

    @classmethod
    async def update_size(
        cls,
        session: AsyncSession,
        size_id: str,
        data: SizeUpdate,
    ):
        size = await cls.update_one_by_id(session, size_id, data)

        if not size:
            return None

        await session.commit()
        return size

    @classmethod
    async def decrease_count(
        cls,
        session: AsyncSession,
        product_id: str,
        size: ASizes,
        quantity: int,
    ):
        """Уменьшить количество при заказе"""
        stmt = (
            cls.stmt()
            .filters(SizeFilter(product_id=product_id, size=size))
            .build()
        )
        size_obj = await cls.find_one_or_none(session, stmt)

        if not size_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Size {size} not found for this product",
            )

        if size_obj.count < quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Not enough stock. Available: {size_obj.count}",
            )

        size_obj.count -= quantity
        await session.flush()
        return size_obj

    # === DELETE ===

    @classmethod
    async def delete_size(cls, session: AsyncSession, size_id: str) -> bool:
        result = await cls.delete_one_by_id(session, size_id)
        if result:
            await session.commit()
        return result