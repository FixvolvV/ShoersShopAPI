from shoersshopapi.api.v1.basecrud import BaseCrud

from sqlalchemy.ext.asyncio import AsyncSession

from shoersshopapi.core.database.models import User as model_user

from shoersshopapi.api.v1.schemas import UserSchema

from shoersshopapi.api.v1.utils import gen_uuid, hash_password
from shoersshopapi.api.v1.schemas.user_schemas import UserWithId

class UserCrud(BaseCrud[model_user]):
    model = model_user


# Функция добавляющая пользователя в DB. 
async def add_user(
    data: UserSchema,
    session: AsyncSession
) -> UserWithId:

    user: UserWithId = UserWithId(**data.model_dump(), id=gen_uuid())

    user.password = hash_password(
        password=str(user.password)
    )

    await UserCrud.add(session=session, values=user)
    await session.commit()

    return user


async def find_user_by_id(
    id: str,
    session: AsyncSession
) -> UserWithId:

    user: UserWithId = UserWithId.model_validate(
        await UserCrud.find_one_or_none_by_id(session=session, id=id)
    )

    return user

