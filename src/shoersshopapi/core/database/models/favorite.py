from shoersshopapi.core.database.models.mixin import UserRelationMixin

from .base import Base

class Favorite(UserRelationMixin, Base):
    _user_back_populates = "favorites"
