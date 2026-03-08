"""Тесты CRUD для Address."""

import pytest
from .helpers import gen_id, AddressCrud, AddressCreate, AddressUpdate


class TestAddressAdd:

    @pytest.mark.asyncio
    async def test_add(self, session):
        aid = gen_id()
        data = AddressCreate(
            id=aid,
            region="Ленинградская область",
            city="Санкт-Петербург",
            street="Невский проспект",
            house="10",
            entrance="1",
            apartment="5",
            postcode=190000,
        )
        await AddressCrud.add(session=session, values=data)

        found = await AddressCrud.find_one_or_none_by_id(session=session, id=aid)
        assert found is not None
        assert found.city == "Санкт-Петербург"
        assert found.street == "Невский проспект"
        assert found.postcode == 190000

    @pytest.mark.asyncio
    async def test_postcode_is_int(self, session):
        aid = gen_id()
        data = AddressCreate(
            id=aid,
            region="МО", city="Город", street="Ул",
            house="1", entrance="1", apartment="1",
            postcode=999999,
        )
        await AddressCrud.add(session=session, values=data)

        found = await AddressCrud.find_one_or_none_by_id(session=session, id=aid)
        assert isinstance(found.postcode, int)
        assert found.postcode == 999999


class TestAddressUpdate:

    @pytest.mark.asyncio
    async def test_update_city_and_street(self, session, sample_address):
        await AddressCrud.update_one_by_id(
            session=session, id=sample_address.id,
            new_values=AddressUpdate(city="Казань", street="Баумана"),
        )
        found = await AddressCrud.find_one_or_none_by_id(session=session, id=sample_address.id)
        assert found.city == "Казань"
        assert found.street == "Баумана"
        assert found.region == sample_address.region

    @pytest.mark.asyncio
    async def test_update_postcode(self, session, sample_address):
        await AddressCrud.update_one_by_id(
            session=session, id=sample_address.id,
            new_values=AddressUpdate(postcode=654321),
        )
        found = await AddressCrud.find_one_or_none_by_id(session=session, id=sample_address.id)
        assert found.postcode == 654321


class TestAddressDelete:

    @pytest.mark.asyncio
    async def test_delete(self, session, sample_address):
        result = await AddressCrud.delete_one_by_id(session=session, id=sample_address.id)
        assert result is True
        found = await AddressCrud.find_one_or_none_by_id(session=session, id=sample_address.id)
        assert found is None

    @pytest.mark.asyncio
    async def test_delete_nonexistent(self, session):
        result = await AddressCrud.delete_one_by_id(session=session, id="no-addr")
        assert result is False