from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from .base import Base

if TYPE_CHECKING:
    from .cart import Cart
    from .order import Order
    from .size import Size

class CartItem(Base):
    __table_args__ = (
        UniqueConstraint(
            "cart_id",
            "size_id",
            name="idx_unique_cart_product"
        ),
    )

    cart_id: Mapped[str] = mapped_column(ForeignKey("carts.id"))
    size_id: Mapped[str] = mapped_column(ForeignKey("sizes.id"))
    quantity: Mapped[int] = mapped_column(default=1, server_default="1")

    cart: Mapped["Cart"] = relationship(back_populates="cart_items")

    items: Mapped["Size"] = relationship(back_populates="sizes_cart_items")


class OrderItem(Base):
    __table_args__ = (
        UniqueConstraint(
            "order_id",
            "size_id",
            name="idx_unique_order_product"
        ),
    )

    order_id: Mapped[str] = mapped_column(ForeignKey("orders.id"))
    size_id: Mapped[str] = mapped_column(ForeignKey("sizes.id"))
    quantity: Mapped[int] = mapped_column(default=1, server_default="1")

    order: Mapped["Order"] = relationship(back_populates="order_items") 

    items: Mapped["Size"] = relationship(back_populates="sizes_order_items")
