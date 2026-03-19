from typing import (
    Union
)

from fastapi import HTTPException

from pydantic import BaseModel
from starlette import status

from shoersshopapi.api.v1.basecrud import BaseCrud

from sqlalchemy.ext.asyncio import AsyncSession

from shoersshopapi.core.database.models import User

from shoersshopapi.api.v1.utils import gen_uuid, hash_password
from shoersshopapi.api.v1.schemas.user_schemas import (
    UserSchema,
    UserUpdate,
    UserFilter,
    UserWithId
)

# Функция добавляющая пользователя в DB. 
class UserCrud(BaseCrud[User]):
    model = User

    # === CREATE ===

    @classmethod
    async def check_user_unique(cls, session: AsyncSession, data: BaseModel) -> bool:

        exception = HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this phone or mail already exists"
        )

        # Берём только те поля, которые были заданы.
        data_dict = data.model_dump(exclude_none=True, exclude_unset=True)
        
        phone = data_dict.get("phone")
        email = data_dict.get("email")

        # Если ни phone, ни email не переданы — проверять нечего
        if not phone and not email:
            return True

        # Проверяем phone если передан
        if phone:
            existing = await cls.find_one_or_none(
                session,
                cls.stmt().filters(UserFilter(phone=phone)).build()
            )
            if existing:
                raise exception

        # Проверяем email если передан
        if email:
            existing = await cls.find_one_or_none(
                session,
                cls.stmt().filters(UserFilter(email=email)).build()
            )
            if existing:
                raise exception

        return True


    @classmethod
    async def create_user(cls, session: AsyncSession, data: UserSchema) -> Union[User, None]:

        # Проверяем что phone и email не заняты
        if await cls.check_user_unique(session, data):

            data = UserWithId(**data.model_dump(), id=gen_uuid())

            data.password = hash_password(
                str(data.password)
            )

            user = await cls.add(session, data)
            await session.commit()

            return user

    # === READ: один пользователь ===

    @classmethod
    async def get_by_id(cls, session: AsyncSession, user_id: str):
        """Получить пользователя по id"""
        stmt = (
            cls.stmt()
            .filters(UserFilter(id=user_id))
            .build()
        )
        return await cls.find_one_or_none(session, stmt)

    @classmethod
    async def get_by_email(cls, session: AsyncSession, email: str):
        """Получить пользователя по email (для авторизации)"""
        stmt = (
            cls.stmt()
            .filters(UserFilter(email=email))
            .build()
        )
        return await cls.find_one_or_none(session, stmt)

    @classmethod
    async def get_by_phone(cls, session: AsyncSession, phone: str):
        """Получить пользователя по телефону"""
        stmt = (
            cls.stmt()
            .filters(UserFilter(phone=phone))
            .build()
        )
        return await cls.find_one_or_none(session, stmt)

    @classmethod
    async def get_with_addresses(cls, session: AsyncSession, user_id: str):
        """Пользователь + его адреса"""
        stmt = (
            cls.stmt()
            .filters(UserFilter(id=user_id))
            .load(User.addresses)
            .build()
        )
        return await cls.find_one_or_none(session, stmt)

    @classmethod
    async def get_with_orders(cls, session: AsyncSession, user_id: str):
        """Пользователь + его заказы"""
        stmt = (
            cls.stmt()
            .filters(UserFilter(id=user_id))
            .load(User.orders)
            .build()
        )
        return await cls.find_one_or_none(session, stmt)

    @classmethod
    async def get_with_reviews(cls, session: AsyncSession, user_id: str):
        """Пользователь + его отзывы"""
        stmt = (
            cls.stmt()
            .filters(UserFilter(id=user_id))
            .load(User.reviews)
            .build()
        )
        return await cls.find_one_or_none(session, stmt)

    @classmethod
    async def get_full(cls, session: AsyncSession, user_id: str):
        """Пользователь со всеми связями"""
        stmt = (
            cls.stmt()
            .filters(UserFilter(id=user_id))
            .load(User.addresses, User.orders, User.reviews)
            .build()
        )
        return await cls.find_one_or_none(session, stmt)

    # === READ: список пользователей ===

    @classmethod
    async def get_all(
        cls,
        session: AsyncSession,
        filters: UserFilter | None = None,
        limit: int = 20,
        offset: int = 0
    ):
        """Получить список пользователей с фильтрами"""
        stmt = (
            cls.stmt()
            .filters(filters)
            .order_by(User.id)
            .limit(limit)
            .offset(offset)
            .build()
        )
        return await cls.find_all(session, stmt)

    # === UPDATE ===

    @classmethod
    async def update_user(
        cls,
        session: AsyncSession,
        user_id: str,
        data: UserUpdate
    ):

        # Проверка на уникальные значения
        if await cls.check_user_unique(session, data):

            if data.password is not None:
                data.password = hash_password(str(data.password))

            user = await cls.update_one_by_id(session, user_id, data)
            await session.commit()

            return user

    # === DELETE ===

    @classmethod
    async def delete_user(cls, session: AsyncSession, user_id: str):
        deleted_id = await cls.delete_one_by_id(session, user_id)
        await session.commit()

        return deleted_id
