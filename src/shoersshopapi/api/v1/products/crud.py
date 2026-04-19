from typing import Union, Sequence

from fastapi import UploadFile, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from shoersshopapi.api.v1.basecrud import BaseCrud
from shoersshopapi.api.v1.schemas.product_schemas import ProductCreate
from shoersshopapi.api.v1.schemas.size_schemas import SizeFilter
from shoersshopapi.api.v1.utils import gen_uuid
from shoersshopapi.core.database.models import Product, Brand, Size
from shoersshopapi.core.minio.image_service import image_service


from shoersshopapi.api.v1.schemas import (
    BrandFilter,
    ProductWithId,
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
        data: ProductCreate,
    ) -> Union[Product, None]:

        instance = ProductWithId(id=gen_uuid(), **data.model_dump())

        product = await cls.add(session, instance)
        await session.commit()

        return product

    # === READ ===

    @classmethod
    async def get_by_id(cls, session: AsyncSession, product_id: str):
        stmt = (
            cls.stmt()
            .filters(ProductFilter(id=product_id))
            .load(Product.brand, Product.sizes)
            .build()
        )

        item = await cls.find_one_or_none(session, stmt)

        if item is None:
            raise

        if item.logo is None:
            return item

        item.logo = await image_service.get_image_url(item.logo)

        if item.brand.brand_logo is None: #pyright: ignore
            return item
 
        item.brand.brand_logo = await image_service.get_image_url(item.brand.brand_logo) #pyright: ignore

        return item

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

        result = await cls.find_all(session, stmt)


        if result is None:
            raise

        for item in result:
            if item.logo is None:
                continue
            
            item.logo = await image_service.get_image_url(item.logo)
        
            if item.brand.brand_logo is None:
                continue

            if not item.brand.brand_logo.startswith("http"):
                item.brand.brand_logo = await image_service.get_image_url(item.brand.brand_logo)

        return result 

    # === UPDATE ===

    @classmethod
    async def update_product(
        cls,
        session: AsyncSession,
        product_id: str,
        data: ProductUpdate,
    ):

        product = await cls.find_one_or_none_by_id(session=session, id=product_id)

        if not product:
            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )

        product = await cls.update_one_by_id(session, product_id, data)
        await session.commit()

        return product

    @classmethod
    async def update_product_logo(
        cls,
        session: AsyncSession,
        product_id: str,
        logo: UploadFile | None = None,
    ):

        product = await cls.find_one_or_none_by_id(session=session, id=product_id)

        if not product:
            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )

        data: ProductUpdate = ProductUpdate()

        if logo:

            if not product.logo: 
                new_logo_path = await image_service.upload_image(logo, "/product", product.id)
                
            else:
                new_logo_path = await image_service.replace_image(
                    old_path=product.logo,
                    file=logo,
                    folder="/product",
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