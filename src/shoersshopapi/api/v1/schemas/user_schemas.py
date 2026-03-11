from pydantic import BaseModel
from typing import (
    List,
    Sequence
)

from shoersshopapi.core.utils.enum import Role


class UserUnique(BaseModel):

    phone: str
    email: str

class User(UserUnique):

    surname: str
    name: str
    patronymic: str
    password: bytes | str
    role: Role = Role.user
    social_link: str | None = None

class UserWithId(User):

    id: str

class Users(BaseModel):

    users: Sequence[UserWithId | None] | None

class RegistrationForm(BaseModel):

    phone: str
    email: str
    password: str
    surname: str
    name: str
    patronymic: str

class LoginFormByPhone(BaseModel):

    phone: str
    password: str

class LoginFormByEmail(BaseModel):

    email: str
    password: str