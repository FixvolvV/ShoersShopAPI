from sqlalchemy import (
    text
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from datetime import datetime

from .base import Base
from .mixin import UserRelationMixin

from shoersshopapi.core.utils.enum import Status


class Order(UserRelationMixin, Base):
    _user_back_populates = Base.__tablename__

    order_date: Mapped[datetime]
    total_amount: Mapped[int]
    status: Mapped[Status] = mapped_column(default=Status.confirmation,  server_default=text("'confirmation'"))


