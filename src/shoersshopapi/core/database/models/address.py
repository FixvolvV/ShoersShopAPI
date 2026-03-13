from typing import (
    TYPE_CHECKING
)

from sqlalchemy.orm import (
    Mapped,
    relationship,
)
from typing import (
    List
)

from sqlalchemy.orm import Mapped
from .base import Base

if TYPE_CHECKING:
    from .order import Order

class Address(Base):

    region: Mapped[str]
    city: Mapped[str]
    street: Mapped[str]
    house: Mapped[str]
    entrance: Mapped[str]
    apartment: Mapped[str]
    postcode: Mapped[int]

    orders: Mapped[List["Order"]] = relationship(   # ← orders (множественное)
        back_populates="address",
        lazy="noload"
    )
    