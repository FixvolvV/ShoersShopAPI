from pydantic import BaseModel
from typing import (
    List
)

from shoersshopapi.core.utils.enum import Role

from .address_schemas import AddressWithId
from .order_schemas import OrderWithId
from .review_schemas import ReviewWithId

#-------------- User Schemes -------------- 

class UserUnique(BaseModel):

    phone: str
    email: str

class UserSchema(UserUnique):

    surname: str
    name: str
    patronymic: str
    password: bytes | str
    role: Role | str = Role.user
    social_link: List[str] | None = None

class UserWithId(UserSchema):

    id: str

class UserUpdate(BaseModel):
    surname: str | None = None
    name: str | None = None
    patronymic: str | None = None
    password: bytes | str | None = None
    social_link: str | None = None
    phone: str | None = None
    email: str | None = None
    role: Role | str | None = None

class UserFull(UserWithId):
    addresses: list[AddressWithId] = []
    orders: list[OrderWithId] = []
    reviews: list[ReviewWithId] = []

#-------------- User Filters -------------- 

class UserFilter(BaseModel):
    id: str | None = None
    phone: str | None = None
    email: str | None = None
    role: Role | str | None = None

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