"""Тесты CRUD для Review."""

import pytest
from sqlalchemy.exc import IntegrityError
from .helpers import gen_id, ReviewCrud, ReviewCreate, ReviewUpdate, Rating


class TestReviewAdd:

    @pytest.mark.asyncio
    async def test_add(self, session, sample_user):
        rid = gen_id()
        data = ReviewCreate(
            id=rid,
            user_id=sample_user.id,
            comment_text="Отличные кроссовки!",
            rating=Rating.very_good,
        )
        await ReviewCrud.add(session=session, values=data)

        found = await ReviewCrud.find_one_or_none_by_id(session=session, id=rid)
        assert found is not None
        assert found.user_id == sample_user.id
        assert found.rating == Rating.very_good
        assert "Отличные" in found.comment_text

    @pytest.mark.asyncio
    async def test_default_rating(self, session, sample_user):
        rid = gen_id()
        data = ReviewCreate(
            id=rid,
            user_id=sample_user.id,
            comment_text="Default rating",
        )
        await ReviewCrud.add(session=session, values=data)

        found = await ReviewCrud.find_one_or_none_by_id(session=session, id=rid)
        assert found.rating == Rating.very_good

    @pytest.mark.asyncio
    async def test_all_ratings(self, session, sample_user):
        for rating in Rating:
            rid = gen_id()
            data = ReviewCreate(
                id=rid,
                user_id=sample_user.id,
                comment_text=f"Rating: {rating.name}",
                rating=rating,
            )
            await ReviewCrud.add(session=session, values=data)

            found = await ReviewCrud.find_one_or_none_by_id(session=session, id=rid)
            assert found.rating == rating

    @pytest.mark.asyncio
    async def test_add_invalid_user_raises(self, session):
        data = ReviewCreate(
            id=gen_id(),
            user_id="ghost",
            comment_text="Ghost",
        )
        with pytest.raises(IntegrityError):
            await ReviewCrud.add(session=session, values=data)

    @pytest.mark.asyncio
    async def test_empty_comment(self, session, sample_user):
        rid = gen_id()
        data = ReviewCreate(
            id=rid,
            user_id=sample_user.id,
            comment_text="",
        )
        await ReviewCrud.add(session=session, values=data)

        found = await ReviewCrud.find_one_or_none_by_id(session=session, id=rid)
        assert found.comment_text == ""

    @pytest.mark.asyncio
    async def test_long_comment(self, session, sample_user):
        rid = gen_id()
        long_text = "А" * 5000
        data = ReviewCreate(
            id=rid,
            user_id=sample_user.id,
            comment_text=long_text,
        )
        await ReviewCrud.add(session=session, values=data)

        found = await ReviewCrud.find_one_or_none_by_id(session=session, id=rid)
        assert len(found.comment_text) == 5000

    @pytest.mark.asyncio
    async def test_user_multiple_reviews(self, session, sample_user):
        for i in range(4):
            data = ReviewCreate(
                id=gen_id(),
                user_id=sample_user.id,
                comment_text=f"Review {i}",
            )
            await ReviewCrud.add(session=session, values=data)


class TestReviewUpdate:

    @pytest.mark.asyncio
    async def test_update_text(self, session, sample_review):
        await ReviewCrud.update_one_by_id(
            session=session, id=sample_review.id,
            new_values=ReviewUpdate(comment_text="Обновлённый"),
        )
        found = await ReviewCrud.find_one_or_none_by_id(session=session, id=sample_review.id)
        assert found.comment_text == "Обновлённый"

    @pytest.mark.asyncio
    async def test_update_rating(self, session, sample_review):
        await ReviewCrud.update_one_by_id(
            session=session, id=sample_review.id,
            new_values=ReviewUpdate(rating=Rating.bad),
        )
        found = await ReviewCrud.find_one_or_none_by_id(session=session, id=sample_review.id)
        assert found.rating == Rating.bad

    @pytest.mark.asyncio
    async def test_update_both(self, session, sample_review):
        await ReviewCrud.update_one_by_id(
            session=session, id=sample_review.id,
            new_values=ReviewUpdate(comment_text="Новый", rating=Rating.normal),
        )
        found = await ReviewCrud.find_one_or_none_by_id(session=session, id=sample_review.id)
        assert found.comment_text == "Новый"
        assert found.rating == Rating.normal


class TestReviewDelete:

    @pytest.mark.asyncio
    async def test_delete(self, session, sample_review):
        result = await ReviewCrud.delete_one_by_id(session=session, id=sample_review.id)
        assert result is True
        found = await ReviewCrud.find_one_or_none_by_id(session=session, id=sample_review.id)
        assert found is None