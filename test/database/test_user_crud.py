"""Тесты CRUD для User."""

import pytest
from sqlalchemy.exc import IntegrityError
from .helpers import (
    gen_id, unique_phone, unique_email,
    UserCrud, UserCreate, UserUpdate,
    Role,
)

from shoersshopapi.core.database.models import User


class TestUserAdd:

    @pytest.mark.asyncio
    async def test_add_saves_all_fields(self, session):
        user_id = gen_id()
        data = UserCreate(
            id=user_id,
            surname="Петров",
            name="Пётр",
            patronymic="Петрович",
            password=b"secure_hash_bytes",
            phone="+79998887701",
            email="petr_crud_test@test.com",
            social_link=["https://vk.com/petr"],
        )

        await UserCrud.add(session=session, values=data)

        found = await UserCrud.find_one_or_none_by_id(session=session, id=user_id)
        assert found is not None
        assert found.id == user_id
        assert found.surname == "Петров"
        assert found.name == "Пётр"
        assert found.patronymic == "Петрович"
        assert found.password == b"secure_hash_bytes"
        assert found.phone == "+79998887701"
        assert found.email == "petr_crud_test@test.com"
        assert found.social_link == ["https://vk.com/petr"]

    @pytest.mark.asyncio
    async def test_add_without_social_link(self, session):
        user_id = gen_id()
        data = UserCreate(
            id=user_id,
            surname="Без", name="Ссылок", patronymic="Тестович",
            password=b"hash",
            phone=unique_phone(),
            email=unique_email(),
        )

        await UserCrud.add(session=session, values=data)

        found = await UserCrud.find_one_or_none_by_id(session=session, id=user_id)
        assert found is not None

    @pytest.mark.asyncio
    async def test_add_password_stored_as_bytes(self, session):
        user_id = gen_id()
        pwd = b"\x00\x01\x02hashed_bcrypt"
        data = UserCreate(
            id=user_id,
            surname="Bytes", name="Pwd", patronymic="Test",
            password=pwd,
            phone=unique_phone(),
            email=unique_email(),
        )

        await UserCrud.add(session=session, values=data)

        found = await UserCrud.find_one_or_none_by_id(session=session, id=user_id)
        assert isinstance(found.password, bytes)
        assert found.password == pwd

    @pytest.mark.asyncio
    async def test_add_default_role_is_user(self, session):
        user_id = gen_id()
        data = UserCreate(
            id=user_id,
            surname="Role", name="Default", patronymic="Test",
            password=b"hash",
            phone=unique_phone(),
            email=unique_email(),
        )

        await UserCrud.add(session=session, values=data)

        found = await UserCrud.find_one_or_none_by_id(session=session, id=user_id)
        assert found.role == Role.user

    @pytest.mark.asyncio
    async def test_add_social_link_multiple(self, session):
        user_id = gen_id()
        links = ["https://t.me/u", "https://vk.com/u", "https://ig.com/u"]
        data = UserCreate(
            id=user_id,
            surname="Multi", name="Link", patronymic="Test",
            password=b"hash",
            phone=unique_phone(),
            email=unique_email(),
            social_link=links,
        )

        await UserCrud.add(session=session, values=data)

        found = await UserCrud.find_one_or_none_by_id(session=session, id=user_id)
        assert found.social_link == links
        assert len(found.social_link) == 3


class TestUserDuplicateConstraints:

    @pytest.mark.asyncio
    async def test_duplicate_email_raises(self, session):
        email = unique_email()
        user1 = User(
            id=gen_id(),
            surname="Dup1", name="Email", patronymic="T",
            password=b"h", phone=unique_phone(), email=email,
        )
        session.add(user1)
        await session.flush()

        data2 = UserCreate(
            id=gen_id(),
            surname="Dup2", name="Email", patronymic="T",
            password=b"h", phone=unique_phone(), email=email,
        )
        with pytest.raises(IntegrityError):
            await UserCrud.add(session=session, values=data2)

    @pytest.mark.asyncio
    async def test_duplicate_phone_raises(self, session):
        phone = unique_phone()
        user1 = User(
            id=gen_id(),
            surname="Dup1", name="Phone", patronymic="T",
            password=b"h", phone=phone, email=unique_email(),
        )
        session.add(user1)
        await session.flush()

        data2 = UserCreate(
            id=gen_id(),
            surname="Dup2", name="Phone", patronymic="T",
            password=b"h", phone=phone, email=unique_email(),
        )
        with pytest.raises(IntegrityError):
            await UserCrud.add(session=session, values=data2)

    @pytest.mark.asyncio
    async def test_duplicate_id_raises(self, session):
        same_id = gen_id()
        user1 = User(
            id=same_id,
            surname="Dup1", name="ID", patronymic="T",
            password=b"h", phone=unique_phone(), email=unique_email(),
        )
        session.add(user1)
        await session.flush()

        data2 = UserCreate(
            id=same_id,
            surname="Dup2", name="ID", patronymic="T",
            password=b"h", phone=unique_phone(), email=unique_email(),
        )
        with pytest.raises(Exception):
            await UserCrud.add(session=session, values=data2)


class TestUserFindById:

    @pytest.mark.asyncio
    async def test_find_existing(self, session, sample_user):
        found = await UserCrud.find_one_or_none_by_id(session=session, id=sample_user.id)
        assert found is not None
        assert found.id == sample_user.id
        assert found.email == sample_user.email

    @pytest.mark.asyncio
    async def test_find_nonexistent(self, session):
        found = await UserCrud.find_one_or_none_by_id(session=session, id="no-such-id")
        assert found is None

    @pytest.mark.asyncio
    async def test_find_returns_user_instance(self, session, sample_user):
        found = await UserCrud.find_one_or_none_by_id(session=session, id=sample_user.id)
        assert isinstance(found, User)


class TestUserUpdate:

    @pytest.mark.asyncio
    async def test_update_name(self, session, sample_user):
        await UserCrud.update_one_by_id(
            session=session, id=sample_user.id,
            new_values=UserUpdate(name="НовоеИмя"),
        )
        found = await UserCrud.find_one_or_none_by_id(session=session, id=sample_user.id)
        assert found.name == "НовоеИмя"
        assert found.surname == sample_user.surname

    @pytest.mark.asyncio
    async def test_update_multiple_fields(self, session, sample_user):
        await UserCrud.update_one_by_id(
            session=session, id=sample_user.id,
            new_values=UserUpdate(name="Алекс", surname="Алексов", phone="+70000000000"),
        )
        found = await UserCrud.find_one_or_none_by_id(session=session, id=sample_user.id)
        assert found.name == "Алекс"
        assert found.surname == "Алексов"
        assert found.phone == "+70000000000"

    @pytest.mark.asyncio
    async def test_update_social_link(self, session, sample_user):
        links = ["https://t.me/new", "https://vk.com/new"]
        await UserCrud.update_one_by_id(
            session=session, id=sample_user.id,
            new_values=UserUpdate(social_link=links),
        )
        found = await UserCrud.find_one_or_none_by_id(session=session, id=sample_user.id)
        assert found.social_link == links

    @pytest.mark.asyncio
    async def test_update_nonexistent(self, session):
        result = await UserCrud.update_one_by_id(
            session=session, id="no-id",
            new_values=UserUpdate(name="Ghost"),
        )
        assert result is None

    @pytest.mark.asyncio
    async def test_update_empty_values(self, session, sample_user):
        original_name = sample_user.name
        await UserCrud.update_one_by_id(
            session=session, id=sample_user.id,
            new_values=UserUpdate(),
        )
        found = await UserCrud.find_one_or_none_by_id(session=session, id=sample_user.id)
        assert found.name == original_name


class TestUserDelete:

    @pytest.mark.asyncio
    async def test_delete_existing(self, session, sample_user):
        result = await UserCrud.delete_one_by_id(session=session, id=sample_user.id)
        assert result is True
        found = await UserCrud.find_one_or_none_by_id(session=session, id=sample_user.id)
        assert found is None

    @pytest.mark.asyncio
    async def test_delete_nonexistent(self, session):
        result = await UserCrud.delete_one_by_id(session=session, id="no-id")
        assert result is False

    @pytest.mark.asyncio
    async def test_delete_twice(self, session, sample_user):
        first = await UserCrud.delete_one_by_id(session=session, id=sample_user.id)
        assert first is True
        second = await UserCrud.delete_one_by_id(session=session, id=sample_user.id)
        assert second is False


class TestUserFullname:

    @pytest.mark.asyncio
    async def test_fullname_property(self, session, sample_user):
        found = await UserCrud.find_one_or_none_by_id(session=session, id=sample_user.id)
        expected = f"{found.surname} {found.name} {found.patronymic}"
        assert found.fullname == expected