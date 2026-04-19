from typing import Union, Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import UploadFile

from shoersshopapi.api.v1.basecrud import BaseCrud
from shoersshopapi.api.v1.utils import gen_uuid

from shoersshopapi.core.settings import settings
from shoersshopapi.core.database.models import Brand
from shoersshopapi.core.minio.image_service import image_service

from shoersshopapi.api.v1.schemas import BrandWithId, BrandFilter, BrandUpdate


class BrandCrud(BaseCrud[Brand]):
    model = Brand

    FOLDER = settings.minio.bucket_name

    # === CREATE ===

    @classmethod
    async def create_brand(
        cls,
        session: AsyncSession,
        brand_name: str,
        brand_logo: UploadFile,
    ) -> Union[Brand, None]:

        primary_id = gen_uuid()

        logo_path = await image_service.upload_image(brand_logo, cls.FOLDER + "/brand", primary_id)

        data = BrandWithId(
            id=primary_id,
            brand_name=brand_name,
            brand_logo=logo_path,
        )

        brand = await cls.add(session, data)
        await session.commit()

        return brand 

    # === READ ===

    @classmethod
    async def get_by_id(cls, session: AsyncSession, brand_id: str):
        stmt = cls.stmt().filters(BrandFilter(id=brand_id)).build()

        item = await cls.find_one_or_none(session, stmt)
 
        item.brand_logo = await image_service.get_image_url(item.brand_logo) #pyright: ignore

        return item

    @classmethod
    async def get_all(
        cls,
        session: AsyncSession,
        filters: BrandFilter | None = None,
        limit: int = 20,
        offset: int = 0,
    ):
        stmt = (
            cls.stmt()
            .filters(filters)
            .limit(limit)
            .offset(offset)
            .build()
        )

        result = await cls.find_all(session, stmt)
    
        if result is None:
            raise

        for item in result:
        
            if item.brand_logo is None:
                continue

            if not item.brand_logo.startswith("http"):
                item.brand_logo = await image_service.get_image_url(item.brand_logo)

        return result

    # === UPDATE ===

    @classmethod
    async def update_brand(
        cls,
        session: AsyncSession,
        brand_id: str,
        brand_name: str | None = None,
        logo: UploadFile | None = None,
    ):
        brand = await cls.find_one_or_none_by_id(session, brand_id)

        if not brand:
            return None

        update_data = BrandUpdate()

        if logo:
            new_logo_path = await image_service.replace_image(
                old_path=brand.brand_logo,
                file=logo,
                folder=cls.FOLDER,
                id=brand.id,
            )
            update_data.brand_logo = new_logo_path

        if brand_name:
            update_data.brand_name = brand_name

        brand = await cls.update_one_by_id(
            session, brand_id, update_data
        )
        await session.commit()

        return brand


    # === DELETE ===

    @classmethod
    async def delete_brand(cls, session: AsyncSession, brand_id: str) -> bool:
        brand = await cls.find_one_or_none_by_id(session, brand_id)

        if not brand:
            return False

        await image_service.delete_image(brand.brand_logo)
        brand = await cls.delete_one_by_id(session, brand_id)
        await session.commit()
        
        return brand