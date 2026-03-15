import pytest
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from shoersshopapi.api.v1.users.crud import UserCrud
from shoersshopapi.api.v1.utils import validate_password
from shoersshopapi.api.v1.schemas.user_schemas import (
    UserSchema,
    UserUpdate,
    UserFilter,
)
from shoersshopapi.core.database.models import User
from shoersshopapi.core.utils.enum import Role

from test.helpers import gen_id, unique_phone, unique_email


#  CREATE

class TestCreateUser:

    @pytest.mark.asyncio
    async def test_create_user_success(self, session: AsyncSession):
        """Успешное создание пользователя"""
        data = UserSchema(
            surname="Новый",
            name="Пользователь",
            patronymic="Тестович",
            password="password123",
            role=Role.user,
            phone=unique_phone(),
            email=unique_email(),
        )

        user = await UserCrud.create_user(session, data)

        assert user is not None
        assert user.surname == "Новый"
        assert user.name == "Пользователь"

    @pytest.mark.asyncio
    async def test_create_user_has_uuid(self, session: AsyncSession):
        """У созданного пользователя есть UUID"""
        data = UserSchema(
            surname="Тест",
            name="Тест",
            patronymic="Тест",
            password="password",
            role=Role.user,
            phone=unique_phone(),
            email=unique_email(),
        )

        user: User | None = await UserCrud.create_user(session, data)

        assert user.id is not None
        assert len(user.id) == 36

    @pytest.mark.asyncio
    async def test_create_user_password_hashed(self, session: AsyncSession):
        """Пароль хешируется при создании"""
        raw_password = "my_secret_password"
        data = UserSchema(
            surname="Тест",
            name="Тест",
            patronymic="Тест",
            password=raw_password,
            role=Role.user,
            phone=unique_phone(),
            email=unique_email(),
        )

        user = await UserCrud.create_user(session, data)

        assert user.password != raw_password
        assert user.password != raw_password.encode()
        assert validate_password(raw_password, user.password) is True

    @pytest.mark.asyncio
    async def test_create_user_wrong_password_fails(self, session: AsyncSession):
        """Неправильный пароль не проходит проверку"""
        data = UserSchema(
            surname="Тест",
            name="Тест",
            patronymic="Тест",
            password="correct_password",
            role=Role.user,
            phone=unique_phone(),
            email=unique_email(),
        )

        user = await UserCrud.create_user(session, data)

        assert validate_password("wrong_password", user.password) is False

    @pytest.mark.asyncio
    async def test_create_user_duplicate_phone(self, session: AsyncSession, sample_user: User):
        """Создание с занятым телефоном → 409"""
        data = UserSchema(
            surname="Другой",
            name="Человек",
            patronymic="Тестович",
            password="password123",
            role=Role.user,
            phone=sample_user.phone,
            email=unique_email(),
        )

        with pytest.raises(HTTPException) as exc_info:
            await UserCrud.create_user(session, data)

        assert exc_info.value.status_code == 409

    @pytest.mark.asyncio
    async def test_create_user_duplicate_email(self, session: AsyncSession, sample_user: User):
        """Создание с занятым email → 409"""
        data = UserSchema(
            surname="Другой",
            name="Человек",
            patronymic="Тестович",
            password="password123",
            role=Role.user,
            phone=unique_phone(),
            email=sample_user.email,
        )

        with pytest.raises(HTTPException) as exc_info:
            await UserCrud.create_user(session, data)

        assert exc_info.value.status_code == 409

#  CHECK UNIQUE

class TestCheckUserUnique:

    @pytest.mark.asyncio
    async def test_unique_passes(self, session: AsyncSession):
        """Уникальные данные проходят проверку"""
        data = UserSchema(
            surname="Тест",
            name="Тест",
            patronymic="Тест",
            password="pass",
            role=Role.user,
            phone=unique_phone(),
            email=unique_email(),
        )

        result = await UserCrud.check_user_unique(session, data)
        assert result is True

    @pytest.mark.asyncio
    async def test_duplicate_phone_raises(self, session: AsyncSession, sample_user: User):
        """Занятый телефон → 409"""
        data = UserSchema(
            surname="Тест",
            name="Тест",
            patronymic="Тест",
            password="pass",
            role=Role.user,
            phone=sample_user.phone,
            email=unique_email(),
        )

        with pytest.raises(HTTPException) as exc_info:
            await UserCrud.check_user_unique(session, data)
        assert exc_info.value.status_code == 409

    @pytest.mark.asyncio
    async def test_duplicate_email_raises(self, session: AsyncSession, sample_user: User):
        """Занятый email → 409"""
        data = UserSchema(
            surname="Тест",
            name="Тест",
            patronymic="Тест",
            password="pass",
            role=Role.user,
            phone=unique_phone(),
            email=sample_user.email,
        )

        with pytest.raises(HTTPException) as exc_info:
            await UserCrud.check_user_unique(session, data)
        assert exc_info.value.status_code == 409

#  READ: один пользователь

class TestGetUser:

    @pytest.mark.asyncio
    async def test_get_by_id_found(self, session: AsyncSession, sample_user: User):
        """Пользователь найден по id"""
        result = await UserCrud.get_by_id(session, sample_user.id)

        assert result is not None
        assert result.id == sample_user.id
        assert result.surname == sample_user.surname

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(self, session: AsyncSession):
        """Пользователь не найден по id"""
        result = await UserCrud.get_by_id(session, "nonexistent-id")
        assert result is None

    @pytest.mark.asyncio
    async def test_get_by_email_found(self, session: AsyncSession, sample_user: User):
        """Пользователь найден по email"""
        result = await UserCrud.get_by_email(session, sample_user.email)

        assert result is not None
        assert result.email == sample_user.email

    @pytest.mark.asyncio
    async def test_get_by_email_not_found(self, session: AsyncSession):
        """Пользователь не найден по email"""
        result = await UserCrud.get_by_email(session, "nonexistent@example.com")
        assert result is None

    @pytest.mark.asyncio
    async def test_get_by_phone_found(self, session: AsyncSession, sample_user: User):
        """Пользователь найден по телефону"""
        result = await UserCrud.get_by_phone(session, sample_user.phone)

        assert result is not None
        assert result.phone == sample_user.phone

    @pytest.mark.asyncio
    async def test_get_by_phone_not_found(self, session: AsyncSession):
        """Пользователь не найден по телефону"""
        result = await UserCrud.get_by_phone(session, "+70000000000")
        assert result is None


#  READ: с подгрузкой связей

class TestGetUserWithRelations:

    @pytest.mark.asyncio
    async def test_get_with_addresses(self, session: AsyncSession, user_with_addresses):
        """Пользователь с адресами"""
        user, addresses = user_with_addresses

        result = await UserCrud.get_with_addresses(session, user.id)

        assert result is not None
        assert hasattr(result, "addresses")
        assert len(result.addresses) == 3

    @pytest.mark.asyncio
    async def test_get_with_addresses_empty(self, session: AsyncSession, sample_user: User):
        """Пользователь без адресов"""
        result = await UserCrud.get_with_addresses(session, sample_user.id)

        assert result is not None
        assert len(result.addresses) == 0

    @pytest.mark.asyncio
    async def test_get_with_addresses_not_found(self, session: AsyncSession):
        """Несуществующий пользователь"""
        result = await UserCrud.get_with_addresses(session, "nonexistent")
        assert result is None

    @pytest.mark.asyncio
    async def test_get_with_orders(self, session: AsyncSession, user_with_orders):
        """Пользователь с заказами"""
        user, orders = user_with_orders

        result = await UserCrud.get_with_orders(session, user.id)

        assert result is not None
        assert len(result.orders) == 3

    @pytest.mark.asyncio
    async def test_get_with_orders_empty(self, session: AsyncSession, sample_user: User):
        """Пользователь без заказов"""
        result = await UserCrud.get_with_orders(session, sample_user.id)

        assert result is not None
        assert len(result.orders) == 0

    @pytest.mark.asyncio
    async def test_get_with_reviews(self, session: AsyncSession, user_with_reviews):
        """Пользователь с отзывами"""
        user, reviews = user_with_reviews

        result = await UserCrud.get_with_reviews(session, user.id)

        assert result is not None
        assert len(result.reviews) == 3

    @pytest.mark.asyncio
    async def test_get_with_reviews_empty(self, session: AsyncSession, sample_user: User):
        """Пользователь без отзывов"""
        result = await UserCrud.get_with_reviews(session, sample_user.id)

        assert result is not None
        assert len(result.reviews) == 0

    @pytest.mark.asyncio
    async def test_get_full(self, session: AsyncSession, user_with_reviews):
        """Пользователь со всеми связями"""
        user, reviews = user_with_reviews  # распаковка tuple

        result = await UserCrud.get_full(session, user.id)

        assert result is not None
        assert hasattr(result, "addresses")
        assert hasattr(result, "orders")
        assert hasattr(result, "reviews")
        assert len(result.reviews) == 3

    @pytest.mark.asyncio
    async def test_get_full_not_found(self, session: AsyncSession):
        """Несуществующий пользователь"""
        result = await UserCrud.get_full(session, "nonexistent")
        assert result is None


#  READ: список пользователей

class TestGetAllUsers:

    @pytest.mark.asyncio
    async def test_get_all_no_filters(self, session: AsyncSession, sample_users: list[User]):
        """Получить всех пользователей"""
        result = await UserCrud.get_all(session)

        assert len(result) >= 5

    @pytest.mark.asyncio
    async def test_get_all_with_role_filter(self, session: AsyncSession, sample_users: list[User]):
        """Фильтр по роли"""
        filters = UserFilter(role=Role.user)
        result = await UserCrud.get_all(session, filters=filters)

        for user in result:
            assert user.role == Role.user

    @pytest.mark.asyncio
    async def test_get_all_with_limit(self, session: AsyncSession, sample_users: list[User]):
        """Лимит"""
        result = await UserCrud.get_all(session, limit=2)

        assert len(result) <= 2

    @pytest.mark.asyncio
    async def test_get_all_with_offset(self, session: AsyncSession, sample_users: list[User]):
        """Смещение"""
        all_users = await UserCrud.get_all(session)
        offset_users = await UserCrud.get_all(session, offset=2)

        assert len(offset_users) == len(all_users) - 2

    @pytest.mark.asyncio
    async def test_get_all_pagination(self, session: AsyncSession, sample_users: list[User]):
        """Пагинация без пересечений"""
        page1 = await UserCrud.get_all(session, limit=2, offset=0)
        page2 = await UserCrud.get_all(session, limit=2, offset=2)

        assert len(page1) == 2
        assert len(page2) == 2

        page1_ids = {u.id for u in page1}
        page2_ids = {u.id for u in page2}
        assert page1_ids.isdisjoint(page2_ids)


#  UPDATE

class TestUpdateUser:

    @pytest.mark.asyncio
    async def test_update_name_success(self, session: AsyncSession, sample_user: User):
        """Успешное обновление имени"""
        data = UserUpdate(name="НовоеИмя", surname="НоваяФамилия")

        result, error = await UserCrud.update_user(session, sample_user.id, data)

        assert result is not None
        assert error is None
        assert result.name == "НовоеИмя"
        assert result.surname == "НоваяФамилия"

    @pytest.mark.asyncio
    async def test_update_phone_success(self, session: AsyncSession, sample_user: User):
        """Успешное обновление телефона"""
        new_phone = unique_phone()
        data = UserUpdate(phone=new_phone)

        result, error = await UserCrud.update_user(session, sample_user.id, data)

        assert result is not None
        assert error is None
        assert result.phone == new_phone

    @pytest.mark.asyncio
    async def test_update_email_success(self, session: AsyncSession, sample_user: User):
        """Успешное обновление email"""
        new_email = unique_email()
        data = UserUpdate(email=new_email)

        result, error = await UserCrud.update_user(session, sample_user.id, data)

        assert result is not None
        assert error is None
        assert result.email == new_email

    @pytest.mark.asyncio
    async def test_update_password_hashed(self, session: AsyncSession, sample_user: User):
        """Пароль хешируется при обновлении"""
        new_password = "new_secret_password"
        data = UserUpdate(password=new_password)

        result, error = await UserCrud.update_user(session, sample_user.id, data)

        assert result is not None
        assert error is None
        assert result.password != new_password
        assert result.password != new_password.encode()
        assert validate_password(new_password, result.password) is True

    @pytest.mark.asyncio
    async def test_update_password_old_invalid(self, session: AsyncSession):
        """После смены пароля старый не работает"""
        data = UserSchema(
            surname="Тест",
            name="Тест",
            patronymic="Тест",
            password="old_password",
            role=Role.user,
            phone=unique_phone(),
            email=unique_email(),
        )
        user = await UserCrud.create_user(session, data)

        update_data = UserUpdate(password="new_password")
        updated_user, error = await UserCrud.update_user(session, user.id, update_data)

        assert updated_user is not None
        assert validate_password("old_password", updated_user.password) is False
        assert validate_password("new_password", updated_user.password) is True

    @pytest.mark.asyncio
    async def test_update_without_password_keeps_old(self, session: AsyncSession):
        """Обновление без пароля не меняет его"""
        data = UserSchema(
            surname="Тест",
            name="Тест",
            patronymic="Тест",
            password="original_password",
            role=Role.user,
            phone=unique_phone(),
            email=unique_email(),
        )
        user = await UserCrud.create_user(session, data)
        old_password_hash = user.password

        update_data = UserUpdate(name="НовоеИмя")
        updated_user, error = await UserCrud.update_user(session, user.id, update_data)

        assert updated_user is not None
        assert updated_user.password == old_password_hash
        assert validate_password("original_password", updated_user.password) is True

    @pytest.mark.asyncio
    async def test_update_duplicate_phone(self, session: AsyncSession, sample_users: list[User]):
        """Обновление с занятым телефоном → 409"""
        user1, user2 = sample_users[0], sample_users[1]
        data = UserUpdate(phone=user2.phone)

        with pytest.raises(HTTPException) as exc_info:
            await UserCrud.update_user(session, user1.id, data)

        assert exc_info.value.status_code == 409

    @pytest.mark.asyncio
    async def test_update_duplicate_email(self, session: AsyncSession, sample_users: list[User]):
        """Обновление с занятым email → 409"""
        user1, user2 = sample_users[0], sample_users[1]
        data = UserUpdate(email=user2.email)

        with pytest.raises(HTTPException) as exc_info:
            await UserCrud.update_user(session, user1.id, data)

        assert exc_info.value.status_code == 409

    @pytest.mark.asyncio
    async def test_update_nonexistent_user(self, session: AsyncSession):
        """Обновление несуществующего пользователя"""
        data = UserUpdate(name="Новое")

        result, error = await UserCrud.update_user(session, "nonexistent-id", data)

        assert result is None
        assert error is None

    @pytest.mark.asyncio
    async def test_update_no_changes(self, session: AsyncSession, sample_user: User):
        """Обновление без изменений"""
        original_name = sample_user.name
        data = UserUpdate()

        result, error = await UserCrud.update_user(session, sample_user.id, data)

        assert result is not None
        assert error is None
        assert result.name == original_name


#  DELETE

class TestDeleteUser:

    @pytest.mark.asyncio
    async def test_delete_success(self, session: AsyncSession, sample_user: User):
        """Успешное удаление"""
        result = await UserCrud.delete_user(session, sample_user.id)
        assert result is True

        check = await UserCrud.get_by_id(session, sample_user.id)
        assert check is None

    @pytest.mark.asyncio
    async def test_delete_not_found(self, session: AsyncSession):
        """Удаление несуществующего"""
        result = await UserCrud.delete_user(session, "nonexistent-id")
        assert result is False

    @pytest.mark.asyncio
    async def test_delete_twice(self, session: AsyncSession, sample_user: User):
        """Двойное удаление"""
        result1 = await UserCrud.delete_user(session, sample_user.id)
        result2 = await UserCrud.delete_user(session, sample_user.id)

        assert result1 is True
        assert result2 is False