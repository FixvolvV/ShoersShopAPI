from typing import (
    List,
    TYPE_CHECKING,
    Optional
)
from sqlalchemy import Double, ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from .base import Base

from shoersshopapi.core.utils.enum import Color

if TYPE_CHECKING:
    from .size import Size
    from .brand import Brand
    from .favorite import Favorite


class Product(Base):

    title: Mapped[str]
    price: Mapped[float]
    color: Mapped[Color]
    logo: Mapped[str | None]
    article: Mapped[str]
    category: Mapped[str]
    avg_grade: Mapped[float]
    brand_id: Mapped[str | None] = mapped_column(ForeignKey("brands.id"))

    sizes: Mapped[List["Size"]] = relationship(
        back_populates="product",
        lazy="noload",
        cascade="all, delete"
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