from sqlalchemy.orm import Mapped

from .base import Base
from .mixin import ProductRelationMixin

class Size(ProductRelationMixin, Base):
    _product_back_populates = "sizes"

    count: Mapped[int]
    size: Mapped[int]