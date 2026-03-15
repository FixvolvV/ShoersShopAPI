"""Тесты CRUD для Favorite."""

import pytest
from sqlalchemy.exc import IntegrityError
from test.helpers import gen_id, FavoriteCrud, FavoriteCreate


class TestFavoriteAdd:

    @pytest.mark.asyncio
    async def test_add(self, session, sample_user, sample_product):
        fid = gen_id()
        data = FavoriteCreate(
            id=fid,
            user_id=sample_user.id,
            product_id=sample_product.id,
        )
        await FavoriteCrud.add(session=session, values=data)

        found = await FavoriteCrud.find_one_or_none_by_id(session=session, id=fid)
        assert found is not None
        assert found.user_id == sample_user.id
        assert found.product_id == sample_product.id

    @pytest.mark.asyncio
    async def test_invalid_user_raises(self, session, sample_product):
        data = FavoriteCreate(
            id=gen_id(),
            user_id="ghost",
            product_id=sample_product.id,
        )
        with pytest.raises(IntegrityError):
            await FavoriteCrud.add(session=session, values=data)

    @pytest.mark.asyncio
    async def test_invalid_product_raises(self, session, sample_user):
        data = FavoriteCreate(
            id=gen_id(),
            user_id=sample_user.id,
            product_id="ghost",
        )
        with pytest.raises(IntegrityError):
            await FavoriteCrud.add(session=session, values=data)


class TestFavoriteDelete:

    @pytest.mark.asyncio
    async def test_delete(self, session, sample_favorite):
        result = await FavoriteCrud.delete_one_by_id(session=session, id=sample_favorite.id)
        assert result is True
        found = await FavoriteCrud.find_one_or_none_by_id(session=session, id=sample_favorite.id)
        assert found is None

    @pytest.mark.asyncio
    async def test_delete_nonexistent(self, session):
        result = await FavoriteCrud.delete_one_by_id(session=session, id="no-fav")
        assert result is False