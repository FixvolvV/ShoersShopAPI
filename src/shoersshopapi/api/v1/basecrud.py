from typing import (
    Generic,
    Sequence,
    TypeVar,
    Union,
    List
)

from sqlalchemy import (
    Result,
    select,
    inspect
)


from sqlalchemy.orm import selectinload

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from pydantic import BaseModel

from shoersshopapi.core.database import Base


class StatementBuilder:

    def __init__(self, model):
        self.model = model
        self._stmt = select(model)
        self._joined = set()

    def _ensure_join(self, relation):
        key = str(relation)
        if key not in self._joined:
            self._stmt = self._stmt.join(relation)
            self._joined.add(key)

    def filters(self, filters, model=None):

        if filters is None:
            return self

        filters_dump = filters.model_dump(exclude_none=True)

        if not filters_dump:
            return self 

        target_model = model or self.model

        if target_model != self.model:

            for rel in inspect(self.model).relationships:
                if rel.mapper.class_ == target_model:
                    self._ensure_join(getattr(self.model, rel.key))
                    break

        for field_name, value in filters_dump.items():
            if field_name.endswith("_min"):
                column = getattr(target_model, field_name.removesuffix("_min"))
                self._stmt = self._stmt.where(column >= value)
            elif field_name.endswith("_max"):
                column = getattr(target_model, field_name.removesuffix("_max"))
                self._stmt = self._stmt.where(column <= value)
            elif isinstance(value, list):
                column = getattr(target_model, field_name)
                self._stmt = self._stmt.where(column.in_(value))
            else:
                column = getattr(target_model, field_name)
                self._stmt = self._stmt.where(column == value)

        return self

    def load(self, *relations):
        for relation in relations:
            self._stmt = self._stmt.options(selectinload(relation))
        return self

    def order_by(self, field, desc: bool = False):
        self._stmt = self._stmt.order_by(field.desc() if desc else field)
        return self

    def limit(self, value: int):
        self._stmt = self._stmt.limit(value)
        return self

    def offset(self, value: int):
        self._stmt = self._stmt.offset(value)
        return self

    def build(self):
        return self._stmt


T = TypeVar("T", bound=Base)

class BaseCrud(Generic[T]):
    model: type[T]

    @classmethod
    def stmt(cls) -> StatementBuilder:
        return StatementBuilder(cls.model)

    @classmethod
    async def add(cls, session: AsyncSession, values: BaseModel) -> Union[T, None]:

        values_dict = values.model_dump(exclude_unset=True)
        instanse = cls.model(**values_dict)

        try:
            session.add(instanse)
            await session.flush()

            return instanse

        except SQLAlchemyError as e:
            await session.rollback()
            raise e
    
    @classmethod
    async def find_all(cls, session: AsyncSession, stmt) -> Union[Sequence, None]:
        
        try:
            result = await session.execute(stmt)

            return result.scalars().unique().all()
            
        except SQLAlchemyError as e:
            raise e

    @classmethod
    async def find_one_or_none(cls, session: AsyncSession, stmt) -> Union[T, None]:

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

            return target

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

