"""Тесты CRUD для Product."""

import pytest
from sqlalchemy.exc import IntegrityError
from test.helpers import gen_id, ProductCrud, ProductCreate, ProductUpdate, Color


class TestProductAdd:

    @pytest.mark.asyncio
    async def test_add(self, session, sample_brand):
        pid = gen_id()
        data = ProductCreate(
            id=pid,
            brand_id=sample_brand.id,
            title="Nike Dunk Low",
            price=15990.0,
            color=Color.black,
            avg_grade="0.0",
        )
        await ProductCrud.add(session=session, values=data)

        found = await ProductCrud.find_one_or_none_by_id(session=session, id=pid)
        assert found is not None
        assert found.title == "Nike Dunk Low"
        assert found.brand_id == sample_brand.id
        assert found.price == 15990.0
        assert found.color == Color.black

    @pytest.mark.asyncio
    async def test_add_without_brand(self, session):
        pid = gen_id()
        data = ProductCreate(
            id=pid,
            title="No Brand",
            price=5000.0,
            color=Color.white,
            avg_grade="0",
            brand_id=None,
        )
        await ProductCrud.add(session=session, values=data)

        found = await ProductCrud.find_one_or_none_by_id(session=session, id=pid)
        assert found is not None
        assert found.brand_id is None

    @pytest.mark.asyncio
    async def test_add_invalid_brand_raises(self, session):
        data = ProductCreate(
            id=gen_id(),
            brand_id="ghost-brand",
            title="Ghost",
            price=1000.0,
            color=Color.blue,
            avg_grade="0",
        )
        with pytest.raises(IntegrityError):
            await ProductCrud.add(session=session, values=data)

    @pytest.mark.asyncio
    async def test_add_zero_price(self, session, sample_brand):
        pid = gen_id()
        data = ProductCreate(
            id=pid,
            brand_id=sample_brand.id,
            title="Free",
            price=0.0,
            color=Color.gray,
            avg_grade="0",
        )
        await ProductCrud.add(session=session, values=data)

        found = await ProductCrud.find_one_or_none_by_id(session=session, id=pid)
        assert found.price == 0.0

    @pytest.mark.asyncio
    async def test_add_all_colors(self, session, sample_brand):
        for color in Color:
            pid = gen_id()
            data = ProductCreate(
                id=pid,
                brand_id=sample_brand.id,
                title=f"Sneaker {color.name}",
                price=10000.0,
                color=color,
                avg_grade="0",
            )
            await ProductCrud.add(session=session, values=data)

            found = await ProductCrud.find_one_or_none_by_id(session=session, id=pid)
            assert found.color == color


class TestProductUpdate:

    @pytest.mark.asyncio
    async def test_update_price(self, session, sample_product):
        await ProductCrud.update_one_by_id(
            session=session, id=sample_product.id,
            new_values=ProductUpdate(price=9999.0),
        )
        found = await ProductCrud.find_one_or_none_by_id(session=session, id=sample_product.id)
        assert found.price == 9999.0
        assert found.title == sample_product.title

    @pytest.mark.asyncio
    async def test_update_title(self, session, sample_product):
        await ProductCrud.update_one_by_id(
            session=session, id=sample_product.id,
            new_values=ProductUpdate(title="Updated Name"),
        )
        found = await ProductCrud.find_one_or_none_by_id(session=session, id=sample_product.id)
        assert found.title == "Updated Name"

    @pytest.mark.asyncio
    async def test_update_avg_grade(self, session, sample_product):
        await ProductCrud.update_one_by_id(
            session=session, id=sample_product.id,
            new_values=ProductUpdate(avg_grade="4.8"),
        )
        found = await ProductCrud.find_one_or_none_by_id(session=session, id=sample_product.id)
        assert found.avg_grade == "4.8"


class TestProductDelete:

    @pytest.mark.asyncio
    async def test_delete(self, session, sample_product):
        result = await ProductCrud.delete_one_by_id(session=session, id=sample_product.id)
        assert result is True
        found = await ProductCrud.find_one_or_none_by_id(session=session, id=sample_product.id)
        assert found is None

    @pytest.mark.asyncio
    async def test_delete_nonexistent(self, session):
        result = await ProductCrud.delete_one_by_id(session=session, id="no-prod")
        assert result is False