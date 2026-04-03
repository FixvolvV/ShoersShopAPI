from typing import (
    List,
    TYPE_CHECKING
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixin import ProductRelationMixin

if TYPE_CHECKING:
    from .product import Product

class Brand(Base):

    brand_name: Mapped[str] = mapped_column(unique=True)
    brand_logo: Mapped[str]

    products: Mapped[List["Product"] | None] = relationship(
        back_populates="brand",
        lazy="noload",
    )
