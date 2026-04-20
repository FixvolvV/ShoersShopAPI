from typing import Union
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from shoersshopapi.core.database.models import Favorite, Product
from shoersshopapi.core.minio.image_service import image_service

from shoersshopapi.api.v1.utils import gen_uuid
from shoersshopapi.api.v1.basecrud import BaseCrud
from shoersshopapi.api.v1.schemas import FavoriteWithId


FAVORITE_NOT_FOUND = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Favorite not found"
)

FAVORITE_ALREADY_EXISTS = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Product already in favorites"
)


class FavoriteCrud(BaseCrud[Favorite]):
    model = Favorite

    # === Получить все избранные товары пользователя ===

    @classmethod
    async def get_favorites(
        cls,
        session: AsyncSession,
        user_id: str,
    ):

        stmt = (
            select(Favorite)
            .where(Favorite.user_id == user_id)
            .options(
                selectinload(Favorite.product).options(
                selectinload(Product.brand),
                selectinload(Product.sizes)
                )
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

    # === Добавить товар в избранное ===

    @classmethod
    async def add_favorite(
        cls,
        session: AsyncSession,
        user_id: str,
        product_id: str,
    ) -> Favorite:

        # Проверяем, нет ли уже такого товара в избранном
        query = select(Favorite).where(
            Favorite.user_id == user_id,
            Favorite.product_id == product_id,
        )
        result = await session.execute(query)
        existing = result.scalar_one_or_none()

        if existing:
            raise FAVORITE_ALREADY_EXISTS

        favorite_data = FavoriteWithId(
            id=gen_uuid(),
            user_id=user_id,
            product_id=product_id,
        )

        favorite = Favorite(**favorite_data.model_dump())
        session.add(favorite)
        await session.flush()
        await session.commit()

        return favorite

    # === Удалить товар из избранного ===

    @classmethod
    async def remove_favorite(
        cls,
        session: AsyncSession,
        user_id: str,
        product_id: str,
    ) -> bool:

        query = select(Favorite).where(
            Favorite.user_id == user_id,
            Favorite.product_id == product_id,
        )
        result = await session.execute(query)
        favorite = result.scalar_one_or_none()

        if not favorite:
            return False

        await session.delete(favorite)
        await session.flush()
        await session.commit()

        return True

    # === Проверить, находится ли товар в избранном ===

    @classmethod
    async def is_favorite(
        cls,
        session: AsyncSession,
        user_id: str,
        product_id: str,
    ) -> bool:

        query = select(Favorite).where(
            Favorite.user_id == user_id,
            Favorite.product_id == product_id,
        )
        result = await session.execute(query)
        return result.scalar_one_or_none() is not None

    # === Очистить все избранное пользователя ===

    @classmethod
    async def clear_favorites(
        cls,
        session: AsyncSession,
        user_id: str,
    ) -> bool:

        query = select(Favorite).where(Favorite.user_id == user_id)
        result = await session.execute(query)
        favorites = result.scalars().all()

        for favorite in favorites:
            await session.delete(favorite)

        await session.flush()
        await session.commit()

        return True