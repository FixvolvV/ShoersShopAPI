from sqlalchemy.orm import Mapped

from .base import Base
from .mixin import ProductRelationMixin

class Brand(ProductRelationMixin, Base):
    _product_back_populates = "brands"

    brand_logo: Mapped[str]
