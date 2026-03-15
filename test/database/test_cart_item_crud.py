"""Тесты CRUD для CartItem."""

import pytest
from sqlalchemy.exc import IntegrityError
from test.helpers import gen_id, CartItemCrud, CartItemCreate, CartItemUpdate, Color
from shoersshopapi.core.database.models.product import Product


class TestCartItemAdd:

    @pytest.mark.asyncio
    async def test_add(self, session, sample_cart, sample_product):
        cid = gen_id()
        data = CartItemCreate(
            id=cid,
            cart_id=sample_cart.id,
            product_id=sample_product.id,
            quantity=2,
        )
        await CartItemCrud.add(session=session, values=data)

        found = await CartItemCrud.find_one_or_none_by_id(session=session, id=cid)
        assert found is not None
        assert found.quantity == 2
        assert found.cart_id == sample_cart.id
        assert found.product_id == sample_product.id

    @pytest.mark.asyncio
    async def test_unique_constraint_cart_product(self, session, sample_cart, sample_product):
        data1 = CartItemCreate(
            id=gen_id(),
            cart_id=sample_cart.id,
            product_id=sample_product.id,
            quantity=1,
        )
        await CartItemCrud.add(session=session, values=data1)

        data2 = CartItemCreate(
            id=gen_id(),
            cart_id=sample_cart.id,
            product_id=sample_product.id,
            quantity=3,
        )
        with pytest.raises(IntegrityError):
            await CartItemCrud.add(session=session, values=data2)

    @pytest.mark.asyncio
    async def test_different_products_in_cart(self, session, sample_cart, sample_brand):
        for i in range(3):
            product = Product(
                id=gen_id(),
                brand_id=sample_brand.id,
                title=f"Cart Product {i}",
                price=5000.0,
                color=Color.white,
                avg_grade="0",
            )
            session.add(product)
            await session.flush()

            data = CartItemCreate(
                id=gen_id(),
                cart_id=sample_cart.id,
                product_id=product.id,
                quantity=i + 1,
            )
            await CartItemCrud.add(session=session, values=data)

    @pytest.mark.asyncio
    async def test_quantity_zero(self, session, sample_cart, sample_product):
        cid = gen_id()
        data = CartItemCreate(
            id=cid,
            cart_id=sample_cart.id,
            product_id=sample_product.id,
            quantity=0,
        )
        await CartItemCrud.add(session=session, values=data)

        found = await CartItemCrud.find_one_or_none_by_id(session=session, id=cid)
        assert found.quantity == 0

    @pytest.mark.asyncio
    async def test_invalid_cart_raises(self, session, sample_product):
        data = CartItemCreate(
            id=gen_id(),
            cart_id="ghost",
            product_id=sample_product.id,
            quantity=1,
        )
        with pytest.raises(IntegrityError):
            await CartItemCrud.add(session=session, values=data)

    @pytest.mark.asyncio
    async def test_invalid_product_raises(self, session, sample_cart):
        data = CartItemCreate(
            id=gen_id(),
            cart_id=sample_cart.id,
            product_id="ghost",
            quantity=1,
        )
        with pytest.raises(IntegrityError):
            await CartItemCrud.add(session=session, values=data)


class TestCartItemUpdate:

    @pytest.mark.asyncio
    async def test_update_quantity(self, session, sample_cart_item):
        await CartItemCrud.update_one_by_id(
            session=session, id=sample_cart_item.id,
            new_values=CartItemUpdate(quantity=10),
        )
        found = await CartItemCrud.find_one_or_none_by_id(session=session, id=sample_cart_item.id)
        assert found.quantity == 10


class TestCartItemDelete:

    @pytest.mark.asyncio
    async def test_delete(self, session, sample_cart_item):
        result = await CartItemCrud.delete_one_by_id(session=session, id=sample_cart_item.id)
        assert result is True
        found = await CartItemCrud.find_one_or_none_by_id(session=session, id=sample_cart_item.id)
        assert found is None