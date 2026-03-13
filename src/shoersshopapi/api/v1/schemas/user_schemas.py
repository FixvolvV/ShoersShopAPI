from pydantic import BaseModel
from typing import (
    Sequence
)

from shoersshopapi.core.utils.enum import Role

#-------------- User Schemes -------------- 

class UserUnique(BaseModel):

    phone: str
    email: str

class UserSchema(UserUnique):

    surname: str
    name: str
    patronymic: str
    password: bytes | str
    role: Role = Role.user
    social_link: str | None = None

class UserWithId(UserSchema):

    id: str

class UsersSchema(BaseModel):

    users: Sequence[UserWithId | None] | None

class UserUpdate(BaseModel):
    surname: str | None = None
    name: str | None = None
    patronymic: str | None = None
    password: bytes | None = None
    social_link: str | None = None
    phone: str | None = None
    email: str | None = None
    role: Role | None = None

#-------------- User Filters -------------- 

class UserFilter(BaseModel):
    id: int | None = None
    phone: str | None = None
    email: str | None = None
    role: Role | None = None

#-------------- User Forms -------------- 

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