"""Тесты CRUD для Order."""

import pytest
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from .helpers import gen_id, OrderCrud, OrderCreate, OrderUpdate, Status


class TestOrderAdd:

    @pytest.mark.asyncio
    async def test_add(self, session, sample_user, sample_address):
        oid = gen_id()
        data = OrderCreate(
            id=oid,
            user_id=sample_user.id,
            address_id=sample_address.id,
            order_date=datetime.utcnow(),
            total_amount=15990,
        )
        await OrderCrud.add(session=session, values=data)

        found = await OrderCrud.find_one_or_none_by_id(session=session, id=oid)
        assert found is not None
        assert found.user_id == sample_user.id
        assert found.address_id == sample_address.id
        assert found.total_amount == 15990

    @pytest.mark.asyncio
    async def test_default_status_is_confirmation(self, session, sample_user, sample_address):
        oid = gen_id()
        data = OrderCreate(
            id=oid,
            user_id=sample_user.id,
            address_id=sample_address.id,
            order_date=datetime.utcnow(),
            total_amount=10000,
        )
        await OrderCrud.add(session=session, values=data)

        found = await OrderCrud.find_one_or_none_by_id(session=session, id=oid)
        assert found.status == Status.confirmation

    @pytest.mark.asyncio
    async def test_add_invalid_user_raises(self, session, sample_address):
        data = OrderCreate(
            id=gen_id(),
            user_id="ghost-user",
            address_id=sample_address.id,
            order_date=datetime.utcnow(),
            total_amount=0,
        )
        with pytest.raises(IntegrityError):
            await OrderCrud.add(session=session, values=data)

    @pytest.mark.asyncio
    async def test_add_invalid_address_raises(self, session, sample_user):
        data = OrderCreate(
            id=gen_id(),
            user_id=sample_user.id,
            address_id="ghost-address",
            order_date=datetime.utcnow(),
            total_amount=0,
        )
        with pytest.raises(IntegrityError):
            await OrderCrud.add(session=session, values=data)

    @pytest.mark.asyncio
    async def test_user_multiple_orders(self, session, sample_user, sample_address):
        for i in range(3):
            data = OrderCreate(
                id=gen_id(),
                user_id=sample_user.id,
                address_id=sample_address.id,
                order_date=datetime.utcnow(),
                total_amount=1000 * (i + 1),
            )
            await OrderCrud.add(session=session, values=data)


class TestOrderUpdate:

    @pytest.mark.asyncio
    async def test_update_total_amount(self, session, sample_order):
        await OrderCrud.update_one_by_id(
            session=session, id=sample_order.id,
            new_values=OrderUpdate(total_amount=50000),
        )
        found = await OrderCrud.find_one_or_none_by_id(session=session, id=sample_order.id)
        assert found.total_amount == 50000

    @pytest.mark.asyncio
    async def test_update_status(self, session, sample_order):
        await OrderCrud.update_one_by_id(
            session=session, id=sample_order.id,
            new_values=OrderUpdate(status=Status.transit),
        )
        found = await OrderCrud.find_one_or_none_by_id(session=session, id=sample_order.id)
        assert found.status == Status.transit

    @pytest.mark.asyncio
    async def test_update_status_flow(self, session, sample_order):
        for status in [Status.confirmation, Status.transit, Status.delivered]:
            await OrderCrud.update_one_by_id(
                session=session, id=sample_order.id,
                new_values=OrderUpdate(status=status),
            )
            found = await OrderCrud.find_one_or_none_by_id(session=session, id=sample_order.id)
            assert found.status == status

    @pytest.mark.asyncio
    async def test_update_nonexistent(self, session):
        result = await OrderCrud.update_one_by_id(
            session=session, id="no-order",
            new_values=OrderUpdate(total_amount=0),
        )
        assert result is None


class TestOrderDelete:

    @pytest.mark.asyncio
    async def test_delete(self, session, sample_order):
        result = await OrderCrud.delete_one_by_id(session=session, id=sample_order.id)
        assert result is True

    @pytest.mark.asyncio
    async def test_delete_nonexistent(self, session):
        result = await OrderCrud.delete_one_by_id(session=session, id="no-order")
        assert result is False