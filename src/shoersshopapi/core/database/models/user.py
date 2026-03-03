from typing import (
    List,
    TYPE_CHECKING,
    Optional
)
from sqlalchemy import (
    JSON,
    text
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from sqlalchemy.ext.hybrid import hybrid_property

from shoersshopapi.core.database.models import favorite

from .base import Base

from shoersshopapi.core.utils.enum import Role

if TYPE_CHECKING:
    from .order import Order
    from .review import Review
    from .favorite import Favorite
    from .cart import Cart

class User(Base):

    phone: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str] 
    surname: Mapped[str]
    patronymic: Mapped[str]
    password: Mapped[bytes]
    social_link: Mapped[List[str]] = mapped_column(JSON, default=list)
    role: Mapped[Role] = mapped_column(default=Role.user,  server_default=text("'user'"))

    reviews: Mapped[List["Review"] | None] = relationship(
        back_populates="Review",
        lazy="joined"
    )

    orders: Mapped[List["Order"] | None] = relationship(
        back_populates="Order",
        lazy="joined"
    )

    favorites: Mapped[List["Favorite"] | None] = relationship(
        back_populates="Favorite",
        lazy="joined"
    )

    cart: Mapped[Optional["Cart"]] = relationship(
        back_populates="Cart",
        lazy="joined"
    )

    @hybrid_property
    def fullname(self) -> str: #pyright: ignore
        return f"{self.surname} {self.name} {self.patronymic}"
    
    @fullname.expression #pyright: ignore
    def fullname(cls):
        return cls.surname + " " + cls.name + " " + cls.patronymic
 
