from typing import (
    List,
    TYPE_CHECKING
)
from sqlalchemy.orm import (
    Mapped,
    relationship,
)

from shoersshopapi.core.database.models import favorite

from .base import Base

from shoersshopapi.core.utils.enum import Color

if TYPE_CHECKING:
    from .size import Size
    from .brand import Brand


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