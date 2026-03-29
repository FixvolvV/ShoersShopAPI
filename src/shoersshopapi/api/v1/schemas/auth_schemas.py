from typing import Optional
from pydantic import BaseModel, model_validator, EmailStr

from shoersshopapi.core.utils.enum import Role

class LoginSchema(BaseModel):
    
    username: str
    password: str

class RegisterSchema(BaseModel):

    phone: str
    email: str
    surname: str
    name: str
    patronymic: str
    password: bytes | str