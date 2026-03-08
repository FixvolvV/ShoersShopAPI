from pydantic import BaseModel
from typing import (
    List
)

class User(BaseModel):

    surname: str
    name: str
    patronymic: str
    password: bytes
    phone: str
    email: str
    role: str
    social_link: str | None

class UserWithId(User):

    id: str

class Users(BaseModel):

    users: List[UserWithId] | None

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