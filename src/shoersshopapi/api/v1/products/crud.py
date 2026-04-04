from typing import Union, Sequence

from fastapi import UploadFile, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from shoersshopapi.api.v1.basecrud import BaseCrud
from shoersshopapi.api.v1.schemas.product_schemas import ProductCreate
from shoersshopapi.api.v1.schemas.size_schemas import SizeFilter
from shoersshopapi.api.v1.utils import gen_uuid
from shoersshopapi.core.database.models import Product, Brand, Size
from shoersshopapi.core.minio.image_service import image_service

from shoersshopapi.core.settings import settings

from shoersshopapi.api.v1.schemas import (
    BrandFilter,
    ProductWithId,
    ProductUpdate,
    ProductFilter
)

class ProductCrud(BaseCrud[Product]):
    model = Product

    FOLDER = settings.minio.bucket_name

    # === CREATE ===

    @classmethod
    async def create_product(
        cls,
        session: AsyncSession,
        data: ProductCreate,
        product_logo: UploadFile
    ) -> Union[Product, None]:

        primary_id = gen_uuid()

        logo_path = await image_service.upload_image(product_logo, cls.FOLDER + "/product", primary_id)

        instance = ProductWithId(id=primary_id, logo=logo_path, **data.model_dump())

        product = await cls.add(session, instance)
        await session.commit()

        return product

    # === READ ===

    @classmethod
    async def get_by_id(cls, session: AsyncSession, product_id: str):
        stmt = (
            cls.stmt()
            .filters(ProductFilter(id=product_id))
            .load(Product.brand)
            .load(Product.sizes)
            .build()
        )
        return await cls.find_one_or_none(session, stmt)

    @classmethod
    async def get_all(
        cls,
        session: AsyncSession,
        filters: ProductFilter | None = None,
        brand_filters: BrandFilter | None = None,
        size_filters: SizeFilter | None = None,
        limit: int = 20,
        offset: int = 0,
    ):
        stmt = (
            cls.stmt()
            .filters(filters)
            .filters(brand_filters, model=Brand)
            .filters(size_filters, model=Size)
            .load(Product.brand)
            .load(Product.sizes)
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
        logo: UploadFile | None = None,
    ):

        product = await cls.find_one_or_none_by_id(session=session, id=product_id)

        if not product:
            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )

        if logo:
            new_logo_path = await image_service.replace_image(
                old_path=product.logo,
                file=logo,
                folder=cls.FOLDER,
                id=product.id,
            )

            data.logo = new_logo_path

        product = await cls.update_one_by_id(session, product_id, data)
        await session.commit()

        return product

    # === DELETE ===

    @classmethod
    async def delete_product(cls, session: AsyncSession, product_id: str) -> bool:
        product = await cls.delete_one_by_id(session, product_id)
        await session.commit()
        return product