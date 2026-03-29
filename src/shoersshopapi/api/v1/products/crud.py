from typing import Union, Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from shoersshopapi.api.v1.basecrud import BaseCrud
from shoersshopapi.api.v1.utils import gen_uuid
from shoersshopapi.core.database.models import Product, Brand

from shoersshopapi.api.v1.schemas import (
    BrandFilter,
    ProductWithId,
    ProductSchema,
    ProductUpdate,
    ProductFilter
)

class ProductCrud(BaseCrud[Product]):
    model = Product

    # === CREATE ===

    @classmethod
    async def create_product(
        cls,
        session: AsyncSession,
        data: ProductSchema,
    ) -> Union[Product, None]:

        data = ProductWithId(id=gen_uuid(), **data.model_dump())

        product = await cls.add(session, data)
        await session.commit()

        return product

    # === READ ===

    @classmethod
    async def get_by_id(cls, session: AsyncSession, product_id: str):
        stmt = (
            cls.stmt()
            .filters(ProductFilter(id=product_id))
            .load(Product.brand)
            .build()
        )
        return await cls.find_one_or_none(session, stmt)

    @classmethod
    async def get_all(
        cls,
        session: AsyncSession,
        filters: ProductFilter | None = None,
        brand_filters: BrandFilter | None = None,
        limit: int = 20,
        offset: int = 0,
    ):
        stmt = (
            cls.stmt()
            .filters(filters)
            .filters(brand_filters, model=Brand)
            .load(Product.brand)
            .order_by(Product.price, desc=True)
            .limit(limit)
            .offset(offset)
            .build()
        )
        return await cls.find_all(session, stmt)

    # === UPDATE ===

    @classmethod
    async def update_product(
        cls,
        session: AsyncSession,
        product_id: str,
        data: ProductUpdate,
    ):

        product = await cls.update_one_by_id(session, product_id, data)
        await session.commit()

        return product

    # === DELETE ===

    @classmethod
    async def delete_product(cls, session: AsyncSession, product_id: str) -> bool:
        product = await cls.delete_one_by_id(session, product_id)
        await session.commit()
        return product