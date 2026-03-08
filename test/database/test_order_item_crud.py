"""Тесты CRUD для OrderItem."""

import pytest
from sqlalchemy.exc import IntegrityError
from .helpers import gen_id, OrderItemCrud, OrderItemCreate, OrderItemUpdate, Color
from src.shoersshopapi.core.database.models.product import Product


class TestOrderItemAdd:

    @pytest.mark.asyncio
    async def test_add(self, session, sample_order, sample_product):
        oid = gen_id()
        data = OrderItemCreate(
            id=oid,
            order_id=sample_order.id,
            product_id=sample_product.id,
            quantity=3,
        )
        await OrderItemCrud.add(session=session, values=data)

        found = await OrderItemCrud.find_one_or_none_by_id(session=session, id=oid)
        assert found is not None
        assert found.quantity == 3
        assert found.order_id == sample_order.id
        assert found.product_id == sample_product.id

    @pytest.mark.asyncio
    async def test_unique_constraint_order_product(self, session, sample_order, sample_product):
        data1 = OrderItemCreate(
            id=gen_id(),
            order_id=sample_order.id,
            product_id=sample_product.id,
            quantity=1,
        )
        await OrderItemCrud.add(session=session, values=data1)

        data2 = OrderItemCreate(
            id=gen_id(),
            order_id=sample_order.id,
            product_id=sample_product.id,
            quantity=5,
        )
        with pytest.raises(IntegrityError):
            await OrderItemCrud.add(session=session, values=data2)

    @pytest.mark.asyncio
    async def test_different_products_in_order(self, session, sample_order, sample_brand):
        for i in range(4):
            product = Product(
                id=gen_id(),
                brand_id=sample_brand.id,
                title=f"Order Product {i}",
                price=7000.0,
                color=Color.black,
                avg_grade="0",
            )
            session.add(product)
            await session.flush()

            data = OrderItemCreate(
                id=gen_id(),
                order_id=sample_order.id,
                product_id=product.id,
                quantity=i + 1,
            )
            await OrderItemCrud.add(session=session, values=data)

    @pytest.mark.asyncio
    async def test_invalid_order_raises(self, session, sample_product):
        data = OrderItemCreate(
            id=gen_id(),
            order_id="ghost",
            product_id=sample_product.id,
            quantity=1,
        )
        with pytest.raises(IntegrityError):
            await OrderItemCrud.add(session=session, values=data)

    @pytest.mark.asyncio
    async def test_invalid_product_raises(self, session, sample_order):
        data = OrderItemCreate(
            id=gen_id(),
            order_id=sample_order.id,
            product_id="ghost",
            quantity=1,
        )
        with pytest.raises(IntegrityError):
            await OrderItemCrud.add(session=session, values=data)


class TestOrderItemUpdate:

    @pytest.mark.asyncio
    async def test_update_quantity(self, session, sample_order_item):
        await OrderItemCrud.update_one_by_id(
            session=session, id=sample_order_item.id,
            new_values=OrderItemUpdate(quantity=10),
        )
        found = await OrderItemCrud.find_one_or_none_by_id(session=session, id=sample_order_item.id)
        assert found.quantity == 10


class TestOrderItemDelete:

    @pytest.mark.asyncio
    async def test_delete(self, session, sample_order_item):
        result = await OrderItemCrud.delete_one_by_id(session=session, id=sample_order_item.id)
        assert result is True
        found = await OrderItemCrud.find_one_or_none_by_id(session=session, id=sample_order_item.id)
        assert found is None

    @pytest.mark.asyncio
    async def test_delete_nonexistent(self, session):
        result = await OrderItemCrud.delete_one_by_id(session=session, id="no-oi")
        assert result is False