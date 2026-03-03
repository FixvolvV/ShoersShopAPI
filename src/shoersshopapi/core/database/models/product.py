from typing import (
    List,
    TYPE_CHECKING
)
from sqlalchemy.orm import (
    Mapped,
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


class Product(Base):

    title: Mapped[str]
    price: Mapped[float]
    color: Mapped[Color]
    avg_grade: Mapped[str]

    sizes: Mapped[List["Size"]] = relationship(
        back_populates="Size",
        lazy="joined"
    )

    brand: Mapped["Brand"] = relationship(
        back_populates="Brand",
        lazy="joined"
    )

    orders: Mapped[List["Order"]] = relationship(
        secondary="orderitems",
        back_populates="orders",
        lazy="noload"
    )

    carts: Mapped[List["Cart"]] = relationship(
        secondary="cartitems",
        back_populates="carts",
        lazy="noload"
    )