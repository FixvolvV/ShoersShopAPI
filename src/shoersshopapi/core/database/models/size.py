from sqlalchemy.orm import Mapped, relationship

from typing import (
    TYPE_CHECKING,
    List,
)

from .base import Base
from .mixin import ProductRelationMixin

if TYPE_CHECKING:
    from .order import Order
    from .cart import Cart
    from .association import CartItem, OrderItem

class Size(ProductRelationMixin, Base):
    _product_back_populates = "sizes"

    count: Mapped[int]
    size: Mapped[int]

    orders: Mapped[List["Order"]] = relationship(
        secondary="orderitems",
        back_populates="sizes",
        lazy="noload",
    )

    carts: Mapped[List["Cart"]] = relationship(
        secondary="cartitems",
        back_populates="sizes",
        lazy="noload",
    )

    sizes_cart_items: Mapped[List["CartItem"]] = relationship(
        back_populates="items"
    )

    sizes_order_items: Mapped[List["OrderItem"]] = relationship(
        back_populates="items"
    )
