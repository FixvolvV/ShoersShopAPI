from typing import (
    List,
    TYPE_CHECKING
)
from sqlalchemy.orm import Mapped, relationship

from .base import Base
from .mixin import ProductRelationMixin

if TYPE_CHECKING:
    from .product import Product

class Brand(Base):

    brand_logo: Mapped[str]

    products: Mapped[List["Product"] | None] = relationship(
        back_populates="brand",
        lazy="selectin"
    )
