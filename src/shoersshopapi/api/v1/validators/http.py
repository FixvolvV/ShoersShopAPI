from typing import Annotated

from fastapi import (
    Depends,
    HTTPException,
)
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError

from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from shoersshopapi.api.v1.schemas import (
    LoginFormByEmail,
    RegistrationForm,
    User,
    Users
)

# from api.v1.crud import (
#     user_get_by_id,
#     user_get,
#     user_get_all
# )

from shoersshopapi.api.v1.schemas.user_schemas import UserWithId
from shoersshopapi.core.settings import (
    settings,
    TOKEN_TYPE_FIELD,
    ACCESS_TOKEN_TYPE,
    REFRESH_TOKEN_TYPE,
)

from shoersshopapi.api.v1.utils import (
    validate_password,
    decode_jwt
)

from shoersshopapi.core.database import database
from shoersshopapi.api.v1.users.crud import UserCrud

# Привязка для правильного получения JWT токена средставми FastAPI
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/authentication/login",
)


def get_current_token_payload(
    token: str,
) -> dict:
    try:
        payload = decode_jwt(
            token=token,
        )
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token error: {e}",
        )
    return payload


def validate_token_type(
    payload: dict,
    token_type: str,
) -> bool:
    current_token_type = payload.get(TOKEN_TYPE_FIELD)
    if current_token_type == token_type:
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"invalid token type {current_token_type!r} expected {token_type!r}",
    )


async def get_user_by_token_sub(
    payload: dict,
    session: AsyncSession
) -> User:
    userid: str | None = payload.get("sub")
    if user := await UserCrud.find_one_or_none_by_id(session=session, id=str(userid)):
        return UserWithId.model_validate(user)
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid (user not found)",
    )


class UserGetterFromToken:
    def __init__(self, token_type: str):
        self.token_type = token_type

    async def __call__(
        self,
        token: str = Depends(oauth2_scheme),
        session: AsyncSession = Depends(database.session_factory),
    ) -> User:

        payload = get_current_token_payload(token)
        validate_token_type(payload, self.token_type)
        return await get_user_by_token_sub(payload, session)


get_current_auth_user = UserGetterFromToken(ACCESS_TOKEN_TYPE)
get_current_auth_user_for_refresh = UserGetterFromToken(REFRESH_TOKEN_TYPE)