from typing import Tuple
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from .base import Base


class CartItem(Base):
    __table_args__ = (
        UniqueConstraint(
            "cart_id",
            "product_id",
            name="idx_unique_cart_product"
        ),
    )

    cart_id: Mapped[str] = mapped_column(ForeignKey("carts.id"))
    product_id: Mapped[str] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int]


class OrderItem(Base):
    __table_args__ = (
        UniqueConstraint(
            "order_id",
            "product_id",
            name="idx_unique_order_product"
        ),
    )

    order_id: Mapped[str] = mapped_column(ForeignKey("orders.id"))
    product_id: Mapped[str] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int]
