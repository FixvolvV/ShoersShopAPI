from pydantic import BaseModel, ConfigDict
from typing import (
    List
)

from shoersshopapi.core.database.models import favorite
from shoersshopapi.core.utils.enum import Role

from .address_schemas import AddressWithId
from .order_schemas import OrderWithId
from .review_schemas import ReviewWithId
from .favorite_schemas import FavoriteWithId

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
    social_link: List[str] = []

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
    reviews: List[ReviewWithId] | None = None
    orders: List[OrderWithId] | None = None 
    addresses: List[AddressWithId] | None = None
    favorites: List[FavoriteWithId] | None = None

#-------------- User Filters -------------- 

class UserFilter(BaseModel):
    id: str | None = None
    phone: str | None = None
    email: str | None = None
    role: Role | str | None = None

    model_config = ConfigDict(from_attributes=True)


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