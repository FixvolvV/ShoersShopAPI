"""Тесты CRUD для Cart."""

import pytest
from sqlalchemy.exc import IntegrityError
from .helpers import gen_id, CartCrud, CartCreate
from src.shoersshopapi.core.database.models.cart import Cart


class TestCartAdd:

    @pytest.mark.asyncio
    async def test_add(self, session, sample_user):
        cid = gen_id()
        data = CartCreate(id=cid, user_id=sample_user.id)
        await CartCrud.add(session=session, values=data)

        found = await CartCrud.find_one_or_none_by_id(session=session, id=cid)
        assert found is not None
        assert found.user_id == sample_user.id

    @pytest.mark.asyncio
    async def test_one_cart_per_user(self, session, sample_user):
        cart1 = Cart(id=gen_id(), user_id=sample_user.id)
        session.add(cart1)
        await session.flush()

        data2 = CartCreate(id=gen_id(), user_id=sample_user.id)
        with pytest.raises(IntegrityError):
            await CartCrud.add(session=session, values=data2)

    @pytest.mark.asyncio
    async def test_invalid_user_raises(self, session):
        data = CartCreate(id=gen_id(), user_id="ghost")
        with pytest.raises(IntegrityError):
            await CartCrud.add(session=session, values=data)


class TestCartDelete:

    @pytest.mark.asyncio
    async def test_delete(self, session, sample_cart):
        result = await CartCrud.delete_one_by_id(session=session, id=sample_cart.id)
        assert result is True
        found = await CartCrud.find_one_or_none_by_id(session=session, id=sample_cart.id)
        assert found is None

    @pytest.mark.asyncio
    async def test_delete_nonexistent(self, session):
        result = await CartCrud.delete_one_by_id(session=session, id="no-cart")
        assert result is False