from typing import (
    List,
    TYPE_CHECKING,
    Optional
)
from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    noload,
    relationship,
)

from shoersshopapi.core.database.models import cart, favorite

from .base import Base

from shoersshopapi.core.utils.enum import Color

if TYPE_CHECKING:
    from .size import Size
    from .brand import Brand
    from .order import Order
    from .cart import Cart
    from .favorite import Favorite


class Product(Base):

    title: Mapped[str]
    price: Mapped[float]
    color: Mapped[Color]
    avg_grade: Mapped[str]
    brand_id: Mapped[str | None] = mapped_column(ForeignKey("brands.id"))

    sizes: Mapped[List["Size"]] = relationship(
        back_populates="product",
        lazy="noload",
        cascade="all, delete-orphan"
    )

    favorites: Mapped[List["Favorite"]] = relationship(
        back_populates="product",
        lazy="noload",
        cascade="all, delete-orphan"
    )

    brand: Mapped[Optional["Brand"]] = relationship(
        back_populates="products",
        lazy="noload"
    )

    orders: Mapped[List["Order"]] = relationship(
        secondary="orderitems",
        back_populates="products",
        lazy="noload",
    )

    carts: Mapped[List["Cart"]] = relationship(
        secondary="cartitems",
        back_populates="products",
        lazy="noload",
    )