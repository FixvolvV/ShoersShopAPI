"""
Тесты, выявляющие баги в BaseCrud.
"""

import pytest
from test.helpers import (
    gen_id, unique_phone, unique_email,
    UserCrud, UserCreate, UserUpdate,
)
from pydantic import BaseModel

class TestBugAddReturnsNone:

    @pytest.mark.asyncio
    async def test_add_returns_none(self, session):
        data = UserCreate(
            id=gen_id(),
            surname="Bug", name="Add", patronymic="Test",
            password=b"hash",
            phone=unique_phone(),
            email=unique_email(),
        )

        result = await UserCrud.add(session=session, values=data)

        assert result is not None, (
            "BUG: BaseCrud.add() возвращает None! "
            "session.add() не возвращает объект. "
            "Замени 'return responce' на 'return instanse'."
        )

    @pytest.mark.asyncio
    async def test_add_saves_despite_returning_none(self, session):
        user_id = gen_id()
        data = UserCreate(
            id=user_id,
            surname="Save", name="Works", patronymic="Test",
            password=b"hash",
            phone=unique_phone(),
            email=unique_email(),
        )

        await UserCrud.add(session=session, values=data)

        found = await UserCrud.find_one_or_none_by_id(session=session, id=user_id)
        assert found is not None
        assert found.surname == "Save"

class TestBugUpdateNoReturn:

    @pytest.mark.asyncio
    async def test_update_returns_none(self, session, sample_user):
        new_values = UserUpdate(name="Обновлённое")

        result = await UserCrud.update_one_by_id(
            session=session, id=sample_user.id, new_values=new_values,
        )

        assert result is not None, (
            "BUG: update_one_by_id() не возвращает объект! "
            "Добавь 'return target' после flush()."
        )

    @pytest.mark.asyncio
    async def test_update_modifies_despite_bug(self, session, sample_user):
        new_values = UserUpdate(name="Работает")

        await UserCrud.update_one_by_id(
            session=session, id=sample_user.id, new_values=new_values,
        )

        found = await UserCrud.find_one_or_none_by_id(session=session, id=sample_user.id)
        assert found.name == "Работает"