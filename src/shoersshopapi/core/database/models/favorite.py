from shoersshopapi.core.database.models.mixin import (
    UserRelationMixin,
    ProductRelationMixin
)
from .base import Base

class Favorite(UserRelationMixin, ProductRelationMixin, Base):
    _user_back_populates = "favorites"
    _user_load_strategy = "raise"
    _product_back_populates = "favorites"

