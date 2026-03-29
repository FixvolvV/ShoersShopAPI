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
    from .association import CartItem, OrderItem


class Product(Base):

    title: Mapped[str]
    price: Mapped[float]
    color: Mapped[Color]
    avg_grade: Mapped[str | None]
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

    product_cart_items: Mapped[List["CartItem"]] = relationship(
        back_populates="product"
    )

    product_order_items: Mapped[List["OrderItem"]] = relationship(
        back_populates="product"
    )

