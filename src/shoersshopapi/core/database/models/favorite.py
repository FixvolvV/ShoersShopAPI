from shoersshopapi.core.database.models.mixin import (
    UserRelationMixin,
    ProductRelationMixin
)
from .base import Base

from sqlalchemy import UniqueConstraint

class Favorite(UserRelationMixin, ProductRelationMixin, Base):
    _user_back_populates = "favorites"
    _user_load_strategy = "raise"
    _product_back_populates = "favorites"

    __table_args__ = (
            UniqueConstraint('user_id', 'product_id', name='uq_user_product_favorite'),
        )