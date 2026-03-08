"""Тесты CRUD для Brand."""

import pytest
from .helpers import gen_id, BrandCrud, BrandCreate, BrandUpdate


class TestBrandAdd:

    @pytest.mark.asyncio
    async def test_add(self, session):
        bid = gen_id()
        data = BrandCreate(id=bid, brand_logo="https://example.com/adidas.png")
        await BrandCrud.add(session=session, values=data)

        found = await BrandCrud.find_one_or_none_by_id(session=session, id=bid)
        assert found is not None
        assert found.brand_logo == "https://example.com/adidas.png"

    @pytest.mark.asyncio
    async def test_add_multiple(self, session):
        ids = []
        for i in range(5):
            bid = gen_id()
            ids.append(bid)
            await BrandCrud.add(
                session=session,
                values=BrandCreate(id=bid, brand_logo=f"logo_{i}.png"),
            )
        for bid in ids:
            found = await BrandCrud.find_one_or_none_by_id(session=session, id=bid)
            assert found is not None


class TestBrandFindById:

    @pytest.mark.asyncio
    async def test_find_existing(self, session, sample_brand):
        found = await BrandCrud.find_one_or_none_by_id(session=session, id=sample_brand.id)
        assert found is not None
        assert found.brand_logo == sample_brand.brand_logo

    @pytest.mark.asyncio
    async def test_find_nonexistent(self, session):
        found = await BrandCrud.find_one_or_none_by_id(session=session, id="no-brand")
        assert found is None


class TestBrandUpdate:

    @pytest.mark.asyncio
    async def test_update_logo(self, session, sample_brand):
        await BrandCrud.update_one_by_id(
            session=session, id=sample_brand.id,
            new_values=BrandUpdate(brand_logo="updated.png"),
        )
        found = await BrandCrud.find_one_or_none_by_id(session=session, id=sample_brand.id)
        assert found.brand_logo == "updated.png"

    @pytest.mark.asyncio
    async def test_update_nonexistent(self, session):
        result = await BrandCrud.update_one_by_id(
            session=session, id="no-brand",
            new_values=BrandUpdate(brand_logo="x"),
        )
        assert result is None


class TestBrandDelete:

    @pytest.mark.asyncio
    async def test_delete(self, session, sample_brand):
        result = await BrandCrud.delete_one_by_id(session=session, id=sample_brand.id)
        assert result is True
        found = await BrandCrud.find_one_or_none_by_id(session=session, id=sample_brand.id)
        assert found is None

    @pytest.mark.asyncio
    async def test_delete_nonexistent(self, session):
        result = await BrandCrud.delete_one_by_id(session=session, id="no-brand")
        assert result is False