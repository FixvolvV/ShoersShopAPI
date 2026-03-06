from typing import (
    Generic,
    Sequence,
    TypeVar,
    Union,
    List
)

from sqlalchemy import (
    Result,
    select
)

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from pydantic import BaseModel

from shoersshopapi.core.database import Base

T = TypeVar("T", bound=Base)

class BaseCrud(Generic[T]):
    model: type[T]

    @classmethod
    async def add(cls, session: AsyncSession, values: BaseModel) -> Union[T, None]:

        values_dict = values.model_dump(exclude_unset=True)
        instanse = cls.model(**values_dict)

        try:
            responce = session.add(instanse)
            await session.flush()

            return responce

        except SQLAlchemyError as e:
            await session.rollback()
            raise e
    
    @classmethod
    async def find_all(cls, session: AsyncSession, filters: BaseModel) -> Union[Sequence, None]:
        
        filters_dict = filters.model_dump(exclude_unset=True, exclude_defaults=True)
        stmt = select(cls.model).where(**filters_dict)
        
        try:
            result = await session.execute(stmt)

            return result.scalars().unique().all()
            
        except SQLAlchemyError as e:
            raise e

    @classmethod
    async def find_one_or_none(cls, session: AsyncSession, filters: BaseModel) -> Union[Result, None]:

        filters_dict = filters.model_dump(exclude_unset=True, exclude_defaults=True)
        stmt = select(cls.model).where(**filters_dict)

        try:
            result: Result = await session.execute(stmt)

            return result.scalar_one_or_none()
        
        except SQLAlchemyError as e:
            raise e
    
    @classmethod
    async def find_one_or_none_by_id(cls, session: AsyncSession, id: str) -> Union[T, None]:

        try:
            result = await session.get(cls.model, id)

            return result
        
        except SQLAlchemyError as e:
            raise e

    @classmethod
    async def update_one_by_id(cls, session: AsyncSession, id: str, new_values: BaseModel) -> Union[T, None]:

        values_dict = new_values.model_dump(exclude_unset=True, exclude_defaults=True)

        try:
            target = await session.get(cls.model, id)

            if not target:
                return None

            for key, value in values_dict.items():
                setattr(target, key, value)

            await session.flush()

        except SQLAlchemyError as e:
            await session.rollback()
            raise e
    
    @classmethod
    async def delete_one_by_id(cls, session: AsyncSession, id: str) -> bool:

        try:
            data = await session.get(cls.model, id)

            if not data:
                return False

            await session.delete(data)
            await session.flush()
            return True 

        except SQLAlchemyError as e:
            raise e

