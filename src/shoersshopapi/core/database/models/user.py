from typing import List
from sqlalchemy import JSON
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)
from sqlalchemy.ext.hybrid import hybrid_property

from .base import Base


class User(Base):

    phone: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str] 
    surname: Mapped[str]
    patronymic: Mapped[str]
    password: Mapped[bytes]
    social_link: Mapped[List[str]]  = mapped_column(JSON, default=list)

    @hybrid_property
    def fullname(self) -> str: #pyright: ignore
        return f"{self.surname} {self.name} {self.patronymic}"
    
    @fullname.expression #pyright: ignore
    def fullname(cls):
        return cls.surname + " " + cls.name + " " + cls.patronymic

