"""Тесты CRUD для Size."""

import pytest
from sqlalchemy.exc import IntegrityError
from .helpers import gen_id, SizeCrud, SizeCreate, SizeUpdate


class TestSizeAdd:

    @pytest.mark.asyncio
    async def test_add(self, session, sample_product):
        sid = gen_id()
        data = SizeCreate(
            id=sid,
            product_id=sample_product.id,
            count=10,
            size=42,
        )
        await SizeCrud.add(session=session, values=data)

        found = await SizeCrud.find_one_or_none_by_id(session=session, id=sid)
        assert found is not None
        assert found.product_id == sample_product.id
        assert found.count == 10
        assert found.size == 42

    @pytest.mark.asyncio
    async def test_multiple_sizes_for_product(self, session, sample_product):
        for sz in [39, 40, 41, 42, 43, 44, 45]:
            data = SizeCreate(
                id=gen_id(),
                product_id=sample_product.id,
                count=5,
                size=sz,
            )
            await SizeCrud.add(session=session, values=data)

    @pytest.mark.asyncio
    async def test_zero_count(self, session, sample_product):
        sid = gen_id()
        data = SizeCreate(
            id=sid, product_id=sample_product.id,
            count=0, size=46,
        )
        await SizeCrud.add(session=session, values=data)

        found = await SizeCrud.find_one_or_none_by_id(session=session, id=sid)
        assert found.count == 0

    @pytest.mark.asyncio
    async def test_invalid_product_raises(self, session):
        data = SizeCreate(
            id=gen_id(), product_id="ghost",
            count=5, size=42,
        )
        with pytest.raises(IntegrityError):
            await SizeCrud.add(session=session, values=data)

    @pytest.mark.asyncio
    async def test_size_is_int(self, session, sample_product):
        sid = gen_id()
        data = SizeCreate(
            id=sid, product_id=sample_product.id,
            count=3, size=44,
        )
        await SizeCrud.add(session=session, values=data)

        found = await SizeCrud.find_one_or_none_by_id(session=session, id=sid)
        assert isinstance(found.size, int)


class TestSizeUpdate:

    @pytest.mark.asyncio
    async def test_update_count(self, session, sample_size):
        await SizeCrud.update_one_by_id(
            session=session, id=sample_size.id,
            new_values=SizeUpdate(count=0),
        )
        found = await SizeCrud.find_one_or_none_by_id(session=session, id=sample_size.id)
        assert found.count == 0

    @pytest.mark.asyncio
    async def test_update_size_value(self, session, sample_size):
        await SizeCrud.update_one_by_id(
            session=session, id=sample_size.id,
            new_values=SizeUpdate(size=44),
        )
        found = await SizeCrud.find_one_or_none_by_id(session=session, id=sample_size.id)
        assert found.size == 44


class TestSizeDelete:

    @pytest.mark.asyncio
    async def test_delete(self, session, sample_size):
        result = await SizeCrud.delete_one_by_id(session=session, id=sample_size.id)
        assert result is True
        found = await SizeCrud.find_one_or_none_by_id(session=session, id=sample_size.id)
        assert found is None