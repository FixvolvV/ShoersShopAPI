# shoersshopapi/api/v1/review/controller.py

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from shoersshopapi.core.database import database
from shoersshopapi.core.utils.enum import Rating
from .crud import ReviewCrud
from shoersshopapi.api.v1.schemas import (
    ReviewSchema,
    ReviewWithId,
    ReviewUpdate,
    ReviewFilter,
    UserWithId
)

from shoersshopapi.api.v1.validators.http import (
    oauth2_scheme,
    get_current_auth_user,
    RoleRequired,
)


router = APIRouter(
    tags=["Reviews"]
)

REVIEWSNOTFOUND = HTTPException(status_code=404, detail="Review not found")

@router.post(
    "/",
    response_model=ReviewWithId,
    status_code=status.HTTP_201_CREATED,
    summary="Оставить отзыв о сайте",
)
async def create_review(
    user: Annotated[
        UserWithId,
        Depends(get_current_auth_user)
    ],
    session: Annotated[
        AsyncSession,
        Depends(database.get_session)
    ],
    data: ReviewSchema,
):
    review = await ReviewCrud.create_review(session, user.id, data)
    return review


@router.get(
    "/",
    summary="Получить все отзывы",
)
async def get_reviews(
    session: Annotated[
        AsyncSession,
        Depends(database.get_session)
    ],
    rating: int | None = None,
    page: Annotated[int, Query(ge=1)] = 1,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
):

    reviews = await ReviewCrud.get_all(
        session,
        filters=ReviewFilter(rating=rating),
        limit=limit,
        offset=(page - 1) * limit,
    )

    result = []
    for review in reviews:
        result.append({
            "id": review.id,
            "user_id": review.user_id,
            "comment_text": review.comment_text,
            "rating": review.rating,
            "surname": review.user.surname,
            "name": review.user.name,
        })

    return result


@router.get(
    "/{review_id}",
    response_model=ReviewWithId,
    summary="Получить отзыв по ID",
)
async def get_review(
    session: Annotated[
        AsyncSession,
        Depends(database.get_session)
    ],
    review_id: str,
):
    review = await ReviewCrud.get_by_id(session, review_id)

    if not review:
        raise REVIEWSNOTFOUND

    return review


@router.get(
    "/user/{user_id}",
    response_model=ReviewWithId,
    summary="Получить отзыв по user id",
)
async def get_user_review(
    user_id: str,
    session: Annotated[
        AsyncSession,
        Depends(database.get_session)
    ],
):
    review = await ReviewCrud.get_by_user_id(session, user_id)

    if not review:
        raise REVIEWSNOTFOUND

    return review


@router.patch(
    "/",
    response_model=ReviewWithId,
    summary="Обновить отзыв",
)
async def update_self_review(
    user: Annotated[
        UserWithId,
        Depends(get_current_auth_user)
    ],
    session: Annotated[
        AsyncSession,
        Depends(database.get_session)
    ],
    data: ReviewUpdate,
):
    review = await ReviewCrud.update_review_by_user_id(session, user.id, data)

    if not review:
        raise REVIEWSNOTFOUND

    return review

@router.patch(
    "/{review_id}",
    response_model=ReviewWithId,
    summary="Обновить отзыв (admin)",
)
async def update_review(
    user: Annotated[
        UserWithId,
        Depends(RoleRequired("admin"))
    ],
    session: Annotated[
        AsyncSession,
        Depends(database.get_session)
    ],
    review_id: str,
    data: ReviewUpdate,
):
    review = await ReviewCrud.update_review_by_id(session, review_id, data)

    if not review:
        raise REVIEWSNOTFOUND

    return review


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить отзыв",
)
async def delete_self_review(
    user: Annotated[
        UserWithId,
        Depends(get_current_auth_user)
    ],
    session: Annotated[
        AsyncSession,
        Depends(database.get_session)
    ],
):
    deleted = await ReviewCrud.delete_self_review(session, user.id)

    if not deleted:
        raise REVIEWSNOTFOUND


@router.delete(
    "/{review_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить отзыв (admin)",
)
async def delete_review(
    user: Annotated[
        UserWithId,
        Depends(RoleRequired("admin"))
    ],
    session: Annotated[
        AsyncSession,
        Depends(database.get_session)
    ],
    review_id: str
):
    deleted = await ReviewCrud.delete_review(session, review_id)

    if not deleted:
        raise REVIEWSNOTFOUND