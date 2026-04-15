# shoersshopapi/api/v1/review/crud.py

import datetime
from typing import Union
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from shoersshopapi.api.v1.basecrud import BaseCrud
from shoersshopapi.api.v1.utils import gen_uuid
from shoersshopapi.core.database.models import Review
from shoersshopapi.core.utils.utils import get_current_df

from pydantic import BaseModel

from shoersshopapi.api.v1.schemas import (
    ReviewSchema,
    ReviewWithId,
    ReviewUpdate,
    ReviewFilter
)

class ReviewCrud(BaseCrud[Review]):
    model = Review

    # === CREATE ===

    @classmethod
    async def create_review(
        cls,
        session: AsyncSession,
        user_id: str,
        data: ReviewSchema,
    ) -> Union[Review, None]:
        
        stmt = (
            cls.stmt()
            .filters(ReviewFilter(user_id=user_id))
            .build()
        )

        review_data = ReviewWithId(
            id=gen_uuid(),
            user_id=user_id,
            comment_text=data.comment_text,
            rating=data.rating.value if hasattr(data.rating, 'value') else data.rating, # pyright: ignore
            created_at=get_current_df()
        )

        review = await cls.add(session, review_data)
        await session.commit()
        return review

    # === READ ===

    @classmethod
    async def get_by_id(cls, session: AsyncSession, review_id: str):
        stmt = cls.stmt().filters(ReviewFilter(id=review_id)).build()
        return await cls.find_one_or_none(session, stmt)

    @classmethod
    async def get_by_user_id(cls, session: AsyncSession, user_id: str):
        stmt = cls.stmt().filters(ReviewFilter(user_id=user_id)).build()
        return await cls.find_one_or_none(session, stmt)

    @classmethod
    async def get_all(
        cls,
        session: AsyncSession,
        filters: ReviewFilter | None = None,
        limit: int = 20,
        offset: int = 0,
    ):
        
        query = (
            select(Review)
            .options(selectinload(Review.user))
            .order_by(Review.id.desc())
            .limit(limit)
            .offset(offset)
        )

        if filters and filters.rating:
            query = query.where(Review.rating == filters.rating)

        result = await session.execute(query)
        return result.scalars().unique().all()

    @classmethod
    async def get_by_user(cls, session: AsyncSession, user_id: str):
         
        stmt = (
            cls.stmt()
            .filters(ReviewFilter(user_id=user_id))
            .build()
        )
        return await cls.find_one_or_none(session, stmt)

    # === UPDATE ===

    @classmethod
    async def update_review_by_id(
        cls,
        session: AsyncSession,
        review_id: str,
        data: ReviewUpdate,
    ):
        review = await cls.find_one_or_none_by_id(session, review_id)

        if not review:
            return None

        review = await cls.update_one_by_id(session, review_id, data)
        await session.commit()
        return review


    @classmethod
    async def update_review_by_user_id(
        cls,
        session: AsyncSession,
        user_id: str,
        data: ReviewUpdate,
    ):

        stmt = cls.stmt().filters(ReviewFilter(user_id=user_id)).build()
        review = await cls.find_one_or_none(session, stmt)

        if not review:
            return None

        review = await cls.update_one_by_id(session, review.id, data)
        await session.commit()
        return review

    # === DELETE ===

    @classmethod
    async def delete_review(
        cls,
        session: AsyncSession,
        review_id: str,
    ) -> bool:
        review = await cls.find_one_or_none_by_id(session, review_id)

        if not review:
            return False

        result = await cls.delete_one_by_id(session, review_id)
        await session.commit()
        return result

    @classmethod
    async def delete_self_review(
        cls,
        session: AsyncSession,
        user_id: str,
    ) -> bool:

        stmt = cls.stmt().filters(ReviewFilter(user_id=user_id)).build()
        review = await cls.find_one_or_none(session, stmt)

        if not review:
            return False

        result = await cls.delete_one_by_id(session, review.id)
        await session.commit()
        return result