from sqlalchemy import delete
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import (
    TYPE_CHECKING,
    List,
)

from .base import Base
from .mixin import ProductRelationMixin

from shoersshopapi.core.utils.enum import ASizes

if TYPE_CHECKING:
    from .order import Order
    from .cart import Cart
    from .association import CartItem, OrderItem

class Size(ProductRelationMixin, Base):
    _product_back_populates = "sizes"

    count: Mapped[int]
    size: Mapped[ASizes] = mapped_column(server_default="39")

    orders: Mapped[List["Order"]] = relationship(
        secondary="orderitems",
        back_populates="sizes",
        lazy="noload",
        cascade="all, delete"
    )

    carts: Mapped[List["Cart"]] = relationship(
        secondary="cartitems",
        back_populates="sizes",
        lazy="noload",
        cascade="all, delete"
    )

    sizes_cart_items: Mapped[List["CartItem"]] = relationship(
        back_populates="items"
    )

    sizes_order_items: Mapped[List["OrderItem"]] = relationship(
        back_populates="items"
    )
