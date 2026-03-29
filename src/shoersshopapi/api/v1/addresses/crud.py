from typing import Union, Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from shoersshopapi.api.v1.basecrud import BaseCrud
from shoersshopapi.api.v1.utils import gen_uuid
from shoersshopapi.core.database.models import Address

from shoersshopapi.api.v1.schemas import (
    AddressSchema,
    AddressWithId,
    AddressUpdate,
    AddressFilter
)

from pydantic import BaseModel


class AddressCrud(BaseCrud[Address]):
    model = Address

    # === CREATE ===

    @classmethod
    async def create_address(
        cls,
        session: AsyncSession,
        user_id: str,
        data: AddressSchema,
    ) -> Union[Address, None]:

        address_data = AddressWithId(
            id=gen_uuid(),
            user_id=user_id,
            **data.model_dump(),
        )
        
        address = await cls.add(session, address_data)
        await session.commit()
        return address

    # === READ ===

    @classmethod
    async def get_by_id(cls, session: AsyncSession, address_id: str):
        stmt = cls.stmt().filters(AddressFilter(id=address_id)).build()
        return await cls.find_one_or_none(session, stmt)

    @classmethod
    async def get_by_user(
        cls,
        session: AsyncSession,
        user_id: str,
    ):
        stmt = (
            cls.stmt()
            .filters(AddressFilter(user_id=user_id))
            .build()
        )
        return await cls.find_all(session, stmt)

    # === UPDATE ===

    @classmethod
    async def update_address(
        cls,
        session: AsyncSession,
        address_id: str,
        user_id: str,
        data: AddressUpdate,
    ):
        address = await cls.find_one_or_none_by_id(session, address_id)

        if not address:
            return None

        if address.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not your address",
            )

        address = await cls.update_one_by_id(session, address_id, data)
        await session.commit()
        return address

    # === DELETE ===

    @classmethod
    async def delete_address(
        cls,
        session: AsyncSession,
        address_id: str,
        user_id: str,
    ) -> bool:
        address = await cls.find_one_or_none_by_id(session, address_id)

        if not address:
            return False

        if address.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not your address",
            )

        result = await cls.delete_one_by_id(session, address_id)
        await session.commit()
        return result