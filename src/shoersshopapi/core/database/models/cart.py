from typing import (
    TYPE_CHECKING,
    List
)

from sqlalchemy.orm import (
    Mapped,
    relationship,
)

from .base import Base
from .mixin import UserRelationMixin


if TYPE_CHECKING:
    from .size import Size
    from .association import CartItem
    


class Cart(UserRelationMixin, Base):
    _user_back_populates = "cart"
    _user_id_unique = True

    sizes: Mapped[List["Size"]] = relationship (
        secondary="cartitems",
        back_populates="carts",
        lazy="noload"
    )

    cart_items: Mapped[List["CartItem"]] = relationship (
        back_populates="cart"
    )