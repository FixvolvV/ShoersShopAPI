from typing import (
    TYPE_CHECKING
)

from sqlalchemy import (
    ForeignKey,
    text
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from datetime import datetime

from .base import Base
from .mixin import UserRelationMixin

from shoersshopapi.core.utils.enum import Status

if TYPE_CHECKING:
    from .address import Address

class Order(UserRelationMixin, Base):
    _user_back_populates = "orders"

    order_date: Mapped[datetime]
    total_amount: Mapped[int]
    status: Mapped[Status] = mapped_column(default=Status.confirmation,  server_default=text("'confirmation'"))

    address_id: Mapped[str] = mapped_column(
        ForeignKey("addresses.id"),
        nullable=False
    )

    address: Mapped["Address"] = relationship (
        back_populates="Address",
        lazy="joined"
    )

